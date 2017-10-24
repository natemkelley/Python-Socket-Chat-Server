cd # echo_server.py
import socket

host = ''        # Symbolic name meaning all available interfaces
port = 9020     # Arbitrary non-privileged port

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
s.listen(True)
conn, addr = s.accept() #does not send and receive on same socket but rather the one return by accept

print('Connected by', addr)
while True:
    data = conn.recv(1024)
    if not data: break
    conn.sendall(data)
conn.close()