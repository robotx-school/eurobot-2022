/* First Robot Code 
 * Robot tasks: 
 * Robot first tasks: check distance between itself and other robots, if it is too low, than stop else decrease speed;
*/

#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>
#include "GyverStepper.h"
#include <Servo.h>
#include <microLED.h>
#define NUMLEDS 1
#define STRIP_PIN 8

GStepper< STEPPER2WIRE> stepperLeft(800, A3, A4, A5);
GStepper< STEPPER2WIRE> stepperRight(800, A0, A1, A2);
microLED<NUMLEDS, STRIP_PIN, MLED_NO_CLOCK, LED_WS2818, ORDER_GRB, CLI_AVER> led;

/*Config*/
const uint64_t pipe = 0xF0F1F2F3F4LL;
RF24 radio(9, 10);
const int robot_id = 0; //Number of the robot(can be 0 - our first robot, or 1 - our second robot)
const int LEDS = true; //Use leds for displaying info
const int SERIAL_DBG = true; //Use serial printing for displaying info
int robot_colors[2] = {mBlue, mYellow}; //if LEDS = true after switching on, a light on the led indicator lights up depending on the number of the robot
int robot_max_speed = 700;
int robot_warning_speed = 100;
const int radio_channel = 11;
/*Config end*/

/*Other variables*/
byte data[8] = {255, 255, 255, 255, 255, 255, 255, 255};
byte return_data[16] = {255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255};
byte result_data[16] = {255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255};
int braked = false; //Is robot braked now
int stepTimer;
int stepcounter;
byte leftMoving;
byte rightMoving; 
int last_stop_time = 0;
/*Other variables end*/

/*Functions*/
int millimeters_to_steps(int mm) {
  //This function converts millimeters to step
  return mm * 9.52381;
}


int get_status(byte* input_data) {
     float dist;
     for (int i = 0; i < 8; i++) {
         return_data[i * 2] = input_data[i] >> 4;
         return_data[i * 2 + 1] = input_data[i] & 0b00001111;
     } 
     int status = 0;
     switch (robot_id)
     {
        case 0:
            /*
             * Test debug for (int i = 0; i < 16; i++){
                Serial.print(return_data[i]);
                Serial.print(" ");
            }
            Serial.println(); */
            
            /*
            return_data[0] = 10;
            return_data[1] = 10;
            return_data[2] = 5;
            return_data[3] = 5; */
            
            
               
            for (int i = 4; i <= 15; i += 2) {
                 dist = sqrt(pow(return_data[0] - return_data[i], 2) + pow(return_data[1] - return_data[i + 1], 2));
                 if ((dist == 2) and (status != 2)) {
                     status = 1;
                 } else if (dist <= 1) {
                     status = 2;
                 }
             }
             if (return_data[2] != 15 and return_data[3] != 15) {
              
                for (int i = 4; i <= 15; i += 2) {
                   dist = sqrt(pow(return_data[2] - return_data[i], 2) + pow(return_data[3] - return_data[i + 1], 2));
                   if ((dist == 2) and (status != 2)) {
                       status = 1;
                   } else if (dist <= 1) {
                       status = 2;
                   }
                } 
             }
             if (dist == 0){
                status = 0;
             }
             Serial.print("Distance: ");
             Serial.println(dist);
             return status;
             break;
        case 1:
            /* 
            return_data[0] = 5;
            return_data[1] = 5;
            return_data[2] = 5;
            return_data[3] = 5;*/
            
            for (int i = 4; i <= 15; i += 2) {
                 int dist = sqrt(pow(return_data[4] - return_data[i], 2) + pow(return_data[5] - return_data[i + 1], 2));
                 if ((dist == 2) and (status != 2)) {
                     status = 1;
                 } else if (dist <= 1) {
                     status = 2;
                 }
             }
             if (return_data[2] != 15 and return_data[3] != 15) {
                for (int i = 4; i <= 15; i += 2) {
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
     
     return status;
}


/*Array of robot's way(IT IS NOT FUNCTION)
  Structure of 1 element: {steps_for_left_motor, steps_for_right_motor, action_type}
  Avaliable action_types:
      99 - just drive
*/
int steps_square[100][3] =
{
  {millimeters_to_steps(238),millimeters_to_steps(238),99},
  {-millimeters_to_steps(107),millimeters_to_steps(107),99},
  {millimeters_to_steps(238),millimeters_to_steps(238),99},
  {-millimeters_to_steps(107),millimeters_to_steps(107),99},
  {millimeters_to_steps(238),millimeters_to_steps(238),99},
  {-millimeters_to_steps(107),millimeters_to_steps(107),99},
  {millimeters_to_steps(238),millimeters_to_steps(238),99},
  {-millimeters_to_steps(107),millimeters_to_steps(107),99},
};

void nextStep() {
 
  if (braked != true){
    if (SERIAL_DBG){Serial.print("Debug: "); Serial.print("Next step: "); Serial.println(robot_id);}
    stepTimer = millis();
    stepperRight.setCurrent(0);
    stepperLeft.setCurrent(0);
    stepcounter++;
    
    // DEBUG FEATURE; REMOVE IN RELEASE !!!
    if (stepcounter == 8) {
      stepcounter = 0;  
    }
    //CODE ABOVE USED FOR TESTING / LOOPING ROBOT's WAY
    
    stepperLeft.setTarget(steps_square[stepcounter][0], RELATIVE);
    stepperRight.setTarget(steps_square[stepcounter][1], RELATIVE);
  }
}
/*Functions end*/

void setup() {
  if (SERIAL_DBG){Serial.begin(115200);}
  delay(2); //?
  radio.begin();
  radio.setChannel(11); // канал (0-127)
  radio.setDataRate(RF24_1MBPS);
  radio.setPALevel(RF24_PA_HIGH);
  radio.openReadingPipe(1, pipe);
  radio.startListening();
  
  if (SERIAL_DBG){Serial.print("Debug: "); Serial.println("Radio initialized - OK");}

  stepperLeft.setRunMode(FOLLOW_POS);
  stepperRight.setRunMode(FOLLOW_POS);
  stepperLeft.setMaxSpeed(robot_max_speed);
  stepperRight.setMaxSpeed(robot_max_speed);
  stepperLeft.setAcceleration(300);
  stepperRight.setAcceleration(300);
  stepperLeft.autoPower(0);
  stepperRight.autoPower(0);
  
  //Temp target
  stepperRight.setTarget(1000, RELATIVE);
  stepperLeft.setTarget(1000, RELATIVE);
  
  if (SERIAL_DBG){Serial.print("Debug: "); Serial.println("Motors initialized - OK");}

  if (LEDS){
    if (!robot_id){
      led.leds[0] = robot_colors[0];
      led.show();
    }else{
      led.leds[0] = robot_colors[1];
      led.show();
    }
  }
  if (SERIAL_DBG){Serial.print("Config: "); Serial.print("RobotID: "); Serial.println(robot_id);}
}


void loop() {
    if (radio.available()){
        radio.read(data, sizeof(data));
        if (not(data[0] == 255 && data[1] == 255 && data[2] == 255 && data[3] == 255 && data[4] == 255 && data[5] == 255 && data[6] == 255 && data[7] == 255)){
          led.leds[0] = 0;
          led.show();
          int status_result = get_status(data);
          Serial.println(status_result);
          switch (status_result){
              if (millis() - last_stop_time){
                case 0:
                    if(SERIAL_DBG){Serial.print("Debug: "); Serial.println("OK - No obstacles");}
                    stepperLeft.setMaxSpeed(robot_max_speed);
                    stepperRight.setMaxSpeed(robot_max_speed);
                    braked = false;
                    if (LEDS){ //Clear LEDS - No warnings
                      led.leds[0] = 0;
                      led.show();
                    }
                    break;
                
                case 1:
                    if(SERIAL_DBG){Serial.print("Debug: "); Serial.println("Warning - Less speed");}
                    stepperLeft.setMaxSpeed(robot_warning_speed);
                    stepperRight.setMaxSpeed(robot_warning_speed);
                    braked = false;
                    if (LEDS){ //Warning; low distance to another robot
                      led.leds[0] = mYellow;
                      led.show();
                    }
                    break;
                 
                case 2:
                    if(SERIAL_DBG){Serial.print("Debug: "); Serial.println("Alarm - Stop | Too low distance");}
                    last_stop_time = millis();
                    if (!braked)
                    {
                       stepperLeft.disable();
                       stepperRight.disable(); 
                       braked = true;
                       if (LEDS){
                        led.leds[0] = mRed;
                        led.show();
                       }
                    }
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
