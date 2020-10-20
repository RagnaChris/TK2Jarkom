#!/usr/bin/env python3

import socket, threading

HOST = '127.0.0.1'
# HOST = '54.157.4.185'
PORT = 65432
queue_jobs = []
MENU_MSG = ["Select command you want to choose ", "1. Type send <program path> <set of arguments>",
        "2. Type else to quit program"]

def start_connection(path_program, arg):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        with open(path_program, "rb") as f:
            data = f.read()
            s.sendall(bytes(str(arg),'utf-8') + b'&&&' + data)
            print("data terkirim")
            s.shutdown(1)
        output = s.recv(1024)
        print("Received jobs result from {} :\n{}".format(path_program, output.decode()))

def send_job():
    global queue_jobs
    while True:
        if len(queue_jobs) != 0:
            job = queue_jobs[0]
            print("Mengirimkan pekerjaan", job)
            queue_jobs = queue_jobs[1:]
            print("Daftar jobs yang belum dilakukan", queue_jobs)
            start_connection(job[0], job[1])

def wait_input():
    while True:
        for msg in MENU_MSG:
            print(msg)
        
        cmd = input().split()
        if cmd[0] == "send":
            path_program, arg = cmd[1], ' '.join(cmd[2:])
            queue_jobs.append([path_program, arg])
        else:
            # handle quit program (not solved)
            sys.exit()

if __name__ == "__main__" :
    # Todo handle argument
    wait = threading.Thread(target=wait_input, args=())
    wait.start()
    send = threading.Thread(target=send_job, args=())
    send.start()

