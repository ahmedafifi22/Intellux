import sys
sys.path.append("..")
import os
import numpy as np
from pathlib import Path

def stop_calibration():
    root = Path(os.path.abspath(__file__)).parents[1]
    index_files_directory = os.path.join( root, 'Intellux', 'mechanical_module', 'calibration_info')
    if os.path.isdir(index_files_directory) == False:
        os.mkdir( index_files_directory)
    calibration_status_file = os.path.join(index_files_directory, 'calibration_status.npy')  
    update_calibration_status(calibration_status_file)

def update_calibration_status(calibration_status_file):
    new_calibration_status = 0
    with open(calibration_status_file, 'wb') as f:
        np.save(f, new_calibration_status)  # Stop calibration

if __name__=='__main__':
    stop_calibration()