 import Rpio.GPIO as IO

#
# This class has 7 variables: LPWMPin: Raspi pin number connected to LPWM of IBT2,
#                           RPWMPin: Raspi pin number connected to RPWM of IBT2,
#                           PWMData: This will store duticycle of PWM (range 0 to 100),
#                           forwwardMotion: This is flag that will set to 1 for forward motion,
#                           backwardMotion: This is flag that will set to 1 for backward motion,,
#                           LPWMctrl: Rpio.GPIO object for LPWMPin,
#                           RPWMctrl: Rpio.GPIO object for RPWMPin.
# This class has 1 constructor and 2 functions: moveMotor : Takes duticycle from -100 to 100 and puts puts data on forward or backward pin accordingly
#                                               printMotor: Just print motor object variable
#
#
#
##########

class motor1_L298n:
    def __init__(self,inputLeftPin, inputRightPin, enablePin):
        self.inputLeftPin = inputLeftPin      #Pins initialization
        self.inputRightPin = inputRightPin      #Pins initialization
        self.enablePin = enablePin                #Pins initialization

        self.PWMData = 0            #PWM data
        self.forwwardMotion = 0     #0 means NO, 1 means yes
        self.backwardMotion = 0     #0 means NO, 1 means yes

         IO.setwarnings(False)
         IO.setmode(IO.BCM)
        
         IO.setup(enablePin, IO.OUT)
         self.enablePinCtrl = IO.PWM(enablePin,100)
         self.enablePinCtrl.start(0)
        
         IO.setup(inputLeftPin,IO.OUT)
         IO.setup(inputRightPin, IO.OUT)

    def moveMotor(self, duticycle):
        self.PWMData = duticycle

        if duticycle > 5:
            self.forwwardMotion = 1
            self.backwardMotion = 0
             IO.output(self.inputLeftPin, IO.HIGH)
             IO.output(self.inputRightPin, IO.LOW)

        elif duticycle < -5:
            self.forwwardMotion = 0
            self.backwardMotion = 1
             IO.output(self.inputLeftPin, IO.LOW)
             IO.output(self.inputRightPin, IO.HIGH)
        else:
            self.forwwardMotion = 0
            self.backwardMotion = 0
            IO.output(self.inputLeftPin, IO.LOW)
            IO.output(self.inputRightPin, IO.LOW)

        self.PWMData = abs(duticycle);
        self.enablePinCtrl.ChangeDutyCycle(self.PWMData)

    def printMotor(self,motorName):
            print(motorName,self.inputLeftPin,self.inputRightPin,self.enablePin,self.PWMData,self.forwwardMotion,self.backwardMotion)

#######################################################################
#######################################################################
############################ CLASS TWO (without PWM) ##################
#######################################################################
#######################################################################
#######################################################################
class motor1_L298n_NOPWM:
    def __init__(self,inputLeftPin, inputRightPin):
        self.inputLeftPin = inputLeftPin      #Pins initialization
        self.inputRightPin = inputRightPin      #Pins initialization
        
        self.forwwardMotion = 0     #0 means NO, 1 means yes
        self.backwardMotion = 0     #0 means NO, 1 means yes
            
        IO.setwarnings(False)
        IO.setmode(IO.BCM)
            
#        IO.setup(enablePin, IO.OUT)                 //EnablePin- NO NEED as Shorted to 5V
#        self.enablePinCtrl = IO.PWM(enablePin,100)
#        self.enablePinCtrl.start(0)

        IO.setup(inputLeftPin,IO.OUT)
        IO.setup(inputRightPin, IO.OUT)

    def moveMotor(self, duticycle):
        self.PWMData = duticycle
        
            if duticycle > 5:
                self.forwwardMotion = 1
                self.backwardMotion = 0
                IO.output(self.inputLeftPin, IO.HIGH)
                IO.output(self.inputRightPin, IO.LOW)
    
            elif duticycle < -5:
                self.forwwardMotion = 0
                self.backwardMotion = 1
                IO.output(self.inputLeftPin, IO.LOW)
                IO.output(self.inputRightPin, IO.HIGH)
            else:
                self.forwwardMotion = 0
                self.backwardMotion = 0
                IO.output(self.inputLeftPin, IO.LOW)
                IO.output(self.inputRightPin, IO.LOW)


        def printMotor(self,motorName):
            print(motorName,self.inputLeftPin,self.inputRightPin,self.forwwardMotion, self.backwardMotion)
