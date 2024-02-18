import sqlite3
import zmq
# import json

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind('tcp://*:5555')

connection = sqlite3.connect('timeOffRequests.db')
cursor = connection.cursor()
cursor.execute(
    '''CREATE TABLE IF NOT EXISTS timeOffRequests(
        requestID           int             primary key,
        employeeID          int(11)         not null,
        startDate           date            not null,
        endDate             date            not null,
        reason              varchar(255)    not null,
        approvingManager    int(11)         default null,
        approved            boolean         default False
    );''')


def create_request(data):
    if len(data) < 4:
        socket.send_json('''Request is missing required data. Note that
        employee ID, start date, end date, and reason for request must be
        included (in that order) for successful request.''')
        return
    elif len(data) > 4:
        socket.send_json('''Request includes extraneous data. Note that
        employee ID, start date, end date, and reason for request must be
        included (in that order) for successful request.''')
        return
    # elif data[1] (start date) > 9 months from today's date, reject request
    # else:
    cursor.execute(
        '''INSERT INTO timeOffRequests (employeeID, startDate, endDate, reason)
            VALUES (%s, %s, %s, '%s'); '''
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
    pass


def get_all_requests(date=None):
    """
    Returns all active time off requests, optionally filtered by given date.
    If a date is given, only requests ending before the given date are
    returned.
    """
    pass


def update_request(data):
    """
    Takes a list of form [requestID: int, managerID: int, approval: Boolean]
    and updates the indicated time-off request.
    """
    pass


def clear_table():
    """
    Clears all time-off requests from the table.
    """
    pass


while True:
    # wait for request
    message = socket.recv_json()
    print('Received request: %s' % message)
    msg_type = message[0].upper()  # case-insensitive
    if msg_type == 'C':
        create_request(message[1])
    elif msg_type == 'E':
        # employee view time off requests
        get_employee_requests(message[1])
    elif msg_type == 'M':
        # manager view time off requests
        # * could include date filter
        if len(message) == 1:
            get_all_requests()
        else:  # included date filter
            get_all_requests(message[1])
    elif msg_type == 'U':
        # update time off request
        update_request(message[1])
    elif msg_type == 'CLEAR ALL DATA':
        # clear table
        clear_table()
