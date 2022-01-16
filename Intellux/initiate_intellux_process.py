import RPi.GPIO as GPIO
import time
import sys

from mechanical_module import Pi_LED, Pi_28BYJ_48
from sensors_module import Pi_ADS1115, Pi_TEMT6000
from control_module import p_controller, Manual_Mode_Controller

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


def Control_room_brightness_using_LED():
    GPIO.setmode(GPIO.BOARD) #defines naming convention to be used for the pins
    led = Pi_LED(pin_number_used=12)
    
    adc = Pi_ADS1115()
    light_sensor_instance = Pi_TEMT6000(adc_instance=adc, adc_channel_used=0, gain=1)
    
    Kp = 0.5
    T = 0.01
    setpoint = 0.3 #specific voltage target
    output_lim_min = 0
    output_lim_max = 3.3
    p_cont = p_controller(Kp, T, setpoint, output_lim_min, output_lim_max)
    
    duty_cycle = 10
    time.sleep(0.5) 
    print('Setpoint | Current sensor voltage | Target sensor voltage | new led duty cycle |')
    print('-' * 37)
    
    try:
        while True:
            current_sensor_voltage_output = light_sensor_instance.get_sensor_input_voltage()
            target_sensor_voltage_output = p_cont.controller_update(current_sensor_voltage_output)
            duty_cycle = duty_cycle * (target_sensor_voltage_output / current_sensor_voltage_output)
            if duty_cycle > 100:
                duty_cycle = 100
            elif duty_cycle < 0:
                duty_cycle = 0
            else:
                duty_cycle = duty_cycle

            led.change_led_duty_cycle(duty_cycle)
            time.sleep(0.5)             # wait .05 seconds at current LED brightness
            value = light_sensor_instance.get_sensor_input_voltage()
            print('{} | {}| {}| {} '.format(setpoint, current_sensor_voltage_output, target_sensor_voltage_output, duty_cycle))
    
    except KeyboardInterrupt:
        print("Ctl C pressed - ending program")

    led.pwm_instance.stop()                         # stop PWM
    GPIO.cleanup()                     # resets GPIO ports used back to input mode

def test_manual_mode():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM) #defines naming convention to be used for the pins
    stepper_motor = Pi_28BYJ_48(in1=17, in2=18, in3=27, in4=22)
    controller = Manual_Mode_Controller()
    print(stepper_motor.motor_global_step_counter)

    while True:
        required_blinds_angle = int(input("Enter desired blinds angle: "))
        required_stepper_motor_position = controller.get_required_stepper_motor_position(required_blinds_angle)
        stepper_motor.move_to_required_stepper_position(required_stepper_motor_position)

def test_manual_mode_v2(required_blinds_angle):
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM) #defines naming convention to be used for the pins
    stepper_motor = Pi_28BYJ_48(in1=17, in2=18, in3=27, in4=22)
    controller = Manual_Mode_Controller()
    print(stepper_motor.motor_global_step_counter)
    required_stepper_motor_position = controller.get_required_stepper_motor_position(int(required_blinds_angle))
    stepper_motor.move_to_required_stepper_position(required_stepper_motor_position)

if __name__=='__main__':
    required_blinds_angle = int(sys.argv[1])
    test_manual_mode_v2(required_blinds_angle)
      
#scp -r "C:\Users\Dell\Desktop\current_development_projects\Intellux\Intellux" pi@192.168.0.64:~/development_projects/intellux
