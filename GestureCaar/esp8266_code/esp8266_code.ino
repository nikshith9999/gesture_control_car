#include <ESP8266WiFi.h>
#include <WiFiUdp.h>

const char* ssid = " ";     // Replace with your Wi-Fi SSID
const char* password = " "; // Replace with your Wi-Fi password

unsigned int udpPort = 4210; 
WiFiUDP udp;

// Motor driver pins (GPIO numbers for ESP8266, e.g., NodeMCU)
const int motorLeftA = 14;   // GPIO14 (D5 on NodeMCU) - Left motors forward (IN1 on L298N)
const int motorLeftB = 12;   // GPIO12 (D6 on NodeMCU) - Left motors backward (IN2 on L298N)
const int motorRightA = 13;  // GPIO13 (D7 on NodeMCU) - Right motors forward (IN3 on L298N)
const int motorRightB = 15;  // GPIO15 (D8 on NodeMCU) - Right motors backward (IN4 on L298N)
const int enableLeft = 5;    // GPIO5 (D1 on NodeMCU) - Left motors enable (ENA on L298N)
const int enableRight = 4;   // GPIO4 (D2 on NodeMCU) - Right motors enable (ENB on L298N)

void setup() {
  // Initialize Serial for debugging
  Serial.begin(115200);
  
  // Set motor pins as outputs
  pinMode(motorLeftA, OUTPUT);
  pinMode(motorLeftB, OUTPUT);
  pinMode(motorRightA, OUTPUT);
  pinMode(motorRightB, OUTPUT);
  pinMode(enableLeft, OUTPUT);
  pinMode(enableRight, OUTPUT);
  
  // Set initial motor state to OFF
  digitalWrite(motorLeftA, LOW);
  digitalWrite(motorLeftB, LOW);
  digitalWrite(motorRightA, LOW);
  digitalWrite(motorRightB, LOW);
  analogWrite(enableLeft, 0);
  analogWrite(enableRight, 0);
  
  // Connect to Wi-Fi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWiFi connected");
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());  // Print IP to use in Python script
  
  // Start UDP server
  udp.begin(udpPort);
  Serial.printf("UDP server started on port %d\n", udpPort);
}

void loop() {
  // Check for incoming UDP packets
  int packetSize = udp.parsePacket();
  if (packetSize) {
    char packetBuffer[255];  // Buffer for incoming data
    int len = udp.read(packetBuffer, 255);
    if (len > 0) {
      packetBuffer[len] = 0;  // Null-terminate the string
    }
    Serial.print("Received command: ");
    Serial.println(packetBuffer);

    // Process commands
    if (strcmp(packetBuffer, "0") == 0) {
      // Stop
      digitalWrite(motorLeftA, LOW);
      digitalWrite(motorLeftB, LOW);
      digitalWrite(motorRightA, LOW);
      digitalWrite(motorRightB, LOW);
      analogWrite(enableLeft, 0);
      analogWrite(enableRight, 0);
      Serial.println("Action: Stop");
    } else if (strcmp(packetBuffer, "1") == 0) {
      // Forward
      digitalWrite(motorLeftA, HIGH);
      digitalWrite(motorLeftB, LOW);
      digitalWrite(motorRightA, HIGH);
      digitalWrite(motorRightB, LOW);
      analogWrite(enableLeft, 255);  // Full speed (adjust 0-255 for PWM)
      analogWrite(enableRight, 255);
      Serial.println("Action: Forward");
    } else if (strcmp(packetBuffer, "2") == 0) {
      // Left
      digitalWrite(motorLeftA, LOW);
      digitalWrite(motorLeftB, HIGH);
      digitalWrite(motorRightA, HIGH);
      digitalWrite(motorRightB, LOW);
      analogWrite(enableLeft, 255);
      analogWrite(enableRight, 255);
      Serial.println("Action: Left");
    } else if (strcmp(packetBuffer, "3") == 0) {
      // Right
      digitalWrite(motorLeftA, HIGH);
      digitalWrite(motorLeftB, LOW);
      digitalWrite(motorRightA, LOW);
      digitalWrite(motorRightB, HIGH);
      analogWrite(enableLeft, 255);
      analogWrite(enableRight, 255);
      Serial.println("Action: Right");
    } else if (strcmp(packetBuffer, "4") == 0) {
      // Backward
      digitalWrite(motorLeftA, LOW);
      digitalWrite(motorLeftB, HIGH);
      digitalWrite(motorRightA, LOW);
      digitalWrite(motorRightB, HIGH);
      analogWrite(enableLeft, 255);
      analogWrite(enableRight, 255);
      Serial.println("Action: Backward");
    }
  }
}