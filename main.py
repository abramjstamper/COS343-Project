from flask import *
from flask import render_template
from flask.ext.mysqldb import MySQL
from forms import *

app = Flask(__name__)
mysql = MySQL()

# configuration settings
app.config["MYSQL_HOST"] = "127.0.0.1"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config['MYSQL_DB'] = 'event'
app.config['SECRET_KEY'] = 'very secret-y key value; shhhhh!'
mysql.init_app(app)

## API

##
## Budget
##

# returns budget for a given event_id
@app.route('/event/<int:event_id>/budget')
def budget(event_id):
    current_budget = Budget.loadBudget(event_id)
    response = current_budget.getAllInvoices();
    return render_template('budget/budget.html', response=response)

##
## Event
##

# returns all events from the database - not user specific (yet)
@app.route('/event')
def event():
    response = Event.getAllEvents()
    return render_template('event/event.html', response=response)

# returns a single event page for a given event_id
@app.route('/event/<int:event_id>')
def event_show(event_id):
    response = Event.loadEvent(event_id)
    return render_template('event/show.html', response=response)

# creates a new event
@app.route('/event/new', methods=['GET', 'POST'])
def newEvent():
    form = NewEvent(request.form)
    if request.method == 'POST' and form.validate():
        thisNewEvent = Event.createEvent(form.name.data, form.description.data, form.date_start, form.date_end.data,
                                         form.setupStart.data, form.teardownEnd.data)
        flash('New Event Created')
        newEvent_id = int(thisNewEvent.id)
        return redirect(url_for('event_show', event_id=(newEvent_id)))

    return render_template('event/new.html', form=form)

##
## Task
##

# returns the tasks for a given event_id
@app.route('/event/<int:event_id>/task')
def task(event_id):
    current_event = Event.loadEvent(event_id)
    response = current_event.getTasksForEvent();
    return render_template('task/task.html', response=response)

# creates a new task fo a given event_id
@app.route('/event/<int:event_id>/task/new', methods=['GET', 'POST'])
def newTask(event_id):
    current_event = Event.loadEvent(event_id)
    form = NewTask(request.form)
    if request.method == 'POST' and form.validate():
        thisNewTask = current_event.createTaskForEvent(form.name.data, form.dueDate.data, form.priority.data, form.status.data, "admin@admin.com")
        flash('New Task Created')
        return redirect(url_for('task', event_id=current_event.id))
    return render_template('task/new.html', form=form)

##
## Ticket
##

# returns tickets for a given event_id
@app.route('/event/<int:event_id>/ticket')
def ticket(event_id):
    current_event = Event.loadEvent(event_id)
    response = current_event.getAllTickets()
    return render_template('ticket/ticket.html', response=response)

##
## Vendor
##

# returns all vendors from the database
@app.route('/vendor')
def vendor():
    response = Vendor.getAllVendors()
    return render_template('vendor/vendor.html', response=response)

##
## Models
##

# an instance of a budget
class Budget:
    id = -1
    event_id = -1
    invoices = []

    def __init__(self, id, event_id):
        self.id = id
        self.event_id = event_id

    # Event.loadEvent() loads a single event based on the key given, and returns an event object of the specified key
    @classmethod
    def loadBudget(cls, key):
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM budget WHERE event_id = %(key)s;", {'key': key})
        data = cur.fetchone()
        id = data[0]
        event_id = data[1]
        return cls(id, event_id)

    def getAllInvoices(self):
        cursor = mysql.connection.cursor()
        cursor.execute(
            'SELECT * FROM invoice WHERE budget_id = %(id)s;',
            {'id': self.id})
        data = cursor.fetchall()
        allInvoices = []
        for i in data:
            allInvoices.append(
                {'event_id': self.event_id, 'id': i[0], 'total': i[1], 'description': i[2], 'isPaid': i[3], 'budget_id': i[4], 'vendor_id': i[5]})
        if allInvoices == []:
            return [{'event_id': self.event_id}]
        return allInvoices

# an instance of an event
class Event():
    id = -1
    name = ""
    eventStart = ""
    eventEnd = ""
    description = ""
    setupStart = ""
    teardownEnd = ""
    tasks = []

    # intializes variables
    def __init__(self, id, name, date_start, date_end, description, setupStart, teardownEnd):
        self.id = id
        self.name = name
        self.description = description
        self.date_start = date_start
        self.date_end = date_end
        self.setupStart = setupStart
        self.teardownEnd = teardownEnd

    # retrieves the tasks for a given event instance and puts them in a dictionary
    def getTasksForEvent(self):
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT event.id, task.id, task.priority, task.name, task.dateDue, task.status, task.assignedTo FROM event.task JOIN event.event ON event_id = event.id WHERE event_id = %(id)s;', {'id' : self.id})
        data = cursor.fetchall()
        allTasks = []
        for i in data:
            allTasks.append({'event_id':i[0], 'id': i[1], 'priority': i[2], 'name': i[3], 'dueDate': i[4], 'status': i[5], 'assignedTo': i[6]})
        if allTasks == []:
            return [{'event_id' : self.id}]
        else:
            self.tasks = allTasks
        return allTasks

    # creates a task for a given event instance - To be implemented
    def createTaskForEvent(self, name, dueDate, priority, status, user):
        #hardcoded params - user_assign - admin@admin.com
        params = {"name": name, "dueDate": dueDate, "priority": priority, "status": status,
                  "user_assign": user, "event_id": self.id}
        query = "INSERT INTO task (priority, name, dateDue, status, assignedTo, event_id) VALUES (%(priority)s, %(name)s, %(dueDate)s, %(status)s, %(user_assign)s, %(event_id)s);"
        conn = mysql.connection
        cursor = conn.cursor()
        # if it's 1 it's changed 1 thing in the table (adding one record) error code needed to catch exceptions
        cursor.execute(query, params)
        conn.commit()
        id = cursor.lastrowid
        self.tasks.append({'event_id':self.id, 'id': id, 'priority': priority, 'name': name, 'dateDue': dueDate, 'status': status, 'assignedTo': user})

    # return all events
    @staticmethod
    def getAllEvents():
        conn = mysql.connection
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM event.event;')
        data = cursor.fetchall()
        return data

    # Event.createEvent() creates an event in the database, and returns an event object
    @classmethod
    def createEvent(cls, name, description, date_start, date_end, setup_start, teardown_end):
        params = {"name": name, "date_start": date_start, "date_end": date_end, "description": description,
                  "setup_start": setup_start, "teardown_end": teardown_end}
        query = "INSERT INTO event (name, date_start, date_end, description, setup_start, teardown_end) VALUES (%(name)s, %(date_start)s, %(date_end)s, %(description)s, %(setup_start)s, %(teardown_end)s);"
        conn = mysql.connection
        cursor = conn.cursor()
        #if it's 1 it's changed 1 thing in the table (adding one record) error code needed to catch exceptions
        cursor.execute(query, params)
        conn.commit()
        id = cursor.lastrowid

        return cls(id, name, date_start, date_end, description, setup_start, teardown_end)

    # Event.loadEvent() loads a single event based on the key given, and returns an event object of the specified key
    @classmethod
    def loadEvent(cls, key):
        # select statment
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM event.event WHERE id = %(key)s;", {'key' : key})
        data = cur.fetchone()
        id = data[0]
        name = data[1]
        date_start = data[2]
        date_end = data[3]
        description = data[4]
        setupStart = data[5]
        teardownEnd = data[6]
        # print(id, name, date_start, date_end, description, setupStart, teardownEnd);
        return cls(id, name, date_start, date_end, description, setupStart, teardownEnd);

    def getAllTickets(self):
        cursor = mysql.connection.cursor()
        cursor.execute(
            'SELECT * FROM ticket WHERE event_id = %(id)s;',
            {'id': self.id})
        data = cursor.fetchall()
        allTickets = []
        for i in data:
            allTickets.append(
                {'event_id': self.id, 'id': i[0], 'price': i[1], 'section': i[2], 'seat_num': i[3], 'isSold': i[4]})
        if allTickets == []:
            return [{'event_id': self.id}]
        return allTickets

class Ticket:
    id = -1
    price = 0.00
    section = -1
    seat_num = -1
    isSold = False
    event_id = -1

    def __init__(self, id, price, section, seat_num, isSold, event_id):
        self.id = id
        self.price = price
        self.section = section
        self.seat_num = seat_num
        self.isSold = isSold
        self.event_id = event_id

    def getAllTickets(self):
        cursor = mysql.connection.cursor()
        cursor.execute(
            'SELECT * FROM ticket WHERE event_id = %(id)s;',
            {'id': self.event_id})
        data = cursor.fetchall()
        allTickets = []
        for i in data:
            allTickets.append(
                {'event_id': self.event_id, 'id': i[0], 'price': i[1], 'section': i[2], 'seat_num': i[3], 'isSold': i[4]})
        if allTickets == []:
            return [{'event_id': self.event_id}]
        return allTickets


# an instance of a vendor
class Vendor:
    id = -1
    name = ""
    phone = ""
    address = ""
    email = ""
    #array of invoices - to be implemented
    invoices = []

    def __init__(self, id, name, phone, address, email):
        self.id = id
        self.name = name
        self.phone = phone
        self.address = address
        self.email = email

    # return all vendors
    @staticmethod
    def getAllVendors():
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM event.vendor;')
        data = cursor.fetchall()
        return data

if __name__ == '__main__':
    app.debug = True
    app.run()