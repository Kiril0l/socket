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
PID_FILE = "/var/run/demon.pid"
WORK = True


srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
srv.bind((HOST, PORT))
srv.listen(20)   #очередь обращений
try:
    client, addr = srv.accept()  #установка соединения(данные о соединении)
    for index in range(1, 10):
        data = client.recv(2048)   #принимаем данные(объем в байтах)
        data_str = data.decode("utf-8")
        print(data)
        if "close" in data_str:
            break
        if "demon_close" in data_str:
            lambda: os.kill(get_pid(), signal.SIGKILL)
        if not data:
            break
        result = f"{data}\n"
        client.send(data)    #возвращает нащи данные
except Exception as e:
    print(e)
finally:
    srv.close()


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

def demon():
    def handler(signum, frame):
        with open("signal.log", "a") as log_file:
            log_file.write(f"Signal: {signum}\n{frame}\n\n")

    signal.signal(signal.SIGUSR1, handler)
    signal.signal(signal.SIGUSR2, handler)


    while True:
        try:
            with open("demon.log", "a") as log_file:
                log_file.write(f"{datetime.now()}\n\n")
        except KeyboardInterrupt:
            with open("signal.log", "a") as log_file:
                log_file.write("Ctrl + C")
        except Exception as e:
            pass
        finally:
            time.sleep(randint(5, 15))


def get_pid():
    pid = 0
    with open(PID_FILE, "r") as pid_file:
        pid = int(pid_file.readline())
    return pid


if __name__ == '__main__':
    try:
        os.mkdir(os.path.join(*os.path.split(PID_FILE)[:-1]))
    except FileNotFoundError:
        try:
            os.makedirs(os.path.join(*os.path.split(PID_FILE)[:-1]))
        except PermissionError:
            print("WTF !!!")
            sys.exit(1)
    except FileExistsError:
        pass
    args = sys.argv[1:]
    if len(args):
        send_signal(args[0])
    else:
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
