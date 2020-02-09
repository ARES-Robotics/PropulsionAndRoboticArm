#include <Arduino.h>
#include "motor.h"

//constrctor:
motor_l298n::motor_l298n(const int forwardPin, const int backwardPin, const int PWMpin){
  this->inputLeftPin = forwardPin;
  this->inputRightPin = backwardPin;
  this->enablePin = PWMpin;
  this->PWMData = 0;
  this->forwardMotion = NO;
  this->backwardMotion = NO;
}

//helper function
void motor_l298n::moveMotor(int PWMvalue){
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
  
  digitalWrite(this->inputLeftPin, this->forwardMotion);
  digitalWrite(this->inputRightPin, this->backwardMotion);
  analogWrite(this->enablePin, this->PWMData);
  
}
