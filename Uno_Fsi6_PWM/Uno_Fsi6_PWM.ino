//#define SER_DEBUG

#include <EnableInterrupt.h>
#include <Servo.h>  //Using servo library to control ESC

#define SERIAL_PORT_SPEED 9600
#define RC_NUM_CHANNELS  5   //changing to 5

#define RC_CH1  0
#define RC_CH2  1
#define RC_CH3  2
#define RC_CH4  3
#define RC_CH5  4                   //============>>>>> Adding index for 5th channel

#define RC_CH1_INPUT  A0
#define RC_CH2_INPUT  A1
#define RC_CH3_INPUT  A2
#define RC_CH4_INPUT  A3
#define RC_CH5_INPUT  A4            //============>>>>> Adding pin for 5th channel

int16_t PWM[RC_NUM_CHANNELS];

uint16_t rc_values[RC_NUM_CHANNELS];
uint32_t rc_start[RC_NUM_CHANNELS];
volatile uint16_t rc_shared[RC_NUM_CHANNELS];   //Read about volatile: https://www.arduino.cc/reference/en/language/variables/variable-scope--qualifiers/volatile/
                                                // 16 bit = 2 byte unsigned integer

void rc_read_values() {
  noInterrupts();
  memcpy(rc_values, (const void *)rc_shared, sizeof(rc_shared));
  interrupts();
}

void calc_input(uint8_t channel, uint8_t input_pin) {
  if (digitalRead(input_pin) == HIGH) {
    rc_start[channel] = micros();
  } else {
    uint16_t rc_compare = (uint16_t)(micros() - rc_start[channel]);
    rc_shared[channel] = rc_compare;
  }
}

void calc_ch1() { calc_input(RC_CH1, RC_CH1_INPUT); }
void calc_ch2() { calc_input(RC_CH2, RC_CH2_INPUT); }
void calc_ch3() { calc_input(RC_CH3, RC_CH3_INPUT); }
void calc_ch4() { calc_input(RC_CH4, RC_CH4_INPUT); }
void calc_ch5() { calc_input(RC_CH5, RC_CH5_INPUT); }     //============>>>>> Adding function for 5th channel

void setPWMInRange(){
  for(int i = 0; i<RC_NUM_CHANNELS; i++){
    if(PWM[i] < -255) PWM[i] = -255;
    else if(PWM[i] > 255) PWM[i] = 255;
  }
}

void setup() {
  Serial.begin(SERIAL_PORT_SPEED);
  
  pinMode(RC_CH1_INPUT, INPUT);
  pinMode(RC_CH2_INPUT, INPUT);
  pinMode(RC_CH3_INPUT, INPUT);
  pinMode(RC_CH4_INPUT, INPUT);
  pinMode(RC_CH5_INPUT, INPUT);                         //============>>>>> Adding pin for 5th channel

  enableInterrupt(RC_CH1_INPUT, calc_ch1, CHANGE);
  enableInterrupt(RC_CH2_INPUT, calc_ch2, CHANGE);
  enableInterrupt(RC_CH3_INPUT, calc_ch3, CHANGE);
  enableInterrupt(RC_CH4_INPUT, calc_ch4, CHANGE);
  enableInterrupt(RC_CH5_INPUT, calc_ch5, CHANGE);      //============>>>>> Adding Interrupts for 5th channel

}

void loop() {
  rc_read_values();
  
#ifdef SER_DEBUG
  Serial.print("CH1:"); Serial.print(rc_values[RC_CH1]); Serial.print("\t");   //FOR LEFT RIGHT
  Serial.print("CH2:"); Serial.print(rc_values[RC_CH2]); Serial.print("\t");   //FOR FRONT BACK
  //Rest of channels are unused!
  Serial.print("CH3:"); Serial.print(rc_values[RC_CH3]); Serial.print("\t");
  Serial.print("CH4:"); Serial.print(rc_values[RC_CH4]); Serial.print("\t");
  Serial.print("CH5:"); Serial.print(rc_values[RC_CH5]); Serial.print("\t");
#endif


  PWM[RC_CH1] = map(rc_values[RC_CH1],1030,1990,-255,255);
  PWM[RC_CH2] = map(rc_values[RC_CH2],1000,1980,-255,255);
  PWM[RC_CH3] = map(rc_values[RC_CH3],990,1970,-255,255);
  PWM[RC_CH4] = map(rc_values[RC_CH4],990,1960,-255,255);
  PWM[RC_CH5] = map(rc_values[RC_CH5],980,1950,-255,255);
  
  setPWMInRange();
  
#ifdef SER_DEBUG 
  Serial.print("P1:"); Serial.print(PWM[RC_CH1]); Serial.print("\t");
  Serial.print("P2:"); Serial.print(PWM[RC_CH2]); Serial.print("\t");   
  Serial.print("P3:"); Serial.print(PWM[RC_CH3]); Serial.print("\t");
  Serial.print("P4:"); Serial.print(PWM[RC_CH4]);Serial.print("\t");
  Serial.print("P5:"); Serial.println(PWM[RC_CH5]);Serial.print("\t");
#endif 
  PWM[RC_CH5] = (PWM[RC_CH5] < 0)?0:1;
  String data = "1,"+String(PWM[RC_CH1])+","+String(PWM[RC_CH2])+","+String(PWM[RC_CH3])+","+String(PWM[RC_CH4])+","+String(PWM[RC_CH5])+",1500";
  Serial.println(data);
  delay(100);
}
