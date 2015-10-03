from flask import request
from wtforms import BooleanField
from wtforms import FieldList
from wtforms import Form
from wtforms import PasswordField
from wtforms import StringField
from wtforms import validators
from flask_wtf import RecaptchaField

# ===================================================
class CourseForm(Form):
	name        = StringField(u'Course Name', [validators.required()])
	sections    = FieldList(StringField(u'Section Name'),
				min_entries = 10,
				max_entries = 10)
	
# ===================================================
class LoginForm(Form):
	email       = StringField(u'Email Address')
	password    = PasswordField(u'Password')
	remember_me = BooleanField(u'Remember Me')

# ===================================================
class RegisterForm(Form):
	email       = StringField(u'Email Address', [validators.Email(message=u'That\'s not a valid email address.')])
	name        = StringField(u'Full Name', [validators.required()])
	password    = PasswordField(u'Password', [
				validators.EqualTo(u'confirm', message=u'Passwords must match'), 
				validators.Length(min=6, message=u'Try a slightly longer password.')
				])
	confirm     = PasswordField(u'Confirm Password')
	teachername = StringField(u'Teacher Name', [validators.required()])
	geography   = StringField(u'Geographic Region')
	hearabout   = StringField(u'How did you find myAutoTA?')
	recaptcha   = RecaptchaField(u'Human?')
