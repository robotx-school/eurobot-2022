#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>
#include "GyverStepper.h"
#include <Servo.h>

/*#include <microLED.h>
#define NUMLEDS 1
#define STRIP_PIN 8*/

GStepper< STEPPER2WIRE> stepperLeft(800, A3, A4, A5);
GStepper< STEPPER2WIRE> stepperRight(800, A0, A1, A2);
//microLED<NUMLEDS, STRIP_PIN, MLED_NO_CLOCK, LED_WS2818, ORDER_GRB, CLI_AVER> led;

const uint64_t pipe = 0xF0F1F2F3F4LL;
RF24 radio(9, 10); // CE, CSN
byte data[8] = {255, 255, 255, 255, 255, 255, 255, 255};
byte return_data[16] = {255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255};
byte result_data[16] = {255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255};
int braked = false;
int stepTimer;
int stepcounter;
byte leftMoving;
byte rightMoving;
int robot_id = 0;
            
int mms(int mm) {
  return mm * 9.52381;
}

int steps_square[100][3] =
{
  {mms(238),mms(238),99},
  {-mms(107),mms(107),99},
  {mms(238),mms(238),99},
  {-mms(107),mms(107),99},
  {mms(238),mms(238),99},
  {-mms(107),mms(107),99},
  {mms(238),mms(238),99},
  {-mms(107),mms(107),99},
};


int get_status(byte* input_data) {
     for (int i=0; i<8; i++) {
         return_data[i * 2] = input_data[i] >> 4;
         return_data[i * 2 + 1] = input_data[i] & 0b00001111;
     } 
     
     
     int status = 0;
     switch (robot_id)
     {
        case 0:
            /*return_data[0] = 10;
            return_data[1] = 10;
            return_data[2] = 5;
            return_data[3] = 5;*/
            /*for (int i; i<=15; i++) {
               Serial.print(return_data[i]);
               Serial.print(" ");
            }
            Serial.println();*/
            
            for (int i=4; i<=15; i+=2) {
                 int dist = sqrt(pow(return_data[0] - return_data[i], 2) + pow(return_data[1] - return_data[i + 1], 2));
                 if ((dist == 2) and (status != 2)) {
                     status = 1;
                 } else if (dist <= 1) {
                     status = 2;
                 }
             }
             if (return_data[2] != 15 and return_data[3] != 15) {
                for (int i=4; i<=15; i+=2) {
                   int dist = sqrt(pow(return_data[2] - return_data[i], 2) + pow(return_data[3] - return_data[i + 1], 2));
                   if ((dist == 2) and (status != 2)) {
                       status = 1;
                   } else if (dist <= 1) {
                       status = 2;
                   }
                } 
             }
             return status;
             break;
        case 1:
            //return_data[0] = 5;
            //return_data[1] = 5;
            //return_data[2] = 5;
            //return_data[3] = 5;
            /*for (int i; i<=15; i++) {
               Serial.print(return_data[i]);
               Serial.print(" ");
            }
            Serial.println();*/
            
            for (int i=4; i<=15; i+=2) {
                 int dist = sqrt(pow(return_data[4] - return_data[i], 2) + pow(return_data[5] - return_data[i + 1], 2));
                 if ((dist == 2) and (status != 2)) {
                     status = 1;
                 } else if (dist <= 1) {
                     status = 2;
                 }
             }
             if (return_data[2] != 15 and return_data[3] != 15) {
                for (int i=4; i<=15; i+=2) {
                   int dist = sqrt(pow(return_data[6] - return_data[i], 2) + pow(return_data[7] - return_data[i + 1], 2));
                   if ((dist == 2) and (status != 2)) {
                       status = 1;
                   } else if (dist <= 1) {
                       status = 2;
                   }
                } 
             }
             return status;
             break;
     }
     
     //Serial.println(status);
     return status;
}


void setup() {
  //Serial.begin(115200);
  delay(2);
  radio.begin();
  radio.setChannel(11); // канал (0-127)
  radio.setDataRate(RF24_1MBPS);
  radio.setPALevel(RF24_PA_HIGH);
  radio.openReadingPipe(1, pipe);
  radio.startListening();

  stepperLeft.setRunMode(FOLLOW_POS);
  stepperRight.setRunMode(FOLLOW_POS);
  stepperLeft.setMaxSpeed(700);
  stepperRight.setMaxSpeed(700);
  stepperLeft.setAcceleration(300);
  stepperRight.setAcceleration(300);
  stepperLeft.autoPower(0);
  stepperRight.autoPower(0);
  
  stepperRight.setTarget(1000, RELATIVE);
  stepperLeft.setTarget(1000, RELATIVE);

  /*if (!robot_id){
      led.leds[0] = mBlue;
      led.show();
  }else{
      led.leds[0] = mYellow;
      led.show();
  }*/

}


void nextStep() {
 
  if (braked != true){
    //Serial.println("New Step");
    stepTimer=millis();
    stepperRight.setCurrent(0);
    stepperLeft.setCurrent(0);
    stepcounter++;
    if (stepcounter == 8) {
      stepcounter = 0;  
    }
    stepperLeft.setTarget(steps_square[stepcounter][0], RELATIVE);
    stepperRight.setTarget(steps_square[stepcounter][1], RELATIVE);
  }
}



void loop() {
    if (radio.available()){
        radio.read(data, sizeof(data));
        if (not(data[0] == 255 && data[1] == 255 && data[2] == 255 && data[3] == 255 && data[4] == 255 && data[5] == 255 && data[6] == 255 && data[7] == 255)){
          //Serial.println("not empty");
           
          int status_result = get_status(data);
          Serial.println(status_result);
          switch (status_result){
            
              case 0:
                //Serial.println("OK");
                stepperLeft.setMaxSpeed(700);
                stepperRight.setMaxSpeed(700);
                braked = false;
                //led.leds[0] = 0;
                //led.show();
                break;
              case 1:
                //Serial.println("Less speed");
                stepperLeft.setMaxSpeed(100);
                stepperRight.setMaxSpeed(100);
                braked = false;
                //led.leds[0] = mYellow;
                //led.show();
                break;
               
              case 2:
                if (!braked)
                {
                  
                   Serial.println(braked);
                   Serial.println("Stop");
                   stepperLeft.disable();
                   stepperRight.disable(); 
                   braked = true;
                   //led.leds[0] = mRed;
                   //led.show();
                   break;
                }    
          } 
        }        
    }
    leftMoving = stepperLeft.tick();
    rightMoving = stepperRight.tick();
    if (!leftMoving and !rightMoving ) {
      nextStep();
    }
}
