import RPi.GPIO as GPIO
import time
import sys

from mechanical_module import Pi_28BYJ_48
from sensors_module import Pi_ADS1115, Pi_TEMT6000
from control_module import p_controller

def test_sensor_output():
    GPIO.setmode(GPIO.BOARD) #defines naming convention to be used for the pins
    led = Pi_LED(pin_number_used=12)
    
    adc = Pi_ADS1115()
    light_sensor_instance = Pi_TEMT6000(adc_instance=adc, adc_channel_used=0, gain=1)

    print('| led duty cycle | sensor voltage |')
    print('-' * 37)
    try:
        while True:
            for duty_cycle in range(0, 101, 5):    # Loop 0 to 100 stepping duty_cycle by 5 each loop
                led.change_led_duty_cycle(duty_cycle)
                time.sleep(0.5)             # wait .05 seconds at current LED brightness
                value = light_sensor_instance.get_sensor_input_voltage()
                print('{} | {} |'.format(duty_cycle, value))
            for duty_cycle in range(95, 0, -5):    # Loop 95 to 5 stepping duty_cycle down by 5 each loop
                led.change_led_duty_cycle(duty_cycle)
                time.sleep(0.5)             # wait .05 seconds at current LED brightness
                value = light_sensor_instance.get_sensor_input_voltage()
                print('{} | {} |'.format(duty_cycle, value))
    
    except KeyboardInterrupt:
        print("Ctl C pressed - ending program")

    led.pwm_instance.stop()                         # stop PWM
    GPIO.cleanup()                     # resets GPIO ports used back to input mode


if __name__=='__main__':
    required_blinds_angle = int(sys.argv[1])
    test_manual_mode_v2(required_blinds_angle)
      
#scp -r "C:\Users\Dell\Desktop\current_development_projects\Intellux\Intellux" pi@192.168.0.64:~/development_projects/intellux
