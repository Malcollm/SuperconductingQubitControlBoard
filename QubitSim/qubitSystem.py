from blochVector import BlochVector
import math
import numpy as np


class QubitSystem:
    def __init__(self, k, stages=64, rez=10, stage_period=1, shape="-"):
        self.state = BlochVector()
        self.k = k
        self.stages = stages
        self.rez = rez  # X bit DAC
        self.stage_period = stage_period
        self.shape = shape

        self.pulses_I = np.zeros(self.stages)
        self.pulses_Q = np.zeros(self.stages)


    def apply_microwave_pulse(self, pulse_length, amp, phase):
        self.state.rotate(phase, pulse_length * amp * self.k)

    def apply_mixer(self, pulse_length, I, Q):
        self.apply_microwave_pulse(pulse_length, math.sqrt(I**2 + Q**2), math.atan2(Q, I))

    def rotate_anl(self, rot_phase, angle_phase):
        if self.shape == "-":
            delta_rot_phase = rot_phase / self.stages
            for i in range(self.stages):
                self.pulses_I[i] = (delta_rot_phase * math.cos(angle_phase)) / (self.k * self.stage_period)
                self.pulses_Q[i] = (delta_rot_phase * math.sin(angle_phase)) / (self.k * self.stage_period)
                self.apply_mixer(self.stage_period, self.pulses_I[i], self.pulses_Q[i])
