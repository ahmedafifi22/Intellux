import RPi.GPIO as GPIO
import Adafruit_ADS1x15
import time


class Pi_TEMT6000:
    """Class getting input from a photoresistor using Rasberry Pi"""

    def __init__(self, adc_instance, adc_channel_used=0, gain=1):
        self.adc_instance = adc_instance
        self.adc_channel_used = adc_channel_used
        self.gain = gain

    def get_sensor_input_voltage(self):
        return self.adc_instance.get_voltage_input_from_channel(self.adc_channel_used, self.gain)

