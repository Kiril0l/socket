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


def demon():
    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind((HOST, PORT))
    srv.listen(20)   #очередь обращений
    storage = {}
    try:
        sock = storage[key]
    except KeyError:
        print(f"Key {key} not found.")
        return
    try:
        while True:
            data = sock.recv(2048)
            response = data.decode("utf-8")
            print(client, response)
            if "close" in response:
                break
            if "demon_close" in response:
                lambda: os.kill(get_pid(), signal.SIGKILL)
            for client, client_sock in storage.items():
                if client != key:
                    client_sock.send(f"{client[0]}\n".encode("utf-8"))
                    client_sock.send(response.encode("utf-8"))
    except Exception as e:
        print(e)
    finally:
        sock.close()
        del storage[key]

def get_pid():
    pid = 0
    with open(PID_FILE, "r") as pid_file:
        pid = int(pid_file.readline())
    return pid


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

if __name__ == '__main__':
    start_demon()


# демон
# 1 создать сокет
# 2 сказать ос, чтоб не резервировала порт
# 3 адрес и порт
# 4 устанавл очередь
# 5 ожидание подключения
# цикл
# 6 получить сообщение от клиента  recv
# 7 проверить не является ли командой
# если да - прервать выполнение цикла и закрыть сокет и удалить пид файл демон_клосе
# если нет преобразовать сообщение в заглавные буквы и отправить клиенту
