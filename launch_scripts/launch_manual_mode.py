import sys
sys.path.append("..")
import RPi.GPIO as GPIO
import argparse

from Intellux import Pi_28BYJ_48
from Intellux import Manual_Mode_Controller

def launch_manual_mode(required_blinds_angle):
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM) #defines naming convention to be used for the pins
    stepper_motor = Pi_28BYJ_48(in1=17, in2=18, in3=27, in4=22)
    controller = Manual_Mode_Controller()
    print(stepper_motor.motor_global_step_counter)
    required_stepper_motor_position = controller.get_required_stepper_motor_position(int(required_blinds_angle))
    stepper_motor.move_to_required_stepper_position(required_stepper_motor_position)

if __name__=='__main__':
    parser = argparse.ArgumentParser(description='please input the required blinds angle to launch manual mode')
    parser.add_argument('-a', '--angle', required=True, type=int, help='The required blinds angle')
    args = parser.parse_args()

    required_blinds_angle = int(args.angle)
    launch_manual_mode(required_blinds_angle)
