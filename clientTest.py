import zmq
# import json

context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect('tcp://localhost:5555')
print('connected to server')

# test successful create requests
for request in range(10):
    print('Sending request %s ...' % request)
    msg = ['C', [request, '2024-03-15', '2024-03-30', 'vacation']]
    socket.send_json(msg)
    # reply
    message = socket.recv_json()
    print('Received reply %s [ %s ]' % (request, message))
# extra entry w/ employeeID 1
msg = ['C', [1, '2024-04-10', '2024-04-22', 'reason']]
socket.send_json(msg)
# reply
message = socket.recv_json()
print('Received reply [ %s ]' % message)

# manager approval of previous request
print('Updating last request w/ manager123 approval')
msg = ['U', [message, 123, True]]
socket.send_json(msg)
# reply
message = socket.recv_json()
print('Received reply [ %s ]' % message)

# test create request w/ missing data
print('Sending request w/ lacking data ...')
msg = ['C', [1, '2024-02-17', '2024-02-30']]  # missing reason for request
socket.send_json(msg)
# reply
message = socket.recv_json()
print('Received reply [ %s ]' % message)

# test create w/ extraneous data
print('Sending request w/ extraneous data ...')
msg = ['C', [1, '2024-02-17', '2024-02-30', 'vacation', 'something extra']]
socket.send_json(msg)
# reply
message = socket.recv_json()
print('Received reply [ %s ]' % message)

# test create w/ start date > 9 months out
print('Sending request >9 months out ...')
msg = ['C', [1, '2025-06-01', '2025-06-02', 'really advanced']]
socket.send_json(msg)
# reply
message = socket.recv_json()
print('Received reply [ %s ]' % message)

# get an employee's active time-off requests
print('Sending request to retrieve all data for employeeID 1 ...')
msg = ['E', 1]
socket.send_json(msg)
# reply
results = socket.recv_json()
print('Received following data:')
for result in results:
    print(result)

# get all data
print('Sending request for all active time-off requests ...')
msg = ['M']
socket.send_json(msg)
# reply
results = socket.recv_json()
print('Received following data:')
for result in results:
    print(result)

# get all data before 2024-02-28
print('Sending request for all active time-off requests before date ...')
msg = ['M', '2024-02-28']
socket.send_json(msg)
# reply
results = socket.recv_json()
print('Received following results:')
for result in results:
    print(result)

# clear data from table
print('Clearing test data from table ...')
msg = ['CLEAR ALL DATA']
socket.send_json(msg)
# reply/verification
message = socket.recv_json()
print('Received reply [ %s ]' % message)
