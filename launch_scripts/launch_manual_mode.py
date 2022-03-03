import sys
sys.path.append("..")
import RPi.GPIO as GPIO
import argparse

from Intellux import Pi_17HS4023_L298N
from Intellux import Manual_Mode_Controller

def launch_manual_mode(required_blinds_angle):
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM) #defines naming convention to be used for the pins

    controller = Manual_Mode_Controller()
    stepper_motor = Pi_17HS4023_L298N(in1=27, in2=17, in3=22, in4=18, enable_a=24, enable_b=23, turning_direction=controller.turning_direction)
    
    #print(stepper_motor.motor_global_step_counter)
    required_stepper_motor_position = controller.get_required_stepper_motor_position(int(required_blinds_angle))
    stepper_motor.move_to_required_stepper_position(required_stepper_motor_position)
    stepper_motor.cleanup()

if __name__=='__main__':
    parser = argparse.ArgumentParser(description='please input the required blinds angle to launch manual mode')
    parser.add_argument('-a', '--angle', required=True, type=int, help='The required blinds angle')
    args = parser.parse_args()

    required_blinds_angle = int(args.angle)
    launch_manual_mode(required_blinds_angle)
