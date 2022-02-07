import sys
import os
sys.path.append("..")
import argparse
import numpy as np

from pathlib import Path
from Intellux import calibrate_intellux
from pdb import set_trace as bp

def start_calibration(turning_direction):
    #bp()
    root = Path(os.path.abspath(__file__)).parents[1]

    index_files_directory = os.path.join( root, 'Intellux', 'mechanical_module', 'calibration_info')
    if os.path.isdir(index_files_directory) == False:
        os.mkdir( index_files_directory)

    calibration_status_file = os.path.join( index_files_directory,
                                                'calibration_status.npy')  # To Load the previous index
    full_range_steps_file = os.path.join(index_files_directory,
                                              'full_range_steps.npy')  # To Load the previous index

    if os.path.isfile(calibration_status_file):  # Load previous index
        calibration_status = np.load(calibration_status_file)
        if calibration_status == 0:
            new_calibration_status = 1
        elif calibration_status == 1:
            new_calibration_status = 0
        else:
            raise ValueError("Unknown value loaded")

        with open(calibration_status_file, 'wb') as f:
            np.save(f, new_calibration_status)  # First time calibration
    else:
        with open(calibration_status_file, 'wb') as f:
            np.save(f, 1)  # First time calibration
        new_calibration_status = 1

    if not os.path.isfile(full_range_steps_file):  # Load previous index
        with open(full_range_steps_file, 'wb') as f:
            np.save(f, 0)

    if new_calibration_status == 1:
        calibration = calibrate_intellux(turning_direction)
        calibration.start_calibration()


if __name__=='__main__':
    parser = argparse.ArgumentParser(description='please input the turning direction to launch calibration mode')
    parser.add_argument('-d', '--direction', required=True, type=int, help='The required turning direction')
    args = parser.parse_args()

    turning_direction = int(args.direction)
    start_calibration(turning_direction)