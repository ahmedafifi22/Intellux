import matplotlib
import time
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import make_interp_spline
from PID_v1 import PID

def PID_v1_test(Kp, Ki, Kd, T, setpoint, output_lim_min, output_lim_max):
    pid = PID(Kp, Ki, Kd, T, setpoint, output_lim_min, output_lim_max)
    total_sampling = 300
    feedback = 0

    feedback_list = []
    time_list = []
    setpoint_list = []

    print("simulating....")
    for i in range(1, total_sampling):
        output = pid.controller_update(feedback)
        if pid.setpoint > 0:
            feedback = feedback + (output - (1 / i))

        if 20 < i < 70:
            pid.update_setpoint(1)

        if 70 <= i < 120:
            pid.update_setpoint(0.5)

        if i >= 120:
            pid.update_setpoint(1.3)

        time.sleep(0.02)
        feedback_list.append(feedback)
        setpoint_list.append(pid.setpoint)
        time_list.append(i)

    time_sm = np.array(time_list)
    time_smooth = np.linspace(time_sm.min(), time_sm.max(), 300)
    feedback_smooth = make_interp_spline(time_list, feedback_list)(time_smooth)

    fig1 = plt.gcf()
    fig1.subplots_adjust(bottom=0.15)

    plt.plot(time_smooth, feedback_smooth, color='red')
    plt.plot(time_list, setpoint_list, color='blue')
    plt.xlim((0, total_sampling))
    plt.ylim((min(feedback_list) - 0.5, max(feedback_list) + 0.5))
    plt.xlabel('time (s)')
    plt.ylabel('PID (PV)')
    plt.title('TEST INTELLUX PID')
    plt.grid(True)
    print("Displaying Results...")
    plt.show()

if __name__=='__main__':
    Kp = 0.5
    Ki = 1
    Kd = 0.0001
    T = 0.01
    setpoint = 0
    output_lim_min = -20
    output_lim_max = 20
    PID_v1_test(Kp, Ki, Kd, T, setpoint, output_lim_min, output_lim_max)
