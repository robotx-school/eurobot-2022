#include "GyverStepper.h"
#include <math.h>

GStepper< STEPPER2WIRE> stepperLeft(800, A3, A4, A5);
GStepper< STEPPER2WIRE> stepperRight(800, A0, A1, A2);

/*Config*/
const int SERIAL_DBG = true; //Use serial printing for displaying info
int robot_max_speed = 1000;
/*Config end*/

/*Other variables*/
int curr_x = 0, curr_y = 0, robot_vect_x, robot_vect_y, robot_vect, robot_vect_1, point_vect, point_vect_1;
float dist, angle; 
int robot_size = 50;
int dest_points[4][2] = {{0, 100}, {100, 100}, {100, 0}, {0, 0}};

int curr_point_ind = 0;
float motor_step, motor_step_1; //Left and Right
float motors_queue = -2; //queue for staright after rotation
int rotation_dist;
const int one_degree_rot = 4255 / 360; 
const float one_px = 0.3035;
byte leftMoving, rightMoving;

/*Other variables end*/

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

//This function converts millimeters to step
int millimeters_to_steps(int mm) {
  return mm * 9.52381;
}

//This function converts radians to degrees| already in base library
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

    struct paired_float ret = {angle, dist};
    return ret;
}

void nextStep(){
  if (motors_queue == -1 || motors_queue == -2){
      struct paired_float curr = calculate_path_to_point(dest_points[curr_point_ind]);
      angle = curr.a;
      dist = millimeters_to_steps(curr.b);
      motor_step = dist; motor_step_1 = dist;
      if (round(angle) == 0){
          angle = 0;
          curr_point_ind++;
      }else{
          rotation_dist = abs(one_degree_rot * angle);
          motor_step = rotation_dist; motor_step_1 = rotation_dist;
          if (angle > 0)
              motor_step_1 *= -1;
          else
              motor_step *= -1;
          //Add straight to queue
          motors_queue = dist;
      }
      //Motors with motor_step and motor_step_1
      //cout << motor_step << " " << motor_step_1 << endl;
      stepperRight.setTarget(motor_step, RELATIVE);
      stepperLeft.setTarget(motor_step_1, RELATIVE);
      
  }else{
      //Motors with dist and dist
      stepperRight.setTarget(motors_queue, RELATIVE);
      stepperLeft.setTarget(motors_queue, RELATIVE);
      motors_queue = -1;
      curr_point_ind++;
  }
  if (curr_point_ind > 4){
    curr_point_ind = 0;
  }
}


/*Functions end*/

void setup() {
  if (SERIAL_DBG) {
    Serial.begin(115200);
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


  if (SERIAL_DBG) {
    Serial.print("Debug: ");
    Serial.println("Motors initialized - OK");
  }

}


void loop() {
  if (!leftMoving and !rightMoving ) {
    nextStep();
  }
  leftMoving = stepperLeft.tick();
  rightMoving = stepperRight.tick();
  
}
