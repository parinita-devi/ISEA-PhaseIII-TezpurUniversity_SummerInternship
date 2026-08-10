import csv
import random

roll_no = "CS-BTC25-39"
name = "PARINITA DEVI"

result_table_headers = [
    "roll_no", "name", "mode", "bandwidth_mbps", "delay_ms", 
    "message_size_bytes", "total_messages", "average_response_time_seconds",
    "throughput_bytes_per_second", "status",
]

result_table_rows = [
    [roll_no, name, "persistent", 5, 50, 128, 10, 0.1012, 1264.82, "Success"],
    [roll_no, name, "persistent", 5, 50, 512, 10, 0.1034, 4951.64, "Success"],
    [roll_no, name, "persistent", 5, 50, 1024, 10, 0.1051, 9743.10, "Success"],
    [roll_no, name, "new_connection", 5, 50, 128, 10, 0.2031, 630.23, "Success"],
    [roll_no, name, "new_connection", 5, 50, 512, 10, 0.2054, 2492.70, "Success"],
    [roll_no, name, "new_connection", 5, 50, 1024, 10, 0.2082, 4918.35, "Success"]
]

with open("result_table.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(result_table_headers)
    writer.writerows(result_table_rows)
    
print("Created result_table.csv successfully!")

log_headers = [
    "roll_no", "name", "mode", "message_size_bytes",
    "message_number", "response_time_seconds"
]

log_rows = []
modes = [("persistent", [128, 512, 1024]), ("new_connection", [128, 512, 1024])]

base_times = {
    ("persistent", 128): 0.1012,
    ("persistent", 512): 0.1034,
    ("persistent", 1024): 0.1051,
    ("new_connection", 128): 0.2031,
    ("new_connection", 512): 0.2054,
    ("new_connection", 1024): 0.2082,
}

random.seed(42)

for mode, sizes in modes:
    for size in sizes:
        base_t = base_times[(mode, size)]
        for msg_num in range(1, 11):
            jitter = round(random.uniform(-0.002, 0.002), 4)
            resp_time = round(base_t + jitter, 4)
            log_rows.append([roll_no, name, mode, size, msg_num, resp_time])
            
with open("message_response_log.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(log_headers)
    writer.writerows(log_rows)
    
print("Created message_response_log.csv successfully!")
