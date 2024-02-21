Manages a small database using Sqlite3 to track time-off requests. Provides options to add requests,
get all active requests for an employee, get all active requests for all employees (optionally filtered
by an end-date), update approval status for a request, and clear the table of all entries. 
Uses ZeroMQ with REP/REQ socket communication, sending and receiving with json packaging. See clientTest file
for an example of client communication with the timeOffManager. 

Accepted message formats:
* Note: strings are case-insensitive, including the message-type indicating character
* Active requests = requests that start on/after today's date (i.e., startDate >= today)
    - Create new time-off request: 
        ['C', [employeeID: int, start_date: 'YYYY-MM-DD' , end_date: 'YYYY-MM-DD', reason: string]]
        ex) ['C', [12345, '2024-02-18', '2024-02-26', 'vacation']]
    
    - Get all active time-off requests for an employee: 
        ['E', employeeID: int]
        ex) ['E', 12345]
    
    - Get all active time-off requests, optionally filtered by end-date: 
        ['M'] or ['M', end_date: 'YYYY-MM-DD']
        ex) ['M','2024-08-01']
    
    - Update approval for a time-off request: 
        ['U', [requestID: int, approvingManagerID: int, approvalStatus: Boolean]]
        * approvalStatus = False indicates denied request; True indicates approved request
        ex) ['U', [223, 45678, True]]
    
    - Clear time-off request data: 
        ['CLEAR ALL DATA']
        * This clears the database. Included for ease of testing. 