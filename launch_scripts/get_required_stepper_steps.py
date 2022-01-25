import sys
sys.path.append("..")
import RPi.GPIO as GPIO
import time
import keyboard

from Intellux import Pi_28BYJ_48

def move_stepper(steps_required):
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM) #defines naming convention to be used for the pins
    stepper_motor = Pi_28BYJ_48(in1=17, in2=18, in3=27, in4=22)
    stepper_motor.turn_CCW(steps_required)
    #stepper_motor.turn_CCW(steps_required)
    print("stepper moved {} steps".format(steps_required))
    GPIO.cleanup()

if __name__=='__main__':
    steps_required = 4096  
    move_stepper(steps_required)