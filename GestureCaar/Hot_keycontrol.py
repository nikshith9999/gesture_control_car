import cv2
import numpy as np
import socket
import keyboard  # pip install keyboard
import time

# IP and port of the ESP8266
UDP_IP = "192.168.137.144"     # Replace with your ESP8266 IP address
UDP_PORT = 4210

# Create UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Initialize OpenCV window
cv2.namedWindow("Hotkey Control")
blank_frame = 255 * np.ones((300, 400, 3), dtype=np.uint8)  # white dummy frame

print("Press W/A/S/D to control, Q to stop, Esc to exit.")

while True:
    # Show dummy video feed (just to keep window open and focused)
    cv2.imshow("Hotkey Control", blank_frame)

    key_pressed = None
    command = None

    if keyboard.is_pressed('w'):
        command = "1"  # Forward
        key_pressed = 'W'
    elif keyboard.is_pressed('a'):
        command = "2"  # Left
        key_pressed = 'A'
    elif keyboard.is_pressed('d'):
        command = "3"  # Right
        key_pressed = 'D'
    elif keyboard.is_pressed('s'):
        command = "4"  # Backward
        key_pressed = 'S'
    elif keyboard.is_pressed('q'):
        command = "0"  # Stop
        key_pressed = 'Q'

    if command:
        sock.sendto(command.encode(), (UDP_IP, UDP_PORT))
        print(f"Sent: {command} (Key: {key_pressed})")
        time.sleep(0.2)  # Small delay to avoid flooding commands

    # Exit on ESC key
    if cv2.waitKey(10) & 0xFF == 27:
        break

# Cleanup
cv2.destroyAllWindows()
sock.close()