import pandas as pd
import matplotlib.pyplot as plt
import os

os.makedirs('graphs', exist_ok=True)

df = pd.read_csv('performance_results.csv')

plt.figure(figsize=(6, 4))
plt.plot(df['clients'], df['avg_delivery_time_ms'], marker='o', color='b', linewidth=2)
plt.title('Number of Clients vs Average Delivery Time')
plt.xlabel('Number of Clients')
plt.ylabel('Avg Delivery Time (ms)')
plt.grid(True)
plt.xticks(df['clients'])
plt.tight_layout()
plt.savefig('graphs/clients_vs_delay.png')
plt.close()

plt.figure(figsize=(6, 4))
plt.plot(df['clients'], df['throughput_msgs_per_sec'], marker='s', color='g', linewidth=2)
plt.title('Number of Clients vs Throughput')
plt.xlabel('Number of Clients')
plt.ylabel('Throughput (msgs/sec)')
plt.grid(True)
plt.xticks(df['clients'])
plt.tight_layout()
plt.savefig('graphs/clients_vs_throughput.png')
plt.close()

print("[+] Performance graphs saved successfully in 'graphs/' folder.")





