import socket
import threading
import csv
import hashlib
import json
import time
from concurrent.futures import ThreadPoolExecutor

# Load Configuration
with open("config.json", "r") as f:
    CONFIG = json.load(f)

HOST = '0.0.0.0'
PORT = CONFIG["server_port"]
SOCKET_TIMEOUT = CONFIG["socket_timeout"]

users_db = {}
active_users = set()
failed_attempts = {}
locked_accounts = set()
lock = threading.Lock()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def load_users():
    try:
        with open('users.csv', mode='r') as f:
            reader = csv.reader(f)
            for row in reader:
                if row:
                    if row[0].strip() == "username":
                        continue
                    users_db[row[0].strip()] = row[1].strip()
        print("[SERVER] Loaded users from users.csv")
    except Exception as e:
        print(f"[SERVER] Error loading users.csv: {e}")

def handle_client(conn, addr):
    print(f"[SERVER] Connected: {addr}")
    conn.settimeout(SOCKET_TIMEOUT)
    current_user = None

    try:
        while True:
            try:
                data = conn.recv(1024).decode().strip()
                if not data:
                    break

                parts = data.split('|')
                command = parts[0]

                if command == "PING":
                    conn.sendall(b"PONG")
                    continue

                if command == "LOGIN":
                    if len(parts) < 3:
                        conn.sendall(b"AUTH_FAILED: Invalid format")
                        continue

                    username, password = parts[1].strip(), parts[2].strip()
                    hashed_pass = hash_password(password)

                    with lock:
                        if username in locked_accounts:
                            conn.sendall(b"AUTH_FAILED: Account locked")
                            continue

                        if username not in users_db or users_db[username] != hashed_pass:
                            failed_attempts[username] = failed_attempts.get(username, 0) + 1
                            if failed_attempts[username] >= CONFIG["max_failed_attempts"]:
                                locked_accounts.add(username)
                                conn.sendall(b"AUTH_FAILED: Account locked")
                            else:
                                conn.sendall(b"AUTH_FAILED: Invalid credentials")
                            continue

                        if username in active_users:
                            conn.sendall(b"AUTH_FAILED: User already logged in")
                            continue

                        active_users.add(username)
                        current_user = username
                        failed_attempts[username] = 0
                        conn.sendall(f"AUTH_SUCCESS: Welcome {username}".encode())
                        print(f"[SERVER] {username} logged in successfully.")

            except socket.timeout:
                print(f"[SERVER] Client {addr} timed out.")
                break

    except Exception as e:
        print(f"[SERVER] Error with {addr}: {e}")
    finally:
        with lock:
            if current_user and current_user in active_users:
                active_users.remove(current_user)
                print(f"[SERVER] Cleaned up session for {current_user}")
        conn.close()

def start_server():
    load_users()
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen(CONFIG["max_clients"])
    print(f"[SERVER STARTED] Listening on port {PORT} with ThreadPoolExecutor...")

    pool = ThreadPoolExecutor(max_workers=CONFIG["thread_pool_size"])

    try:
        while True:
            conn, addr = server.accept()
            pool.submit(handle_client, conn, addr)
    except KeyboardInterrupt:
        print("\n[SERVER SHUTDOWN] Shutting down gracefully...")
    finally:
        pool.shutdown(wait=False)
        server.close()

if __name__ == "__main__":
    start_server()