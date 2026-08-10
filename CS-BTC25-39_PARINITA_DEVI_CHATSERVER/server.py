import socket
import threading
from datetime import datetime

HOST = '0.0.0.0'
PORT = 5000

clients = {}
lock = threading.Lock()

def log_event(event_type, username, client_ip):
    timestamp = datetime.now().strftime("%H:%M:%S")
    log_line = f"{timestamp},{event_type},{username},{client_ip}\n"
    print(log_line.strip())

def log_chat(username, message):
    timestamp = datetime.now().strftime("%H:%M:%S")
    log_line = f"{timestamp},{username},{message}\n"
    with open("chat_log.txt", "a") as f:
        f.write(log_line)

def broadcast(message, sender_socket=None):
    with lock:
        for client_sock in list(clients.keys()):
            if client_sock != sender_socket:
                try:
                    client_sock.sendall(message.encode('utf-8'))
                except Exception:
                    client_sock.close()
                    del clients[client_sock]

def handle_client(client_socket, client_address):
    ip_addr = client_address[0]
    username = ""
    try:
        client_socket.sendall("Enter Username: ".encode('utf-8'))
        username = client_socket.recv(1024).decode('utf-8').strip()

        if not username:
            username = "Anonymous"

        with lock:
            clients[client_socket] = (username, ip_addr)

        log_event("CONNECTED", username, ip_addr)

        while True:
            data = client_socket.recv(1024)
            if not data:
                break

            message = data.decode('utf-8').strip()
            if not message:
                continue

            log_chat(username, message)

            broadcast_msg = f"[{username}] {message}"
            broadcast(broadcast_msg, sender_socket=client_socket)

    except ConnectionResetError:
        pass
    finally:
        with lock:
            if client_socket in clients:
                log_event("DISCONNECTED", username, ip_addr)
                del clients[client_socket]
        client_socket.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen(5)
    print(f"[*] Chat Server listening on {HOST}:{PORT}")

    while True:
        client_sock, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(client_sock, addr))
        thread.daemon = True
        thread.start()

if __name__ == "__main__":
    start_server()



