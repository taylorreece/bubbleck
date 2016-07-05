#!/usr/bin/python3
# This script is designed to be run constantly (invoked every minute)

import smtplib

from bck import database
from bck import bckconfig
from bck import user

db = database.BckDB()

#===================================
def send_emails():
	query = 'SELECT * FROM email_users WHERE sent_at IS NULL'
	emails = db.queryDictList(query)
	for email in emails:
		message = "From: {0}\r\n".format(bckconfig.smtp_username)
		to  = ['']
		cc  = ['']
		bcc = ['']
		if email['usersid']:
			u = user.getUserByID(email['usersid'])
			to = [u.email]
		if email['additional_to']:	
			to  = to + email['additional_to'].split(',')
		if to:
			message = message + "To: {0}\r\n".format(','.join(to))
		if email['additional_cc']:
			cc  = email['additional_cc'].split(',')
			message = message + "CC: {0}\r\n".format(','.join(cc))
		if email['additional_bcc']:
			bcc  = email['additional_bcc'].split(',')
		if email['subject']:
			message = message + "Subject: {0}\r\n\r\n".format(email['subject'])
		if email['body']:
			message = message + email['body']
		server = smtplib.SMTP('{0}:{1}'.format(bckconfig.smtp_server, bckconfig.smtp_port))
		if bckconfig.smtp_use_tls:
			server.starttls()
		server.login(bckconfig.smtp_username, bckconfig.smtp_password)
		server.sendmail(bckconfig.smtp_username, to + cc + bcc, message)
		server.quit()
		print('Sent email (id={0}) successfully'.format(email['emailsid']))
		query = 'UPDATE email_users SET sent_at=NOW() WHERE emailsid={0}'.format(emailsid)
		db.queryNoResults(query,(email['emailsid'],))


send_emails()
