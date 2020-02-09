#include <Arduino.h>
#include "motor_ibt2.h"

//constrctor:
motor_ibt2::motor_l298n(int LPWMPin, int RPWMPin){
  this->LPWMPin = LPWMPin;
  this->RPWMPin = RPWMPin;
  this->PWMData = 0;
  this->forwardMotion = NO;
  this->backwardMotion = NO;
}

//helper function
void motor_ibt2::moveMotor(int PWMvalue){
  this->PWMData = PWMvalue;

  if(this->PWMData > THRESHOLD){
    this->forwardMotion = YES;
    this->backwardMotion = NO;
  }else if(this->PWMData < (-1)*THRESHOLD){
    this->forwardMotion = NO;
    this->backwardMotion = YES;
  }else{
    this->forwardMotion = NO;
    this->backwardMotion = NO;
  }
  this->PWMData = abs(this->PWMData);
  
  int LPWM_data = (this->forwardMotion)*(this->PWMData);
  int RPWM_data = (this->backwardMotion)*(this->PWMData);
    
  analogWrite(this->LPWMPin, LPWM_data);
  analogWrite(this->RPWMPin, RPWM_data);
  
}
