import time
import socket
import csv
import os
import matplotlib.pyplot as plt

# Ensure output directories exist
os.makedirs("graphs", exist_ok=True)

SERVER_IP = "127.0.0.1"
PORT = 12345
CLIENT_COUNTS = [1, 5, 10, 15, 20]

results = []

print("[BENCHMARK] Starting scalability test...")

for count in CLIENT_COUNTS:
    sockets = []
    start_time = time.time()
    successful_connections = 0

    for _ in range(count):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(2.0)
            s.connect((SERVER_IP, PORT))
            sockets.append(s)
            successful_connections += 1
        except Exception:
            pass

    end_time = time.time()
    total_time = end_time - start_time
    avg_latency_ms = (total_time / count) * 1000 if count > 0 else 0
    throughput_rps = successful_connections / total_time if total_time > 0 else 0

    # Clean up sockets
    for s in sockets:
        try:
            s.close()
        except Exception:
            pass

    results.append({
        "concurrent_clients": count,
        "avg_latency_ms": round(avg_latency_ms, 2),
        "throughput_rps": round(throughput_rps, 2)
    })
    print(f"Clients: {count} | Avg Latency: {round(avg_latency_ms, 2)} ms | Throughput: {round(throughput_rps, 2)} req/s")

# 1. Save results to performance_results.csv
csv_path = "performance_results.csv"
with open(csv_path, mode="w", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=["concurrent_clients", "avg_latency_ms", "throughput_rps"])
    writer.writeheader()
    writer.writerows(results)

print(f"[BENCHMARK] Saved results to {csv_path}")

# 2. Plot Latency Graph
clients = [r["concurrent_clients"] for r in results]
latencies = [r["avg_latency_ms"] for r in results]
throughputs = [r["throughput_rps"] for r in results]

plt.figure(figsize=(8, 5))
plt.plot(clients, latencies, marker='o', color='b', label='Avg Latency (ms)')
plt.title('Latency vs Concurrent Clients')
plt.xlabel('Number of Concurrent Clients')
plt.ylabel('Average Latency (ms)')
plt.grid(True)
plt.savefig('graphs/latency_vs_clients.png')
plt.close()

# 3. Plot Throughput Graph
plt.figure(figsize=(8, 5))
plt.plot(clients, throughputs, marker='s', color='g', label='Throughput (req/s)')
plt.title('Throughput vs Concurrent Clients')
plt.xlabel('Number of Concurrent Clients')
plt.ylabel('Throughput (Requests/sec)')
plt.grid(True)
plt.savefig('graphs/throughput_vs_clients.png')
plt.close()

print("[BENCHMARK] Successfully generated graphs in 'graphs/' directory!")