import socket

SERVER_ADDR = ("127.0.0.1", 1111)

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.sendto("Hello, server".encode("utf-8"), SERVER_ADDR)

data, _ = client.recvfrom(1024)
print("Клиент получил:", data.decode("utf-8"))

client.close()