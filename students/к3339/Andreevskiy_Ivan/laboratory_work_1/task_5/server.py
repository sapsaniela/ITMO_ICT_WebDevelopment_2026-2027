import socket
from urllib.parse import parse_qs
 
HOST = "127.0.0.1"
PORT = 1115

grades = {}
 
 
def render_page():
    rows = ""
    for subject, marks in grades.items():
        marks_str = ", ".join(str(m) for m in marks)
        rows += f"<tr><td>{subject}</td><td>{marks_str}</td></tr>\n"
 
    if not rows:
        rows = "<tr><td colspan='2'>Оценок пока нет</td></tr>"
 
    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="utf-8">
    <title>Журнал оценок</title>
</head>
<body>
    <h1>Журнал оценок</h1>
    <table border="1" cellpadding="6">
        <tr><th>Дисциплина</th><th>Оценки</th></tr>
        {rows}
    </table>
 
    <h2>Добавить оценку</h2>
    <form method="POST" action="/">
        Дисциплина: <input type="text" name="subject"><br><br>
        Оценка: <input type="number" name="grade" min="1" max="5"><br><br>
        <input type="submit" value="Отправить">
    </form>
</body>
</html>"""
 
 
def build_response(status, body):
    body_bytes = body.encode("utf-8")
    headers = (
        f"HTTP/1.1 {status}\r\n"
        "Content-Type: text/html; charset=utf-8\r\n"
        f"Content-Length: {len(body_bytes)}\r\n"
        "Connection: close\r\n"
        "\r\n"
    ).encode("utf-8")
    return headers + body_bytes
 
 
def recv_request(conn):
    data = b""
    while b"\r\n\r\n" not in data:
        chunk = conn.recv(4096)
        if not chunk:
            break
        data += chunk
 
    header_part, _, rest = data.partition(b"\r\n\r\n")
    headers_text = header_part.decode("utf-8", errors="replace")
 
    content_length = 0
    for line in headers_text.split("\r\n"):
        if line.lower().startswith("content-length:"):
            content_length = int(line.split(":", 1)[1].strip())
 
    body = rest
    while len(body) < content_length:
        chunk = conn.recv(4096)
        if not chunk:
            break
        body += chunk
 
    return headers_text, body.decode("utf-8", errors="replace")
 
 
def handle_request(headers_text, body_text):
    if not headers_text:
        return build_response("400 Bad Request", "<h1>Пустой запрос</h1>")
 
    request_line = headers_text.split("\r\n")[0]
    parts = request_line.split(" ")
    if len(parts) < 2:
        return build_response("400 Bad Request", "<h1>Некорректный запрос</h1>")
 
    method, path = parts[0], parts[1]
 
    if method == "GET":
        return build_response("200 OK", render_page())
 
    elif method == "POST":
        params = parse_qs(body_text)
        subject = params.get("subject", [""])[0].strip()
        grade_str = params.get("grade", [""])[0].strip()
 
        if subject and grade_str.isdigit():
            grade = int(grade_str)
            grades.setdefault(subject, []).append(grade)
 
        return build_response("200 OK", render_page())
 
    else:
        return build_response("405 Method Not Allowed", "<h1>Метод не поддерживается</h1>")
 
 
def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen()
    print(f"Сервер запущен: http://{HOST}:{PORT}")
 
    while True:
        conn, addr = server.accept()
        try:
            headers_text, body_text = recv_request(conn)
 
            response = handle_request(headers_text, body_text)
            conn.sendall(response)
        finally:
            conn.close()
 
 
if __name__ == "__main__":
    main()