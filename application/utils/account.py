#coding:utf-8
from flask import session
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import random
import datetime
from db_helper import DBHelper
from md5_util import get_md5_value

class Account(object):
	"""docstring for AccountUtil"""

	@staticmethod
	def register(username, email, password):
		DBHelper.create_user(username, email, password)

	@staticmethod
	def isRegister(email):
		user = DBHelper.get_user(email)
		if user:
			return True
		return False

	@staticmethod
	def login(email, password):
		password = get_md5_value(password)
		user = DBHelper.get_user(email)
		if user:
			if user.password == password:
				session['email'] = email
				return True
			else:
				return False
		return False

	@staticmethod
	def logout():
		session.pop('email', None)

	@staticmethod
	def isLogin():
		if 'email' in session:
			return True
		return False

	@staticmethod
	def get_current_user():
		email = session['email']
		user = DBHelper.get_user(email)
		return user
	@staticmethod
	def generate_url(user):
		key = random.sample('zyxwvutsrqponmlkjihgfedcba',6)
		time = datetime.datetime.now();
		md5 = get_md5_value(user.username+key+time)
		DBHelper.create_reset_info(user.id, time, md5)
		return '127.0.0.1/' + md5

	@staticmethod
	def send_email(user):
		smtpserver = 'smtp.163.com'
		username = '***'
		password = '***'
		sender = 'hhxnbw@163.com'
		receiver = user.name
		msg = MIMEText(Account.generate_url(),'text','utf-8')
		msg['Subject'] = Header("重置密码", 'utf-8')
		try:
			smtp = smtplib.SMTP()
			smtp.connect(smtpserver)
			smtp.login(username, password)
			smtp.sendmail(sender, receiver, msg.as_string())
			smtp.quit()
			return True
		except smtplib.SMTPException:
			return False