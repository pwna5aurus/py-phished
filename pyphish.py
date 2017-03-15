import sys
import threading
import tornado.ioloop
import tornado.web
import csv
import smtplib
import base64



#filename = ".\\index.html"
phish_f = "phish.html"
targets = "targets.csv"
#ph_msg = ".\\ph_msg.txt"
#fin = open(filename, 'rb').read()
pin = open(phish_f, 'rb').read()
tin = open(targets, 'rb')
csv_r = csv.DictReader(tin, dialect='excel')
csv_d = list(csv_r)
row_count = len(csv_d)
disp = {}
caught = {}
i = 0
fr_addr = 'accounts@alitheia.com'
to_addr = ''
#msg = open(ph_msg, 'rb').read()
ph_link = ''

def testmail():

	# Send an HTML email with an embedded image and a plain text message for
	# email clients that don't want to display the HTML.

	from email.MIMEMultipart import MIMEMultipart
	from email.MIMEText import MIMEText
	from email.MIMEImage import MIMEImage

	# Define these once; use them twice!
	strFrom = '"Accounts Receivable"<internal@accounts.westcentralus.cloudapp.azure.com>'
	strTo = 'ben.floyd@pse.com'

	# Create the root message and fill in the from, to, and subject headers
	msgRoot = MIMEMultipart()
	msgRoot['Subject'] = 'Expired invoice...'
	msgRoot['From'] = strFrom
	msgRoot['To'] = strTo
	#msgRoot.preamble = 'This is a multi-part message in MIME format/'

	# Encapsulate the plain and HTML versions of the message body in an
	# 'alternative' part, so message agents can decide which they want to display.
	msgAlternative = MIMEMultipart('alternative')
	msgRoot.attach(msgAlternative)

	msgText = MIMEText('Your mail client does not support HTML.')
	msgAlternative.attach(msgText)

	# We reference the image in the IMG SRC attribute by the ID we give it below
	msgText = MIMEText('<h1>Hi, <br><br>We just wanted to follow up from our meeting the other day when we talked about zeroing out the balance.  Please let me know!<br><br>Best,<br>Ben<br><br>P.S.<a href="http://accounts.westcentralus.cloudapp.azure.com"><b>Please go update your account with us!<br><br><img src="cid:image1"><br></a>', 'html')
	msgAlternative.attach(msgText)

	# This example assumes the image is in the current directory
	fp = open('test.jpg', 'rb')
	msgImage = MIMEImage(fp.read(), _subtype="jpeg")
	fp.close()

	# Define the image's ID as referenced above
	msgImage.add_header('Content-ID', '<image1>')
	msgRoot.attach(msgImage)

	# Send the email (this example assumes SMTP authentication is required)
	import smtplib
	smtp = smtplib.SMTP()
	smtp.connect('localhost')
	#smtp.login('exampleuser', 'examplepass')
	smtp.sendmail(strFrom, strTo, msgRoot.as_string())
	print msgRoot.as_string()
	smtp.quit()



def pop_csv():
	i = 0
	with open('targets.csv') as csvfile:
		reader = csv.DictReader(csvfile)
		for row in reader:
			#print row['Email'], row['First Name']
			disp[i] = {"Email": row['Email'], "F_name": row['First Name']}
			i += 1
	# rownum = 0
	# rowtot = row_count
	# while rownum < rowtot:
		# print rownum
		# if rownum == 0:
			# print csv
			# rownum += 1
	# rownum = csv_r.line_num()
	# print ("Csv line number is %d" % rownum)
	# '''rownum = 0
	# for row in csv_r:
	# # Save header row.
		# if rownum ==0:
			# header = row
			# cols = row.split(",")
			# disp[rownum] = [str(item) for item in row]
		# else:
			# colnum = 0
			# for col in row:
				# disp[rownum,colnum] = col
				# colnum += 1
				# rownum += 1'''
	#print(disp)
		print row_count
		print 'Dear %s,\n\tWe regret to inform you that you have been phished.\n\n%s' % (disp[2]["F_name"], base64.b64encode(disp[2]["Email"]))



class MainHandler(tornado.web.RequestHandler):
    def get(self):
		#self.write(csv_r)
		#self.write(disp)
		self.write(pin)
		#testmail()
	
class StopHandler(tornado.web.RequestHandler):
    #def initialize(self, db):
        #self.db = db

    def get(self):
		self.write("Stopping phishing campaign...")
		ioloop = tornado.ioloop.IOLoop.instance()
		ioloop.add_callback(ioloop.stop)
		print "Asked Tornado to exit"
		
	#app = Application([
		#url(r"/", MainHandler),
		#url(r"/stop", StopHandler)
    #])
class AccountHandler(tornado.web.RequestHandler):
    def get(self, ph_id):
		print ph_id
		global i
		test = base64.b64decode(ph_id)
		with open('targets.csv') as csvfile:
			reader = csv.DictReader(csvfile)
			for row in reader:
				#print row['Email'], row['First Name']
				#disp[i] = {"Email": row['Email'], "F_name": row['First Name']}
				if row['Email'] == test:
					self.write(row['Email'])
					caught[i] = {"Email": row['Email'], "F_name": row['First Name'], "L_name": row['Last Name']}
					i += 1
					print "Added %s" % row['Email']
		
		print len(caught)
		
			
def make_app():
    return tornado.web.Application([
		(r"/", MainHandler),
		(r"/stop", StopHandler),
		(r"/account/(.*)", AccountHandler)
    ])



def startTornado():
	app = make_app()
	app.listen(80)
	tornado.ioloop.IOLoop.instance().start()
	
def stopTornado():
    ioloop = tornado.ioloop.IOLoop.instance()
    ioloop.add_callback(ioloop.stop)
    print "Asked Tornado to exit"

#def target():
#	rownum = 0
#	print ("Csv line number is " %s, csv_r.line_num())
#	'''for row in csv_r:
#		# Save header row.
#		if rownum ==0:
#			header = row
#		else:
#			colnum = 0
#			for col in row:
#				print '%-8s: %s' % (header[colnum], col)
#				colnum += 1
#				rownum += 1'''
				

def main():
	print("Starting web server...")
	#pop_csv()
	t = threading.Thread(target=startTornado) 
	try:
		t.start()
	# signal : CTRL + BREAK on windows or CTRL + C on linux
	except KeyboardInterrupt:
		t.stop()	
		time.sleep(5)
		stopTornado()
		t.join()


if __name__ == "__main__":
    main()
