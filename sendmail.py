
# coding: utf-8

# This function will send email to DVS common mailbox (`dvsprojectdev@gmail.com`). To add more receipients, we would need to add them to the email forwarding list inside gmail. This is because the emailing script used here goes through an unsecured channel (`smtp.gmail.com:587`) and all emails from this smtp server will be blocked by outlook.
# <br\>
# <br\>
# The work around is to perform email forwarding through DVS gmail account. This way, the emails are secured (SSL) and will go through outlook. Please ask Google for more info on adding more email addresses for gmail forwarding service. There should be tons of write up on this topic.

# In[ ]:


import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.Utils import COMMASPACE, formatdate
from email import Encoders
import os
import datetime
import unicodecsv as csv

smtpUser = 'dvsprojectdev@gmail.com'
smtpPass = 'singstatdvs123'

toAdd = 'dvsprojectdev@gmail.com'
fromAdd = smtpUser

today = datetime.date.today()

subject  = 'DGS Metadata File %s' % today.strftime('%Y %b %d')
header = 'To :' + toAdd + '\n' + 'From : ' + fromAdd + '\n' + 'Subject : ' + subject + '\n'
header2 = '<To :' + toAdd + '><' + 'From : ' + fromAdd + '><' + 'Subject : ' + subject + '>'
body = 'This is a extract of data.gov.sg metadata taken on %s' % today.strftime('%Y %b %d')

attach = 'DGS-extract.zip'

print header


def sendMail(to, subject, text, files=[]):
    assert type(to)==list
    assert type(files)==list

    msg = MIMEMultipart()
    msg['From'] = smtpUser
    msg['To'] = COMMASPACE.join(to)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject

    msg.attach( MIMEText(text) )

    for file in files:
        part = MIMEBase('application', "octet-stream")
        part.set_payload( open(file,"rb").read() )
        Encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename="%s"'
                       % os.path.basename(file))
        msg.attach(part)

    server = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo_or_helo_if_needed()
    server.starttls()
    server.ehlo_or_helo_if_needed()
    server.login(smtpUser,smtpPass)
    server.sendmail(smtpUser, to, msg.as_string())

    print 'Done'

    server.quit()


sendMail( [toAdd], subject, body, [attach] )

# Writes a log file upon success
with open('log.txt','a') as f2:
    writer = csv.DictWriter(f2, fieldnames=['Date','Action'], encoding='utf-8')
    writer.writerow({'Date':today, 'Action':'sendMail()' + header2})
    f2.close()

