import os
import fcntl
import socket
import select
import threading

HOST = "127.0.0.1"
PORT = 5000



def executor(key):
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
            for client, client_sock in storage.items():
                if client != key:
                    client_sock.send(f"{client[0]}\n".encode("utf-8"))
                    client_sock.send(response.encode("utf-8"))
    except Exception as e:
        print(e)
    finally:
        sock.close()
        del storage[key]



srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
srv.bind((HOST, PORT))
srv.listen(20)   #очередь обращений
storage = {}
try:
    flag = True
    while flag:
        client, addr = srv.accept()  #установка соединения(данные о соединении)
        storage[addr] = client
        worker = threading.Thread(target=executor, args=(addr,))
        worker.start()
    # for index in range(1, 10):
    #     data = client.recv(2048)   #принимаем данные(объем в байтах)
    #     data_str = data.decode("utf-8")
    #     print(data)
    #     if not data:
    #         break
    #     result = f"{data}\n"
    #     client.send(data)    #возвращает нащи данные
except Exception as e:
    print(e)
finally:
    srv.close()
