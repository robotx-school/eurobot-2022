#include "GyverStepper.h"
#include <math.h>

GStepper< STEPPER2WIRE> stepperLeft(800, 5, 2, 8);
GStepper< STEPPER2WIRE> stepperRight(800, 6, 3, 8);

/*Config*/
const int SERIAL_DBG = true; //Use serial printing for displaying info
int robot_max_speed = 1000;
/*Config end*/

/*Other variables*/
int curr_x = 151, curr_y = 455, robot_vect_x, robot_vect_y, robot_vect, robot_vect_1, point_vect, point_vect_1;
float dist, angle; 
int robot_size = 50;
int WAY_SIZE = 6;
int SIDE = 0;
/* Struct: point_x, point_y, action_after_step, trigger(interruption) */
/*int dest_points[8][4] = {{247, 548, 0, 0},
                        {318, 469, 1, 0},
                        {48, 84, 0, 0},
                        {451, 106, 0, 1},//Zone 0 if clear zone
                        {451, 591, 0, 0},
                        {-2, -2, -2, -2},
                        {603, 198, 0, 0}, //Zone 1 if zone not clear
                        {-1, -1, 0, 0}};*/
int dest_points[3][4] = {{753, 455, 0, 0}, {151, 455, 0, 0}, {-1, -1, 0, 0}};
bool finish = false;
int curr_point_ind = 0;
int motor_step, motor_step_1; //Left and Right
int motors_queue = -2; //queue for staright after rotation
int rotation_dist;
const int one_degree_rot = 12.3; 
float one_px = 1.625; // virtual field width / real field width
bool cam_data = false;
byte leftMoving, rightMoving;

/*Other variables end*/
/*Actions
0 - no action
1 - action_1
2 - action_2
3 - wait camera
//While actions
4 - while not data
*/
/*Functions*/

//Structs for returning
struct paired
{
   int a, b;
};
struct paired_float
{
   float a, b;
};

void action_1(){
  Serial.println("Performing action 1; Getting objects");
}

void action_2(){
  Serial.println("Performing action 2; Dropping objects");
}

bool check_cam(){
  return cam_data;
}
//This function converts millimeters to step
int millimeters_to_steps(int mm) {
  return mm * 9.52381;
}

//This function converts radians to degrees| already in math.h library
//float degrees(float radian){
//    return radian * (180 / 3.14159265359);
//}

//Calculate vect coordinates from 4 points(start and finish)
struct paired vect_from_4points(int x, int y, int x1, int y1){
    struct paired tmp = {x1 - x, y1 - y};
    return tmp;
}

//Calculate angle between two vectors
float angle_between_2vectors(float ax, float ay, float bx, float by){
    return degrees(atan2(ax * by - ay * bx, ax * bx + ay * by));
}


struct paired_float calculate_path_to_point(int point[2]){
    
    struct paired tmp = vect_from_4points(curr_x, curr_y, robot_vect_x, robot_vect_y);
    robot_vect = tmp.a;
    robot_vect_1 = tmp.b;
    struct paired tmp_2 = vect_from_4points(curr_x, curr_y, point[0], point[1]);
    point_vect = tmp_2.a;
    point_vect_1 = tmp_2.b;

    angle = angle_between_2vectors(robot_vect, robot_vect_1, point_vect, point_vect_1);
    dist = one_px * sqrt(pow(curr_x - point[0], 2) + pow(curr_y - point[1], 2));

    curr_x = point[0];
    curr_y = point[1];
    robot_vect_x = point[0] + point_vect / 5; 
    robot_vect_y = point[1] + point_vect_1 / 5;
    //Serial.println(dist);
    //Serial.println(angle);
    struct paired_float ret = {angle, dist};
    return ret;
}

void recreate_path_side(){
  //Use global array with coords
  //Use for right side
  for (int i = 0; i < WAY_SIZE; i++){
    dest_points[i][0] = 903 - dest_points[i][0];
    dest_points[i][1] = dest_points[i][1];
  }
}

void nextStep(){
  if (motors_queue == -1 || motors_queue == -2){
      //Serial.print("Executing step: ");
      //Serial.println(curr_point_ind);
      if (dest_points[curr_point_ind - 1][2] != 0 && curr_point_ind != 0){
        switch(dest_points[curr_point_ind - 1][2])
        {
          case 1:
            action_1();
            break;
          case 2:
            action_2();
            break;
        }
      }
      if (dest_points[curr_point_ind - 1][3] != 0 && curr_point_ind != 0){
        switch(dest_points[curr_point_ind - 1][3])
        {
          case 1:
            if (check_cam()){
              Serial.print("Driving to zone 0");
            }else{
              Serial.println("Driving to zone 1");
              curr_point_ind = 6;
            }
            break;
        }
      }
      struct paired_float curr = calculate_path_to_point(dest_points[curr_point_ind]);
      angle = curr.a;
      //Serial.println(curr.b);
      dist = millimeters_to_steps(curr.b);
      motor_step = dist; motor_step_1 = dist;
      if (round(angle) == 0){
          angle = 0;
          curr_point_ind++;
      }else{
          rotation_dist = one_degree_rot * angle;
          
          motor_step = rotation_dist; motor_step_1 = rotation_dist;
          
          if (angle > 0)
              motor_step *= -1;
          else
              motor_step_1 *= -1;
          //Add straight to queue
          motors_queue = abs(dist);
      }
       //Distance
      //Motors with motor_step and motor_step_1
      Serial.println(motor_step);
      Serial.println(motor_step_1);
      stepperRight.setTarget(motor_step, RELATIVE);
      stepperLeft.setTarget(motor_step_1, RELATIVE);
      
  }else{
      Serial.println(motors_queue);
      Serial.println(motors_queue);
      //Motors with dist and dist
      stepperRight.setTarget(motors_queue, RELATIVE);
      stepperLeft.setTarget(motors_queue, RELATIVE);
      motors_queue = -1;
      curr_point_ind++;
  }

}


/*Functions end*/

void setup() {
  if (SERIAL_DBG) {
    Serial.begin(115200);
  }
  //Check side and regen array and robot coords
  if (SIDE){
      robot_size = -1 * robot_size;
      curr_x = 903 - curr_x;
      recreate_path_side();
  }

  //Start
  robot_vect_x = curr_x + robot_size;
  robot_vect_y = curr_y;


  stepperLeft.setRunMode(FOLLOW_POS);
  stepperRight.setRunMode(FOLLOW_POS);
  stepperLeft.setMaxSpeed(robot_max_speed);
  stepperRight.setMaxSpeed(robot_max_speed);
  stepperLeft.setAcceleration(300);
  stepperRight.setAcceleration(300);
  stepperLeft.autoPower(0);
  stepperRight.autoPower(0);

  Serial.print("One px in mms: ");
  Serial.println(one_px);


  if (SERIAL_DBG) {
    Serial.print("Debug: ");
    Serial.println("Motors initialized - OK");
  }
  //Coolibration
  
  Serial.print("One px in millimeters: ");
  Serial.println(one_px, 10);


}


void loop() {
  if (!leftMoving and !rightMoving and !finish) {
    if (dest_points[curr_point_ind][0] != -1){
      nextStep();
    }else{
      Serial.println("Finish; Stopping");
      stepperLeft.brake();
      stepperRight.brake();
      stepperLeft.disable();
      stepperRight.disable();
      while (1)
      {
        delay(10000);
      }
        
    }
    
  }
  leftMoving = stepperLeft.tick();
  rightMoving = stepperRight.tick();
  
}
