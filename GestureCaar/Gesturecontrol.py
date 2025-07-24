import cv2
import mediapipe as mp
import socket

# UDP settings
UDP_IP = "192.168.137.124"  # Replace with ESP8266's IP address
UDP_PORT = 4210
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# Start video capture
cap = cv2.VideoCapture(0)  # Use 0 for default webcam

def count_fingers(hand_landmarks):
    # Get finger landmarks
    landmarks = hand_landmarks.landmark
    fingers = 0
    
    # Thumb (tip higher than joint)
    if landmarks[4].x < landmarks[3].x:  # Adjust for hand orientation
        fingers += 1
    # Index, Middle, Ring, Pinky
    finger_tips = [8, 12, 16, 20]
    finger_joints = [6, 10, 14, 18]
    for tip, joint in zip(finger_tips, finger_joints):
        if landmarks[tip].y < landmarks[joint].y:
            fingers += 1
    
    return fingers

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    
    # Flip frame for mirror effect
    frame = cv2.flip(frame, 1)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Process frame with MediaPipe
    results = hands.process(frame_rgb)
    
    command = None
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            fingers = count_fingers(hand_landmarks)
            
            # Map finger count to commands
            if fingers == 0:  # Fist
                command = "0"
                cv2.putText(frame, "Stop", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            elif fingers == 1:
                command = "1"
                cv2.putText(frame, "Forward", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            elif fingers == 2:
                command = "2"
                cv2.putText(frame, "Left", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            elif fingers == 3:
                command = "3"
                cv2.putText(frame, "Right", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            elif fingers == 4:
                command = "4"
                cv2.putText(frame, "Backward", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    
    # Send command to ESP8266
    if command:
        sock.sendto(command.encode(), (UDP_IP, UDP_PORT))
    
    # Display frame
    cv2.imshow("Hand Gesture Control", frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()
hands.close()
sock.close()