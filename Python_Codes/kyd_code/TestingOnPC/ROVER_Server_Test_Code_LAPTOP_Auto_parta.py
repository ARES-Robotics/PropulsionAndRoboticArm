##### Attrey Bhatt Codes - https://github.com/attreyabhatt/Reverse-Shell ###########
# If we are hacker then this file will go to our server that has a static ip address

#importing socket so that we can connect two computer
import socket
#importing PySerial and time
import serial
import time, threading
import motor_ibt2
import motor_l298n
import os
import math;

###################ARDUINO SERIAL OBJECT#################################################
### FOR IMU
ArduinoSerialPortMac = '/dev/tty.usbmodem14201'
ArduinoSerialPortPi = '/dev/ttyACM0'
arduinoSerial = serial.Serial(ArduinoSerialPortMac, 115600, timeout = 1)

# FOR GPS:
ArduinoGPSSerialPortMac = '/dev/tty.usbserial-1410'
ArduinoGPSSerialPortPi = '/dev/ttyACM0'
arduinoGPSSerial = serial.Serial(ArduinoGPSSerialPortMac, 9600, timeout = 1)

#FOR nano
#NanoSerialPortMac = '/dev/tty.usbmodem14101'
#NanoSerialPortPi = '/dev/ttyACM0'
#NanoSerial = serial.Serial(NanoSerialPortMac, 9600, timeout = 1)

#################################
# VARIABLES FOR PROPULSION MOTOR:
#################################
mode = 0;
motorspeed1 = 0
motorspeed2 = 0

motorPWM1 = 0
motorPWM2 = 0

currYaw = 0;
pastYaw = 0;
turnValue = 0;
forward_left_motor = motor_ibt2.motor1_ibt2(6,13)
forward_right_motor = motor_ibt2.motor1_ibt2(25,8)
backward_left_motor = motor_ibt2.motor1_ibt2(19,26)
backward_right_motor = motor_ibt2.motor1_ibt2(7,1)

latDestination = 12.843908
longDestination = 80.154008

latcurr = 0.00;
longcurr = 0.00;

distance = 0.00;
#########################################################
#########################################################
groundIP = "192.168.43.45"
def IPCheckRoutine():
    print(time.ctime())
    response = os.system("ping -c 1 " + groundIP)
    if response == 0:
        print('BASE - CONNECTED');
    else:
        if(mode == 0):
            dataFromBase = "0,0,0"
            index1 = dataFromBase.index(',')
            propulsion(dataFromBase,index1);
        else:
            dataFromBase = "1,0,0,0,0,0,0"
            index1 = dataFromBase.index(',')
            roboticArm(dataFromBase,index1);
        print('BASE - NOT CONNECTED',dataFromBase)
    threading.Timer(3, IPCheckRoutine).start()

#########################################################
######################################

######################################################################################################################
########## Function to Create a Socket ( socket connect two computers)
######################################################################################################################
def create_socket():
    try:
        #Creating following 3 global variables
        global host
        global port
        global s         #This is socket variable which is named s
        
        #Assigning values to these 3 global variables
        host = ""
        port = 9999
        s = socket.socket()    # Creating a socket and assigning it to s
    
    except socket.error as msg:
        print("Socket creation error: " + str(msg))


######################################################################################################################
########## # Binding the socket and listening for connections:
# Before accepting connection we listen for connections after binding host and port with the socket
######################################################################################################################
def bind_socket():
    try:
        # Declaring them again so that we can use the above global variable
        global host
        global port
        global s
        print("Binding the Port: " + str(port))
        
        s.bind((host, port))
        s.listen(5)
    
    except socket.error as msg:
        print("Socket Binding error" + str(msg) + "\n" + "Retrying...")
        bind_socket()

######################################################################################################################
###########   Establish connection with a client (socket must be listening)
######################################################################################################################
def socket_accept():
    #s.accept retuens : conn: object of a conversation and address is a list of IP adress and a port
    conn, address = s.accept()
    print("Connection has been established! |" + " IP " + address[0] + " | Port" + str(address[1]))
    read_commands(conn) #A function defined below to send command to client
    conn.close() #whenever the connection has been establised, at the end we want to close the connection

######################################################################################################################
###########  # Send commands to client/victim or a friend
######################################################################################################################
def send_commands(conn,data):
    conn.send(str.encode(data))
######################################################################################################################
###########  # Send commands to client/victim or a friend
######################################################################################################################

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
#                       print('In strToInt',i,x)
    if (flag ==1):
        return (-1)*x
    else:
        return x

def calc_dist():
    R = 6372800  # Earth radius in meters
    
    lat1 = latcurr;
    lon1 = longcurr;
    lat2 = latDestination;
    lon2 = longDestination;
    
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi       = math.radians(lat2 - lat1)
    dlambda    = math.radians(lon2 - lon1)
    
    a = math.sin(dphi/2)**2 + \
        math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
    
    return 2*R*math.atan2(math.sqrt(a), math.sqrt(1 - a))

def storeYaw():
    print("Reading Yaw")
    global currYaw;
    data = str(arduinoSerial.readline());
    data = data[2:len(data)-1]
    #print("Read Yaw data = ",data)
    if(len(data) >= 5):
        data = data[:len(data) - 5]
    #   print("Read Yaw data 2 = ",data)
    if(len(data) < 5):
        currYaw = float(data);
    print("Read Yaw data 3 = ",currYaw)

def storeGPScoordinates():
    global latcurr, longcurr;
    data = str(arduinoGPSSerial.readline());
    data = data[2:len(data)-1]
    if(len(data) >= 5):
        data = data[:len(data) - 4]
    index1 = data.index(" ")
    print(index1)
    #print(data)
    latcurr = float(data[0:index1])
    longcurr = float(data[index1+1:])
    print("COORDINATES: ",latcurr, longcurr)

def propulsion():
    print("in propulsion")
    global mode,motorspeed1, motorspeed2, forward_left_motor, forward_right_motor, backward_left_motor, backward_right_motor;
    global pastYaw, currYaw, latDestination, longDestination, distance;
    global latcurr, longcurr;
    
    global motorPWM1, motorPWM2;
    
    storeGPScoordinates();
    
    distance = calc_dist();
    
    print("DISTANCE FROM TARGET", distance)
    
    GPSreadcount = 0;
    
    while(distance > 5):
        storeYaw();
        #Give this signal until desired yaw:
        if(currYaw - pastYaw > 0):
            motorPWM1 = 20;
            motorPWM2 = 40;
        elif(currYaw - pastYaw < 0):
            motorPWM1 = 40;
            motorPWM2 = 20;
        else:
            motorPWM1 = 30;
            motorPWM2 = 30;
            storeYaw(); #Keep updating the yaw value-

        print("PWM DATAS: ",motorPWM1, motorPWM2)
        #Then give straight command until next instruction arrives
        forward_left_motor.moveMotor(motorPWM1)
        backward_left_motor.moveMotor(motorPWM1)
        forward_right_motor.moveMotor(motorPWM1)
        backward_right_motor.moveMotor(motorPWM1)
        
        if(GPSreadcount % 100 == 0):
            storeGPScoordinates();
            distance = calc_dist();
            
        GPSreadcount += 1;

    
        if(GPSreadcount > 100000):
            GPSreadcount -= 100000;
        
        print("DISTANCE FROM TARGET",GPSreadcount, distance)
            
    #STOP ALL MOTORS.
    forward_left_motor.moveMotor(0)
    backward_left_motor.moveMotor(0)
    forward_right_motor.moveMotor(0)
    backward_right_motor.moveMotor(0)

def read_commands(conn):
    global mode,motorspeed1, motorspeed2, forward_left_motor, forward_right_motor, backward_left_motor, backward_right_motor;
    global pastYaw, currYaw, latDestination, longDestination;
    
    #Read first 20 data and IGNORE them:
    for i in range (500):
        data = str(arduinoSerial.readline());
        print(data)
    #Read first 20 data and ignore them:
    for i in range (5):
        data = str(arduinoGPSSerial.readline());
        print(data)
    while True:
        #Read any data from sockets
        dataFromBase = str(conn.recv(1024),"utf-8")
        print(dataFromBase)
        #Now noting the yaw value before moving
        storeYaw();
        pastYaw = currYaw;
        #Now noting the GPS destination before moving
        latDestination = 12.843908
        longDestination = 80.154008
        
        print("\n Received Data = "+dataFromBase)
        print("pastYAW",pastYaw)
        
#       print('lengthOfData', len(dataFromBase))
        if(len(dataFromBase) >= 1):
            send_commands(conn,'YES')
            propulsion();
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
    create_socket()
    bind_socket()
    socket_accept()
############################################################
#Sending fake data
#    processDataToArduino('1,1001,1002,1003,1004,1005,1006');
#    time.sleep(2)
#    processDataToArduino('0,0,0,0,0,0,0');
########################################

main()

