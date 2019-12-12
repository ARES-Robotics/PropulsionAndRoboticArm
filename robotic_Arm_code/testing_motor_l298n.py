import motor_l298n

fowrard_left_motor = motor_l298n.motor1_L298n(2,3,4)  #Parameters are input LPWM_and RPWM pin of IBT2
fowrard_left_motor.moveMotor(-25)                 #Duticycle ranging from -100 to 100 [+ve means forward, -ve means backwards]


#Testing by printing
fowrard_left_motor.printMotor()