import time

class on_off_controller:
    '''on/off controller for intellux apparatus'''
    def __init__(self, Kp, T, setpoint, output_lim_min, output_lim_max):
        self.Kp = Kp
        self.sample_time = T
        self.setpoint = setpoint
        self.output_lim_min = output_lim_min
        self.output_lim_max = output_lim_max

        self.P_term = 0
        self.time_of_last_controller_update = time.time()

    def controller_update(self, indoor_sensor_measurement):
        '''
        Calculates Proportional correction value for given sensor feedback
    
        Parameters:
            sensor_measurement (float): current sensor reading 
        Returns:
            output (float): controller output
        '''
        current_time = time.time()
        delta_time = current_time - self.time_of_last_controller_update
        if delta_time >= self.sample_time:
            error = self.setpoint - indoor_sensor_measurement
            self.P_term = self.Kp * error

            target_correction = self.P_term 
            target_sensor_voltage_output = indoor_sensor_measurement + target_correction            

            #Controller output feasibility check
            if target_sensor_voltage_output > self.output_lim_max:
                target_sensor_voltage_output = self.output_lim_max
            elif target_sensor_voltage_output < self.output_lim_min:
                target_sensor_voltage_output = self.output_lim_min
            else:
                target_sensor_voltage_output = target_sensor_voltage_output

            self.time_of_last_controller_update = current_time
            return target_sensor_voltage_output

    def map_to_stepper_position(self):
        jhf
    
    def update_setpoint(self, setpoint):
        '''
        updates the desired the setpoint that the controller tries to get to
    
        Parameters:
            setpoint (float): New desired setpoint
        '''
        self.setpoint = setpoint

    def clear(self):
        '''Clears controller computations and coefficients'''
        self.P_term = 0
        self.time_of_last_controller_update = time.time()


