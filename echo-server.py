#!/usr/bin/env python3

import socket

HOST = ''
PORT = 65432

print("Waiting for connection")

# Socketnya pakai IPv4 dan TCP
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print(conn)
        print('Connected by', addr)
        while True:
            data = conn.recv(1024)
            if not data:
                break
            conn.sendall(data)
