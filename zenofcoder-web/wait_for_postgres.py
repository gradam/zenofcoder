import socket
import time
import os

port = int(os.environ["DB_PORT"])
host = os.environ['DB_HOST']

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
while True:
    try:
        s.connect((host, port))
        s.close()
        break
    except socket.error as ex:
        time.sleep(0.1)
print('Connected to Database')
