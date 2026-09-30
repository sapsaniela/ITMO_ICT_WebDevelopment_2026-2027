import socket
import threading

HOST = "127.0.0.1"
PORT = 1114


def receive_messages(sock):
    while True:
        try:
            data = sock.recv(1024)
            if not data:
                print("Соединение с сервером закрыто")
                break
            print(data.decode("utf-8"), end="")
        except OSError:
            break


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))

    prompt = sock.recv(1024).decode("utf-8")
    nickname = input(prompt)
    sock.sendall(nickname.encode("utf-8"))

    thread = threading.Thread(target=receive_messages, args=(sock,), daemon=True)
    thread.start()

    print("Чат запущен. Для выхода введите /exit")
    while True:
        message = input()
        try:
            sock.sendall(message.encode("utf-8"))
        except OSError:
            break
        if message == "/exit":
            break

    sock.close()


if __name__ == "__main__":
    main()