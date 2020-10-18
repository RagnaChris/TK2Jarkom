#!/usr/bin/env python3

import socket

# HOST = '127.0.0.1'
HOST = '54.157.4.185'
PORT = 65432

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(b'Hello, world')
    data = s.recv(1024)

print('Received', repr(data))
