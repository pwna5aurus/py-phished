# Send an HTML email with an embedded image and a plain text message for
# email clients that don't want to display the HTML.

from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEImage import MIMEImage

# Define these once; use them twice!
strFrom = '"Accounts Receivable"<rooty@mailserver.s0stgakqb2ju1ifzv343gza4hb.yx.internal.cloudapp.net>'
strTo = 'nick.pittak@pse.com'

# Create the root message and fill in the from, to, and subject headers
msgRoot = MIMEMultipart()
msgRoot['Subject'] = 'FW: Expired invoice...'
msgRoot['From'] = strFrom
msgRoot['To'] = strTo
#msgRoot.preamble = 'This is a multi-part message in MIME format/'

# Encapsulate the plain and HTML versions of the message body in an
# 'alternative' part, so message agents can decide which they want to display.
msgAlternative = MIMEMultipart('alternative')
msgRoot.attach(msgAlternative)

msgText = MIMEText('This is the alternative plain text message.')
msgAlternative.attach(msgText)

# We reference the image in the IMG SRC attribute by the ID we give it below
msgText = MIMEText('<h1>Hi, Nick,<br><br>We just wanted to follow up from our meeting the other day when we talked about zeroing out the balance.  Please let me know!<br><br>Best,<br>Ben<br><br>P.S.<a href="http://mailserver.s0stgakqb2ju1ifzv343gza4hb.yx.internal.cloudapp.net"><b>Please go update your account with us!<br><br><img src="cid:image1"><br></a>', 'html')
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
