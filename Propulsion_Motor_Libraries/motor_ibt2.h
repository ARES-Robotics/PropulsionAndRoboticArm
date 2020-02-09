/*
 * motor_ibt2.h
 */

#ifndef motor_ibt2
#define motor_ibt2

#define YES 1
#define NO 0

#define THRESHOLD 10 //Motor will move only if PWM signal is more than this

class motor_ibt2{
  public:
   motor_l298n(int LPWMPin, int RPWMPin);
   
   int LPWMPin;
   int RPWMPin;

   int PWMData;
   
   //These two will be used to tell to set forward or backward motion
   int forwardMotion;
   int backwardMotion;
    
   void moveMotor(int PWMvalue);
};


#endif
