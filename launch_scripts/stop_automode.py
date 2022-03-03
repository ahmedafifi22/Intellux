import sys
sys.path.append("..")
import os
import numpy as np
from pathlib import Path

def stop_automode():
    root = Path(os.path.abspath(__file__)).parents[1]
    index_files_directory = os.path.join( root, 'Intellux', 'control_module', 'controller_info')
    if os.path.isdir(index_files_directory) == False:
        os.mkdir( index_files_directory)
    automode_status_file = os.path.join(index_files_directory, 'automode_status.npy')  
    update_automode_status(automode_status_file)

def update_automode_status(automode_status_file):
    new_automode_status = 0
    with open(automode_status_file, 'wb') as f:
        np.save(f, new_automode_status)  # Stop automode

if __name__=='__main__':
    stop_automode()