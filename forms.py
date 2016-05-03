from wtforms import *
from datetime import datetime, date
from wtforms_components import NumberInput, DateRange
from flask.ext.wtf import *

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
    email = TextField('Email')
    password = PasswordField('Password')

class NewUser(Form):
    name = TextField('Name')
    email = TextField('Email')
    password = PasswordField('Password')
    password_conf = PasswordField('Password Confirmation')