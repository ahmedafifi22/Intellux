import time

class PID:
    '''PID controller class for intellux

        derived discrete PID equations:
            p[n]= Kp * e[n] 
            i[n] = i[n-1] + ((Ki * T * (e[n] + e[n-1])) / 2)
            d[n] = (Kd * 2 * (e[n] - e[n-1]) / T) - d[n-1]
            controller output = p[n] + i[n] + d[n]

        Parameters:
            Kp (float): constant gain for the proportional component of the PID controller
            Ki (float): constant gain for the integrator component of the PID controller
            Kd (float): constant gain for the differentiator component of the PID controller
            T (float): sampling time
            setpoint (float): desired setpoint that controller should get to
            output_lim_min (float): minimum possible output that the system could get to
            output_lim_max (float): maximum possible output that the system could get to
    '''
    def __init__(self, Kp, Ki, Kd, T, setpoint, output_lim_min, output_lim_max):
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.sample_time = T
        self.setpoint = setpoint
        self.output_lim_min = output_lim_min
        self.output_lim_max = output_lim_max

        self.prev_error = 0
        self.prev_output = 0
        self.prev_measurement = 0
        self.P_term = 0
        self.I_term = 0
        self.D_term = 0
        self.time_of_last_controller_update = time.time()

    def controller_update(self, sensor_measurement):
        '''
        Calculates PID correction value for given sensor feedback
    
        Parameters:
            sensor_measurement (float): current sensor reading 
        Returns:
            output (float): controller output
        '''
        current_time = time.time()
        delta_time = current_time - self.time_of_last_controller_update
        if delta_time >= self.sample_time:
            error = self.setpoint - sensor_measurement
            self.P_term = self.Kp * error
            self.I_term = self.I_term + (0.5 * self.Ki * self.sample_time * (error + self.prev_error))
            #self.D_term = ((self.Kd * 2 * (error - self.prev_error)) / self.sample_time) - self.D_term
            self.D_term = ((self.Kd * 2 * (sensor_measurement - self.prev_measurement)) / self.sample_time) - self.D_term

            #dynamic integrator clamping
            #calculate integrator limits
            integrator_lim_max = max((self.output_lim_max - self.P_term) , 0)
            integrator_lim_min = min(0, (self.output_lim_min - self.P_term))

            #Anti-windup via integrator clamping
            if self.I_term > integrator_lim_max:
                self.I_term = integrator_lim_max
            elif self.I_term < integrator_lim_min:
                self.I_term = integrator_lim_min
            else:
                self.I_term = self.I_term
            
            output = self.P_term + self.I_term + self.D_term

            #Controller output feasibility check
            if output > self.output_lim_max:
                output = self.output_lim_max
            elif output < self.output_lim_min:
                output = self.output_lim_min
            else:
                output = output

            self.prev_error = error
            self.prev_output = output
            self.prev_measurement = sensor_measurement
            self.time_of_last_controller_update = current_time
            return output

    def update_setpoint(self, setpoint):
        '''
        updates the desired the setpoint that the controller tries to get to
    
        Parameters:
            setpoint (float): New desired setpoint
        '''
        self.setpoint = setpoint

    def clear(self):
        '''Clears PID computations and coefficients'''
        self.prev_error = 0
        self.prev_output = 0
        self.prev_measurement = 0
        self.P_term = 0
        self.I_term = 0
        self.D_term = 0
        self.time_of_last_controller_update = time.time()


