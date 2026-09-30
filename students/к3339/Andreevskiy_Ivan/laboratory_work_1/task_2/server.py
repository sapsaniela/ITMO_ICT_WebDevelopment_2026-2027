import socket

HOST = "127.0.0.1"
PORT = 1112


def calculate_T_Area(a, b, h):
    return ((a + b) / 2) * h


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
server.listen()
print(f"Сервер запущен на {HOST}:{PORT}")

conn, addr = server.accept()
print("Подключился клиент:", addr)

data = conn.recv(1024).decode("utf-8")
print("Получены параметры:", data)

try:
    a_str, b_str, h_str = data.split()
    a, b, h = float(a_str), float(b_str), float(h_str)
    area = calculate_T_Area(a, b, h)
    result = f"Площадь трапеции: {area}"
except ValueError:
    result = "Ошибка: некорректные данные"

conn.sendall(result.encode("utf-8"))

conn.close()
server.close()