import socket
import threading

# Server Configuration
HOST = '0.0.0.0'  # Listen on all available network interfaces
PORT = 5000

# Dictionary to keep track of connected clients: {username: socket}
clients = {}
clients_lock = threading.Lock()

def broadcast(message, sender_socket=None):
    """Send a message to all connected clients except the sender."""
    with clients_lock:
        for client_socket in list(clients.values()):
            if client_socket != sender_socket:
                try:
                    client_socket.send(message.encode('utf-8'))
                except:
                    # Handle broken connection
                    client_socket.close()

def handle_client(client_socket, client_address):
    """Handle communication with an individual client."""
    username = None
    try:
        # First message received from client is their username
        username = client_socket.recv(1024).decode('utf-8').strip()
        
        with clients_lock:
            # Prevent duplicate usernames
            if username in clients or not username:
                client_socket.send("ERROR: Username taken or invalid. Disconnecting.".encode('utf-8'))
                client_socket.close()
                return
            
            clients[username] = client_socket

        print(f"[+] {username} connected from {client_address}")
        
        # Notify everyone that a new user joined
        join_msg = f"SYSTEM: {username} has joined the chat!"
        broadcast(join_msg)

        # Main message loop
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            
            message = data.decode('utf-8').strip()

            # Handle Private Messaging (/msg target_user message)
            if message.startswith("/msg "):
                parts = message.split(" ", 2)
                if len(parts) >= 3:
                    target_user = parts[1]
                    private_msg = parts[2]

                    with clients_lock:
                        if target_user in clients:
                            target_socket = clients[target_user]
                            formatted_msg = f"[Private from {username}]: {private_msg}"
                            target_socket.send(formatted_msg.encode('utf-8'))
                            client_socket.send(f"[Private to {target_user}]: {private_msg}".encode('utf-8'))
                        else:
                            client_socket.send(f"SYSTEM: User '{target_user}' not found.".encode('utf-8'))
                else:
                    client_socket.send("SYSTEM: Usage: /msg <username> <message>".encode('utf-8'))
            else:
                # Regular Broadcast Message
                formatted_msg = f"{username}: {message}"
                print(f"[{username}]: {message}")
                broadcast(formatted_msg, sender_socket=client_socket)

    except (ConnectionResetError, BrokenPipeError):
        pass
    finally:
        # Cleanup when client disconnects
        if username:
            with clients_lock:
                if username in clients:
                    del clients[username]
            print(f"[-] {username} disconnected.")
            broadcast(f"SYSTEM: {username} has left the chat.")
        
        client_socket.close()

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Reuse port immediately after restart
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)
    print(f"[*] Server listening on {HOST}:{PORT}...")

    while True:
        client_socket, client_address = server_socket.accept()
        # Start a new thread for each client
        thread = threading.Thread(target=handle_client, args=(client_socket, client_address), daemon=True)
        thread.start()

if __name__ == "__main__":
    start_server()
