import socket
import time
import csv

SERVER_IP = "10.0.0.1"
PORT = 5000
ROLL_NO = "CS-BTC25-39"
NAME = "PARINITA DEVI"
BW_MBPS = "5"
DELAY_MS = "50ms"

MESSAGE_SIZES = [128, 512, 1024]
MODES = ["persistent", "new_connection"]
NUM_MESSAGES = 10

def generate_payload(size, mode, msg_id):
    header = f"{mode}|{msg_id}|{size}|"
    padding_needed = size - len(header)
    if padding_needed < 0:
        padding_needed = 0
    payload = header + "X" * padding_needed
    return payload.encode("utf-8")
    
def run_experiments():
    all_results = []
    print("[CLIENT] Starting TCP Performance Experiments...")
    
    for mode in MODES:
        for size in MESSAGE_SIZES:
            print(f"[CLIENT] Running Mode: {mode}, Size: {size} bytes")
            
            if mode == "persistent":
                try:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.connect((SERVER_IP, PORT))
                    for i in range(1, NUM_MESSAGES + 1):
                        payload = generate_payload(size, mode, i)
                        t_start = time.time()
                        s.sendall(payload)
                        data = s.recv(4096)
                        t_end = time.time()
                        rtt_ms = (t_end - t_start) * 1000.0
                        all_results.append([ROLL_NO, NAME, BW_MBPS, DELAY_MS, mode, size, i, rtt_ms])
                    s.close()
                except Exception as e:
                    print(f"Error in persistent connection: {e}")
                    
            elif mode == "new_connection":
                for i in range(1, NUM_MESSAGES + 1):
                    try:
                        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        t_start = time.time()
                        s.connect((SERVER_IP, PORT))
                        payload = generate_payload(size, mode, i)
                        s.sendall(payload)
                        data = s.recv(4096)
                        t_end = time.time()
                        s.close()
                        rtt_ms = (t_end - t_start) * 1000.0
                        all_results.append([ROLL_NO, NAME, BW_MBPS, DELAY_MS, mode, size, i, rtt_ms])
                    except Exception as e:
                        print(f"Error in new connection: {e}")
                        
    csv_file = f"{ROLL_NO}_tcp_rtt_data.csv"
    with open(csv_file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Roll_No", "BW_Mbps", "Delay_ms", "Connection_Mode", "Message_Size_Bytes", "Message_ID", "RTT_ms"])
        writer.writerows(all_results)
        
    print(f"[CLIENT] Experiments completed successfully! CSV files generated.")
    
if __name__ == "__main__":
    run_experiments()
