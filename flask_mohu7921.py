import time
from datetime import datetime
import os
import socket
import smtplib
from email.mime.text import MIMEText
from dateutil.relativedelta import relativedelta
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
app = Flask(__name__,static_folder ='./templates/')

import smtplib
from email.mime.text import MIMEText
import os

"""
function to generate emails and send
"""
def mail(msg, subject):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.set_debuglevel(0)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login('moizhussain08@gmail.com', 'fall2015')

    fromaddr = "moizhussain08@gmail.com"
    toaddrs  = "moizhussain.92@gmail.com"
    #subject = "Notification: Link Bandwidth Exceeded"

    msg = MIMEText(msg)
    msg['From'] = fromaddr
    msg['To'] = toaddrs
    msg['Subject'] = subject

    server.sendmail(fromaddr, toaddrs, msg.as_string())
    server.quit()

"""
function to serve the html pages to the browser with styling.
"""
@app.route('/templates/<path:filename>')
def send_staticfiles(filename):
    return send_from_directory('./templates', filename)

"""
default function which return the login page
"""
@app.route("/")
def login():
    return render_template('pc_home.html')

"""
This function is used to check if login credentials are valid.
static credentials are used. username = admin, password = 1234
"""
@app.route("/loginAuth", methods=["POST","GET"])
def loginAuth():
    usName = request.form["username"]
    Pass = request.form["password"]
    message = "Invalid Credentials. Try again."
    if str(usName) == 'admin':
        if str(Pass) == '1234':
            '''reading = open("blockedSites.txt", 'ab+')
            readlist = []
            for line in reading.read().split('\n'):
                if line:
                    readlist.append(line)
            reading.close()'''
            return render_template('pc_home2.html')
        else:
            return render_template('pc_home.html', message = message)
    else:
        return render_template('pc_home.html', message = message)

"""
it displays the list of blocked sites by reading from the file
"""
@app.route("/templates/view", methods=["GET", "POST"])
def view():
    #message = "Please click any icon the left side to begin"
    reading = open("blockedSites.txt", 'ab+')
    readlist = []
    for line in reading.read().split('\n'):
        if line:
            readlist.append(line)
    reading.close()
    return render_template('pc_view.html', blocked = readlist)

"""
This function is used to add the sites to be blocked and
keeps appending them in the webpage.
"""
@app.route("/templates/pc_block.html", methods=["GET"])
@app.route("/templates/Block", methods=["POST","GET"])
def Block():
    if not request.method == 'GET':
        web = request.form["Add"]
        block_list = open("blockedSites.txt", 'ab+')
        sites = web + "\n"
        check = block_list.read()
        if str(web) in check:
            message = "Either the site is already blocked or it has been"
            message += " entered in incorrect format."
            return render_template ('pc_block.html', message = message)

        if str(web).startswith('www'):
            if str(socket.gethostbyname(web)) != '':
                writelist = block_list.write(sites)
                block_list.close()
        else:
            return render_template ('pc_block.html', message = "Enter correct format.")

    reading = open("blockedSites.txt", 'ab+')
    readlist = []
    for line in reading.read().split('\n'):
        if line:
            readlist.append(line)
    reading.close()
    return render_template('pc_block.html', blocked = readlist)

"""
This function is used to perform the remove operation
of the websites from the blocking list.
"""
@app.route("/templates/pc_removeblock.html", methods=["GET","POST"])
@app.route("/templates/remove", methods=["POST","GET"])
def remove():
    if not request.method == 'GET':
        web = request.form["Remove"]

        block_list = open("blockedSites.txt", 'ab+')
        blockread = block_list.read().split("\n")
        block_list.close()
        for item in blockread:
            if str(item) == web:
                blockread.remove(item)
                message = 'Removed!'
            else:
                message = "Enter the correct name!"
        string =  '\n'.join(blockread)
        block_list = open("blockedSites.txt", 'w')
        blockwrite = block_list.write(string)
        block_list.close()
        return render_template('pc_removeblock.html', message = message)
    return render_template('pc_removeblock.html')

"""
This function is used to check if the user wants to renew or
end their service.
It generates a bill when the service is ended and also
emails the user on successful cancellation or renewal of the
service.
"""
@app.route("/templates/renew", methods=["POST","GET"])
def renew():
    choice = request.form["choice"]
    #currentTime = time.strftime("%Y-%m-%d %H:%M:%S")
    date_after_month = datetime.today()+ relativedelta(months=3)
    print 'Today: ',datetime.today().strftime('%d/%m/%Y')
    afterMonth = date_after_month.strftime('%d/%m/%Y')
    if str(choice) == 'Renew':
        time = datetime.today().strftime('%d/%m/%Y')
        timefile = open('time.txt', 'w')
        timefile.write(time)
        timefile.close()
        msg = "Your Subscription is successfully renewed."
        msg += " It is valid for the next 3 months. "
        msg += " Expiry date: " + afterMonth
        mail(msg, "Successful Renewal")
        return msg
    elif str(choice) == 'End':
        if os.path.exists('time.txt'):
            timefile = open('time.txt', 'r')
            timeread = timefile.read()
            timeThen = datetime.strptime(timeread,'%d/%m/%Y')
            now = datetime.today().strftime('%d/%m/%Y')
            timeNow = datetime.strptime(now,'%d/%m/%Y')

            diff = timeNow - timeThen
            factor = int(diff.days)
            bill = str(5*factor)
            msg = "Your subscription was cancelled successfully."
            msg += " Your Bill is: $" + bill +", Charges: $5 per day."
            msg += " You used the service for %s days. "% (str(factor))
            mail(msg, "Successful Cancellation")
            return msg
    else:
        return "wrong choice"

if __name__ == '__main__':
    app.run(debug=True)
