import sys
sys.path.append("..")
import RPi.GPIO as GPIO
import argparse
import time

from Intellux import Pi_28BYJ_48
from Intellux import Pi_ADS1115, Pi_TEMT6000
from Intellux import Auto_Mode_Controller


def launch_automode(required_setpoint, degrees_until_controller_update, indoor_sensor_mount_angle, hysteresis_value):
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM) #defines naming convention to be used for the pins

    adc = Pi_ADS1115()
    indoor_lux_sensor_instance = Pi_TEMT6000(adc_instance=adc, adc_channel_used=0, gain=1)
    outdoor_lux_sensor_instance = Pi_TEMT6000(adc_instance=adc, adc_channel_used=1, gain=1)
    
    stepper_motor = Pi_28BYJ_48(in1=17, in2=18, in3=27, in4=22)
    controller = Auto_Mode_Controller(degrees_until_controller_update, indoor_sensor_mount_angle, hysteresis_value)

    print('Required Setpoint | Current indoor sensor voltage |  Current outdoor sensor voltage  | new_stepper_position |')
    print('-' * 37)
    while True:
        indoor_sensor_voltage = indoor_lux_sensor_instance.get_sensor_input_voltage()
        outdoor_sensor_voltage = outdoor_lux_sensor_instance.get_sensor_input_voltage()
        current_stepper_position = stepper_motor.motor_global_step_counter

        if controller.check_setpoint_achievable(required_setpoint, outdoor_sensor_voltage):
            new_stepper_position = controller.controller_update(required_setpoint, indoor_sensor_voltage, current_stepper_position)
            stepper_motor.move_to_required_stepper_position(required_stepper_motor_position)
        else:
            #communicate to UI
            Print("Setpoint {} not achievable, outdoor lighting is: {}".format(required_setpoint, outdoor_sensor_voltage))
            pass 

        print('| {} | {} | {} | {} | {} | {} |'.format(required_setpoint, indoor_sensor_voltage, outdoor_sensor_voltage, new_stepper_position))
        time.sleep(0.1)             
    GPIO.cleanup()
    
if __name__=='__main__':
    parser = argparse.ArgumentParser(description='please input the required setpoint (0-3.3v) to launch auto mode')
    parser.add_argument('-s', '--setpoint', required=True, type=int, help='The required setpoint')
    args = parser.parse_args()

    setpoint = float(args.setpoint)
    indoor_sensor_mount_angle = 90
    degrees_until_controller_update = 1 
    hysteresis_value = 0.1
    
    launch_automode(required_setpoint, degrees_until_controller_update, indoor_sensor_mount_angle, hysteresis_value)
      