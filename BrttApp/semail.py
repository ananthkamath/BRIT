#!/usr/bin/python

import smtplib
import email
from email.MIMEMultipart import MIMEMultipart
from email.mime.base import MIMEBase

def send_email(fname,email_id):
    sender = 'test@test.com'
    receiver = email_id

    msg = MIMEMultipart('mixed')
    msg['Subject'] = "Results of your ER test"
    msg['From'] = "ananth.atg@gmail.com"
    msg['To'] = "akamath@akamai.com"
    fp = open(fname, 'rb')
    file1=email.mime.base.MIMEBase('application','vnd.ms-excel')
    file1.set_payload(fp.read())
    fp.close()
    email.encoders.encode_base64(file1)
    file1.add_header('Content-Disposition','attachment',filename=fname)
    msg.attach(file1)
    composed = msg.as_string()
   
    try:
        server = smtplib.SMTP('smtp.gmail.com',587)
        server.ehlo()
        server.starttls()
        server.login("test@test.com","")
        server.sendmail(sender, receiver, composed)         
        server.quit()
        print "Successfully sent email"
    except:
        print "Error: unable to send email"
