import socket
import threading
import csv
import hashlib

HOST = '0.0.0.0'
PORT = 12345

users_db = {}
active_users = set()
failed_attempts = {}
locked_accounts = set()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def load_users():
    try:
        with open('users.csv', mode='r') as f:
            reader = csv.reader(f)
            for row in reader:
                if row:
                    # Skip header line if present
                    if row[0].strip() == "username":
                        continue
                    username = row[0].strip()
                    password_hash = row[1].strip()
                    users_db[username] = password_hash
        print("[SERVER] Loaded users from users.csv")
    except Exception as e:
        print(f"[SERVER] Error loading users.csv: {e}")

def handle_client(conn, addr):
    print(f"[SERVER] New connection from {addr}")
    current_user = None

    try:
        while True:
            data = conn.recv(1024).decode().strip()
            if not data:
                break

            parts = data.split('|')
            command = parts[0]

            if command == "LOGIN":
                if len(parts) < 3:
                    conn.sendall(b"AUTH_FAILED: Invalid request format")
                    continue

                username = parts[1].strip()
                password = parts[2].strip()
                hashed_pass = hash_password(password)

                if username in locked_accounts:
                    conn.sendall(b"AUTH_FAILED: Account temporarily locked due to 5 failed attempts")
                    continue

                if username not in users_db:
                    conn.sendall(b"AUTH_FAILED: Invalid credentials")
                    continue

                if username in active_users:
                    conn.sendall(b"AUTH_FAILED: User already logged in")
                    continue

                if users_db[username] == hashed_pass:
                    active_users.add(username)
                    current_user = username
                    failed_attempts[username] = 0
                    conn.sendall(f"AUTH_SUCCESS: Welcome {username}".encode())
                    print(f"[SERVER] {username} logged in successfully.")
                else:
                    failed_attempts[username] = failed_attempts.get(username, 0) + 1
                    if failed_attempts[username] >= 5:
                        locked_accounts.add(username)
                        conn.sendall(b"AUTH_FAILED: Account temporarily locked due to 5 failed attempts")
                        print(f"[SERVER] Account {username} has been locked.")
                    else:
                        remaining = 5 - failed_attempts[username]
                        conn.sendall(f"AUTH_FAILED: Invalid credentials ({remaining} attempts left)".encode())

    except Exception as e:
        print(f"[SERVER] Connection error with {addr}: {e}")
    finally:
        if current_user and current_user in active_users:
            active_users.remove(current_user)
            print(f"[SERVER] {current_user} disconnected.")
        conn.close()

def start_server():
    load_users()
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen(5)
    print(f"[SERVER STARTED] Listening on port {PORT}...")

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

if __name__ == "__main__":
    start_server()