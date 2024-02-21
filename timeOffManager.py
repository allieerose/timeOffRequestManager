import sqlite3
import zmq
import datetime

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind('tcp://*:5555')

connection = sqlite3.connect('timeOffRequests.db')
cursor = connection.cursor()
cursor.execute(
    '''CREATE TABLE IF NOT EXISTS timeOffRequests(
        employeeID          int             not null,
        startDate           date            not null,
        endDate             date            not null,
        reason              varchar(255)    not null,
        approvingManager    int             default null,
        approved            boolean         default False
    );''')
connection.commit()


def create_request(data):
    """
    Adds a time-off request with the given data to the table. If the entry
    is successful, returns the requestID for the created entry. Otherwise,
    returns a descriptive message noting reason for failed request.
    """
    # check if correct amount of data is included
    if len(data) < 4:
        socket.send_json('Request is missing required data. Note that employee'
                         ' ID, start date, end date, and reason for request '
                         'must be included (in that order) for successful '
                         'request.')
        return
    if len(data) > 4:
        socket.send_json('Request includes extraneous data. Note that employee'
                         ' ID, start date, end date, and reason for request '
                         'must be included (in that order) for successful '
                         'request.')
        return
    # check that request starts within the next 9 months
    today = datetime.datetime.today() + datetime.timedelta()
    start_date = datetime.datetime.strptime(data[1], '%Y-%m-%d')
    days_until = (start_date - today).days
    if days_until > 270:  # 270 days = 9 months
        socket.send_json('Request is too far in advance. Requests must be '
                         'within the next 9 months.')
        return
    # request is valid - add it to the table
    cursor.execute(
        '''INSERT INTO timeOffRequests (employeeID, startDate, endDate, reason)
            VALUES (%s, '%s', '%s', '%s'); '''
        % (data[0], data[1], data[2], data[3])
    )
    requestID = cursor.lastrowid
    connection.commit()
    socket.send_json(requestID)


def get_employee_requests(employeeID):
    """
    Takes an employee ID and returns all active time off requests. Active time
    off requests are requests that start after today's date.
    """
    cursor.execute('''SELECT rowid, startDate, endDate, reason,
                   approvingManager, approved
                   FROM timeOffRequests
                   WHERE employeeID = %s AND startDate >= date('%s')
                   ORDER BY startDate ASC;'''
                   % (employeeID, datetime.date.today()))
    result = cursor.fetchall()
    connection.commit()
    socket.send_json(result)


def get_all_requests(date=None):
    """
    Returns all active time off requests, optionally filtered by given date.
    If a date is given, only requests ending before the given date are
    returned.
    """
    if date is None:
        cursor.execute('''SELECT rowid, *
                       FROM timeOffRequests
                       WHERE startDate >= date('%s')
                       ORDER BY startDate ASC;'''
                       % datetime.date.today())
    else:
        cursor.execute('''SELECT rowid, *
                       FROM timeOffRequests
                       WHERE startDate >= date('%s')
                       AND endDate < date(%s)
                       ORDER BY startDate ASC;'''
                       % (datetime.date.today(), date))
    result = cursor.fetchall()
    connection.commit()
    socket.send_json(result)


def update_request(data):
    """
    Takes a list of form [requestID: int, managerID: int, approval: Boolean]
    and updates the indicated time-off request.
    """
    requestID = data[0]
    managerID = data[1]
    approval = data[2]
    cursor.execute('''UPDATE timeOffRequests
                   SET approvingManager = %s, approved = %s
                   WHERE rowid = %s'''
                   % (managerID, approval, requestID))
    connection.commit()
    if approval:
        socket.send_json('Time-off request %s approved by manager %s'
                         % (requestID, managerID))
    else:
        socket.send_json('Time-off request %s denied by manager %s'
                         % (requestID, managerID))


def clear_table():
    """
    Clears all time-off requests from the table.
    """
    cursor.execute('''DELETE FROM timeOffRequests;''')
    connection.commit()
    cursor.execute('''VACUUM;''')  # clear unused space for data management
    connection.commit()
    socket.send_json('Table successfully cleared of all data.')


while True:
    # wait for request
    message = socket.recv_json()
    print('Received request: %s' % message)
    msg_type = message[0].upper()  # case-insensitive
    if msg_type == 'C':  # add time-off request
        create_request(message[1])
    elif msg_type == 'E':  # employee view time-off requests
        get_employee_requests(message[1])
    elif msg_type == 'M':  # manager view time-off requests
        if len(message) == 1:
            get_all_requests()
        else:  # included date filter
            get_all_requests(message[1])
    elif msg_type == 'U':  # update time-off request
        update_request(message[1])
    elif msg_type == 'CLEAR ALL DATA':  # clear table
        clear_table()
