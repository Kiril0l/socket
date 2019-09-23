import os
import sys
import time
from datetime import datetime
from random import randint
import signal
import psutil
import socket

HOST = "127.0.0.1"
PORT = 5000
PID_FILE = "/var/run/step/demon/demon.pid"
WORK = True


def start_demon():
    if os.path.isfile(PID_FILE):
        with open(PID_FILE, "r") as pid_file:
            pid = int(pid_file.readline())
            for process in psutil.process_iter():
                if process.pid == pid:
                    print("Demon is working.")
                    return
    pid = os.fork()
    if pid:
        with open(PID_FILE, "w") as pid_file:
            pid_file.write(f"{pid}")
        print("Demon was started.")
        print(f"Demon has pid: {pid}")
    else:
        demon()
