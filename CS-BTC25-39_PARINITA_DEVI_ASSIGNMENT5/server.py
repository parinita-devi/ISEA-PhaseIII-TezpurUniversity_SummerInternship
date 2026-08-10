import socket
import threading
import datetime
import csv
import os

HOST = '0.0.0.0'
PORT = 5000

# Data structures to manage connected clients and stats
# clients dict format: {username: {"socket": conn, "ip": ip, "port": port, "login_time": time, "status": status}}
clients = {}
clients_lock = threading.Lock()

# Global statistics
stats = {
    "total_clients": 0,
    "total_messages": 0,
    "broadcast_messages": 0,
    "private_messages": 0
}
stats_lock = threading.Lock()

CSV_FILE = 'chat_history.csv'

# Initialize CSV file with headers if it doesn't exist
if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, mode='w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp", "sender", "receiver", "message_type", "message"])

def log_chat(sender, receiver, msg_type, message):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(CSV_FILE, mode='a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([timestamp, sender, receiver, msg_type, message])

def get_last_5_messages(username):
    user_msgs = []
    if os.path.exists(CSV_FILE):
        with open(CSV_FILE, mode='r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['sender'] == username:
                    user_msgs.append(f"[{row['timestamp']}] ({row['message_type']}) To {row['receiver']}: {row['message']}")
    return user_msgs[-5:]

def broadcast(message, sender_username=None):
    with clients_lock:
        for user, info in clients.items():
            if user != sender_username:
                try:
                    info["socket"].sendall(message.encode('utf-8'))
                except:
                    pass

def handle_client(conn, addr):
    client_ip, client_port = addr
    username = None
    
    try:
        # Prompt for registration
        conn.sendall("ENTER_USERNAME".encode('utf-8'))
        username = conn.recv(1024).decode('utf-8').strip()
        
        with clients_lock:
            if username in clients:
                conn.sendall("ERROR Username already taken. Disconnecting.".encode('utf-8'))
                conn.close()
                return
            login_time = datetime.datetime.now().strftime("%H:%M:%S")
            clients[username] = {
                "socket": conn,
                "ip": client_ip,
                "port": client_port,
                "login_time": login_time,
                "status": "Online"
            }
        
        with stats_lock:
            stats["total_clients"] += 1
            
        print(f"[+] {username} connected from {client_ip}:{client_port} at {login_time}")
        
        # Broadcast join notification
        broadcast(f"*** {username} has joined the chat ***\n", sender_username=username)
        
        # Persistent history: Send last 5 messages sent by this user
        history = get_last_5_messages(username)
        if history:
            conn.sendall("\n--- Your Last 5 Messages ---\n".encode('utf-8'))
            for msg in history:
                conn.sendall((msg + "\n").encode('utf-8'))
            conn.sendall("-----------------------------\n".encode('utf-8'))
            
        # Main communication loop
        while True:
            data = conn.recv(1024).decode('utf-8')
            if not data:
                break
                
            msg = data.strip()
            
            # Command: /list
            if msg == "/list":
                with clients_lock:
                    online_users = [f"{u} ({info['ip']}:{info['port']})" for u, info in clients.items()]
                conn.sendall(f"Online Users:\n" + "\n".join(online_users) + "\n".encode('utf-8'))
                
            # Command: /msg <username> <message>
            elif msg.startswith("/msg "):
                parts = msg.split(' ', 2)
                if len(parts) < 3:
                    conn.sendall("Usage: /msg <username> <message>\n".encode('utf-8'))
                    continue
                
                target_user, pmsg = parts[1], parts[2]
                target_sock = None
                
                with clients_lock:
                    if target_user in clients:
                        target_sock = clients[target_user]["socket"]
                
                if target_sock:
                    target_sock.sendall(f"[Private from {username}]: {pmsg}\n".encode('utf-8'))
                    log_chat(username, target_user, "Private", pmsg)
                    with stats_lock:
                        stats["private_messages"] += 1
                        stats["total_messages"] += 1
                else:
                    conn.sendall(f"Error: User '{target_user}' not found or offline.\n".encode('utf-8'))
                    
            # Server statistics display (Optional admin check)
            elif msg == "/stats":
                with stats_lock, clients_lock:
                    stat_msg = (f"\n--- Server Statistics ---\n"
                                f"Connected Users: {len(clients)}\n"
                                f"Total Processed: {stats['total_messages']}\n"
                                f"Broadcast Msgs: {stats['broadcast_messages']}\n"
                                f"Private Msgs: {stats['private_messages']}\n"
                                f"-------------------------\n")
                conn.sendall(stat_msg.encode('utf-8'))

            # Normal Broadcast Message
            else:
                formatted_msg = f"[{username}]: {msg}\n"
                broadcast(formatted_msg, sender_username=username)
                log_chat(username, "ALL", "Broadcast", msg)
                with stats_lock:
                    stats["broadcast_messages"] += 1
                    stats["total_messages"] += 1

    except Exception as e:
        print(f"Error handling {username}: {e}")
    finally:
        if username:
            with clients_lock:
                if username in clients:
                    del clients[username]
            print(f"[-] {username} disconnected.")
            broadcast(f"*** {username} has left the chat ***\n")
        conn.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen(5)
    print(f"Server started on port {PORT}...")
    
    while True:
        conn, addr = server.accept()
        threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()

if __name__ == "__main__":
    start_server()
