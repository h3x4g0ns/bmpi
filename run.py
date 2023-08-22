import subprocess
import threading
import os
import sys
import fcntl
import select
from colorama import init
from termcolor import colored

def set_nonblocking(fd):
    flags = fcntl.fcntl(fd, fcntl.F_GETFL)
    fcntl.fcntl(fd, fcntl.F_SETFL, flags | os.O_NONBLOCK)

def run_command(command, app_name, color):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    set_nonblocking(process.stdout.fileno())
    set_nonblocking(process.stderr.fileno())
    while True:
        reads, _, _ = select.select([process.stdout, process.stderr], [], [])
        for fd in reads:
            output = fd.readline().decode().strip()
            if output:
                print(colored(f"[{app_name}]", color), output)
        if process.poll() is not None:
            break
    return process.returncode

def run_webserver():
    app_name = "webserver"
    command = "cd webserver && go run main.go"
    return run_command(command, app_name, "green")

def run_viz():
    app_name = "viz"
    command = "cd viz && npm run start"
    return run_command(command, app_name, "red")

# Runs each service as a seperate thread
thread_names = [run_webserver, run_viz]
threads = [threading.Thread(target=thread) for thread in thread_names]
init()
[thread.start() for thread in threads]
[thread.join() for thread in threads]