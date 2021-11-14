import RPi.GPIO as GPIO
import time


class Pi_LED:
    """Class for contolling an LED using Rasberry Pi"""

    def __init__(self, pin_number_used=12):
        self.pin_number_used = pin_number_used
        pi_pwm_pins = {12, 35, 40}
        if self.pin_number_used in pi_pwm_pins:
            self.setup_pwm_output()
        else:
            self.setup_digital_output()

    def setup_pwm_output(self):
        GPIO.setup(self.pin_number_used, GPIO.OUT)
        self.pwm_instance = GPIO.PWM(self.pin_number_used, 100)
        self.pwm_instance.start(0) #start pwm with 0% duty cycle

    def setup_digital_output(self):
        GPIO.setup(self.pin_number_used, GPIO.OUT)
        GPIO.output(self.pin_number_used, GPIO.LOW) #start with LED off

    def change_led_duty_cycle(self, duty_cycle):
        self.pwm_instance.ChangeDutyCycle(duty_cycle)

    def change_led_digital_output(self, led_status):
        if led_status == 1:
            GPIO.output(self.pin_number_used, GPIO.HIGH)
        elif led_status == 0:
            GPIO.output(self.pin_number_used, GPIO.LOW)
        else:
            raise ValueError("led_status must be one of %r." % valid_led_status)
