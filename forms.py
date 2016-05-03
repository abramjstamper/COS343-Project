from flask.ext.wtf import Form
from wtforms import TextField, DateTimeField, PasswordField, validators
#from flask.wtf import Form, TextField, PasswordField, validators
from datetime import datetime, date
from wtforms_components import NumberInput, DateRange, Email, EmailField
#from wtforms.fields.html5 import EmailField


class NewEvent(Form):
    name = TextField('Event Name')
    description = TextField('Description')
    date_start = DateTimeField('Date Start')
    date_end = DateTimeField('Date End')
    setupStart = DateTimeField('Setup Start Date')
    teardownEnd = DateTimeField('Teardown End Date')

    #validators=[DateRange(min=datetime.now())]

class NewTask(Form):
    name = TextField('Task Name')
    dueDate = DateTimeField('Due Date')
    priority = TextField('Priority')
    status = TextField('Status')
    assignTo = TextField('User Assigned To')

class Login(Form):
    email = EmailField('Email', validators=[validators.Email(), validators.DataRequired()])
    password = PasswordField('Password', validators=[validators.DataRequired()])

class NewUser(Form):
    name = TextField('Name', validators=[validators.DataRequired()])
    email = EmailField('Email', validators=[Email(), validators.DataRequired()])
    password = PasswordField('Password', validators=[validators.EqualTo('password_conf', message='Passwords must match'), validators.DataRequired()])
    password_conf = PasswordField('Password Confirmation', validators=[validators.DataRequired()])