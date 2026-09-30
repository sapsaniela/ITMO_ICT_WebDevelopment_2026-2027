import socket

HOST = "127.0.0.1"
PORT = 1113

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
server.listen()
print(f"Сервер запущен: http://{HOST}:{PORT}")

while True:
    conn, addr = server.accept()
    request = conn.recv(4096)

    with open("index.html", "r", encoding="utf-8") as f:
        body = f.read().encode("utf-8")

    headers = (
        "HTTP/1.1 200 OK\r\n"
        "Content-Type: text/html; charset=utf-8\r\n"
        f"Content-Length: {len(body)}\r\n"
        "Connection: close\r\n"
        "\r\n"
    ).encode("utf-8")

    conn.sendall(headers + body)
    conn.close()