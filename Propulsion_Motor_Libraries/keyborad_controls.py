##################################################################################
########################IMPORTING LIBRARIES ######################################
##################################################################################
#importing socket so that we can connect two computer
import socket
#importing time
import time
#importing Serial to take data from serial port
#import serial
#importing the keyboard listener from pynput
from pynput import keyboard

##################################################################################
###################### SOCKET OBJECT AND VARIABLES ###################################################
##################################################################################
s = socket.socket()
host = '192.168.43.75'  #IP Address of the Raspberry pi
port = 9999            #Must be same as that in server.py
print('hello1')
#In client.py we use another way to bind host and port together by using connect function()
s.connect((host, port))
print('hello2')
###########################SERIAL OBJECT ##############################################
# serialPortMac = '/dev/tty.usbmodem14101' #FOR MACBOOK
# serialPortWin = '/dev/ttyUSB0'           #FOR WINDOWS
# serialPortUbuntu = '/dev/ttyACM0'        #FOR UBUNTU
# ser = serial.Serial(serialPortUbuntu, 9600,timeout=0.005)

def sendDatatoRaspi():
    global forwardBackwardSpeed
    global leftRightSpeed
    stringData = '1,' + str(forwardBackwardSpeed) + ',' + str(leftRightSpeed)
    # Sendng this data from socket to the raspberry pi
    s.send(str.encode(stringData))
    # After sending we check if it was recieved or not
    checkDataTranfer = s.recv(1024)
    print(checkDataTranfer)
##################################################################################
############################### Variables amd functions for speed ################
##################################################################################
forwardBackwardSpeed = 0;
leftRightSpeed = 0;
def increaseForwardBackwardSpeed():
    global forwardBackwardSpeed
    forwardBackwardSpeed = forwardBackwardSpeed + 1;
    if(forwardBackwardSpeed > 100):
        forwardBackwardSpeed = 100;
    printSpeeds()
    sendDatatoRaspi()

def decreaseForwardBackwardSpeed():
    global forwardBackwardSpeed
    forwardBackwardSpeed = forwardBackwardSpeed - 1;
    if (forwardBackwardSpeed < -100):
        forwardBackwardSpeed = -100;
    printSpeeds()
    sendDatatoRaspi()

def increaseleftRightSpeed():
    global leftRightSpeed
    leftRightSpeed = leftRightSpeed + 1;
    if (leftRightSpeed > 100):
        leftRightSpeed = 100;
    printSpeeds()
    sendDatatoRaspi()

def decreaseleftRightSpeed():
    global leftRightSpeed
    leftRightSpeed = leftRightSpeed - 1;
    if (leftRightSpeed < -100):
        leftRightSpeed = -100;
    printSpeeds()
    sendDatatoRaspi()

def stopMotor():
    global leftRightSpeed
    global forwardBackwardSpeed
    leftRightSpeed = 0
    forwardBackwardSpeed = 0
    printSpeeds()
    sendDatatoRaspi()
##################################################################################
############################### print statements ##################################
##################################################################################
def printSpeeds():
    global forwardBackwardSpeed
    global leftRightSpeed
    stringData = '1,' + str(forwardBackwardSpeed) + ',' + str(leftRightSpeed)
    print(" - ",stringData)

##################################################################################
############################### keyboard listener commands  ######################
##################################################################################
def on_press(key):
        
    if(format(key)=='Key.up'):
        increaseForwardBackwardSpeed();
    elif(format(key)=='Key.down'):
        decreaseForwardBackwardSpeed();
    elif(format(key)=='Key.left'):
        decreaseleftRightSpeed();
    elif(format(key)=='Key.right'):
        increaseleftRightSpeed();
    elif key == keyboard.Key.esc:
        print('stopingMotor')
        stopMotor();

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

