import sys
sys.path.append("..")
import RPi.GPIO as GPIO
import time

from Intellux import Pi_ADS1115, Pi_TEMT6000

def test_sensors():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM) #defines naming convention to be used for the pins

    adc = Pi_ADS1115()
    indoor_lux_sensor_instance = Pi_TEMT6000(adc_instance=adc, adc_channel_used=0, gain=1)
    outdoor_lux_sensor_instance = Pi_TEMT6000(adc_instance=adc, adc_channel_used=3, gain=1)
    
    print('Current indoor sensor voltage |  Current outdoor sensor voltage')
    print('-' * 37)
    while True:
        indoor_sensor_voltage = indoor_lux_sensor_instance.get_sensor_input_voltage()
        outdoor_sensor_voltage = outdoor_lux_sensor_instance.get_sensor_input_voltage()
        print('| {} | {} |'.format(indoor_sensor_voltage, outdoor_sensor_voltage))

if __name__=='__main__':
    test_sensors()