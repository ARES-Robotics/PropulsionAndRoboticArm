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
  setMotorOutputPinout();
}

void loop() {
  int pwmData[6] = {0,0,0,0,0,0};
  
  int pwmData[0] = analogRead(A0);
  int pwmData[1] = analogRead(A1);
  int pwmData[2] = analogRead(A2);
  int pwmData[3] = analogRead(A3);
  int pwmData[4] = analogRead(A4);
  int pwmData[5] = analogRead(A5);

 
  
  for(int i=0; i<6; i++){
    if(pwmData[i] > 20){
      pwmData[i] = map(pwmData[i],0,1023,-255,255);
    }else{
      pwmData[i] = 0;
    }
    
    motors[i].moveMotor(pwmData[i]);
  }
 
}

void setMotorOutputPinout(){
  pinMode(MOTOR_FOR_0, OUTPUT);
  pinMode(MOTOR_BAC_0, OUTPUT);
  pinMode(MOTOR_PWM_0, OUTPUT);

  pinMode(MOTOR_FOR_1, OUTPUT);
  pinMode(MOTOR_BAC_1, OUTPUT);
  pinMode(MOTOR_PWM_1, OUTPUT);

  pinMode(MOTOR_FOR_2, OUTPUT);
  pinMode(MOTOR_BAC_2, OUTPUT);
  pinMode(MOTOR_PWM_2, OUTPUT);

  pinMode(MOTOR_FOR_3, OUTPUT);
  pinMode(MOTOR_BAC_3, OUTPUT);
  pinMode(MOTOR_PWM_3, OUTPUT);

  pinMode(MOTOR_FOR_4, OUTPUT);
  pinMode(MOTOR_BAC_4, OUTPUT);
  pinMode(MOTOR_PWM_4, OUTPUT);

  pinMode(MOTOR_FOR_5, OUTPUT);
  pinMode(MOTOR_BAC_5, OUTPUT);
  pinMode(MOTOR_PWM_5, OUTPUT);
}

void setInputPinout(){
  pinMode(A0, INPUT);
  pinMode(A1, INPUT);
  pinMode(A2, INPUT);
  pinMode(A3, INPUT);
  pinMode(A4, INPUT);
  pinMode(A5, INPUT);
}
