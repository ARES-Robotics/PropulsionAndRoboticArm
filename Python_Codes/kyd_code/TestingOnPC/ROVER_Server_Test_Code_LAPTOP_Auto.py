##### Attrey Bhatt Codes - https://github.com/attreyabhatt/Reverse-Shell ###########
# If we are hacker then this file will go to our server that has a static ip address


#importing PySerial and time
import serial
import time, threading
import motor_ibt2
import motor_l298n
import os

###################ARDUINO SERIAL OBJECT #################################################
ArduinoSerialPortMac = '/dev/tty.usbmodem14101'
ArduinoSerialPortPi = '/dev/ttyACM0'
arduinoSerial = serial.Serial(ArduinoSerialPortMac, 9600, timeout = 1)

NanoSerialPortMac = '/dev/tty.usbmodem14101'
NanoSerialPortPi = '/dev/ttyACM0'
NanoSerial = serial.Serial(NanoSerialPortMac, 9600, timeout = 1)

################################
# VARIABLES FOR PROPULSION MOTOR:
#################################
mode = 0;
motorspeed1 = 0
motorspeed2 = 0
forward_left_motor = motor_ibt2.motor1_ibt2(2,3)
forward_right_motor = motor_ibt2.motor1_ibt2(14,15)

backward_left_motor = motor_ibt2.motor1_ibt2(4,17)
backward_right_motor = motor_ibt2.motor1_ibt2(18,23)

#########################################################
######################################

def strToInt(string):
    if(len(string) == 0):
#        print('string length 0')
        return 0;
    x=0
    flag = 0
    if(string[0]=='-'):
        flag=1
        
    for i in range (0,len(string)):
                    if string[i].isdigit():
                        x+=int(string[i])*10**int(len(string)-i-1)
#                        print('In strToInt',i,x)
    if (flag ==1):
        return (-1)*x
    else:
        return x

def propulsion(dataFromBase, index1):
        global mode,motorspeed1, motorspeed2, forward_left_motor, forward_right_motor, backward_left_motor, backward_right_motor;
        
        index2 = dataFromBase.index(',',index1+1)
           
        motorspeed = dataFromBase[index1+1:index2]
        temp1 = float(motorspeed)
        motorspeed1 = temp1
        motorspeed2 = temp1

        motorspeed = dataFromBase[index2+1:]
        temp2 = float(motorspeed)
        motorspeed1 = motorspeed1 - temp2
        motorspeed2 = motorspeed2 + temp2
        
        print('motorspeed1',motorspeed1)
        print('motorspeed2',motorspeed2)
        
        
        if (motorspeed1 > 100):
            motorspeed1 = 100
        elif (motorspeed1 < -100):
            motorspeed1 = -100
            
        if (motorspeed2 > 100):
            motorspeed2 = 100
        elif (motorspeed2 < -100):
            motorspeed2 = -100

        print('motorspeed1',motorspeed1)
        print('motorspeed2',motorspeed2)
            
        forward_left_motor.moveMotor(motorspeed2)
        backward_left_motor.moveMotor(motorspeed2)

        forward_right_motor.moveMotor(motorspeed1)
        backward_right_motor.moveMotor(motorspeed1)

def read_commands():
    global mode,motorspeed1, motorspeed2, forward_left_motor, forward_right_motor, backward_left_motor, backward_right_motor;
    #IPCheckRoutine()
    while True:
        dataFromBase =
        print("\n Received Data = "+dataFromBase)
#        print('lengthOfData', len(dataFromBase))
        if(len(dataFromBase) > 3):
            send_commands(conn,'YES')
            index1 = dataFromBase.index(',')
            modeStr = dataFromBase[0:index1]
            
            mode = strToInt(modeStr)
            
            if(mode == 0):
                propulsion(dataFromBase,index1);
            elif(mode == 1):
                roboticArm(dataFromBase,index1);
    
        else:
            send_commands(conn,'NO')

######################################################################################################################
###########  # Process Data from raspberrypi to Arduino
######################################################################################################################
#def processDataToArduino(data):
 #   arduinoSerial.write(str(data).encode())

#####################################################################################################################
###########  # Remove b'' and\r\n from the string
######################################################################################################################
def makeDataWhatArduinoSent(data):
    return data[2:len(data)-5]
    
######################################################################################################################
###########  # MAIN
######################################################################################################################
def main():
    read_commands()
############################################################
#Sending fake data
#    processDataToArduino('1,1001,1002,1003,1004,1005,1006');
#    time.sleep(2)
#    processDataToArduino('0,0,0,0,0,0,0');
########################################

main()

