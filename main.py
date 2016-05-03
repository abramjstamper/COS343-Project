from flask import *
import flask.ext.login as flask_login
from flask import render_template
from flask.ext.mysqldb import MySQL
from forms import *

#App
app = Flask(__name__)

# configuration settings
app.config["MYSQL_HOST"] = "127.0.0.1"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config['MYSQL_DB'] = 'event'
app.config['SECRET_KEY'] = 'very secret-y key value; shhhhh!'

#initializations
mysql = MySQL()
mysql.init_app(app)
login_manager = flask_login.LoginManager()
login_manager.init_app(app)

## API

##
## Budget
##

# returns budget for a given event_id
@app.route('/event/<int:event_id>/budget')
def budget(event_id):
    current_budget = Budget.loadBudget(event_id)
    response = current_budget.getAllInvoices()
    response.append({"totalSold": Budget.getTotalCountPaid(event_id)})
    response.append({"totalSold": Budget.getTotalExpenses(event_id)})
    return render_template('budget/budget.html', response=response)

##
## Event
##

# edits an event based on a given event_id
@app.route('/event/<int:event_id>/edit', methods=['GET', 'POST'])
def editEvent(event_id):
    form = NewEvent(request.form)
    if request.method == 'GET':
        current_event = Event.loadEvent(event_id)
        form.name.data = current_event.name
        form.description.data = current_event.description
        form.date_start.data = current_event.date_start
        form.date_end.data = current_event.date_end
        form.setupStart.data = current_event.setupStart
        form.teardownEnd.data = current_event.teardownEnd
    if request.method == 'POST' and form.validate():
        thisNewEvent = Event.updateEvent(event_id, form.name.data, form.description.data, form.date_start.data, form.date_end.data,
                                         form.setupStart.data, form.teardownEnd.data)
        flash('Event ' + str(event_id) +' Updated')
        newEvent_id = int(event_id)
        return redirect(url_for('event_show', event_id=event_id))
    return render_template('event/edit.html', form=form)

# returns all events from the database - not user specific (yet)
@app.route('/event')
def all_events():
    response = Event.getAllEvents()
    return render_template('event/event.html', response=response)

# returns a single event page for a given event_id
@app.route('/event/<int:event_id>')
def event(event_id):
    response = {}
    response['event'] = Event.loadEvent(event_id)
    response['budget'] = Budget.loadBudget(event_id).getAllInvoices()
    response['budget'].append({"totalSold": Budget.getTotalCountPaid(event_id)})
    response['budget'].append({"totalSold": Budget.getTotalExpenses(event_id)})
    response['task'] = Task.getTasksForEvent(event_id)
    response['ticket'] = Ticket.getAllTickets(event_id)
    response['ticket'].append({"totalSold": Ticket.getTotalCountSold(event_id)})
    response['ticket'].append({"totalSold": Ticket.getTotalPriceSold(event_id)})
    return render_template('event/show.html', response=response)

# creates a new event
@app.route('/event/new', methods=['GET', 'POST'])
def newEvent():
    form = NewEvent(request.form)
    if request.method == 'POST' and form.validate():
        thisNewEvent = Event.createEvent(form.name.data, form.description.data, form.date_start.data, form.date_end.data,
                                         form.setupStart.data, form.teardownEnd.data)
        flash('New Event Created')
        newEvent_id = int(thisNewEvent.id)
        return redirect(url_for('event_show', event_id=(newEvent_id)))
    return render_template('event/new.html', form=form)

###
### Login/Log Out
###

@app.route('/user/new', methods=['GET', 'POST'])
def newUser():
    form = NewUser(request.form)
    if request.method == 'POST' and form.validate():
        newUser = User.createUser(form.name.data, form.email.data, form.password.data, form.password_conf.data)
        flash('New User Created')
        return redirect(url_for('login'))
    return render_template('login/new.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = Login(request.form)
    if request.method == 'GET':
        return render_template('login/login.html', form=form)
    email = form.email.data
    users = User.getUsers()
    if form.password.data == users[email]['password']:
        user = User()
        user.id = email
        flask_login.login_user(user)
        return redirect(url_for('protected'))

    return 'Bad login'

@app.route('/protected')
@flask_login.login_required
def protected():
    return 'Logged in as: ' + flask_login.current_user.id

@app.route('/logout')
def logout():
    flask_login.logout_user()
    return 'Logged out'

@login_manager.unauthorized_handler
def unauthorized_handler():
    return 'Unathorized'

##
## Task
##

# edits a task for a given event_id and given task_id
@app.route('/event/<int:event_id>/task/<int:task_id>/edit', methods=['GET', 'POST'])
def editTask(event_id, task_id):
    form = NewTask(request.form)
    if request.method == 'GET':
        current_event = Event.loadEvent(event_id)
        current_task = Task.loadTask(task_id)
        form.priority.data = current_task.priority
        form.name.data = current_task.name
        form.dueDate.data = current_task.dateDue
        form.status.data = current_task.status
        form.assignTo.data = current_task.assignedTo
    if request.method == 'POST' and form.validate():
        thisUpdatedTask = Task.updateTask(task_id, form.priority.data, form.name.data, form.dueDate.data,
                                         form.status.data,
                                         form.assignTo.data, event_id)
        flash('Task ' + str(task_id) + ' Updated')
        updatedTask_id = int(task_id)
        return redirect(url_for('task', event_id=event_id))
    return render_template('task/edit.html', form=form)

# returns the tasks for a given event_id
@app.route('/event/<int:event_id>/task/new', methods=['GET', 'POST'])
def newTask(event_id):
    current_event = Event.loadEvent(event_id)
    form = NewTask(request.form)
    if request.method == 'POST' and form.validate():
        thisNewTask = Task.createTaskForEvent(form.name.data, form.dueDate.data, form.priority.data, form.status.data, "admin@admin.com", event_id)
        flash('New Task Created')
        return redirect(url_for('task', event_id=current_event.id))
    return render_template('task/new.html', form=form)

# retrevies all the tasks for a given event_id
@app.route('/event/<int:event_id>/task')
def task(event_id):
    current_event = Event.loadEvent(event_id)
    response = Task.getTasksForEvent(event_id)
    return render_template('task/task.html', response=response)

##
## Ticket
##

# returns tickets for a given event_id
@app.route('/event/<int:event_id>/ticket')
def ticket(event_id):
    current_event = Event.loadEvent(event_id)
    response = Ticket.getAllTickets(event_id)
    response.append({"totalSold": Ticket.getTotalCountSold(event_id)})
    response.append({"totalSold": Ticket.getTotalPriceSold(event_id)})
    return render_template('ticket/ticket.html', response=response)

@app.route('/user')
def users():
    response = User.getUsers()
    return render_template('user/user.html', response=response)

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

###
### Budget/Invoice
###

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

    @staticmethod
    def getTotalExpenses(event_id):
        cursor = mysql.connection.cursor()
        cursor.execute(
            'SELECT SUM(total) FROM invoice WHERE budget_id = %(id)s AND isPaid = 1;',
            {'id': event_id})
        data = cursor.fetchone()
        return data[0]

    @staticmethod
    def getTotalCountPaid(event_id):
        cursor = mysql.connection.cursor()
        cursor.execute(
            'SELECT count(isPaid) FROM invoice WHERE budget_id = %(id)s AND isPaid = 1;',
            {'id': event_id})
        data = cursor.fetchone()
        return data[0]

###
### Event
###

class Event():
    id = -1
    name = ""
    eventStart = ""
    eventEnd = ""
    description = ""
    setupStart = ""
    teardownEnd = ""

    # intializes variables
    def __init__(self, id, name, date_start, date_end, description, setupStart, teardownEnd):
        self.id = id
        self.name = name
        self.description = description
        self.date_start = date_start
        self.date_end = date_end
        self.setupStart = setupStart
        self.teardownEnd = teardownEnd

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

    @classmethod
    def updateEvent(cls, event_id, name, description, date_start, date_end, setup_start, teardown_end):
        params = {"name": name, "date_start": date_start, "date_end": date_end, "description": description,
                  "setup_start": setup_start, "teardown_end": teardown_end, "event_id": event_id}
        query = "UPDATE event SET name= %(name)s, date_start= %(date_start)s, date_end= %(date_end)s, description= %(description)s, setup_start= %(setup_start)s, teardown_end= %(teardown_end)s WHERE id= %(event_id)s;"
        conn = mysql.connection
        cursor = conn.cursor()
        # if it's 1 it's changed 1 thing in the table (adding one record) error code needed to catch exceptions
        print(cursor.execute(query, params))
        conn.commit()
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

###
### Task
###

class Task:
    id = -1
    priority = -1
    name = ""
    dateDue = ""
    status = ""
    assignedTo = ""
    event_id = -1

    def __init__(self, id, priority, name, dateDue, status, assignedTo, event_id):
        self.id = id
        self.priority = priority
        self.name = name
        self.dateDue = dateDue
        self.status = status
        self.assignedTo = assignedTo
        self.event_id = event_id

    @classmethod
    def loadTask(cls, task_id):
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM task WHERE id = %(key)s;", {'key': task_id})
        data = cur.fetchone()
        id = data[0]
        priority = data[1]
        name = data[2]
        dateDue = data[3]
        status = data[4]
        assignedTo = data[5]
        event_id = data[6]
        return cls(id, priority, name, dateDue, status, assignedTo, event_id)


    # creates a task for a given event instance - To be implemented
    @classmethod
    def createTaskForEvent(cls, name, dueDate, priority, status, user, event_id):
        #hardcoded params - user_assign - admin@admin.com
        params = {"name": name, "dueDate": dueDate, "priority": priority, "status": status,
                  "user_assign": user, "event_id": event_id}
        query = "INSERT INTO task (priority, name, dateDue, status, assignedTo, event_id) VALUES (%(priority)s, %(name)s, %(dueDate)s, %(status)s, %(user_assign)s, %(event_id)s);"
        conn = mysql.connection
        cursor = conn.cursor()
        # if it's 1 it's changed 1 thing in the table (adding one record) error code needed to catch exceptions
        cursor.execute(query, params)
        conn.commit()
        id = cursor.lastrowid

        return cls(id, priority, name, dueDate, status, user, event_id)

    @classmethod
    def updateTask(cls, task_id, priority, name, dateDue, status, assignedTo, event_id):
        params = {"task_id": task_id, "priority": priority, "name": name, "dateDue": dateDue,
                  "status": status, "assignedTo": assignedTo, "event_id": event_id}
        query = "UPDATE task SET id= %(task_id)s, priority= %(priority)s, name= %(name)s, dateDue= %(dateDue)s, status= %(status)s, assignedTo= %(assignedTo)s WHERE id= %(task_id)s;"
        conn = mysql.connection
        cursor = conn.cursor()
        # if it's 1 it's changed 1 thing in the table (adding one record) error code needed to catch exceptions
        print(cursor.execute(query, params))
        conn.commit()
        return cls(id, priority, name, dateDue, status, assignedTo, event_id)

    # retrieves the tasks for a given event instance and puts them in a dictionary
    @staticmethod
    def getTasksForEvent(event_id):
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT event.id, task.id, task.priority, task.name, task.dateDue, task.status, task.assignedTo FROM event.task JOIN event.event ON event_id = event.id WHERE event_id = %(id)s;', {'id' : event_id})
        data = cursor.fetchall()
        allTasks = []
        for i in data:
            allTasks.append({'event_id':i[0], 'id': i[1], 'priority': i[2], 'name': i[3], 'dueDate': i[4], 'status': i[5], 'assignedTo': i[6]})
        if allTasks == []:
            return [{'event_id' : event_id}]
        return allTasks

###
### Ticket
###

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

    @staticmethod
    def getAllTickets(event_id):
        cursor = mysql.connection.cursor()
        cursor.execute(
            'SELECT * FROM ticket WHERE event_id = %(id)s;',
            {'id': event_id})
        data = cursor.fetchall()
        allTickets = []
        for i in data:
            allTickets.append(
                {'event_id': event_id, 'id': i[0], 'price': i[1], 'section': i[2], 'seat_num': i[3], 'isSold': i[4]})
        if allTickets == []:
            return [{'event_id': event_id}]
        return allTickets

    @staticmethod
    def getTotalPriceSold(event_id):
        cursor = mysql.connection.cursor()
        cursor.execute(
            'SELECT SUM(price) FROM ticket WHERE event_id = %(id)s AND isSold = 1;',
            {'id': event_id})
        data = cursor.fetchone()
        return data[0]

    @staticmethod
    def getTotalCountSold(event_id):
        cursor = mysql.connection.cursor()
        cursor.execute(
            'SELECT count(isSold) FROM ticket WHERE event_id = %(id)s AND isSold = 1;',
            {'id': event_id})
        data = cursor.fetchone()
        return data[0]

class User(flask_login.UserMixin):
    pass

    @login_manager.user_loader
    def user_loader(email):
        if(email not in User.getUsers()):
            return

        user = User()
        user.id = email
        return user

    @login_manager.request_loader
    def request_loader(request):
        email = request.form.get('email')
        if (email not in User.getUsers()):
            return

        user = User()
        user.id = email

        user.is_authenticated = request.form['password'] == users[email]['password']

        return user

    @staticmethod
    def getUsers():
        conn = mysql.connection
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM event.user;')
        data = {}
        for i in cursor.fetchall():
            newUser = {}
            newUser['isAdmin']=i[0]
            newUser['name'] = i[1]
            newUser['password'] = i[3]
            newUser['is_authenticated'] = i[4]
            newUser['is_active'] = i[5]
            data[i[2]] = newUser
        return data

    @staticmethod
    def createUser(name, email, password, password_conf):
        if password == password_conf:
            params = {"isAdmin": False, "name": name, "email": email, "password": password, "isAuthenticated": False,
                      "isActive": True}
            query = "INSERT INTO user (isAdmin, name, email, password, isAuthenticated, isActive) VALUES (%(isAdmin)s, %(name)s, %(email)s, %(password)s, %(isAuthenticated)s, %(isActive)s);"
            conn = mysql.connection
            cursor = conn.cursor()
            # if it's 1 it's changed 1 thing in the table (adding one record) error code needed to catch exceptions
            cursor.execute(query, params)
            conn.commit()
            id = cursor.lastrowid
            return id

        raise RuntimeError


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