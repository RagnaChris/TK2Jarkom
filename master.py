#!/usr/bin/env python3

import socket, threading

class Worker:
    def __init__(self, HOST, job_status='Available', status='Available', job='Empty'):
        self.HOST = HOST
        self.job_status = job_status
        self.status = status
        self.job = job

PORT = 65432
queue_jobs = []
lst_worker = []
flag = True
MENU_MSG = ["Select command you want to choose ", "1. Type send <program path> <set of arguments>",
        "2. Type 'status' to see every worker and job status"]

def start_connection(path_program, arg, worker):
    global queue_jobs, flag
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(5)

        try:
            s.connect((worker.HOST, PORT))
        except:
            worker.status = 'Dead'
            worker.job_status = 'Dead'
            queue_jobs.insert(0,worker.job)
            return
        finally:
            flag = True

        with open(path_program, "rb") as f:
            data = f.read()
            s.sendall(bytes(str(arg),'utf-8') + b'&&&' + data)
            worker.job_status = 'Running'
            s.shutdown(1)
        
        s.settimeout(None)
        status_code, output = check_jobs_status(s.recv(1024))

        print("Received jobs result from {} {} :\n{}".format(path_program,arg, output.decode()))
        worker.status = 'Available'
        worker.job_status = 'Finished' if status_code == 0 else 'Failed'

def show_worker_information():
    print('-' * 80)
    print("{} {: <15} {: <10} {: <10} {: <30}".format("No", "HOST_IP", "JOB STATUS", "STATUS",
        "JOB NAME"))
    for i, worker in enumerate(lst_worker):
        print("{}. {: <15} {: <10} {: <10} {: <30}".format(i+1,worker.HOST,
               worker.job_status, worker.status, ' '.join(worker.job)))
    print('-' * 80)

'''
In this method we use '&&&' for divide status_code and output data.
For example:
b'0&&&This is output data'
This method parse output into status_code and output data.
'''
def check_jobs_status(output):
    status_code = output[0:output.rfind(b'&&&')].decode()
    data = output[output.rfind(b'&&&')+3:]
    return (int(status_code), data)
    
'''
In this method, it just naively find the first worker that are available.
Return None when no worker available.
'''
def get_available_worker():
    for worker in lst_worker:
        if worker.status == 'Available':
            return worker

    return None

def send_job():
    global queue_jobs, flag
    while True:
        worker_available = get_available_worker()
        if len(queue_jobs) != 0 and worker_available and flag:
            print(worker_available.HOST)
            job = queue_jobs[0]
            queue_jobs = queue_jobs[1:]
            worker_available.status = 'Running'

            worker_available.job = job

            print("Mengirimkan pekerjaan", job)
            print("Daftar jobs yang belum dilakukan", queue_jobs)
            threading.Thread(target=start_connection, args=(job[0],
                job[1],worker_available)).start()

'''
Wait for user input in order to execute send or status command.
'''
def wait_input():
    while True:
        for msg in MENU_MSG:
            print(msg)
        
        cmd = input().split()
        if cmd[0] == "send":
            path_program, arg = cmd[1], ' '.join(cmd[2:])
            queue_jobs.append([path_program, arg])
        elif cmd[0] == "status":
            show_worker_information()

if __name__ == "__main__" :
    with open("ip_worker.txt", "r") as f:
        # Only work in python 3.8+
        while (HOST := f.readline()) != '':
            lst_worker.append(Worker(HOST.rstrip()))
        
    wait = threading.Thread(target=wait_input, args=())
    wait.start()
    send = threading.Thread(target=send_job, args=())
    send.start()

