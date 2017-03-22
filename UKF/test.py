import numpy as np
import filters

Ts = 5  # based on the noble library measurement acquiring Ts

Vx = Vy = Px = Py = 0
current_state_mean = np.array([Vx, Vy, Px, Py]).reshape(4, 1)

# Error Covariance
# from previous testing results using 1 estimote and 2 minew (using all estimotes will make a better error covariance)
Px_cov = 0.25
Py_cov = 0.23
Vx_cov = (Px_cov / Ts) ** 2  # as an error propagation formula of Vx = Px/Ts
Vy_cov = (Py_cov / Ts) ** 2

current_state_error_cov = np.diag([Vx_cov, Vy_cov, Px_cov, Py_cov])

process_noise = np.array([(Ts ** 2) / 8, (Ts ** 2) / 8, Ts / 2, Ts / 2])  # assumptions for P and integral errors for V
measurement_noise = np.array([(0.24 / Ts) ** 2, (0.24 / Ts) ** 2, 0.24, 0.24])  # according to testing data analysis

measurement = np.array([0, 0, 0, 0])

try:
    file_hand = open('measurements.txt')
except:
    print 'no data measurements file with the exact name of \"measurements.txt\"'
    exit()
for line in file_hand:

    measurement[2] = line.split()[0]
    measurement[3] = line.split()[2]
    [filtered_state_mean, filtered_state_cov] = filters.ukf(current_state_mean, current_state_error_cov, measurement, Ts, process_noise, measurement_noise)
    [current_state_mean, current_state_error_cov] = [filtered_state_mean, filtered_state_cov]

