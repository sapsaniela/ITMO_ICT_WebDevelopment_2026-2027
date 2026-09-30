import socket

HOST = "127.0.0.1"
PORT = 1111

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind((HOST, PORT))
print(f"Сервер запущен на {HOST}:{PORT}")

data, client_addr = server.recvfrom(1024)
print("Сервер получил:", data.decode("utf-8"))

server.sendto("Hello, client".encode("utf-8"), client_addr)

server.close()