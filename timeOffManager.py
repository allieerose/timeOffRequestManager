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
        return '''Request is missing required data. Note that employee ID,
        start date, end date, and reason for request must be included
        (in that order) for successful request.'''
    if len(data) > 4:
        return '''Request includes extraneous data. Note that employee ID,
        start date, end date, and reason for request must be included
        (in that order) for successful request.'''
    # if data[1] (start date) > 9 months from today's date, reject request
    cursor.execute(
        '''INSERT INTO timeOffRequests (employeeID, startDate, endDate, reason)
            VALUES (%s, %s, %s, '%s'); '''
        % (data[0], data[1], data[2], data[3])
    )
    requestID = cursor.lastrowid
    connection.commit()
    socket.send_json(requestID)


while True:
    # wait for request
    message = socket.recv_json()
    print('Received request: %s' % message)
    print(message[0])
    print(message[1])
    if message[0].upper() == 'C':
        create_request(message[1])
