import socket
import datetime
 
HOST = '10.0.0.1'
PORT = 5000

def run_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)
    print(f"[SERVER] TCP Server listening on {HOST}:{PORT}")

    with open("server_log.txt", "a") as log_file:
        while True:
            try:
                conn, addr = server_socket.accept()
                while True:
                    data = conn.recv(2048)
                    if not data:
                        break

                    decoded = data.decode('utf-8', errors='ignore')
                    parts = decoded.split('|')

                    if len(parts) >= 3:
                        if len(parts) == 4:
                            mode, msg_id, size, _ = parts[0], parts[1], parts[2], parts[3]
                        else:
                            mode = "unknown"
                            msg_id, size, _ = parts[0], parts[1], parts[2]

                        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]

                        ack_msg = f"ACK|{msg_id}|{size}"
                        conn.sendall(ack_msg.encode('utf-8'))

                        log_entry = f"{timestamp}, {addr[0]}, {mode}, {msg_id}, {size}, ACK sent\n"
                        log_file.write(log_entry)
                        log_file.flush()
                        print(f"[SERVER] Handled Msg {msg_id} ({size} bytes) from {mode}")

            except Exception as e:
                print(f"[SERVER] Error: {e}")
                break

if __name__ == "__main__":
    run_server()


