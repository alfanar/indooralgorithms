import numpy as np

import cov, models




def ukf(current_state_mean,current_state_error_cov,measurement,Ts,process_noise,measurement_noise):
    
    # Glossary:
    #
    # nx: state vector size
    # ssp: state sigma points
    # msp: measurement sigma points
    # pnssp: predicted next state sigma points
    # ussp: update state sigma points
    # umsp: updated measurement sigma points
    # zn: zero noise
    # st: state telda
    # pnsm: predicted next state mean
    # pnsec: predicted next state error covariance
    # mm: measurement mean
    # mc: measurement covariance
    # ust: updated state telda
    # pmm: predicted measurement mean
    # pmc: predicted measurement covariance
    # pmcc: predicted measurement cross covariance
    # kg: kalman gain

    # pad the current state mean vector with 0s for the new beacons data
    current_state_mean = np.pad(current_state_mean,(0,len(measurement)-len(current_state_mean)),'constant')

    nx = len(current_state_mean)

    ssp = np.zeros(shape=(nx, 2 * nx))
    msp = np.zeros(shape=(nx, 2 * nx))
    pnssp = np.zeros(shape=(nx, 2 * nx))
    ussp = np.zeros(shape=(nx, 2 * nx))
    umsp = np.zeros(shape=(nx, 2 * nx))

    # %%%%%%%%%%%%%%%%%%%%%%%%%%%
    # % 1) get the segma points %
    # %%%%%%%%%%%%%%%%%%%%%%%%%%%
    st = np.linalg.cholesky(nx * current_state_error_cov)

    for i in range(0, nx):
        ssp.T[i] = current_state_mean + st.T[i]

    for i in range(nx, 2*nx):
        ssp.T[i] = current_state_mean - st.T[i - nx]

    # %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # % 2) time update (prediction step) %
    # %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    for i in range(0, 2*nx):
        pnssp.T[i] = models.process_model(ssp.T[i], Ts, process_noise)

    pnsm = np.mean(pnssp, 1)
    pnsec = cov.covariance_vector(pnssp, pnsm, pnssp, pnsm, 2 * nx)

    # %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # % 3) estimate measurement mean and covariance using sigma points %
    # %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    for i in range(0, 2 * nx):
        msp.T[i] = models.measurement_model(ssp.T[i], Ts, measurement_noise)

    mm = np.mean(msp, 1)
    mc = cov.covariance_vector(msp, mm, msp, mm, 2 * nx)

    # %%%%%%%%%%%%%%%%%%%%%%%%%%
    # % 4) sigma points update %
    # %%%%%%%%%%%%%%%%%%%%%%%%%%
    ust = np.linalg.cholesky(nx * pnsec)

    for i in range(0, nx):
        ussp.T[i] = pnsm + ust.T[i]

    for i in range(nx, 2 * nx):
        ussp.T[i] = pnsm - ust.T[i - nx]

    # %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # % 5) measurement update (filter step) %
    # %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    for i in range(0, 2 * nx):
        umsp.T[i] = models.measurement_model(ussp.T[i], Ts, measurement_noise)

    pmm = np.mean(umsp, 1)
    pmc = cov.covariance_vector(umsp, pmm, umsp, pmm, 2 * nx) + mc

    psmcc = cov.covariance_vector(ussp, pnsm, umsp, pmm, 2 * nx)

    kg = np.dot(psmcc, np.linalg.inv(pmc))

    filtered_state_mean = pnsm + np.dot(kg, (measurement - pmm))
    filtered_state_cov = pnsec - np.dot(np.dot(kg, pmc), kg.T)

    return [filtered_state_mean, filtered_state_cov]
