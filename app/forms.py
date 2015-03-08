from wtforms import (Form, TextField, PasswordField, HiddenField,
                     validators, RadioField, SelectField, TextAreaField, FileField)

import pycountry

# For older versions of wtforms.
#from wtforms.validators import DataRequired
#from wtforms.validators import Required, EqualTo, validators, Length
#from flask.ext.wtf import Form, TextField, PasswordField
#from flask.ext.wtf import Required, EqualTo, validators, Length


# Set your classes here.
class RegisterForm(Form):
    """
    Form for Register user
    """
    #Need to change the email using Email validator.

    name = TextField('Username',[validators.Required('Username should have 4-35 characters'),
                     validators.Length(min=4, max=35)])
    email = TextField('Email', [validators.Required("Email should be 4-35 characters"),
                      validators.Length(min=4, max=35)])
    password = PasswordField('Password', [validators.Required("passwords max length 30"),
                             validators.Length(min=4, max=30)])
    confirm = PasswordField('Repeat Password', [validators.Required("Passwords must match"),
                            validators.EqualTo
                            ('password', message='Passwords did not match')])
    institution = TextField('Company', [validators.Required("Max 40 characters"),
                            validators.Length(min=3, max=40)])


class LoginForm(Form):
    """
    Form for Login of the user
    """
    name = TextField('Username', [validators.Required(),
        validators.Length(min=3, max=50)])
    password = PasswordField('Password', [validators.Required(),
        validators.Length(min=3, max=80)])


class ForgotForm(Form):
    """
    Forgot password form of the user
    """
    email = TextField('Email', [validators.Required(),
                      validators.Length(min=3, max=50)])
    security_question = TextField('Security Question', [validators.Required(),
                                  validators.Length(min=10, max=40)])
    security_answer = TextField('Security Answer', [validators.Required(),
                                validators.Length(min=6, max=40)])


class CreateMessageForm(Form):
    """
    Create Message form
    """

    message = TextAreaField('message', [validators.Required(),
        validators.Length(min=3, max=360)])



class SearchJobForm(Form):
    """
    Search Job form
    """

    job_keyword = TextField('job_keyword')
    job_companyname = TextField('job_companyname')
    job_title = TextField('job_title')


