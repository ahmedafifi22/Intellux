import os
import numpy as np
from pathlib import Path

class Manual_Mode_Controller:
    '''controller class for intellux manual mode. This controller will be an open loop system 
    which is composed of a mapping function that will map the input blinds angle to a specific 
    stepper motor position. This mapping function will be determined in the future by inspecting
    the physical system through trial and error until we can approximate a linear relationship
    between the stepper motor position and the blinds angle'''
    def __init__(self):
        root = Path(os.path.abspath(__file__)).parents[1]
        full_range_steps_file = os.path.join(root, 'mechanical_module', 'calibration_info', 'full_range_steps.npy') 
        turning_direction_file = os.path.join(root, 'mechanical_module', 'calibration_info', 'turning_direction.npy')  

        if not os.path.isfile(full_range_steps_file) or not os.path.isfile(turning_direction_file):   
            #UI Feedback
            raise ValueError("intellux not calibrated, please calibrate first")
        else:
            self.full_range_steps = np.load(full_range_steps_file)
            self.turning_direction = np.load(turning_direction_file) #motor calibrated turning direction
            print("The full range steps used by manual mode is ", self.full_range_steps)
        self.full_range_degrees = 180 #number of degrees on the blinds that make up the blinds full range of motion

    def get_required_stepper_motor_position(self, required_blinds_angle):
        assert (required_blinds_angle <= self.full_range_degrees)
        assert (required_blinds_angle >= 0)
        required_stepper_position = int((required_blinds_angle * self.full_range_steps) / self.full_range_degrees)
        return required_stepper_position
