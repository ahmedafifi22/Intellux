import RPi.GPIO as GPIO
import time


class Pi_photoresistor:
    """Class getting input from a photoresistor using Rasberry Pi"""

    def __init__(self, pin_number_used=12):
        self.pin_number_used = pin_number_used

#scp -r "C:\Users\Dell\Desktop\current_development_projects\Intellux\Intellux" pi@192.168.0.64:~/development_projects/intellux