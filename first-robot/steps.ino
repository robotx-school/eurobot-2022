#include <RF24_config.h>
#include <RF24.h>
#include <printf.h>
#include <nRF24L01.h>
#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>
#include "GyverStepper.h"
#include <Servo.h>
#define COLOR_DEBTH 3
#define STRIP_PIN 8
#define NUMLEDS 1
#define SIDE_PIN 4
#define STARTER_PIN 7
#define FRONT_PIN 1
#define DIST1_PIN A6
#define DIST2_PIN A7


GStepper< STEPPER2WIRE> stepperLeft(800, 5, 2, 8);
GStepper< STEPPER2WIRE> stepperRight(800, 6, 3, 8);

//Servos
Servo servo;
Servo servo_1;
Servo servo_2;
Servo servo_3;

const uint64_t pipe = 0xF1F1F1F1F1LL;
RF24 radio(9, 10); // CE, CSNsteps_match_blue[stepcounter][2] == 100
byte matchStarted = 0;
byte readyToStart = 0;
byte returnMode = 0;
byte flagOpened = 0;
uint32_t stopTimer = 0;
uint32_t matchTimer = 0;
uint8_t stopMode = 0;
uint32_t flagTimer = 0;
uint32_t stepTimer = 0;
int targetLeft;
int targetRight;
byte leftMoving;
byte rightMoving;
byte mooring = 0;

const int open_servo_0 = 180;
const int close_servo_0 = 15;
const int open_servo_1 = 0;
const int close_servo_1 = 173;

byte dalnomerOn = 1;
byte side = 0;
int stepcounter = -1;
int rotation = 4320; //Deprecated
int one_degree = 12.999; 
byte data[9];
uint32_t timer;
Servo steering;
int steeringpos = 90;
int sp, spL, spR;
int set_current_side = 0;


/*
   0  - шаг до нажатия переднего выключателя, не учитывать передние дальномеры
   1  - шаг без учета передних дальномеров
   2  - шаг с переходом к следующему по таймеру stepTimer
   3  - шаг с ожиданием изменения значения переменной mooring. ждем данных с компаса
   4  - шаг с переходом на 70 шаг, если швартовка на S
   25 - изменение колёс местами

*/  

int mms(int mm)
{
  return mm * 9.52381;
}
// 1000 шагов - 105 мм
int steps_match_blue[50][4] =
{
  {0, 0, 1, 10},
  {mms(350),mms(350),1, 0},
  {one_degree * 92, -one_degree * 92, 1, 0},
  {mms(725), mms(725), 1, 0},
  {one_degree * 50, -one_degree * 50, 1, 4},
  {mms(255), mms(255), 1, 5},
  {0, 0, 1, 7},
  {-mms(110), -mms(110), 1, 0},
  {-one_degree * 185, one_degree * 185, 1, 0},
  {-mms(300), -mms(300), 1, 6},
  {0, 0, 1, 7}, 
  {mms(300), mms(300), 1, 0},
  {-one_degree * 79, one_degree * 79, 1, 0},
  {mms(500), mms(500), 1, 0},
  {one_degree * 30, -one_degree * 30, 1, 0},
  {mms(950), mms(950), 1, 4},
  {0, 0, 1, 7}, 
  {0, 0, 1, 9},
  {-500, -500, 1, 0},
  {0, 0, 1, 12},
  {560, 560, 1, 0},
  {-mms(150), -mms(150), 1, 0},
  {0, 0, 1, 5},
  {one_degree * 90, -one_degree * 90, 1, 0},
  {-mms(300), -mms(300), 1, 0},
  {mms(940), mms(940), 1, 0},
  {one_degree * 121, -one_degree * 121, 1, 3}, 
  {mms(1600), mms(1600), 200, 0}, //drop
  {-mms(200), -mms(200), 1, 8},
  {mms(300), mms(300), 1, 0},
  {-mms(200), -mms(200), 1, 8},
  {-one_degree * 180, one_degree * 180, 1, 2},
  {-one_degree * 45, one_degree * 45, 1, 0},
  {mms(760), mms(760), 1, 0},
  {one_degree * 90, -one_degree * 90, 1, 0},
  {mms(660), mms(660), 1, 0},
  {one_degree * 121, -one_degree * 121, 1, 3},
  {mms(1380), mms(1380), 1, 0},
  {-mms(200), -mms(200), 1, 8},
  {mms(350), mms(350), 1, 0},
  {-mms(200), -mms(200), 1, 0},
  {-one_degree * 250, one_degree * 250, 1, 0},
  {mms(560), mms(560), 1, 0}
  
  
 };

int steps_match_yellow[35][4];

void action_1(){
  //Открыть серво для сбора фишек
  Serial.println("Performing action 1; Opening");
  servo.write(open_servo_0);
  servo_1.write(open_servo_1);
}

void action_2(){
  //Закрыть серво для сбора фишек
  Serial.println("Performing action 2; Closing");
   servo.write(close_servo_0);
  servo_1.write(close_servo_1);
}

void action_3(){
  //Серво среднее положение
  Serial.println("Performing action 3; Middle");
   servo.write(120);
   servo_1.write(close_servo_1 / 2);
}

void action_4(){
  //Серво для подъёма статуи(опускаем)
  Serial.println("Performing action 4; statue servo 0");
  servo_2.write(90);
}

void action_5(){
  //Серво для подъёма статуи, поднимаем
  Serial.println("Action 5");
  for (int step_u = 105; step_u >= 0; step_u--){
    servo_2.write(step_u);
    delay(10);
  }
  
}
void action_6(){
  Serial.println("Action 6");
  for (int i = 100; i >= 0; i--){
    servo_3.write(i);
    delay(10);
  }
  
  
}

void action_send_signal(){
  Send9ziro(); //Send drop statue signal
}
void action_7(){
  //Wait
  delay(1300);
}

void action_8(){
  servo.write(60);
  servo_1.write(130);
}

void action_tolk(){
  servo_2.write(160);
}
//Extra useful functions(NOT INITED in switch/case)

void change_speed(int left_motor_speed, int right_motor_speed){
    //How to use this params inside way init?????
    //We need to develop a new way architecture
    stepperLeft.setMaxSpeed(left_motor_speed);
    stepperRight.setMaxSpeed(right_motor_speed);
}




void Send9ziro(){
  byte _[9];
  radio.setChannel(10);
  radio.setDataRate(RF24_1MBPS);
  radio.setPALevel(RF24_PA_HIGH);
  radio.setAutoAck(1);
  radio.stopListening();
  radio.openWritingPipe(pipe);
  _[8] = 0;
  radio.write(&_, sizeof(_));
  radio.setChannel(10); // канал (0-127)
  radio.setDataRate(RF24_1MBPS);
  radio.setPALevel(RF24_PA_HIGH);
  radio.openReadingPipe(1, pipe);
  radio.startListening();
}


void setup() {
  pinMode(SIDE_PIN, INPUT_PULLUP);
  pinMode(STARTER_PIN, INPUT_PULLUP);
  
  /*
  pinMode(SIDE_PIN, INPUT_PULLUP);
  pinMode(STARTER_PIN, INPUT_PULLUP);
  pinMode(DIST1_PIN, INPUT_PULLUP);
  pinMode(DIST2_PIN, INPUT_PULLUP);
  pinMode(FRONT_PIN, INPUT_PULLUP);
  */
  Serial.begin(9600);
  
  //steering.attach(6);
  radio.begin();
  delay(2);
  radio.setChannel(10); // канал (0-127)
  radio.setDataRate(RF24_1MBPS);
  radio.setPALevel(RF24_PA_HIGH);
  radio.openReadingPipe(1, pipe);
  radio.startListening();

  //Servo init
  servo_2.attach(A2);
  servo.attach(A1);
  servo_1.attach(A0);
  servo_3.attach(A3);
  
  //Prepare servos; close them
  servo.write(close_servo_0);
  servo_1.write(close_servo_1);
  servo_2.write(0);
  servo_3.write(100);
  //action_6();
  
  
  //Steppers
  stepperLeft.setRunMode(FOLLOW_POS);
  stepperRight.setRunMode(FOLLOW_POS);
  stepperLeft.setMaxSpeed(70);
  stepperRight.setMaxSpeed(70);
  stepperLeft.setAcceleration(0);
  stepperRight.setAcceleration(0);
  stepperLeft.autoPower(0);
  stepperRight.autoPower(0);

  //Test motors
  //stepperRight.setTarget(100, RELATIVE);
  //stepperLeft.setTarget(100, RELATIVE);
  
  //digitalRead(SIDE_PIN) == 0
  if (digitalRead(SIDE_PIN) == 0) { // Another side
    side = 1;
    for (int step = 0; step <= 44; step++){
        //We need to change only rotations
        if(steps_match_blue[step][0] < 0 || steps_match_blue[step][1] < 0){
            if (step == 2){
              steps_match_blue[2][0]  = -one_degree * 93;
              steps_match_blue[2][1]  = one_degree * 93;
            }else if(step == 3){
              steps_match_blue[3][0]  = 715;
              steps_match_blue[3][1]  = 715;
            }else if(step == 8){
              steps_match_blue[8][0]  = one_degree * 175;
              steps_match_blue[8][1]  = -one_degree * 175;
            }else if (step == 25){
              steps_match_blue[25][0]  = mms(940);
              steps_match_blue[25][1]  = mms(940);
            }else if (step == 26){
              steps_match_blue[26][0]  = -one_degree * 119;
              steps_match_blue[26][1]  = one_degree * 119;
            } else if(step == 36){
              steps_match_blue[36][0]  = -one_degree * 130;
              steps_match_blue[36][1]  = one_degree * 130;
            }else{
              if (!(steps_match_blue[step][0] < 0 && steps_match_blue[step][1] < 0)){ 
                 steps_match_blue[step][0]  = -steps_match_blue[step][0];
                 steps_match_blue[step][1] = -steps_match_blue[step][1];
              }
            }
            
        }
    }

    /*
    Serial.println("Another side");
    side = 0;
    for (int i = 0; i <= 99; i++) {
    if (!steps_match_blue[i][0] and !steps_match_blue[i][1] and !steps_match_blue[i][2] ) break;
      
      if ( (steps_match_blue[i][0]>0 and steps_match_blue[i][1]<0) or (steps_match_blue[i][0]<0 and steps_match_blue[i][1]>0) ) {
        steps_match_yellow[i][0] = -steps_match_blue[i][0];
        steps_match_yellow[i][1] = -steps_match_blue[i][1];
        
      } else if (steps_match_blue[i][2] == 25){
        steps_match_yellow[i][0] = steps_match_blue[i][1];
        steps_match_yellow[i][1] = steps_match_blue[i][0];
      }else {
        steps_match_yellow[i][0] = steps_match_blue[i][0];
        steps_match_yellow[i][1] = steps_match_blue[i][1];
        
      }
      steps_match_yellow[i][2] = steps_match_blue[i][2];
  }
  for (int i = 71; i <= 99;i++) {
    if (!steps_match_blue[i][0] and !steps_match_blue[i][1] and !steps_match_blue[i][2] ) break;
      
      if ( (steps_match_blue[i][0]>0 and steps_match_blue[i][1]<0) or (steps_match_blue[i][0]<0 and steps_match_blue[i][1]>0) ) {
        steps_match_yellow[i][0] = -steps_match_blue[i][0];
        steps_match_yellow[i][1] = -steps_match_blue[i][1];
        
      } else if (steps_match_blue[i][2] == 25){
        steps_match_yellow[i][0] = steps_match_blue[i][1];
        steps_match_yellow[i][1] = steps_match_blue[i][0];
      }else {
        steps_match_yellow[i][0] = steps_match_blue[i][0];
        steps_match_yellow[i][1] = steps_match_blue[i][1];
        
      }
      steps_match_yellow[i][2] = steps_match_blue[i][2];
  }*/
  } else {
    side = 1;
  }
}


void nextStep() {
  stepTimer = millis();
  stepperRight.setCurrent(0);
  stepperLeft.setCurrent(0);
  stepcounter++;
  if (!(side ? steps_match_blue[stepcounter][0] : steps_match_yellow[stepcounter][0]) &&
      !(side ? steps_match_blue[stepcounter][1] : steps_match_yellow[stepcounter][1]) &&
      !(side ? steps_match_blue[stepcounter][2] : steps_match_yellow[stepcounter][2])) {
    stepperRight.disable();
    stepperLeft.disable();
    stopMode = 1;
    
  } else {
    stepperLeft.setTarget((side?steps_match_blue[stepcounter][0]:steps_match_yellow[stepcounter][0]), RELATIVE);
    stepperRight.setTarget((side?steps_match_blue[stepcounter][1]:steps_match_yellow[stepcounter][1]), RELATIVE);
  }
  if (steps_match_blue[stepcounter - 1][3] != 0){
    switch(steps_match_blue[stepcounter - 1][3])
      {
        case 1:
          action_1();
          break;
        case 2:
          action_2();
          break;
        case 3:
          action_3();
          break;
        case 4:
          action_4();
          break;
        case 5:
          action_5();
          break;
        case 6:
          action_6();
          break;
        case 7:
          action_7();
          break;
        case 8:
          action_8();
          break;
        case 9:
          action_send_signal(); 
          break;
        case 10:
          //Speedup
          change_speed(2500, 2500);
          break;
        case 11:
          //Less speed 
          change_speed(2200, 2200);
          break;
        case 12:
           action_tolk();
           break;
      }
  }
}
void match() {
  if ( (side?steps_match_blue[(stepcounter<0?0:stepcounter)][2]:steps_match_yellow[(stepcounter<0?0:stepcounter)][2]) == 0) {
    if (digitalRead(FRONT_PIN) == 0) {
      nextStep();
    }
  } else if ( (side?steps_match_blue[(stepcounter<0?0:stepcounter)][2]:steps_match_yellow[(stepcounter<0?0:stepcounter)][2]) == 2) {
    if (millis()-stepTimer>5000) {
      nextStep();
    }
  } else if ( (side?steps_match_blue[(stepcounter<0?0:stepcounter)][2]:steps_match_yellow[(stepcounter<0?0:stepcounter)][2]) == 3) {
    /*if (mooring) {
      //Отправляем данные о швартовке на второго робота
      for (int i=0;i<=10;i++) radio.write(&mooring, sizeof(mooring));
      //
      nextStep();
    } else if (millis()-stepTimer>5000) {
      mooring=1;
      //Отправляем данные о швартовке на второго робота
      for (int i=0;i<=10;i++) radio.write(&mooring, sizeof(mooring));
      //
      nextStep();
    }*/
  }else if ( (side?steps_match_blue[(stepcounter<0?0:stepcounter)][2]:steps_match_yellow[(stepcounter<0?0:stepcounter)][2]) == 4) {
    if (mooring==1 and !leftMoving and !rightMoving) {
      stepcounter=70;
      nextStep();
    }else if (!leftMoving and !rightMoving)
      nextStep();
  } else {
    if (!leftMoving and !rightMoving ) {
      if (returnMode) returnMode = 0;
      nextStep();
    }
  }

  if (leftMoving and rightMoving and !returnMode) {
        //Serial.println(analogRead(DIST1_PIN));
        /*if (dalnomerOn and (digitalRead(DIST1_PIN) or digitalRead(DIST2_PIN)) and (side?steps_match_blue[stepcounter][2]:steps_match_yellow[stepcounter][2]) > 1) {
      stepperLeft.brake();
      stepperRight.brake();
      stepcounter--;
      returnMode = 1;
      stepperLeft.setTarget(-stepperLeft.getCurrent(), RELATIVE);
      stepperRight.setTarget(-stepperRight.getCurrent(), RELATIVE);
    }*/
    //steps_match_blue[stepcounter][2] == 100
    if (dalnomerOn and (analogRead(DIST1_PIN) > 600) and (steps_match_blue[stepcounter][2] == 100)) {
      
      stepperLeft.brake();
      stepperRight.brake();
      stepcounter--;
      returnMode = 1;
      stepperLeft.setTarget(-stepperLeft.getCurrent(), RELATIVE);
      stepperRight.setTarget(-stepperRight.getCurrent(), RELATIVE);
    }
    if (dalnomerOn and (analogRead(DIST2_PIN) > 600) and (steps_match_blue[stepcounter][2] == 100) ){
      stepperLeft.brake();
      stepperRight.brake();
      stepcounter--;
      returnMode = 1;
      stepperLeft.setTarget(-stepperLeft.getCurrent(), RELATIVE);
      stepperRight.setTarget(-stepperRight.getCurrent(), RELATIVE);
    }
  }
}

void loop()
{
   if (matchStarted){
    leftMoving = stepperLeft.tick();
    rightMoving = stepperRight.tick();
    //Serial.println("Tick");
   }

  /********************Когда робот запущен, выполняем программу********************/
  if (matchStarted and !stopMode) match();
  /********************Когда робот запущен, выполняем программу********************/

  if (!readyToStart and !matchStarted) {//только включили робота, ждем установки пускового шнура
    if (digitalRead(STARTER_PIN) == 0) {
      readyToStart = 1;
      Serial.println("Ready");
      delay(1000);
      
    }
  }
  if (readyToStart and !matchStarted) {//готов к старту ждем выдергивания шнура
    if (digitalRead(STARTER_PIN) == 1) {
      matchStarted = 1;
      Serial.println("matchStarted = 1");
      stepperLeft.setMaxSpeed(2200);
      stepperRight.setMaxSpeed(2200);
      stepperLeft.setAcceleration(1900);
      stepperRight.setAcceleration(1900);
      stepperLeft.enable();
      stepperRight.enable();
      matchTimer = millis();
      
    }
  }
  if (((millis() - matchTimer) > 9800000) and matchStarted) {//остановка робота в конце матча
    Serial.println("Finish");
    stepperLeft.brake();
    stepperRight.brake();
    stepperLeft.disable();
    stepperRight.disable();
    while (1) {
      delay(100000);
    }
  }
  if (leftMoving and rightMoving ) {
    stopTimer = millis(); //когда моторы двигаются обновляем таймер
  }
}
