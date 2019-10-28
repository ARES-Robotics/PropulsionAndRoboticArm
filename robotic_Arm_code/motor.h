/*
 * motor.h
 */

#ifndef motor_h
#define motor_h

#define YES 1
#define NO 0

#define THRESHOLD 10 //Motor will move only if PWM signal is more than this

class motor_l298n{
  public:
   motor_l298n(int forwardPin, int backwardPin, int PWMpin);
   
   
   int inputLeftPin;
   int inputRightPin;
   int enablePin;

   int PWMData;
   int forwardMotion;
   int backwardMotion;
   void moveMotor(int PWMvalue);
};


#endif
