#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>

const uint64_t pipe = 0xF0F1F2F3F4LL;

byte data[8];

RF24 radio(9, 10);

void setup() {
  Serial.begin(115200);
  radio.begin();
  delay(2);
  radio.setChannel(11);
  radio.setDataRate(RF24_1MBPS);
  radio.setPALevel(RF24_PA_HIGH);
  radio.setAutoAck(1);
  radio.stopListening();
  radio.openWritingPipe(pipe);
}

void loop() {
  if (Serial.available() > 0) {
    delay(2);
    Serial.readBytes(data, sizeof(data));
    while (Serial.available()) {
      byte g = Serial.read();
    }
    for (int i = 0; i < 8; i++) {
      Serial.print(data[i]);
    }
    Serial.println();
    radio.write(data, sizeof(data));
    delay(20);
  }
}
