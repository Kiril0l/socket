import socket
import fcntl
from random import randit

HOST = "192.168.4.182"
PORT = 5000


message = [
    "kmflkdmaflkdamflsd",
    "fdasfdasfsdfdas",
    "asdf;l;ldasf;ladsf;l"
    "vnbvbnvbnvbnbnbn"
]
user = input("Введите логин:")
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
client.connect((HOST, PORT))
fcntl.fcntl(client, fcntl.LOCK_NB)
client.send(use.encode("utf-8"))
while True:
    message = messages[randit(0)]
    data = f"User:{user}\r\n{message}\n"
    try:
        client.send(data.encode("utf-8"))
    except Exception as e:
        print(e)
    try:
        request = client.recv(2048)
    except Exception as e:
        print(e)
    print(request.decode("utf-8"))
