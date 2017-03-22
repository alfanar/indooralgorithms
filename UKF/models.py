import numpy as np


def measurement_model(state, Ts, measurement_noise,type='VP'):

    if type == 'VP':

        V0 = state[0:2]
        P0 = state[2:4]

        Vnoise = measurement_noise[0:2]
        Pnoise = measurement_noise[2:4]

        V = V0 + Vnoise
        P = P0 + (Ts / 2) * (V0 + V) + Pnoise

        next_state = np.concatenate((V, P))

        return next_state


def process_model(state, Ts, process_noise,type='VP'):

    if type == 'VP':

        V0 = state[0:2]
        P0 = state[2:4]

        Vnoise = process_noise[0:2]
        Pnoise = process_noise[2:4]

        V = V0 + Vnoise
        P = P0 + (Ts / 2) * (V0 + V) + Pnoise

        next_state = np.concatenate((V, P))

        return next_state