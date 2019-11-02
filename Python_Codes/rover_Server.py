
##### Attrey Bhatt Codes - https://github.com/attreyabhatt/Reverse-Shell ###########
# If we are hacker then this file will go to our server that has a static ip address

#importing socket so that we can connect two computer
import socket
#importing PySerial and time
import serial
import time

###################ARDUINO SERIAL OBJECT#################################################
serialPortMac = '/dev/tty.usbmodem14101'
serialPortPi = '/dev/ttyACM0'
arduinoSerial = serial.Serial(serialPortMac, 9600, timeout = 1)



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
def read_commands(conn):
    while True:
        dataFromBase = str(conn.recv(1024),"utf-8")
        print(dataFromBase + "\n")
        if(len(dataFromBase) > 3):
            send_commands(conn,'1')
            processDataToArduino(dataFromBase)
        
            while arduinoSerial.inWaiting() < 1:
                pass
            serialData = str(arduinoSerial.readline())
            if(len(serialData) > 2):
                print(makeDataWhatArduinoSent(serialData))
        else:
            send_commands(conn,'0')

######################################################################################################################
###########  # Process Data from raspberrypi to Arduino
######################################################################################################################
def processDataToArduino(data):
    arduinoSerial.write(str(data).encode())

######################################################################################################################
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
    processDataToArduino('1,1001,1002,1003,1004,1005,1006');
    time.sleep(2)
    processDataToArduino('0,0,0,0,0,0,0');
########################################

main()







