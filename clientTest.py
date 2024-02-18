import zmq
# import json

context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect('tcp://localhost:5555')
print('connected to server')

for request in range(10):
    print('Sending request %s ...' % request)
    msg = ['C', [request, '2024-02-17', '2024-02-30', 'vacation']]
    socket.send_json(msg)
    # reply
    message = socket.recv_json()
    print('Received reply %s [ %s ]' % (request, message))
