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
