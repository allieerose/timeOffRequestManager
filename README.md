Accepted message formats:
* Note: strings are case-insensitive, including the message-type indicating character
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