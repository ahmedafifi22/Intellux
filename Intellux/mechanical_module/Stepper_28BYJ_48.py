import RPi.GPIO as GPIO
import time
import os
import numpy as np
from pathlib import Path


class Pi_28BYJ_48:
    """Class for contolling the 28BYJ-48 stepper motor using Rasberry Pi"""
    def __init__(self, in1=17, in2=18, in3=27, in4=22):
        self.in1 = in1
        self.in2 = in2
        self.in3 = in3
        self.in4 = in4

        self.setup_motor_pins()
        
        self.motor_pins = [in1,in2,in3,in4]
        
        self.full_revolution_step_count = 4096 #5.625*(1/64) per step, 4096 steps is 360°

        # careful lowering this, at some point you run into the mechanical limitation of how quick your motor can move
        self.step_sleep = 0.002 #2 milliseconds
        
        # defining stepper motor sequence (found in documentation http://www.4tronix.co.uk/arduino/Stepper-Motors.php)
        self.step_sequence = [[1,0,0,1],
                            [1,0,0,0],
                            [1,1,0,0],
                            [0,1,0,0],
                            [0,1,1,0],
                            [0,0,1,0],
                            [0,0,1,1],
                            [0,0,0,1]]

        self.root = Path(os.path.abspath(__file__)).parents[0]
        self.index_files_directory = os.path.join(self.root,'stepper_position')
        if os.path.isdir(self.index_files_directory) == False:
            os.mkdir(self.index_files_directory)
            print(self.index_files_directory)

        self.motor_step_sequence_counter_file = os.path.join(self.index_files_directory, 'motor_step_sequence_counter.npy') # To Load the previous index
        self.motor_global_step_counter_file = os.path.join(self.index_files_directory, 'motor_global_step_counter.npy') # To Load the previous index
        
        if os.path.isfile(self.motor_step_sequence_counter_file) == True: #Load previous index
            self.motor_step_sequence_counter = np.load(self.motor_step_sequence_counter_file)
        else:
            with open(self.motor_step_sequence_counter_file, 'wb') as f:
                np.save(f, 0)
            self.motor_step_sequence_counter = np.load(self.motor_step_sequence_counter_file)
        
        if os.path.isfile(self.motor_global_step_counter_file) == True: #Load previous index
            self.motor_global_step_counter = np.load(self.motor_global_step_counter_file)
        else:
            with open(self.motor_global_step_counter_file, 'wb') as f:
                np.save(f, 0)
            self.motor_global_step_counter = np.load(self.motor_global_step_counter_file)

    def setup_motor_pins(self):
        # setting up
        GPIO.setup(self.in1, GPIO.OUT)
        GPIO.setup(self.in2, GPIO.OUT)
        GPIO.setup(self.in3, GPIO.OUT)
        GPIO.setup(self.in4, GPIO.OUT)
        
        # initializing
        GPIO.output(self.in1, GPIO.LOW)
        GPIO.output(self.in2, GPIO.LOW)
        GPIO.output(self.in3, GPIO.LOW)
        GPIO.output(self.in4, GPIO.LOW)

    def turn_CW(self, num_of_steps):
        for i in range(num_of_steps):
            self.motor_step_sequence_counter = (self.motor_step_sequence_counter - 1) % 8
            for pin in range(0, len(self.motor_pins)):
                GPIO.output( self.motor_pins[pin], self.step_sequence[self.motor_step_sequence_counter][pin] )
            time.sleep(self.step_sleep)
            self.motor_global_step_counter = self.motor_global_step_counter + 1  

    def turn_CCW(self, num_of_steps):
        for i in range(num_of_steps):
            self.motor_step_sequence_counter = (self.motor_step_sequence_counter + 1) % 8
            for pin in range(0, len(self.motor_pins)):
                GPIO.output( self.motor_pins[pin], self.step_sequence[self.motor_step_sequence_counter][pin] )
            time.sleep(self.step_sleep)
            self.motor_global_step_counter = self.motor_global_step_counter - 1
            assert(self.motor_global_step_counter >= 0)

    def move_to_required_stepper_position(self, required_stepper_position):
        steps_difference = required_stepper_position - self.motor_global_step_counter
        if steps_difference < 0:
            self.turn_CCW(abs(steps_difference))
            assert(required_stepper_position == self.motor_global_step_counter)
            self.save_stepper_positions()
            print(self.motor_global_step_counter)
        elif steps_difference > 0:
            self.turn_CW(steps_difference)
            assert(required_stepper_position == self.motor_global_step_counter)
            self.save_stepper_positions()
            print(self.motor_global_step_counter)
        else:
            self.save_stepper_positions()

    def save_stepper_positions(self):
        np.save(self.motor_step_sequence_counter_file, self.motor_step_sequence_counter)
        np.save(self.motor_global_step_counter_file, self.motor_global_step_counter)

    def cleanup(self):
        GPIO.output(self.in1, GPIO.LOW)
        GPIO.output(self.in2, GPIO.LOW)
        GPIO.output(self.in3, GPIO.LOW)
        GPIO.output(self.in4, GPIO.LOW)
        GPIO.cleanup()




