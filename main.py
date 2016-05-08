from flask import *
import flask.ext.login as flask_login
from flask import render_template
from flask.ext.mysqldb import MySQL
from forms import *

# App
app = Flask(__name__)

# configuration settings
app.config["MYSQL_HOST"] = "127.0.0.1"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config['MYSQL_DB'] = 'event'
app.config['SECRET_KEY'] = 'very secret-y key value; shhhhh!'

# initializations
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
@flask_login.login_required
def budget(event_id):
    current_event = Event.loadEvent(event_id)
    current_budget = Budget.loadBudget(event_id)
    invoices = current_budget.convert_invoice_to_output()
    return render_template('budget/budget.html', current_event=current_event, current_budget=current_budget, invoices=invoices)

@app.route('/event/<int:event_id>/budget/new', methods=['GET', 'POST'])
@flask_login.login_required
def newInvoice(event_id):
    form = NewInvoice(request.form)
    current_budget = Budget.loadBudget(event_id)
    form.vendor_id.choices = Vendor.getVendorChoices()
    if request.method == 'POST' and form.validate():
        current_budget.createInvoice(form.total.data, form.description.data, form.isPaid.data, form.vendor_id.data)
        flash("New Invoice Created")
        return redirect(url_for('budget', event_id=event_id))
    return render_template('budget/new.html', form=form)

@app.route('/event/<int:event_id>/budget/<int:invoice_id>/edit', methods=['GET', 'POST'])
@flask_login.login_required
def editInvoice(event_id, invoice_id):
    #rendor's form
    form = NewInvoice(request.form)
    form.vendor_id.choices = Vendor.getVendorChoices()

    #loads budget/invoice
    current_event = Event.loadEvent(event_id)
    current_budget = Budget.loadBudget(event_id)
    current_invoice = current_budget.getAllInvoices()[invoice_id]
    if request.method == 'GET':
        #puts values into the form
        form.description.data = current_invoice['description']
        form.isPaid.data = current_invoice['isPaid']
        form.total.data = current_invoice['total']
        form.vendor_id.data = current_invoice['vendor_id']

    if request.method == 'POST' and form.validate():
        #self, total, description, isPaid, vendor_id, invoice_id
        current_invoice = current_budget.updateInvoice(form.total.data, form.description.data, form.isPaid.data, form.vendor_id.data, invoice_id)
        flash(current_invoice['description'] + " Updated")
        return redirect(url_for('budget', event_id=event_id))

    return render_template('budget/edit.html', form=form)

##
## Event
##

# edits an event based on a given event_id
@app.route('/event/<int:event_id>/edit', methods=['GET', 'POST'])
@flask_login.login_required
def editEvent(event_id):
    form = NewEvent(request.form)
    current_event = Event.loadEvent(event_id)
    if request.method == 'GET':
        form.name.data = current_event.name
        form.description.data = current_event.description
        form.date_start.data = current_event.date_start
        form.date_end.data = current_event.date_end
        form.setupStart.data = current_event.setupStart
        form.teardownEnd.data = current_event.teardownEnd
    if request.method == 'POST' and form.validate():
        thisNewEvent = Event.updateEvent(event_id, form.name.data, form.description.data, form.date_start.data,
                                         form.date_end.data,
                                         form.setupStart.data, form.teardownEnd.data)
        flash(current_event.name + ' Updated')
        return redirect(url_for('event', event_id=current_event.id))
    return render_template('event/edit.html', current_event=current_event, form=form)


# returns all events from the database - not user specific (yet)
@app.route('/event')
@flask_login.login_required
def all_events():
    response = Event.getAllEvents()
    return render_template('event/event.html', response=response)


# returns a single event page for a given event_id
@app.route('/event/<int:event_id>')
@flask_login.login_required
def event(event_id):
    current_event = Event.loadEvent(event_id)
    current_budget = Budget.loadBudget(event_id)
    current_tasks = Task.getTasksNotComplete(event_id)
    totalTixSold = Ticket.getTotalCountSold(event_id)
    totalIncome = Ticket.getTotalPriceSold(event_id)
    totalTix = Ticket.getTotalCount(event_id)
    totalTixNotSold = Ticket.getTotalCountNotSold(event_id)

    return render_template('event/show.html', current_event=current_event, current_tasks=current_tasks, current_budget=current_budget,
                           totalIncome=totalIncome, totalTixSold=totalTixSold,
                           totalTix= totalTix, totalTixNotSold=totalTixNotSold)

@app.route('/event/<int:event_id>/delete')
@flask_login.login_required
def delete_event(event_id):
    current_event = Event.loadEvent(event_id)
    current_event.deleteEvent()
    return redirect(url_for('all_events'))

# creates a new event
@app.route('/event/new', methods=['GET', 'POST'])
@flask_login.login_required
def newEvent():
    form = NewEvent(request.form)
    if request.method == 'POST' and form.validate():
        current_event = Event.createEvent(form.name.data, form.description.data, form.date_start.data,
                                         form.date_end.data,
                                         form.setupStart.data, form.teardownEnd.data)
        current_budget = Budget.createBudget(current_event.id)
        flash('New Event Created')
        newEvent_id = int(current_event.id)
        return redirect(url_for('event', event_id=newEvent_id))
    return render_template('event/new.html', form=form)


###
### Login/Log Out
###
@app.route('/')
def redirect_to_login():
    return redirect("/login")


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

    #blank user input
    if (not form.password.data) or (not form.email.data):
        flash("Empty password or email field")
        return redirect(url_for("login"))

    #checks to see if user exists
    if form.email.data in users.keys():
        #checks to see if passwords match
        if form.password.data == users[email]['password']:
            user = User()
            user.id = email
            flask_login.login_user(user)
            return redirect(url_for('protected'))
        else:
            flash("Incorrect email or password")
    else:
        flash("User does not exist")
    return redirect(url_for("login"))


@app.route('/protected')
@flask_login.login_required
def protected():
    flash("Welcome " + flask_login.current_user.get_name() + "!")
    return redirect(url_for("all_events"))


@app.route('/logout')
def logout():
    flask_login.logout_user()
    flash("You have been logged out!")
    return redirect(url_for("login"))


@login_manager.unauthorized_handler
def unauthorized_handler():
    flash("You are not authorized to access this page.")
    return redirect(url_for("login"))


##
## Task
##

# edits a task for a given event_id and given task_id
@app.route('/event/<int:event_id>/task/<int:task_id>/edit', methods=['GET', 'POST'])
@flask_login.login_required
def editTask(event_id, task_id):
    form = NewTask(request.form)
    current_event = Event.loadEvent(event_id)
    form.assignTo.choices = User.userChoices()
    form.status.choices = [(0, 'Not Complete'), (1, 'Pending'), (2, 'Complete')]
    if request.method == 'GET':
        current_task = Task.loadTask(task_id)
        form.priority.data = current_task.priority
        form.name.data = current_task.name
        form.dueDate.data = current_task.dateDue
        form.status.data = int(current_task.status)
        form.assignTo.data = current_task.assignedTo
    if request.method == 'POST' and form.validate():
        current_task = Task.updateTask(task_id, form.priority.data, form.name.data, form.dueDate.data,
                                       form.status.data,
                                       form.assignTo.data, event_id)
        flash(current_task.name + ' Updated')
        return redirect(url_for('task', event_id=current_event.id))
    return render_template('task/edit.html', form=form)


# returns the tasks for a given event_id
@app.route('/event/<int:event_id>/task/new', methods=['GET', 'POST'])
@flask_login.login_required
def newTask(event_id):
    current_event = Event.loadEvent(event_id)
    form = NewTask(request.form)
    form.status.choices = [(0, 'Not Complete'), (1, 'Pending'), (2, 'Complete')]
    form.assignTo.choices = User.userChoices()
    if request.method == 'POST' and form.validate():
        thisNewTask = Task.createTaskForEvent(form.name.data, form.dueDate.data, form.priority.data, form.status.data,
                                              form.assignTo.data, event_id)
        flash('New Task Created')
        return redirect(url_for('task', event_id=current_event.id))
    return render_template('task/new.html', form=form)


# retrevies all the tasks for a given event_id
@app.route('/event/<int:event_id>/task')
@flask_login.login_required
def task(event_id):
    current_event = Event.loadEvent(event_id)
    response = Task.getTasksForEvent(event_id)
    return render_template('task/task.html', response=response, current_event=current_event)


##
## Ticket
##

# returns tickets for a given event_id
@app.route('/event/<int:event_id>/ticket')
@flask_login.login_required
def ticket(event_id):
    current_event = Event.loadEvent(event_id)
    response = Ticket.getAllTickets(event_id)
    response.append({"totalSold": Ticket.getTotalCountSold(event_id)})
    response.append({"totalSold": Ticket.getTotalPriceSold(event_id)})
    return render_template('ticket/ticket.html', current_event=current_event, response=response)

@app.route('/event/<int:event_id>/ticket/new', methods=['GET', 'POST'])
@flask_login.login_required
def newTicket(event_id):
    current_event = Event.loadEvent(event_id)
    form = NewTicket(request.form)
    if request.method == 'POST' and form.validate():
        Ticket.createTickets(form.numTicketsTotal.data, form.numSections.data, form.numSeatsPerSection.data, True, form.price.data, event_id)
        flash('New Tickets Created')
        return redirect(url_for('ticket', event_id=current_event.id))
    return render_template('ticket/new.html', form=form)

###
### User
###

@app.route('/user')
@flask_login.login_required
def users():
    response = User.getUsers()
    return render_template('user/user.html', response=response)


##
## Vendor
##

# returns all vendors from the database
@app.route('/vendor')
@flask_login.login_required
def vendor():
    response = Vendor.getAllVendors()
    return render_template('vendor/vendor.html', response=response)

##
## Models
##cursor = cnx.cursor(dictionary=True)

###
### Budget/Invoice
###

class Budget:
    id = -1
    event_id = -1
    invoices = []
    totalCountPaid = -1
    totalCountNotPaid = -1
    totalExpenses = -1
    totalInvoiceCount = -1


    def __init__(self, id, event_id):
        self.id = id
        self.event_id = event_id

    # Event.loadEvent() loads a single event based on the key given, and returns an event object of the specified key
    @classmethod
    def loadBudget(cls, key):
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM budget WHERE event_id = %(key)s;", {'key': key})
        data = cur.fetchone()
        if data != None:
            id = data[0]
            event_id = data[1]
            self = cls(id, event_id)
            self.totalCountPaid = self.getTotalCountPaid()
            self.totalCountNotPaid = self.getTotalCountNotPaid()
            self.totalExpenses = self.getTotalExpenses()
            self.totalInvoiceCount = self.getTotalCountInvoice()
            self.invoices = self.getAllInvoices()
            return self
        return cls(-1, key)

    def updateInvoice(self, total, description, isPaid, vendor_id, invoice_id):
        params = {"total": total, "description": description, "isPaid": isPaid, "vendor_id": vendor_id,
                  "budget_id": self.id, "invoice_id": invoice_id}
        query = "UPDATE invoice SET total= %(total)s, description= %(description)s, isPaid= %(isPaid)s, vendor_id= %(vendor_id)s, budget_id= %(budget_id)s WHERE id= %(invoice_id)s;"
        conn = mysql.connection
        cursor = conn.cursor()
        # if it's 1 it's changed 1 thing in the table (adding one record) error code needed to catch exceptions
        cursor.execute(query, params)
        conn.commit()

        newInvoice = {}
        newInvoice['vendor_id'] = vendor_id
        newInvoice['total'] = total
        newInvoice['description'] = description
        newInvoice['isPaid'] = isPaid
        newInvoice['budget_id'] = self.id
        newInvoice['event_id'] = self.event_id
        self.invoices[invoice_id] = newInvoice
        return newInvoice


    @classmethod
    def createBudget(cls, event_id):
        params = {"event_id": event_id}
        query = "INSERT INTO budget (event_id) VALUES (%(event_id)s);"
        conn = mysql.connection
        cursor = conn.cursor()
        # if it's 1 it's changed 1 thing in the table (adding one record) error code needed to catch exceptions
        cursor.execute(query, params)
        conn.commit()
        id = cursor.lastrowid
        return cls(id, event_id)

    def getAllInvoices(self):
        if self.id == -1:
            return [{'event_id': self.event_id}]
        cursor = mysql.connection.cursor()
        cursor.execute(
            'SELECT * FROM invoice WHERE budget_id = %(id)s;',
            {'id': self.id})
        data = {}
        for i in cursor.fetchall():
            newInvoice = {}
            newInvoice['vendor_id'] = i[5]
            newInvoice['total'] = i[1]
            newInvoice['description'] = i[2]
            newInvoice['isPaid'] = i[3]
            newInvoice['budget_id'] = i[4]
            newInvoice['event_id'] = self.event_id
            data[i[0]] = newInvoice
        self.invoices = data
        return data

    def convert_invoice_to_output(self):
        data = self.invoices
        for i in self.invoices:
            for j in self.invoices[i]:
                if j == "vendor_id":
                    current_vendor = Vendor.loadVendor(self.invoices[i][j])
                    data[i][j] = current_vendor.name
                elif j == "isPaid":
                    data[i][j] = Misc.convert_to_bool(self.invoices[i][j])
        return data

    def getTotalExpenses(self):
        cursor = mysql.connection.cursor()
        cursor.execute(
            'SELECT SUM(total) FROM invoice WHERE budget_id = %(id)s;',
            {'id': self.id})
        data = cursor.fetchone()
        return data[0]

    def getTotalCountPaid(self):
        cursor = mysql.connection.cursor()
        cursor.execute(
            'SELECT count(isPaid) FROM invoice WHERE budget_id = %(id)s AND isPaid = 1;',
            {'id': self.id})
        data = cursor.fetchone()
        return data[0]

    def getTotalCountInvoice(self):
        cursor = mysql.connection.cursor()
        cursor.execute(
            'SELECT count(isPaid) FROM invoice WHERE budget_id = %(id)s;',
            {'id': self.id})
        data = cursor.fetchone()
        return data[0]

    def getTotalCountNotPaid(self):
        cursor = mysql.connection.cursor()
        cursor.execute(
            'SELECT count(isPaid) FROM invoice WHERE budget_id = %(id)s AND isPaid = 0;',
            {'id': self.id})
        data = cursor.fetchone()
        return data[0]

    def createInvoice(self, total, description, isPaid, vendor_id):
        params = {"total": total, "description": description,
                  "isPaid": isPaid, "budget_id": self.id, "vendor_id": vendor_id}
        query = "INSERT INTO invoice (total, description, isPaid, budget_id, vendor_id) VALUES (%(total)s, %(description)s, %(isPaid)s, %(budget_id)s, %(vendor_id)s);"
        conn = mysql.connection
        cursor = conn.cursor()
        # if it's 1 it's changed 1 thing in the table (adding one record) error code needed to catch exceptions
        cursor.execute(query, params)
        conn.commit()
        id = cursor.lastrowid
        params["budget_id"] = self.id
        params["event_id"] = self.event_id
        self.invoices[id] = params
        return params


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

    def getname(self):
        return self.name

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
        # if it's 1 it's changed 1 thing in the table (adding one record) error code needed to catch exceptions
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
        cursor.execute(query, params)
        conn.commit()
        return cls(id, name, date_start, date_end, description, setup_start, teardown_end)

    # Event.loadEvent() loads a single event based on the key given, and returns an event object of the specified key
    @classmethod
    def loadEvent(cls, key):
        # select statment
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM event.event WHERE id = %(key)s;", {'key': key})
        data = cur.fetchone()
        id = data[0]
        name = data[1]
        date_start = data[2]
        date_end = data[3]
        description = data[4]
        setupStart = data[5]
        teardownEnd = data[6]
        # print(id, name, date_start, date_end, description, setupStart, teardownEnd);
        return cls(id, name, date_start, date_end, description, setupStart, teardownEnd)

    #deletes an event and all associated entities
    def deleteEvent(self):
        params ={"event_id": self.id}
        query = '''
        START TRANSACTION;
        DELETE FROM ticket WHERE %(event_id)s = event_id;
        DELETE FROM task WHERE %(event_id)s = event_id;
        DELETE FROM invoice WHERE budget_id = (SELECT id FROM budget WHERE %(event_id)s = event_id);
        DELETE FROM budget WHERE %(event_id)s = event_id;
        DELETE FROM event_for_user WHERE %(event_id)s = event_id;
        DELETE FROM event WHERE %(event_id)s = id;
        COMMIT;
        '''
        conn = mysql.connection
        cursor = conn.cursor()
        cursor.execute(query, params)
    #conn.commit()

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
        # hardcoded params - user_assign - admin@admin.com
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
        cursor.execute(query, params)
        conn.commit()
        return cls(id, priority, name, dateDue, status, assignedTo, event_id)

    # retrieves the tasks for a given event instance and puts them in a dictionary
    @staticmethod
    def getTasksForEvent(event_id):
        cursor = mysql.connection.cursor()
        cursor.execute(
            'SELECT event.id, task.id, task.priority, task.name, task.dateDue, task.status, task.assignedTo FROM event.task JOIN event.event ON event_id = event.id WHERE event_id = %(id)s;',
            {'id': event_id})
        data = cursor.fetchall()
        allTasks = []
        for i in data:
            allTasks.append(
                {'event_id': i[0], 'id': i[1], 'priority': i[2], 'name': i[3], 'dueDate': i[4], 'status':  Misc.convert_status(i[5]),
                 'assignedTo': User.get_name_id(i[6])})
        if allTasks == []:
            return [{'event_id': event_id}]
        return allTasks

    # retrieves the tasks for a given event instance and puts them in a dictionary
    @staticmethod
    def getTasksNotComplete(event_id):
        cursor = mysql.connection.cursor()
        cursor.execute(
            'SELECT event.id, task.id, task.priority, task.name, task.dateDue, task.status, task.assignedTo FROM event.task JOIN event.event ON event_id = event.id WHERE event_id = %(id)s AND (status = 0 OR status = 1);',
            {'id': event_id})
        data = cursor.fetchall()
        allTasks = []
        for i in data:
            allTasks.append(
                {'event_id': i[0], 'id': i[1], 'priority': i[2], 'name': i[3], 'dueDate': i[4], 'status':  Misc.convert_status(i[5]),
                 'assignedTo': User.get_name_id(i[6])})
        if allTasks == []:
            return [{'priority': 'All Tasks Completed'}]
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
                {'event_id': event_id, 'id': i[0], 'price': i[1],
                 'section': Misc.convert_null(i[2]), 'seat_num': Misc.convert_null(i[3]),
                 'isSold': Misc.convert_to_bool(i[4])})
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

    @staticmethod
    def getTotalCount(event_id):
        cursor = mysql.connection.cursor()
        cursor.execute(
            'SELECT count(isSold) FROM ticket WHERE event_id = %(id)s;',
            {'id': event_id})
        data = cursor.fetchone()
        return data[0]

    @staticmethod
    def getTotalCountNotSold(event_id):
        cursor = mysql.connection.cursor()
        cursor.execute(
            'SELECT count(isSold) FROM ticket WHERE event_id = %(id)s AND isSold = 0;',
            {'id': event_id})
        data = cursor.fetchone()
        return data[0]

    @staticmethod
    def createTickets(numTicketsTotal, numSections, numSeatsPerSection, isSold, price, event_id):
        conn = mysql.connection
        cursor = conn.cursor()
        query = "START TRANSACTION; "
        if(numTicketsTotal == ""):
            for i in range(int(numSections)):
                for j in range(int(numSeatsPerSection)):
                    query += "INSERT INTO ticket (price, section, seat_num, isSold, event_id) VALUES (" + price + ", " + str(i) + ", " + str(j) + ", " + str(isSold) + ", " + str(event_id) + "); "
        else:
            for i in range(int(numTicketsTotal)):
                query += "INSERT INTO ticket (price, isSold, event_id) VALUES (" + price + ", "\
                         + str(isSold) + ", " + str(event_id) + "); "
        query += " COMMIT;"
        cursor.execute(query)



###
### User
###

class User(flask_login.UserMixin):
    pass

    @login_manager.user_loader
    def user_loader(email):
        if (email not in User.getUsers()):
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

    def is_admin(self):
        conn = mysql.connection
        cursor = conn.cursor()
        cursor.execute('SELECT isAdmin FROM user WHERE email = %(key)s', {'key': self.id})
        return cursor.fetchone()[0]

    def get_name(self):
        conn = mysql.connection
        cursor = conn.cursor()
        cursor.execute('SELECT name FROM user WHERE email = %(key)s', {'key': self.id})
        return cursor.fetchone()[0]

    @staticmethod
    def get_name_id(id):
        conn = mysql.connection
        cursor = conn.cursor()
        cursor.execute('SELECT name FROM user WHERE email = %(key)s', {'key': id})
        return cursor.fetchone()[0]

    # def is_authenticated(self):
    #     conn = mysql.connection
    #     cursor = conn.cursor()
    #     cursor.execute('SELECT isAuthenticated FROM user WHERE email = %(key)s', {'key': self.id})
    #     return cursor.fetchone()[0] == 1

    @staticmethod
    def getUsers():
        conn = mysql.connection
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM event.user;')
        data = {}
        for i in cursor.fetchall():
            newUser = {}
            newUser['isAdmin'] = i[0]
            newUser['name'] = i[1]
            newUser['password'] = i[3]
            newUser['is_authenticated'] = i[4]
            newUser['is_active'] = i[5]
            data[i[2]] = newUser
        return data

    @staticmethod
    def userChoices():
        users = User.getUsers()
        response = []
        for user in users:
            response.append((user, User.get_name_id(user)))
        response.remove(('admin@admin.com', 'admin'))
        return response

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
    zip = ""
    state = ""
    city = ""
    # array of invoices - to be implemented
    invoices = []

    def __init__(self, id, name, phone, address, email, city, state, zip):
        self.id = id
        self.name = name
        self.phone = phone
        self.address = address
        self.email = email
        self.city = city
        self.state = state
        self.zip = zip

    @classmethod
    def loadVendor(cls, vendor_id):
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM vendor WHERE id = %(key)s;", {'key': vendor_id})
        data = cur.fetchone()
        id = data[0]
        name = data[1]
        phone = data[2]
        address = data[3]
        email = data[4]
        city = data[5]
        state = data[6]
        zip = data[7]
        return cls(id, name, phone, address, email, city, state, zip)


    # return all vendors
    @staticmethod
    def getAllVendors():
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM event.vendor;')
        data = cursor.fetchall()
        return data

    @staticmethod
    def getVendorChoices():
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT id FROM event.vendor;')
        data = cursor.fetchall()
        response = []
        for i in data:
            current_vendor = Vendor.loadVendor(i)
            response.append((current_vendor.id, current_vendor.name))
        return response

class Misc:
    @staticmethod
    def convert_to_bool(value):
        if value == 1:
            return 'Yes'
        else:
            return 'No'

    @staticmethod
    def convert_null(value):
        if value == 'null':
            return ""
        else:
            return value

    @staticmethod
    def convert_status(value):
        if value == "2":
            return "Complete"
        elif value == "1":
            return "Pending"
        else:
            return "Not complete"

if __name__ == '__main__':
    app.debug = True
    app.run()