import socket
import hashlib
import datetime


def start_server(host='localhost', port=80, active_users=10):
    global sock
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.bind((host, port))
        print(f'Using port {port}')
    except OSError:
        sock.bind(('localhost', 80))
        print("Using port 80")
    except OSError:
        sock.bind(('localhost', 8080))
        print("Using port 8080")

    sock.listen(active_users)


def client_connection():
    while True:
        try:
            conn, addr = sock.accept()
            print("Connected", addr)
            data = conn.recv(8192).decode('utf-8')
            if data.find('Referer: http://localhost/register.html') != -1:
                resp = load_page(register_user(data))
                conn.send(resp)
                conn.shutdown(socket.SHUT_WR)
            else:
                resp = load_page(data)
                conn.send(resp)
                conn.shutdown(socket.SHUT_WR)
        except TypeError:
            pass


def load_page(request_data):
    try:
        HDRS = 'HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8\r\n\r\n'
        HDRS_404 = 'HTTP/1.1 404 OK\r\nContent-Type: text/html; charset=utf-8\r\n\r\n'
        HDRS_403 = 'HTTP/1.1 403 OK\r\nContent-Type: text/html; charset=utf-8\r\n\r\n'
        path = request_data.split(' ')[1]
        response = ''
        if path.split('.')[1] in ['html', 'css', 'js', 'png', 'ico', 'php', 'txt']:
            try:
                with open('views'+path, 'rb') as file:
                    response = file.read()
                return HDRS.encode('utf-8') + response
            except (FileNotFoundError, PermissionError, AttributeError):
                return (HDRS_404 + '404 PAGE NOT FOUND').encode('utf-8')
        else:
            return (HDRS_403 + '403 FORBIDDEN').encode('utf-8')
    except (IndexError, AttributeError):
        pass


def register_user(data):
    try:
        user = data[data.find('login='):].split('&')
        user = dict(tuple([tuple(i.split('=')) for i in user]))
        path = f'C:/Users/Пользователь1/PycharmProjects/Flask/user/{hashlib.md5(user["login"].encode()).hexdigest()}.txt'
        try:
            open(path, 'r')
        except FileNotFoundError:
            with open(path, 'w') as file:
                file.write(f'login:{user["login"]}\npassword:{hashlib.sha256(user["pass"].encode()).hexdigest()}\ntime:{datetime.datetime.now()}\n')
            with open(f'C:/Users/Пользователь1/PycharmProjects/Flask/user/{hashlib.sha256(user["pass"].encode()).hexdigest()}.txt', 'w') as file:
                file.write(user["pass"])
            return 'create /create.html'
        return 'exist /exist.html'
    except ValueError:
        pass

if __name__ == '__main__':
    start_server()
    client_connection()
