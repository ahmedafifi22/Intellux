import time
import Adafruit_ADS1x15

class Pi_ADS1115:
    """Class to setup the Adafruit ADS1115 analog to digital converter for use in the scope of the intellux project"""

    def __init__(self):
        self.adc_instance = Adafruit_ADS1x15.ADS1115()
        self.gain_FSR_dict = { #full scale input range of the ADC which is defined in datasheet
            2/3: 6.144,
            1:   4.096,
            2:   2.048,
            4:   1.024,
            8:   0.512,
            16:  0.256}

    def get_voltage_input_from_channel(self, channel_num, gain=1):
        digital_output_code = self.adc_instance.read_adc(channel_num, gain=gain)
        FSR = 2 * self.gain_FSR_dict[gain] # multiply by two since we need to account for the +- 
        LSB_size = FSR / (2**16) #This is the resolution (weight of the least significant bit)
        input_voltage = digital_output_code * LSB_size
        return input_voltage

