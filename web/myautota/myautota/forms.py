from flask import request
from wtforms import BooleanField
from wtforms import Form
from wtforms import PasswordField
from wtforms import StringField
from wtforms import validators
from flask_wtf import RecaptchaField

# ===================================================
class LoginForm(Form):
	email       = StringField(u'Email Address', [validators.Email(message=u'That\'s not a valid email address.')])
	password    = PasswordField(u'Password')
	remember_me = BooleanField(u'Remember Me')

# ===================================================
class RegisterForm(Form):
	email       = StringField(u'Email Address', [validators.Email(message=u'That\'s not a valid email address.')])
	name        = StringField(u'Full Name')
	password    = PasswordField(u'Password', [
				validators.EqualTo(u'confirm', message=u'Passwords must match'), 
				validators.Length(min=6, message=u'Try a slightly longer password.')
				])
	confirm     = PasswordField(u'Confirm Password')
	teachername = StringField(u'Teacher Name')
	geography   = StringField(u'Geographic Region')
	hearabout   = StringField(u'How did you find myAutoTA?')
	recaptcha   = RecaptchaField(u'Human?')
