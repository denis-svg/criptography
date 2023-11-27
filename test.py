import socket
import winsound

receiver_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
receiver_socket.bind(('0.0.0.0', 12345))
print("Waiting for broadcasts...")

def beep():
    winsound.Beep(1000, 1000)  # Beep at 1000 Hz for 200 milliseconds

try:
    while True:
        # data, address = receiver_socket.recvfrom(1024)
        # print(f"Received message from {address}: '{data.decode('utf-8')}'")
        beep()  # Call the function to make a beep sound
except KeyboardInterrupt:
    print("Receiver stopped.")
    receiver_socket.close()
