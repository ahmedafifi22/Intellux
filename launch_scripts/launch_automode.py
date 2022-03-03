import os
import sys
sys.path.append("..")
import RPi.GPIO as GPIO
import numpy as np
import argparse
from pathlib import Path
import time

from Intellux import Pi_17HS4023_L298N
from Intellux import Pi_ADS1115, Pi_TEMT6000
from Intellux import Auto_Mode_Controller


def launch_automode(required_setpoint, degrees_until_controller_update, indoor_sensor_mount_angle, hysteresis_value):
    root = Path(os.path.abspath(__file__)).parents[1]
    index_files_directory = os.path.join( root, 'Intellux', 'control_module', 'controller_info')
    if os.path.isdir(index_files_directory) == False:
        os.mkdir( index_files_directory)
    automode_status_file = os.path.join(index_files_directory, 'automode_status.npy')  
    update_automode_status(automode_status_file)

    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM) #defines naming convention to be used for the pins

    adc = Pi_ADS1115()
    indoor_lux_sensor_instance = Pi_TEMT6000(adc_instance=adc, adc_channel_used=0, gain=1)
    outdoor_lux_sensor_instance = Pi_TEMT6000(adc_instance=adc, adc_channel_used=3, gain=1)

    controller = Auto_Mode_Controller(degrees_until_controller_update, indoor_sensor_mount_angle, hysteresis_value)
    stepper_motor = Pi_17HS4023_L298N(in1=27, in2=17, in3=22, in4=18, enable_a=24, enable_b=23, turning_direction=controller.turning_direction)

    print('Required Setpoint | Current indoor sensor voltage | Current outdoor sensor voltage | New angle positon |')
    print('-' * 37)

    automode_status_last_update_time = os.path.getmtime(automode_status_file)
    while True:
        if os.path.getmtime(automode_status_file) == automode_status_last_update_time:
            #file was not updated, read right away
            automode_status = np.load(automode_status_file)
        else:
            time.sleep(1)
            #file was updated, wait 1 second before reading
            automode_status = np.load(automode_status_file)

        if automode_status == 1:
            stepper_motor.setup_motor_pins()
            indoor_sensor_voltage = indoor_lux_sensor_instance.get_sensor_input_voltage()
            outdoor_sensor_voltage = outdoor_lux_sensor_instance.get_sensor_input_voltage()
            current_stepper_position = stepper_motor.motor_global_step_counter

            if controller.check_setpoint_achievable(required_setpoint, outdoor_sensor_voltage):
                new_stepper_position = controller.controller_update(required_setpoint, indoor_sensor_voltage, current_stepper_position)
                new_angle_position = int(controller.full_range_degrees * (new_stepper_position / controller.full_range_steps)) 
                print('|  Setpoint: {}V  |  indoor: {}V  |  outdoor: {}V  |  new_angle:{}deg  |'.format(required_setpoint, indoor_sensor_voltage, outdoor_sensor_voltage, new_angle_position))

                stepper_motor.move_to_required_stepper_position(new_stepper_position)
                stepper_motor.cleanup()
            else:
                #UI Feedback
                stepper_motor.cleanup()
                with open(automode_status_file, 'wb') as f:
                    np.save(f, 0)  # Stop automode
                raise ValueError("Setpoint: {} lux not achievable, outdoor lighting is: {} lux".format(required_setpoint, outdoor_sensor_voltage))
        else:
            print("User stopped automode")
            break

def update_automode_status(automode_status_file):
    if os.path.isfile(automode_status_file):  # Load previous index
        automode_status = np.load(automode_status_file)
        if automode_status == 0:
            new_automode_status = 1
        elif automode_status == 1:
            raise ValueError("System already running auto mode, turn off auto mode to update preferences")
        else:
            raise ValueError("Unknown automode status value loaded")

        with open(automode_status_file, 'wb') as f:
            np.save(f, new_automode_status)  
    else:
        new_automode_status = 1 # First time running automode
        with open(automode_status_file, 'wb') as f:
            np.save(f, new_automode_status)  
    

if __name__=='__main__':
    parser = argparse.ArgumentParser(description='please input the required setpoint (0-3.3v) to launch auto mode')
    parser.add_argument('-s', '--setpoint', required=True, type=float, help='The required setpoint')
    args = parser.parse_args()

    setpoint = float(args.setpoint)
    indoor_sensor_mount_angle = 90
    degrees_until_controller_update = 5
    hysteresis_value = 0.1
    
    launch_automode(setpoint, degrees_until_controller_update, indoor_sensor_mount_angle, hysteresis_value)
    