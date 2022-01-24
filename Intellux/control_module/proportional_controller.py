import time

class p_controller:
    '''Proportional controller for intellux apparatus

        derived discrete PID equations:
            p[n]= Kp * e[n] 
            controller output = p[n] 

        Parameters:
            Kp (float): constant gain for the proportional component of the controller
            T (float): sampling time
            sensor_voltage_output_lim_min (float): minimum possible output that the sensor voltage could get to
            sensor_voltage_output_lim_max (float): maximum possible output that the sensor voltage could get to
    '''
    def __init__(self, Kp, T, sensor_voltage_output_lim_min, sensor_voltage_output_lim_max):
        self.Kp = Kp
        self.sample_time = T
        self.sensor_voltage_output_lim_min = sensor_voltage_output_lim_min
        self.sensor_voltage_output_lim_max = sensor_voltage_output_lim_max

        self.P_term = 0
        self.time_of_last_controller_update = time.time()

    def controller_update(self, setpoint_voltage, current_sensor_voltage):
        '''
        Calculates Proportional correction value for given sensor feedback
    
        Parameters:
            setpoint_voltage (float): desired setpoint that controller should get to
            current_sensor_voltage (float): current sensor reading 
            current_stepper_position (int): current stepper motor position 
        Returns:
            output (float): controller output
        '''
        current_time = time.time()
        delta_time = current_time - self.time_of_last_controller_update
        if delta_time >= self.sample_time:
            error = setpoint_voltage - current_sensor_voltage
            self.P_term = self.Kp * error

            target_correction = self.P_term 
            target_sensor_voltage_output = current_sensor_voltage + target_correction            

            #Controller output feasibility check
            if target_sensor_voltage_output > self.sensor_voltage_output_lim_max:
                target_sensor_voltage_output = self.sensor_voltage_output_lim_max
            elif target_sensor_voltage_output < self.sensor_voltage_output_lim_min:
                target_sensor_voltage_output = self.sensor_voltage_output_lim_min
            else:
                target_sensor_voltage_output = target_sensor_voltage_output

            self.time_of_last_controller_update = current_time
            return target_sensor_voltage_output

    def clear(self):
        '''Clears controller computations and coefficients'''
        self.P_term = 0
        self.time_of_last_controller_update = time.time()
