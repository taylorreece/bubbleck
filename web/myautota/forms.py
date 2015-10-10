from flask import request
from wtforms import BooleanField
from wtforms import FieldList
from wtforms import Form
from wtforms import PasswordField
from wtforms import SelectField
from wtforms import StringField
from wtforms import validators
from flask_wtf import RecaptchaField

# ===================================================
class CourseForm(Form):
	max_num_sections = 20
	name        = StringField(u'Course Name', [validators.required()])
	num_sections= SelectField(u'# of Sections', choices=[(str(x),str(x)) for x in range(1,max_num_sections+1)])
	sections    = FieldList(StringField(u'Section'),
				min_entries = max_num_sections)
	
# ===================================================
class LoginForm(Form):
	email       = StringField(u'Email Address')
	password    = PasswordField(u'Password')
	remember_me = BooleanField(u'Remember Me')

# ===================================================
class UserForm(Form):
	email       = StringField(u'Email Address', [validators.Email(message=u'That\'s not a valid email address.')])
	name        = StringField(u'Full Name', [validators.required()])
	teachername = StringField(u'Teacher Name', [validators.required()])

# ===================================================
class RegisterForm(UserForm):
	password    = PasswordField(u'Password', [
				validators.EqualTo(u'confirm', message=u'Passwords must match'), 
				validators.Length(min=6, message=u'Try a slightly longer password.')
				])
	confirm     = PasswordField(u'Confirm Password')
	geography   = StringField(u'Geographic Region')
	hearabout   = StringField(u'How did you find myAutoTA?')
	recaptcha   = RecaptchaField(u'Are You Human?')
