#include <Wire.h>            // For OLED
#include <SPI.h>             // For UWB
#include <DW1000.h>          // Ultra Wide Band library
#include <esp_now.h>         // ESP-NOW direct communication
#include <WiFi.h>            // ESP32 WiFi
#include <Adafruit_SSD1306.h>// OLED display
#include <SimpleTimer.h>     // Timer Library

#define BUTTON_PIN 0         // Pin for push button
Adafruit_SSD1306 display(128, 64, &Wire, -1);
SimpleTimer timer;

uint8_t receiverAddress[] = {0xFF,0xFF,0xFF,0xFF,0xFF,0xFF}; // Replace with actual MAC, if available

void setup() {
  pinMode(BUTTON_PIN, INPUT);
  WiFi.mode(WIFI_STA);
  esp_now_init();
  esp_now_add_peer(receiverAddress, ESP_NOW_ROLE_SLAVE, 1, NULL, 0);
  display.begin(SSD1306_SWITCHCAPVCC, 0x3C);
  DW1000.begin();
  timer.setInterval(2000, sendButtonStatus); // Every 2 seconds
}

void loop() {
  timer.run();
  DW1000.doRanging();
  float distance = DW1000.getDistance();
  display.clearDisplay();
  display.setCursor(0,0);
  display.print("Distance: ");
  display.print(distance);
  display.print(" m");
  display.display();
}

void sendButtonStatus() {
  uint8_t btnState = digitalRead(BUTTON_PIN);
  esp_now_send(receiverAddress, &btnState, sizeof(btnState));
}
