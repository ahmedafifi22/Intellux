import time
import os
from pathlib import Path

from Stepper_17HS4023_Driver_L298N import Pi_17HS4023_L298N

class calibrate_intellux:
    '''intellux calibration class with target of finding full range steps'''
    def __init__(self):
        self.stepper_motor = Pi_17HS4023_L298N(in1=13, in2=11, in3=15, in4=12, enable_a=18, enable_b=16)
