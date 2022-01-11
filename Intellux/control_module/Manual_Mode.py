import time

class Manual_Mode_Controller:
    '''controller class for intellux manual mode. This controller will be an open loop system 
    which is composed of a mapping function that will map the input blinds angle to a specific 
    stepper motor position. This mapping function will be determined in the future by inspecting
    the physical system through trial and error until we can approximate a linear relationship
    between the stepper motor position and the blinds angle'''
    def __init__(self):
        self.full_range_steps = 2048 #number of steps required from the stepper motor to cover the blinds full range of motion
        self.full_range_degrees = 180 #number of degrees on the blinds that make up the blinds full range of motion

    def get_required_stepper_motor_position(self, required_blinds_angle):
        assert (required_blinds_angle <= self.full_range_degrees)
        assert (required_blinds_angle >= 0)
        required_stepper_position = int((required_blinds_angle * self.full_range_steps) / self.full_range_degrees)
        return required_stepper_position
