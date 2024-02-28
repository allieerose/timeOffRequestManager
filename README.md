Manages a small database using Sqlite3 to track time-off requests. Provides options to add requests,
get all active requests for an employee, get all active requests for all employees (optionally filtered
by a start-date), update approval status for a request, and clear the table of all entries. 
Uses ZeroMQ with REP/REQ socket communication, sending and receiving with json packaging. 
Requests are sent with send_json() and replies are retrieved with recv_json(). See below for an example.


## Accepted message formats:
* Note: strings are case-insensitive, including the message-type indicating character
* Active requests = requests that start on/after today's date (i.e., endDate >= today)
    - Create new time-off request: 
        ['C', [employeeID: int, start_date: 'YYYY-MM-DD' , end_date: 'YYYY-MM-DD', reason: string]]
        ex) ['C', [12345, '2024-02-18', '2024-02-26', 'vacation']]
    
    - Get all active time-off requests for an employee: 
        ['E', employeeID: int]
        ex) ['E', 12345]
    
    - Get all active time-off requests, optionally filtered by start-date: 
        ['M'] or ['M', end_date: 'YYYY-MM-DD']
        ex) ['M','2024-08-01']
    
    - Update approval for a time-off request: 
        ['U', [requestID: int, approvingManagerID: int, approvalStatus: Boolean]]
        * approvalStatus = False indicates denied request; True indicates approved request
        ex) ['U', [223, 45678, True]]
    
    - Clear time-off request data: 
        ['CLEAR ALL DATA']
        * This clears the database. Included for ease of testing.

## Example request/response retrieval:
```
import zmq
# establish socket connection
context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect('tcp://localhost:5555')
# send message
message = ['C', [12345, '2024-02-18', '2024-02-26', 'vacation']]
socket.send_json(message)
# receive reply
reply = socket.recv_json()
```

## UML Diagram
![UML Diagram drawio (1)](https://github.com/allieerose/timeOffRequestManager/assets/114102628/438f4c25-cba5-4653-b15e-d239d553d8af)
