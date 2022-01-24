import time
from proportional_controller import p_controller

class Auto_Mode_Controller:
    '''controller class for intellux auto mode. This controller will mainly be composed of a
    PID controller which will be tuned to try and meet the timing and performance requirements
    set in the requirements specifications. The controller output will then be mapped to a specific
    stepper motor position that the mechanical module would have to adjust to. This new stepper motor 
    position would in turn reflect a new blinds angle. After the adjustment, the sensors module would 
    then gather new brightness readings, thus forming a feedback loop'''

    def __init__(self, indoor_sensor_mount_angle):
        self.full_range_steps = 2048 #number of steps required from the stepper motor to cover the blinds full range of motion (0 - 180)
        self.full_range_degrees = 180 #number of degrees on the blinds that make up the blinds full range of motion
        self.max_setpoint = 3.3 #Max voltage that the lux sensor can achieve 

        self.indoor_sensor_mount_angle = indoor_sensor_mount_angle
        self.max_brightness_position = int(self.full_range_steps * (self.indoor_sensor_mount_angle / self.full_range_degrees)) #stepper position that achieves max brigtness (90 degrees)
        
        self.controller = p_controller(Kp=0.5,
                                       T=0.01, 
                                       sensor_voltage_output_lim_min=0, 
                                       sensor_voltage_output_lim_max=max_setpoint)

    def check_setpoint_achievable(self, required_setpoint, outdoor_sensor_voltage):
        if required_setpoint > outdoor_sensor_voltage:
            return False
        else:
            return True

    def map_to_stepper_position(self, target_sensor_voltage_output, current_sensor_voltage_output, current_stepper_position):
        new_stepper_position = current_stepper_position * (target_sensor_voltage_output / current_sensor_voltage_output)
        if new_stepper_position > self.max_brightness_position:
            new_stepper_position = self.max_brightness_position
        elif new_stepper_position < 0:
            new_stepper_position = 0
        else:
            new_stepper_position = new_stepper_position
        return new_stepper_position

    def get_required_stepper_motor_position(self, required_setpoint, current_sensor_voltage_output, current_stepper_position):
        assert (required_setpoint <= self.max_setpoint)
        assert (required_setpoint >= 0)
        target_sensor_voltage_output = self.controller.controller_update(required_setpoint, current_sensor_voltage_output)
        new_stepper_position = self.map_to_stepper_position(target_sensor_voltage_output, current_sensor_voltage_output, current_stepper_position)
        return new_stepper_position
