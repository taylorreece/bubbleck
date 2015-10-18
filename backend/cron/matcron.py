#!/usr/bin/python3
# This script is designed to be run constantly (invoked every minute)

import smtplib

from mat import database
from mat import matconfig
from mat import user

db = database.MatDB()

#===================================
def sendEmails():
	query = 'SELECT * FROM email_users WHERE sent_at IS NULL'
	emails = db.queryDictList(query)
	for email in emails:
		message = "From: %s\r\n" % matconfig.smtp_username
		to  = ['']
		cc  = ['']
		bcc = ['']
		if email['usersid']:
			u = user.getUserByID(email['usersid'])
			to = [u.email]
		if email['additional_to']:	
			to  = to + email['additional_to'].split(',')
		if to:
			message = message + "To: %s\r\n" % ','.join(to)
		if email['additional_cc']:
			cc  = email['additional_cc'].split(',')
			message = message + "CC: %s\r\n" % ','.join(cc)
		if email['additional_bcc']:
			bcc  = email['additional_bcc'].split(',')
		if email['subject']:
			message = message + "Subject: %s\r\n\r\n" % email['subject']
		if email['body']:
			message = message + email['body']
		server = smtplib.SMTP('%s:%s' % (matconfig.smtp_server, matconfig.smtp_port))
		if matconfig.smtp_use_tls:
			server.starttls()
		server.login(matconfig.smtp_username, matconfig.smtp_password)
		server.sendmail(matconfig.smtp_username, to + cc + bcc, message)
		server.quit()
		print('Sent email (id=%s) successfully' % email['emailsid'])
		query = 'UPDATE email_users SET sent_at=NOW() WHERE emailsid=%s'
		db.queryNoResults(query,(email['emailsid'],))


sendEmails()
