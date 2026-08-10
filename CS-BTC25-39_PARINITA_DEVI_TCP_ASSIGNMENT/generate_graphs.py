import pandas as pd
import matplotlib.pyplot as plt
import os

os.makedirs("graphs", exist_ok=True)

df_results = pd.read_csv("CS-BTC25-39_tcp_rtt_data.csv")
df_logs = pd.read_csv("CS-BTC25-39_tcp_rtt_data.csv")

plt.figure(figsize=(8, 5))
avg_by_mode = df_results.groupby("mode")["average_response_time_seconds"].mean()
avg_by_mode.plot(kind="bar", color=['#2b6cb0', 'e53e3e'])
plt.title("Average Response Time: Persistent vs New Connection")
plt.xlabel("TCP Mode")
plt.ylabel("Average Response Time (seconds)")
plt.xticks(rotation=0)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig("graphs/mode_vs_response_time.png")
plt.close()

plt.figure(figsize=(8, 5))
for mode, group in df_results.groupby("mode"):
    plt.plot(group["message_size_bytes"], group["throughput_bytes_per_second"], marker='o', label=mode, linewidth=2)
plt.title("Message Size vs Throughput")
plt.xlabel("Message Size (bytes)")
plt.ylabel("Throughput (bytes/sec)")
plt.legend()
plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig("graphs/message_size_vs_throughput.png")
plt.close()

plt.figure(figsize(10, 5))
df_512 = df_logs[df_logs["message_size_bytes"] ==512]
for mode, group in df_512.groupby("mode"):
    plt.plot(group["message_number"], group["response_time_seconds"], marker='s', label=f"512 bytes ({mode})")
plt.title("Response Time per Message (512-Byte Messages)")
plt.xlabel("Message Number")
plt.ylabel("Response Time (seconds)")
plt.legend()
plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig("graphs/message_response_time.png")
plt.close()

print("[GRAPHS] All 3 graphs generated successfully in graphs/ directory!")



