from wtforms import Form, TextField, DateTimeField, validators
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
    dateDue = TextField('Due Date')
    priority = NumberInput()
    status = TextField('status')
    assignTo = TextField('assignedTo')

    #validators=[DateRange(min=datetime.now())]