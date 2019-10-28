#include "pindef.h"

//Making objects for all motors we have.
motor_l298n motor0(MOTOR_FOR_0,MOTOR_BAC_0,MOTOR_PWM_0);
motor_l298n motor1(MOTOR_FOR_1,MOTOR_BAC_1,MOTOR_PWM_1);
motor_l298n motor2(MOTOR_FOR_2,MOTOR_BAC_2,MOTOR_PWM_2);
motor_l298n motor3(MOTOR_FOR_3,MOTOR_BAC_3,MOTOR_PWM_3);
motor_l298n motor4(MOTOR_FOR_4,MOTOR_BAC_4,MOTOR_PWM_4);
motor_l298n motor5(MOTOR_FOR_5,MOTOR_BAC_5,MOTOR_PWM_5);


motor_l298n motors[6] = {motor0, motor1, motor2, motor3, motor4, motor5};

void setup() {
  
}

void loop() {

  
}
