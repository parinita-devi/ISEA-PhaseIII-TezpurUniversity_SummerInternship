import socket
import threading
import sys
import time

SERVER_IP = '10.0.0.1' # Standard Mininet h1 IP
PORT = 5000

def receive_messages(sock):
    while True:
        try:
            msg = sock.recv(1024).decode('utf-8')
            if not msg:
                break
            print(msg, end='')
        except:
            break

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((SERVER_IP, PORT))
    except Exception as e:
        print(f"Could not connect to server: {e}")
        return

    # Handle Initial Handshake / Username Registration
    initial = sock.recv(1024).decode('utf-8')
    if "ENTER_USERNAME" in initial:
        if len(sys.argv) > 1:
            username = sys.argv[1]
        else:
            username = input("Enter Username: ")
        sock.sendall(username.encode('utf-8'))

    # Thread for listening incoming messages
    threading.Thread(target=receive_messages, args=(sock,), daemon=True).start()

    # If automated benchmark arguments are provided
    if len(sys.argv) > 2 and sys.argv[2] == "--auto":
        count = int(sys.argv[3]) if len(sys.argv) > 3 else 50
        time.sleep(1)
        for i in range(count):
            sock.sendall(f"Automated benchmark message {i+1} from {sys.argv[1]}".encode('utf-8'))
            time.sleep(0.01) # Small delay to prevent overflow
        time.sleep(2)
        sock.close()
        return

    # Interactive Loop
    try:
        while True:
            msg = input()
            if msg.lower() == 'exit':
                break
            sock.sendall(msg.encode('utf-8'))
    except KeyboardInterrupt:
        pass
    finally:
        sock.close()

if __name__ == "__main__":
    main()
