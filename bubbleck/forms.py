from flask import request, g
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
	''' Form for editing an existing course '''
	max_num_sections = 20
	name        = StringField(u'Course Name', [validators.required()])
	sections    = FieldList(StringField(u'Section'),
				min_entries = max_num_sections)

# ===================================================
class NewCourseForm(CourseForm):
	''' Form for creating a new course '''
	max_num_sections = 20
	num_sections= SelectField(u'# of Sections', choices=[(str(x),str(x)) for x in range(1,max_num_sections+1)])
	
# ===================================================
class ForgottenPasswordForm(Form):
	''' Form for requesting a password reset '''
	email       = StringField(u'Email Address', [validators.Email(message=u'That\'s not a valid email address.')])

# ===================================================
class LoginForm(Form):
	''' Form for login screen '''
	email       = StringField(u'Email Address', [validators.Email(message=u'That\'s not a valid email address.')])
	password    = PasswordField(u'Password')
	remember_me = BooleanField(u'Remember Me')

# ===================================================
class UserForm(Form):
	''' Form for editing an existing user '''
	email       = StringField(u'Email Address', [validators.Email(message=u'That\'s not a valid email address.')])
	name        = StringField(u'Full Name', [validators.required()])
	teachername = StringField(u'Teacher Name', [validators.required()])

# ===================================================
class RegisterForm(UserForm):
	''' Form for creating a new user '''
	password    = PasswordField(u'Password', [
				validators.EqualTo(u'confirm', message=u'Passwords must match'), 
				validators.Length(min=6, message=u'Try a slightly longer password.')
				])
	confirm     = PasswordField(u'Confirm Password')
	geography   = StringField(u'Geographic Region')
	hearabout   = StringField(u'How did you find Bubble&#x2714;')
	recaptcha   = RecaptchaField(u'Are You Human?')

# ===================================================
class ChangePasswordForm(Form):
	''' Form for changing an existing password '''
	oldpassword = PasswordField(u'Current Password')
	newpassword = PasswordField(u'New Password', [
				validators.EqualTo(u'confirm', message=u'Passwords must match'), 
				validators.Length(min=6, message=u'Try a slightly longer password.')
				])
	confirm     = PasswordField(u'Confirm Password')
