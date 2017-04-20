"""Py-Phished v1.0
Ben Floyd, License: BSD-3 Clause
Py-Phished is a python-based webserver/email client for internal phishing campaigns.

The goal is to test company training efficacy and email safety and assess the overall response
rate to malicious phishing attempts.  The emailer can be controlled via the site with /start and
/stop commands.  Base64 encoded email addresses are sent to "victims" as part of the link for 
tracking purposes.

Inputs: csv file with email, first name, last name
Usage:  http://url/start
        http://url/stop
Output: caught.csv



In future versions, metrics are planned.
"""



import sys
import threading
import tornado.ioloop
import tornado.web
import csv
import smtplib
import base64
import time
import signal
import os


phish_f = "phish.html"
targets = "targets.csv"
pin = open(phish_f, 'rb').read()
tin = open(targets, 'rb')
csv_r = csv.DictReader(tin, dialect='excel')
disp = {}
db = {}
caught = {}
i = 0
j = 0

#Return address
#fr_addr = 'noreply@account.internal'
#to_addr = ''
#ph_link = ''

#Handle CTRL+C (linux only)
def signal_handler(signal, frame):
	print('Caught %s' % signal)
	print "Stopping phishing campaign..."
        ioloop = tornado.ioloop.IOLoop.instance()
        ioloop.add_callback(ioloop.stop)
	e.set()
        print "Asked Tornado to exit"
	sys.exit(0)

#Mass emailer.  Set to stagger 100 emails with a 10s pause
class phish_campaign:

	def __init__(self):
		target = {}
	       	csvfile = 'targets.csv'
	        reader = csv.DictReader(csvfile, dialect='excel')
		global j
		global db
		global e
		#global disp
		targets = {}
		print 'Rows in DB = %d' % len(db)
		while j < len(db) and not e.isSet():
			#print db[j]
			#print 'E.isSet() = %s' % e.isSet()
			if (j % 100 == 0):
				if (j != 0):
					print 'Sleeping for 10s'
					time.sleep(1)
					if not e.isSet():
					#print row['Email'], row['First Name']
						print 'J = %d' % j #, row['Email']
						targets[j] = {"Email": db[j]['Email'], "F_name": db[j]['F_name']}
  		               			testmail(targets[j])
				else:
					if not e.isSet():
                                        #print row['Email'], row['First Name']
                                        	print 'J = %d' % j #, row['Email']
                                        	targets[j] = {"Email": db[j]['Email'], "F_name": db[j]['F_name']}
                                        	testmail(targets[j])

			else:
				time.sleep(1)
				#print row['Email'], row['First Name']
     	               		targets[j] = {"Email": db[j]['Email'], "F_name": db[j]['F_name']}
				testmail(targets[j])
				#print j
			#print j
  	               	j += 1


#Called by "phish_campaign"
def testmail(target):

	# Send an HTML email with an embedded image and a plain text message for
	# email clients that don't want to display the HTML.

	from email.MIMEMultipart import MIMEMultipart
	from email.MIMEText import MIMEText
	from email.MIMEImage import MIMEImage
	strFrom = '"Account Notification"<noreply@accounts.internal>'
	strTo = target['Email']
	strFname = target['F_name']

	# Create the root message and fill in the from, to, and subject headers
	msgRoot = MIMEMultipart()
	msgRoot['Subject'] = 'Web Monitoring Program'
	msgRoot['From'] = strFrom
	msgRoot['To'] = strTo
	msgRoot.preamble = 'This is a multi-part message in MIME format'

	# Encapsulate the plain and HTML versions of the message body in an
	# 'alternative' part, so message agents can decide which they want to display.
	#msgAlternative = MIMEMultipart('alternative')
	#msgRoot.attach(msgAlternative)
	
	t_txt = '**Your mail client does not support HTML.  \n\nDear ' + strFname + ',  \n\nYou have been automatically enrolled in the Web Activity Monitoring Program.  We have partnered with your company to track your browsing to prevent sensitive information leakage.  Please visit "http://ow.ly/slrT30aZWgE/account/' + base64.b64encode(strTo) + '"\n\n\nThanks,\n\nThe Team\nAlitheia Tech, Inc.'
	#msgText = MIMEText(t_txt, 'plain')
	#msgAlternative.attach(msgText)


	f_html = (open('phish.html','rb')).read()
	m_html = MIMEText(f_html, 'html')
	
	# We reference the image in the IMG SRC attribute by the ID we give it below
	link = """<a href="http://ec2-54-201-17-210.us-west-2.compute.amazonaws.com/account/""" + base64.b64encode(strTo) + '''">Account Management</a>'''
	print link
	msgText = """\
	<html>
	<head><body>
	<p>Hello """ + strFname + """,<br><br>You have been automatically enrolled in the Web Activity Monitoring Program.  We have partnered with your company to track your browsing and prevent sensitive information leakage. <br><br><br>Thanks,<br><br>-The Team<br><br>Alitheia Tech, Inc.<br><img src=cid:image1><br><br> To manage your account, please visit <br><br><a href="http://ec2-54-201-17-210.us-west-2.compute.amazonaws.com/account/""" + base64.b64encode(strTo) + '''">Account Management</a>'''
	temp = open('temp.htm', 'w+')
	temp.write(msgText)
	temp.close()
	msgRoot.attach(MIMEText(open("temp.htm").read(), 'html'))

	# This example assumes the image is in the current directory
	fp = open('lock.jpg', 'rb')
	msgImage = MIMEImage(fp.read(), _subtype="jpeg")
	fp.close()

	# Define the image's ID as referenced above
	msgImage.add_header('Content-ID', '<image1>')
	msgRoot.attach(msgImage)

	# Send the email (this example assumes SMTP authentication is required)
	import smtplib
	smtp = smtplib.SMTP()
	smtp.connect('localhost')
	smtp.sendmail(strFrom, strTo, msgRoot.as_string())
	print "Email sent to %s" % msgRoot['To']
	smtp.quit()
	os.remove('temp.htm')

#Populate a python dict with the contents of "targets.csv"
def pop_csv():
	i = 0
	global reader
	global fo
	fo = open('targets.csv', 'rb')
	reader = csv.DictReader(fo, dialect='excel')
	for row in reader:
		#print row #['Email'], row['First Name']
		db[i] = {"Email": row['Email'], "F_name": row['First Name'], "L_name": row['Last Name'], "Dept": row['Department'], "Loc": row['Location'], "Company": row['Company']}
		i += 1
	print 'Phishing targets populated.'


#Tornado web handler for root "/" request
class MainHandler(tornado.web.RequestHandler):
    def get(self):
		self.write('<html>Welcome to Alitheia\'s website.  Undergoing Maintenance....</html>')
	

#Tornado web handler for "/start" request
class StartHandler(tornado.web.RequestHandler):
	def get(self):
		global e
		e.clear()
		print "Web Request:  Starting Phishing emails..."
		pc = threading.Thread(target=phish_campaign)
		pc.start()

#Tornado web handler for "/stop" request
class StopHandler(tornado.web.RequestHandler):
    #def initialize(self, db):
        #self.db = db
	def get(self):
		global e
		e.set()
		print "Web Request: Stopping phishing emails..."


#Tornado web handler for "/account/<base64encoded_email>"
#Logs incoming, successful phishing attempts
class AccountHandler(tornado.web.RequestHandler):
    def get(self, ph_id):
		print ph_id
		import os
		file = 'caught.csv'
		if os.path.exists(file):
			fp = open(file,'a')
		else:
			fp = open(file,'w')
			header = "email, firstname, lastname\n"
			fp.write(header)
		global i
		test = base64.b64decode(ph_id)
		with open('targets.csv') as csvfile:
			reader = csv.DictReader(csvfile)
			for row in reader:
				if row['Email'] == test:
					buf = row['Email'] + ', ' +  row['First Name'] + ', ' + row['Last Name'] + '\n'
					fp.write(buf)
					self.write(pin)
					caught[i] = {"Email": row['Email'], "F_name": row['First Name'], "L_name": row['Last Name']}
					i += 1
					print "Added %s" % row['Email']
		
		#print "Total people phished: " + len(caught)
		
	
#Defining handlers for various web requests in Tornado			
def make_app():
    return tornado.web.Application([
		(r"/", MainHandler),
		(r"/stop", StopHandler),
		(r"/account/(.*)", AccountHandler),
		(r"/start", StartHandler)
    ])


#define listen port here (default is 80)
def startTornado():
	app = make_app()
	app.listen(80)
	tornado.ioloop.IOLoop.instance().start()
	
def stopTornado():
	import os,signal
	os.kill(os.getpid(), signal.SIGINT)
				

#start threaded Tornado instance on port 80
#handle web requests
#let Tornado take it from there.
def main():
	print("Starting web server...")
	#pop_csv()
	global e
	e = threading.Event()
	t = threading.Thread(target=startTornado) 
	t.start()
	pop_csv()

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    main()
    while True:           # added
        signal.pause()    # added
