# import Rpio.GPIO as IO

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

class motor1_ibt2:
    def __init__(self,LPWMPin, RPWMPin):
        self.LPWMPin = LPWMPin      #Pins initialization
        self.RPWMPin = RPWMPin      #Pins initialization
        self.PWMData = 0            #PWM data
        self.forwwardMotion = 0     #0 means NO, 1 means yes
        self.backwardMotion = 0     #0 means NO, 1 means yes

        # IO.setwarnings(False)
        # IO.setmode(IO,BCM)
        #
        # IO.setup(LPWMPin, IO, OUT)
        # self.LPWMctrl = IO.PWM(LPWMPin,100) £
        # self.LPWMctrl.start(0)
        #
        # IO.setup(RPWMPin,IO,OUT)
        # self.RPWMctrl = IO.PWM(RPWMPin, 100)
        # self.RPWMctrl.start(0)

    def moveMotor(self, duticycle):
        self.PWMData = duticycle

        if duticycle > 10:
            self.forwwardMotion = 1
            self.backwardMotion = 0
        elif duticycle < -10:
            self.forwwardMotion = 0
            self.backwardMotion = 1
        else:
            self.forwwardMotion = 0
            self.backwardMotion = 0

        self.PWMData = abs(duticycle);

        # LPWM_duticycle = (self.forwwardMotion)*(self.PWMData);
        # RPWM_duticycle = (self.backwardMotion) * (self.PWMData);
        #
        # self.LPWMctrl.ChangeDutyCycle(LPWM_duticycle)
        # self.RPWMctrl.ChangeDutyCycle(RPWM_duticycle)

    def printMotor(self):
        print(self.LPWMPin)
        print(self.RPWMPin)
        print(self.PWMData)
        print(self.forwwardMotion)
        print(self.backwardMotion)
