import time
#from hysteresis_controller import hysteresis_control

class Auto_Mode_Controller:
    '''controller class for intellux auto mode. This controller will mainly be composed of a
    Hysteresis controller which will be tuned to try and meet the timing and performance requirements
    set in the requirements specifications. The controller output will be an instruction of whether to
    open the blinds, close the blinds, or do nothing. After the adjustment, the sensors module would 
    then gather new brightness readings, thus forming a feedback loop'''

    def __init__(self, degrees_until_controller_update, indoor_sensor_mount_angle, hysteresis_value):
        self.full_range_steps = 2048 #number of steps required from the stepper motor to cover the blinds full range of motion (0 - 180)
        self.full_range_degrees = 180 #number of degrees on the blinds that make up the blinds full range of motion
        self.max_setpoint = 3.3 #Max voltage that the lux sensor can achieve

        self.indoor_sensor_mount_angle = indoor_sensor_mount_angle
        self.max_brightness_position = int(self.full_range_steps * (self.indoor_sensor_mount_angle / self.full_range_degrees)) #stepper position that achieves max brigtness (90 degrees)
        self.stepper_steps_until_controller_update = (self.degrees_until_controller_update / self.full_range_degrees) * self.full_range_steps #controller update every  degree which is 
        self.hysteresis_value = hysteresis_value

    def check_setpoint_achievable(self, required_setpoint, outdoor_sensor_voltage):
        if required_setpoint > outdoor_sensor_voltage:
            return False
        else:
            return True

    def controller_update(self, setpoint, indoor_sensor_measurement, current_stepper_position):
        assert (required_setpoint <= self.max_setpoint)
        assert (required_setpoint >= 0)

        if indoor_sensor_measurement < setpoint - self.hysteresis_value:
            #open blinds to increase incoming brightness
            if current_stepper_position < self.max_brightness_position:
                target_stepper_position = current_stepper_position + self.stepper_steps_until_controller_update
                if target_stepper_position > self.max_brightness_position:
                    target_stepper_position = self.max_brightness_position         
            elif current_stepper_position > self.max_brightness_position:
                target_stepper_position = current_stepper_position - self.stepper_steps_until_controller_update
                if target_stepper_position < self.max_brightness_position:
                    target_stepper_position = self.max_brightness_position   

        elif indoor_sensor_measurement > setpoint + self.hysteresis_value:
            #close blinds to decrease incoming brightness
            if current_stepper_position < self.max_brightness_position:
                target_stepper_position = current_stepper_position - self.stepper_steps_until_controller_update
                if target_stepper_position < 0:
                    target_stepper_position = 0
            elif current_stepper_position > self.max_brightness_position:
                target_stepper_position = current_stepper_position + self.stepper_steps_until_controller_update
                if target_stepper_position > self.full_range_steps:
                    target_stepper_position = self.full_range_steps

        else:
            #in hysteresis range
            target_stepper_position = current_stepper_position

        return target_stepper_position
