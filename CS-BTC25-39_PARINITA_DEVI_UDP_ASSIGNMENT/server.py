import socket

HOST = "10.0.0.1"
PORT = 5005

server = socket.socket(
    socket.AF_INET,
    socket.SOCK_DGRAM
    )
server.bind((HOST, PORT))

print("Server started...")
print("Waiting for messages...")

received = set()
duplicates = 0

while True:
    data, addr = server.recvfrom(1024)
    message = data.decode()
     
    if message == "END":
        break
    seq, text = message.split("|", 1)
    
    if seq in received:
        duplicates += 1
    else:
        received.add(seq)
    print(f"Received: {text}")
    ack = f"ACK|{seq}"
    server.sendto(ack.encode(), addr)
    
print("\nTOTAL_UNIQUE_MESSAGES_RECEIVED =", len(received))
print("TOTAL_DUPLICATES_DETECTED =", duplicates)
print("STATUS = SUCCESS")
server.close()
