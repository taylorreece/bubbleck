from flask import request
from wtforms import BooleanField
from wtforms import Form
from wtforms import PasswordField
from wtforms import StringField
from wtforms import validators

# ===================================================
class LoginForm(Form):
	email       = StringField('Email Address', [validators.Email(message=u'That\'s not a valid email address.')])
	password    = PasswordField('Password', [validators.Length(min=6, max=35)])
	remember_me = BooleanField('Remember Me')

# ===================================================
class RegisterForm(Form):
	email       = StringField('Email Address', [
				validators.Email(message=u'That\'s not a valid email address.')
				])
	name        = StringField('Full Name')
	password    = PasswordField('Password', [
				validators.EqualTo('confirm', message='Passwords must match'), 
				validators.Length(min=6, message=u'Try a slightly longer password....')
				])
	confirm     = PasswordField('Confirm Password')
	teachername = StringField('Full Name')
