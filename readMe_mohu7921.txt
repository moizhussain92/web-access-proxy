Network Management Project - Parental Control
======================================================
			- By Moiz Hussain

Project Components
------------------
1. Flask script which implements the Graphical user interface.
2. Proxy server script, which blocks the websites, configured on the GUI.
3. HTML pages.
4. 2 text files created while execution.


How to test the project
-----------------------
- Save both the python scripts in the root directory. /home/netman/Documents
						     ========================
- The html pages, css styling, and images should be save in a templates folder under the root directory: /home/netman/Documents/templates
													==================================
- To test the flask code, normally open the mozilla firefox and type in the address bar : "127.0.0.1:5000"
- To test the proxy server after adding the sites to be blocked, do the following:
		-open firefox and set manual proxy settings to IP: 127.0.0.1 and Port: 1234
		-start bowsing.




How does it work
----------------

The project implements a parental control interface which performs the following functions:
- Login using Parent credential (Statically configured) 
===================================
Username = admin, password = 1234
===================================
- View function: used to view the websites which have been already blocked.
- block: to block websites.
- Subscription: To renew or end the subscription. Accordingly, a bill is generated when the service ends.
- Email - Whenever the subscrption is renewed or cancelled, an email is sent with details.