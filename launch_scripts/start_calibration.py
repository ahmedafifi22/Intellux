import sys
import os
sys.path.append("..")
import argparse
import numpy as np

from pathlib import Path
from Intellux import calibrate_intellux

def start_calibration(turning_direction):
    root = Path(os.path.abspath(__file__)).parents[1]

    stepper_files_directory = os.path.join(root, 'Intellux', 'mechanical_module', 'stepper_position')
    if os.path.isdir(stepper_files_directory) == False:
        os.mkdir(stepper_files_directory)
    motor_step_sequence_counter_file = os.path.join(stepper_files_directory, 'motor_step_sequence_counter.npy') 
    motor_global_step_counter_file = os.path.join(stepper_files_directory, 'motor_global_step_counter.npy') 
    reset_stepper_position_files(motor_step_sequence_counter_file, motor_global_step_counter_file)
    
    calibration_files_directory = os.path.join(root, 'Intellux', 'mechanical_module', 'calibration_info')
    if os.path.isdir(calibration_files_directory) == False:
        os.mkdir(calibration_files_directory)
    calibration_status_file = os.path.join(calibration_files_directory, 'calibration_status.npy') 
    full_range_steps_file = os.path.join(calibration_files_directory, 'full_range_steps.npy')  
    turning_direction_file = os.path.join(calibration_files_directory, 'turning_direction.npy')     
    
    new_calibration_status = update_calibration_status(calibration_status_file)
    if not os.path.isfile(full_range_steps_file):  # Load previous index
        with open(full_range_steps_file, 'wb') as f:
            np.save(f, 0)

    with open(turning_direction_file, 'wb') as f:
        np.save(f, turning_direction)

    if new_calibration_status == 1:
        calibration = calibrate_intellux(turning_direction)
        calibration.start_calibration()

def update_calibration_status(calibration_status_file):
    if os.path.isfile(calibration_status_file):  # Load previous index
        calibration_status = np.load(calibration_status_file)
        if calibration_status == 0:
            new_calibration_status = 1
        elif calibration_status == 1:
            raise ValueError("System already in process of calibration")
        else:
            raise ValueError("Unknown calibration status value loaded")

        with open(calibration_status_file, 'wb') as f:
            np.save(f, new_calibration_status)  # First time calibration
    else:
        new_calibration_status = 1 # First time calibration
        with open(calibration_status_file, 'wb') as f:
            np.save(f, new_calibration_status)  
    return new_calibration_status

def reset_stepper_position_files(motor_step_sequence_counter_file, motor_global_step_counter_file):
    with open(motor_step_sequence_counter_file, 'wb') as f: 
        np.save(f, 0) #reset stepper position file to 0
    with open(motor_global_step_counter_file, 'wb') as f:
        np.save(f, 0) #reset stepper position file to 0

if __name__=='__main__':
    parser = argparse.ArgumentParser(description='please input the turning direction to start calibrating as an int (0-CW or 1-CCW)')
    parser.add_argument('-d', '--direction', required=True, type=int, choices={0,1}, help='The required turning direction')
    args = parser.parse_args()

    turning_direction = int(args.direction)
    start_calibration(turning_direction)