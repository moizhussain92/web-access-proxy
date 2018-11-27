import SocketServer
import SimpleHTTPServer
import urllib
import sys
import os

PORT = 1234

class Proxy(SimpleHTTPServer.SimpleHTTPRequestHandler):
    """
    This Function reads the file of blocked sites and compares
    them with the request sent at the browser. If the request
    matches any of the names listed in the blocked site, then the webpage
    is redirected. If the name does not match, then the request is accepted
    and the browser return the desired response.
    """


    def do_GET(self):
        if os.path.exists('blockedSites.txt'):
            list = open("blockedSites.txt", "r")
            list_read = list.read().split('\n')
            global newlist
            newlist = []
            for item in list_read:
                if item != '':
                    domain = item.split('.')[1]
                    newlist.append(domain)

            print 'item: ', item
            print 'selfpath: ', self.path
            domain = self.path.split('/')[2]
            name = domain.split('.')[1]
            print "NAME: ", name
            if name in newlist:
                self.copyfile(open('./templates/pc_proxyblock.html'), self.wfile)
            else:
                print 'in list'
                self.copyfile(urllib.urlopen(self.path), self.wfile)

        else:
            self.copyfile(urllib.urlopen(self.path), self.wfile)

httpd = SocketServer.ForkingTCPServer(('127.0.0.1', PORT), Proxy)
print "serving at port", PORT
httpd.serve_forever() # Used to keep the server running forever.
