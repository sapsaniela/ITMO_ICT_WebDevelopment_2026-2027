import socket
import threading

HOST = "127.0.0.1"
PORT = 1114

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
server.listen()
print(f"Сервер чата запущен на {HOST}:{PORT}")

clients = {}         
clients_lock = threading.Lock()


def broadcast(message, exclude_conn=None):
    with clients_lock:
        for conn in list(clients.keys()):
            if conn is exclude_conn:
                continue
            try:
                conn.sendall(message.encode("utf-8"))
            except OSError:
                pass


def handle_client(conn, addr):
    try:
        conn.sendall("Введите ваш ник: ".encode("utf-8"))
        nickname = conn.recv(1024).decode("utf-8").strip()

        with clients_lock:
            clients[conn] = nickname
        print(f"{nickname} подключился ({addr})")
        broadcast(f"[{nickname} присоединился к чату]\n", exclude_conn=conn)

        while True:
            data = conn.recv(1024)
            if not data:
                break

            text = data.decode("utf-8").strip()
            if not text:
                continue

            if text == "/exit":
                break

            broadcast(f"{nickname}: {text}\n", exclude_conn=conn)

    except ConnectionResetError:
        pass
    finally:
        with clients_lock:
            nickname = clients.pop(conn, "Неизвестный")
        print(f"{nickname} отключился")
        broadcast(f"[{nickname} покинул чат]\n", exclude_conn=conn)
        conn.close()


while True:
    conn, addr = server.accept()
    thread = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
    thread.start()