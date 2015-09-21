from wtforms import Form, BooleanField, StringField, validators, PasswordField
from flask import request

class LoginForm(Form):
	email       = StringField('Email Address', [validators.Email(message=u'That\'s not a valid email address.')])
	password    = PasswordField('Password', [validators.Length(min=6, max=35)])
	remember_me = BooleanField('Remember Me')
