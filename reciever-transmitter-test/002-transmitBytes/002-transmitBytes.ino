#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>
const uint64_t pipe = 0xF0F1F2F3F4LL;
byte data[8];
RF24 radio(9, 10); // CE, CSN
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
  pinMode(2,INPUT_PULLUP);
  pinMode(3,INPUT_PULLUP);
}

void loop()
{
  for (byte i=0;i<=7;i++){
    data[i]=255;
  }
  data[0]=85;
  //Serial.print(digitalRead(2));
  //Serial.println(digitalRead(3));
  if (!digitalRead(2)) {
    data[4]=87;
  } else if (!digitalRead(3)){
    data[4]=102;
  } else {
    data[4]=255;
  }
  for (int i=0;i<=7;i++) {
    Serial.print(data[i]);
    Serial.print(" ");
  }
  Serial.println();
  radio.write(&data, sizeof(data));
  delay(100);
}
