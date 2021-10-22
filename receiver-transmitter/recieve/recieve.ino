#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>

const uint64_t pipe = 0xF0F1F2F3F4LL;

byte data[8] = {1, 1, 1, 1, 1, 1, 1, 1};
byte data_2[16];
int flag = 0;
RF24 radio(9, 10);

void setup() {
  Serial.begin(115200);
  radio.begin();
  delay(2);
  radio.setChannel(11); // канал (0-127)
  radio.setDataRate(RF24_1MBPS);
  radio.setPALevel(RF24_PA_HIGH);
  radio.openReadingPipe(1, pipe);
  radio.startListening();
}

void loop() {
  flag = 0;
  radio.read(data, sizeof(data));
  delay(20);
  for (int i = 0; i < 8; i++) {
    flag+=data[i];
  }
  if (flag > 0) {
//    for (int i = 0; i < 8; i++) {
//      Serial.print(data[i]);
//    }
    for (int i = 0; i < 8; i++) {
      data_2[i*2] = data[i] >> 4;
      data_2[i*2+1] = data[i] & 0b00001111;
    }
    for (int i = 0; i < 16; i++) {
      Serial.print(data_2[i]);
      Serial.print(" ");
    }
    Serial.println();
  }
}
