import socket
import threading
import sys
import time

SERVER_IP = '127.0.01'
PORT = 5000

def receive_messages(sock):
    while True:
        try:
            data = sock.recv(1024)
            if not data:
                break
            print(data.decode('utf-8'))
        except Exception:
            break

def run_interactive():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((SERVER_IP, PORT))

    initial_prompt = sock.recv(1024).decode('utf-8')
    username = input(initial_prompt)
    sock.sendall(username.encode('utf-8'))

    thread = threading.Thread(target=receive_messages, args=(sock,))
    thread.daemon = True
    thread.start()

    while True:
        try:
            msg = input()
            if msg.lower() == 'exit':
                break
            sock.sendall(msg.encode('utf-8'))
        except KeyboardInterrupt:
            break
    sock.close()

def run_benchmark(username, num_messages=20):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((SERVER_IP, PORT))

    sock.recv(1024)
    sock.sendall(username.encode('utf-8'))

    time.sleep(0.5)

    delays = []
    start_total = time.time()

    for i in range(num_messages):
        t0 = time.time()
        msg = f"Benchmark message {i+1} from {username}"
        sock.sendall(msg.encode('utf-8'))
        t1 = time.time()
        delays.append((t1 - t0) * 1000.0)
        time.sleep(0.05)

    end_total = time.time()
    sock.close()

    total_time = end_total - start_total
    avg_delay = sum(delays) / len(delays)
    return num_messsages, avg_delay, total_time

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--benchmark":
        user = sys.argv[2] if len(sys.argv) > 2 else "Parinita"
        msgs, avg_d, tol_t = run_benchmark(user)
        print(f"RESULT,{msgs},{avg_d:.2f},{tot_t:.2f}")
    else:
        run_interactive()



