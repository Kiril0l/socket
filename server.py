import socket

HOST = "127.0.0.1"
PORT = 5000

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
        if not data:
            break
        result = f"{data}\n"
        client.send(data)    #возвращает нащи данные
except Exception as e:
    print(e)
finally:
    srv.close()


# демон в фоне создает сокет, получает данные и их обрабатывает. демон_клосе он пишет я завершился и удаляет пид
