#include <DW1000.h>
#include <esp_now.h>
#include <WiFi.h>

#define BUZZER_PIN 2

void setup() {
  pinMode(BUZZER_PIN, OUTPUT);
  WiFi.mode(WIFI_STA);
  esp_now_init();
  esp_now_register_recv_cb(onReceiveData);
  DW1000.begin();
}

void loop() {
  DW1000.doRanging();
  // No need to handle button here—see callback
}

void onReceiveData(const uint8_t *mac, const uint8_t *data, int len) {
  if(*data == 0) {  // Button pressed
    playTune();
  }
}

void playTune() {
  for (int i = 0; i < 5; i++) {
    digitalWrite(BUZZER_PIN, HIGH);
    delay(100);
    digitalWrite(BUZZER_PIN, LOW);
    delay(100);
  }
}
