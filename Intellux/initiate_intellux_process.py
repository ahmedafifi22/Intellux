import RPi.GPIO as GPIO
import time

from end_effector_movement import Pi_LED


if __name__=='__main__':
    GPIO.setmode(GPIO.BOARD) #defines naming convention to be used for the pins
    led = Pi_LED(pin_number_used=12)
    
    try:
        while True:                      # Loop until Ctl C is pressed to stop.
            for duty_cycle in range(0, 101, 5):    # Loop 0 to 100 stepping duty_cycle by 5 each loop
                led.change_led_duty_cycle(duty_cycle)
                time.sleep(0.05)             # wait .05 seconds at current LED brightness
                print(duty_cycle)
            for duty_cycle in range(95, 0, -5):    # Loop 95 to 5 stepping duty_cycle down by 5 each loop
                led.change_led_duty_cycle(duty_cycle)
                time.sleep(0.05)             # wait .05 seconds at current LED brightness
                print(duty_cycle)
    
    except KeyboardInterrupt:
        print("Ctl C pressed - ending program")

    led.pwm_instance.stop()                         # stop PWM
    GPIO.cleanup()                     # resets GPIO ports used back to input mode


