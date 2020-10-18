#!/usr/bin/env python3

import socket, os

HOST = ''
PORT = 65432

print("Waiting for connection")

def write_program(conn):
    while True:
        # print("masih menunggu")
        data = conn.recv(1024)
        if not data:
            break
        else:
            with open("program-test", "ab") as f:
                f.write(data)

def run_program():
    os.system("chmod +x program-test")
    os.system("./program-test > program-test.out")

def send_output(conn):
    with open("program-test.out", "rb") as f:
         data = f.read()
         print(repr(data))
         conn.sendall(data)

# Socketnya pakai IPv4 dan TCP
while True:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        conn, addr = s.accept()
        with conn:
            print(conn)
            print('Connected by', addr)

            write_program(conn)
            run_program()
            send_output(conn)

            os.system("rm program-test program-test.out") # clean program
