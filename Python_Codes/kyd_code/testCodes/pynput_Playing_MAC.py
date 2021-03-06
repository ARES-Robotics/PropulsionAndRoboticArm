##################################################################################
########################IMPORTING LIBRARIES ######################################
##################################################################################
#importing socket so that we can connect two computer
import socket
#importing time
import time
#importing Serial to take data from serial port
import serial
#importing the keyboard listener from pynput
from pynput import keyboard

##################################################################################
###################### SOCKET OBJECT AND VARIABLES ###################################################
##################################################################################
mode = 0;   #0-> Propulsion, 1-> Robotic Arm
forwardBackwardSpeed = 0;
leftRightSpeed = 0;
deltaIncrement = 1;

def sendDatatoRaspi():
    global forwardBackwardSpeed
    global leftRightSpeed
    stringData = str(mode) + ',' + str(forwardBackwardSpeed) + ',' + str(leftRightSpeed)
    # Sendng this data from socket to the raspberry pi
    s.send(str.encode(stringData))
    # After sending we check if it was recieved or not
    checkDataTranfer = s.recv(1024)
    print(checkDataTranfer)
##################################################################################
############################### Variables amd functions for speed ################
##################################################################################

def increaseForwardBackwardSpeed():
    global forwardBackwardSpeed
    global deltaIncrement
    forwardBackwardSpeed = forwardBackwardSpeed + deltaIncrement;
    if(forwardBackwardSpeed > 100):
        forwardBackwardSpeed = 100;
    printSpeeds()
    # sendDatatoRaspi()

def decreaseForwardBackwardSpeed():
    global forwardBackwardSpeed
    global deltaIncrement
    forwardBackwardSpeed = forwardBackwardSpeed - deltaIncrement;
    if (forwardBackwardSpeed < -100):
        forwardBackwardSpeed = -100;
    printSpeeds()
    # sendDatatoRaspi()

def increaseleftRightSpeed():
    global leftRightSpeed
    global deltaIncrement
    leftRightSpeed = leftRightSpeed + deltaIncrement;
    if (leftRightSpeed > 100):
        leftRightSpeed = 100;
    printSpeeds()
    # sendDatatoRaspi()

def decreaseleftRightSpeed():
    global leftRightSpeed
    global deltaIncrement
    leftRightSpeed = leftRightSpeed - deltaIncrement;
    if (leftRightSpeed < -100):
        leftRightSpeed = -100;
    printSpeeds()
    # sendDatatoRaspi()

def stopAllMotors():
    global leftRightSpeed
    global forwardBackwardSpeed
    leftRightSpeed = 0;
    forwardBackwardSpeed = 0;
    printSpeeds();



##################################################################################
############################### print statements ##################################
##################################################################################
def printSpeeds():
    global forwardBackwardSpeed
    global leftRightSpeed
    global mode
    stringData = str(mode) + ',' + str(forwardBackwardSpeed) + ',' + str(leftRightSpeed)
    print(" - ",stringData)

##################################################################################
############################### keyboard listener commands  ######################
##################################################################################
def on_press(key):
    global deltaIncrement
    global mode
    keyData = str(key)
    #print('pressed val = ',keyData)
    #print('length', len(keyData))
    #data = '{0}'.format(key) This will work too than str(key)
    #print('data',data)
    
    #print('length of data',len(data))
    if(format(key)=='Key.up'):
        increaseForwardBackwardSpeed();
    elif(format(key)=='Key.down'):
        decreaseForwardBackwardSpeed();
    elif(format(key)=='Key.left'):
        decreaseleftRightSpeed();
    elif(format(key)=='Key.right'):
        increaseleftRightSpeed();
    elif(format(key) == 'Key.space'):
        stopAllMotors();
    elif(format(key) == 'Key.enter'):
        mode = mode ^ 1             #Change Mode value
        print('MODE CHANGED - 0: Propulsion, 1: Robotic Arm')
    else: #It is a character (length = 10) or a number (length = 3)
        if(len(keyData) == 3): # If it is a number
            shotenKeyData = keyData[1];
            
            if(shotenKeyData == '1'):
                deltaIncrement = 1;
            elif(shotenKeyData == '2'):
                deltaIncrement = 5;
            elif(shotenKeyData == '3'):
                deltaIncrement = 10;
                
            elif(shotenKeyData == 'w'): #w
                print('It is w');
            elif(shotenKeyData == 'd'):#d
                print('It is d');
            elif (shotenKeyData == 'a'):  # a
                print('It is a');
            elif (shotenKeyData == 's'):  # s
                print('It is s');
            elif (shotenKeyData == 'r'):  # r
                print('It is r');
            elif (shotenKeyData == 't'):  # t
                print('It is t');
            elif (shotenKeyData == 'o'):  # o
                print('It is o');
            elif (shotenKeyData == 'p'):  # p
                print('It is p');
            elif (shotenKeyData == 'c'):  # c
                print('It is c');
            elif (shotenKeyData == 'v'):  # v
                print('It is v');
            elif (shotenKeyData == 'z'):  # z
                print('It is z');
            elif (shotenKeyData == 'x'):  # x
                print('It is x');

def on_release(key):
    #print("Stop")
    if key == keyboard.Key.esc:      # Stop listener
        return False
    

with keyboard.Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()

listener = keyboard.Listener(
    on_press=on_press,
    on_release=on_release)
listener.start()
##################################################################################
##################################################################################
