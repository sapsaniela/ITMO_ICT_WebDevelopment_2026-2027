import socket

HOST = "127.0.0.1"
PORT = 1112

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

print("Вычисление площади трапеции")
a = input("Введите основание a:")
b = input("Введите основание b:")
h = input("Введите высоту h:")

message = f"{a} {b} {h}"
client.sendall(message.encode("utf-8"))

data = client.recv(1024)
print(data.decode("utf-8"))

client.close()