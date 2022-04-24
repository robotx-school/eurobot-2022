#include <Servo.h>
#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>
#include <microLED.h>

#define STRIP_PIN 2
#define NUMLEDS 25

microLED<NUMLEDS, STRIP_PIN, MLED_NO_CLOCK, LED_WS2818, ORDER_GRB, CLI_AVER> led;
const uint64_t pipe = 0xF1F1F1F1F1LL;
RF24 radio(9, 10); // CE, CSNF1
byte data[9];
uint32_t timer;
uint8_t mode = 0;
uint8_t numLed = 0;
uint8_t hsv = 0;
uint8_t dir = 1;
uint8_t hsvDir = 1;


void setup() {
  pinMode(2, OUTPUT);
  led.setBrightness(255);
  for (int i = 0; i <= NUMLEDS - 1; i++) {
    led.leds[i] = mHSV(i, 0, 0);
  }
  led.show();
  Serial.begin(115200);
  radio.begin();
  delay(2);
  radio.setChannel(90); // канал (0-127)
  radio.setDataRate(RF24_1MBPS);
  radio.setPALevel(RF24_PA_HIGH);
  radio.openReadingPipe(1, pipe);
  radio.startListening();
}

void loop()
{

  if (radio.available()) {

    radio.read(&data, sizeof(data));
    if (data[8] == 0) {
      mode = 1;
    }
  }
  if (mode and millis() - timer > 10) {
    led.leds[numLed] = mHSV(hsv, 255, 255);
    led.show();
    timer = millis();
    /*
      if (numLed<24) numLed++;
      else numLed=0;
      hsv++;
    */

    if (dir) numLed++;
    else numLed--;
    if (numLed == 24 or numLed == 0) dir = !dir;
    
    if (hsvDir) hsv++;
    else hsv--;
    if (hsv == 180 or hsv == 0) hsvDir = !hsvDir;

  }
}
