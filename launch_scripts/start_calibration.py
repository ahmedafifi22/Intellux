import sys
import os
sys.path.append("..")
import argparse
import numpy as np

from pathlib import Path
from Intellux import calibrate_intellux

def start_calibration(turning_direction):
    root = Path(os.path.abspath(__file__)).parents[0]
    index_files_directory = os.path.join( root, 'calibration_info')
    if os.path.isdir(index_files_directory) == False:
        os.mkdir( index_files_directory)

    calibration_status_file = os.path.join( index_files_directory,
                                                'calibration_status.npy')  # To Load the previous index
    full_range_steps_file = os.path.join(index_files_directory,
                                              'full_range_steps.npy')  # To Load the previous index

    if os.path.isfile(calibration_status_file):  # Load previous index
        calibration_status = np.load(calibration_status_file)
        with open(calibration_status_file, 'wb') as f:
            np.save(f, not calibration_status)  # First time calibration
    else:
        with open(calibration_status_file, 'wb') as f:
            np.save(f, 1)  # First time calibration
        calibration_status = 1

    if not os.path.isfile(full_range_steps_file):  # Load previous index
        with open(full_range_steps_file, 'wb') as f:
            np.save(f, 0)

    if not calibration_status == 1:
        calibration = calibrate_intellux(turning_direction)
        calibration.start_calibration()




if __name__=='__main__':
    parser = argparse.ArgumentParser(description='please input the turning direction to launch calibration mode')
    parser.add_argument('-d', '--direction', required=True, type=int, help='The required turning direction')
    args = parser.parse_args()

    turning_direction = int(args.direction)
    start_calibration(turning_direction)