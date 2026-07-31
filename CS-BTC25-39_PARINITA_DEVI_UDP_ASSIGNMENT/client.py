import socket
import time

HOST = "10.0.0.1"
PORT = 5005

client = socket.socket(
    socket.AF_INET, 
    socket.SOCK_DGRAM
)
client.settimeout(1)
messages = [
     "Hello",
     "How are you?",
     "UDP Test",
     "Networking",
     "Python",
     "Message 6",
     "Message 7",
     "Message 8",
     "Message 9",
     "Message 10"
]

total_packets = 0
retransmissions = 0
start = time.time()

for i, msg in enumerate(messages, start=1):
    packet = f"{i}|{msg}"
    while True:
       try:
            client.sendto(packet.encode(), (HOST, PORT))
            total_packets += 1

            data, addr = client.recvfrom(1024)
            ack = data.decode()
            if ack == f"ACK|{i}":
                 print(f"ACK received for Message {i}")
                 break
       except socket.timeout:
            retransmissions += 1
            print(f"Timeout! Retransmitting Message {i}")
client.sendto("END".encode(), (HOST,PORT))

end = time.time()
print("\nTOTAL_MESSAGES = 10")
print("TOTAL_PACKETS_SENT =", total_packets)
print("TOTAL_RETRANSMISSIONS =", retransmissions)
print(f"TRANSFER_TIME_SECONDS = {round(end - start, 2)}")
print("STATUS = SUCCESS")

client.close()






