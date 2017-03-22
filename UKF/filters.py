import numpy as np

import cov, models




def ukf(current_state_mean, current_state_error_cov, measurement, Ts, process_noise, measurement_noise):

    current_state_mean = np.pad(current_state_mean,(0,len(measurement)-len(current_state_mean)),'constant') #pad the current state mean vector with 0s for the new beacons data

    state_vector_size = len(current_state_mean)

    state_sigma_points = np.zeros(shape=(state_vector_size, 2 * state_vector_size))
    measurement_sigma_points = np.zeros(shape=(state_vector_size, 2 * state_vector_size))
    predicted_next_state_sigma_points = np.zeros(shape=(state_vector_size, 2 * state_vector_size))
    updated_state_sigma_points = np.zeros(shape=(state_vector_size, 2 * state_vector_size))
    updated_measurement_sigma_points = np.zeros(shape=(state_vector_size, 2 * state_vector_size))

    # %%%%%%%%%%%%%%%%%%%%%%%%%%%
    # % 1) get the segma points %
    # %%%%%%%%%%%%%%%%%%%%%%%%%%%
    state_telda = np.linalg.cholesky(state_vector_size * current_state_error_cov)

    for i in range(0, state_vector_size):
        state_sigma_points.T[i] = current_state_mean + state_telda.T[i]

    for i in range(state_vector_size, 2*state_vector_size):
        state_sigma_points.T[i] = current_state_mean - state_telda.T[i - state_vector_size]

    # %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # % 2) time update (prediction step) %
    # %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    for i in range(0, 2*state_vector_size):
        predicted_next_state_sigma_points.T[i] = models.process_model(state_sigma_points.T[i], Ts, process_noise)

    predicted_next_state_mean = np.mean(predicted_next_state_sigma_points, 1)
    predicted_next_state_error_cov = cov.covariance_vector(predicted_next_state_sigma_points, predicted_next_state_mean,
                                                       predicted_next_state_sigma_points, predicted_next_state_mean,
                                                       2 * state_vector_size)

    # %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # % 3) estimate measurement mean and covariance using sigma points %
    # %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    for i in range(0, 2 * state_vector_size):
        measurement_sigma_points.T[i] = models.measurement_model(state_sigma_points.T[i], Ts, measurement_noise)

    measurement_mean = np.mean(measurement_sigma_points, 1)
    measurement_cov = cov.covariance_vector(measurement_sigma_points, measurement_mean, measurement_sigma_points,
                                        measurement_mean, 2 * state_vector_size)

    # %%%%%%%%%%%%%%%%%%%%%%%%%%
    # % 4) sigma points update %
    # %%%%%%%%%%%%%%%%%%%%%%%%%%
    updated_state_telda = np.linalg.cholesky(state_vector_size * predicted_next_state_error_cov)

    for i in range(0, state_vector_size):
        updated_state_sigma_points.T[i] = predicted_next_state_mean + updated_state_telda.T[i]

    for i in range(state_vector_size, 2 * state_vector_size):
        updated_state_sigma_points.T[i] = predicted_next_state_mean - updated_state_telda.T[i - state_vector_size]

    # %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # % 5) measurement update (filter step) %
    # %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    for i in range(0, 2 * state_vector_size):
        updated_measurement_sigma_points.T[i] = models.measurement_model(updated_state_sigma_points.T[i], Ts, measurement_noise)

    predicted_measurement_mean = np.mean(updated_measurement_sigma_points, 1)
    predicted_measurement_cov = cov.covariance_vector(updated_measurement_sigma_points, predicted_measurement_mean,
                                                  updated_measurement_sigma_points, predicted_measurement_mean,
                                                  2 * state_vector_size)

    predicted_state_measurement_cross_cov = cov.covariance_vector(updated_state_sigma_points, predicted_next_state_mean,
                                                              updated_measurement_sigma_points,
                                                              predicted_measurement_mean, 2 * state_vector_size)

    kalman_gain = np.dot(predicted_state_measurement_cross_cov, np.linalg.inv(predicted_measurement_cov))

    filtered_state_mean = predicted_next_state_mean + np.dot(kalman_gain, (measurement - predicted_measurement_mean))
    filtered_state_cov = predicted_next_state_error_cov - np.dot(np.dot(kalman_gain, predicted_measurement_cov),
                                                                 kalman_gain.T)

    return [filtered_state_mean, filtered_state_cov]
