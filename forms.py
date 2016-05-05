from flask.ext.wtf import Form
from wtforms import TextField, DateTimeField, PasswordField, validators, BooleanField, ValidationError, SelectField
#from flask.wtf import Form, TextField, PasswordField, validators
from datetime import datetime, date
from wtforms_components import NumberInput, DateRange, Email, EmailField, DecimalField
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
    status = SelectField('Status', choices=[(0, 'Not Complete'), (1, 'Pending'), (2, 'Complete')], coerce=int)
    assignTo = TextField('User Assigned To')

class Login(Form):
    email = EmailField('Email', validators=[validators.Email(), validators.DataRequired()])
    password = PasswordField('Password', validators=[validators.DataRequired()])

class NewUser(Form):
    name = TextField('Name', validators=[validators.DataRequired()])
    email = EmailField('Email', validators=[Email(), validators.DataRequired()])
    password = PasswordField('Password', validators=[validators.EqualTo('password_conf', message='Passwords must match'), validators.DataRequired()])
    password_conf = PasswordField('Password Confirmation', validators=[validators.DataRequired()])

class NewInvoice(Form):
    total = TextField('Total', validators=[validators.DataRequired()])
    description = TextField('Description')
    isPaid = BooleanField('Has been paid?')
    vendor_id = TextField('Vendor ID', validators=[validators.DataRequired()])

class NewTicket(Form):
    numTicketsTotal = TextField('Number of Total Tickets Being Sold')
    numSeatsPerSection = TextField('Number of Seats Per Section')
    numSections = TextField('Number of sections')
    price = TextField('Price', validators=[validators.DataRequired()])

    #if int(numTicketsTotal.data) != int(numSeatsPerSection.data) * int(numSections.data):
     #   raise ValidationError('Number of Total Tickets Being Sold Must Equal Number of Seats Per Section multipled by Number of Sections')

