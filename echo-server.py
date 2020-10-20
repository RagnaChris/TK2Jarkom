#!/usr/bin/env python3

import socket, os

HOST = ''
PORT = 65432
arg = ''

print("Waiting for connection")

def write_program(conn):
    global arg
    buff = b''
    while True:
        # print("masih menunggu")
        data = conn.recv(1024)
        buff += data
        if not data:
            break

    arg = buff[0:buff.rfind(b'&&&')].decode()
    data = buff[buff.rfind(b'&&&')+3:]
    print(arg)
    with open("program-test", "ab") as f:
        f.write(data)


def run_program():
    os.system("chmod +x program-test")
    os.system("./program-test " +  arg + " > program-test.out")

def send_output(conn):
    with open("program-test.out", "rb") as f:
         data = f.read()
         print(repr(data))
         conn.sendall(data)

# Socketnya pakai IPv4 dan TCP
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    while True:
        s.listen()
        conn, addr = s.accept()
        with conn:
            print(conn)
            print('Connected by', addr)

            write_program(conn)
            run_program()
            send_output(conn)

            os.system("rm program-test program-test.out") # clean program
