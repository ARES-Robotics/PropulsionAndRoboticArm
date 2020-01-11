import Rpio.GPIO as IO

class motor1_ibt2:
    def __init__(self,LPWMPin, RPWMPin):
        self.LPWMPin = LPWMPin      #Pins initialization
        self.RPWMPin = RPWMPin      #Pins initialization
        self.PWMData = 0            #PWM data
        self.forwwardMotion = 0     #0 means NO, 1 means yes
        self.backwardMotion = 0     #0 means NO, 1 means yes

        IO.setwarnings(False)
        IO.setmode(IO.BCM)
        
        IO.setup(LPWMPin, IO.OUT)
        self.LPWMctrl = IO.PWM(LPWMPin,100)
        self.LPWMctrl.start(0)
        
        IO.setup(RPWMPin,IO.OUT)
        self.RPWMctrl = IO.PWM(RPWMPin, 100)
        self.RPWMctrl.start(0)

    def moveMotor(self, duticycle):
        self.PWMData = duticycle

        if duticycle > 7:
            self.forwwardMotion = 1
            self.backwardMotion = 0
        elif duticycle < -7:
            self.forwwardMotion = 0
            self.backwardMotion = 1
        else:
            self.forwwardMotion = 0
            self.backwardMotion = 0

        self.PWMData = abs(duticycle);

        LPWM_duticycle = (self.forwwardMotion)*(self.PWMData);
        RPWM_duticycle = (self.backwardMotion) * (self.PWMData);
        
        self.LPWMctrl.ChangeDutyCycle(LPWM_duticycle)
        self.RPWMctrl.ChangeDutyCycle(RPWM_duticycle)

    def printMotor(self,motorName): print(motorName,self.LPWMPin,self.RPWMPin,self.PWMData,self.forwwardMotion,self.backwardMotion)
