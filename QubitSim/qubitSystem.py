from blochVector import BlochVector
import math


class QubitSystem:
    def __init__(self, k):
        self.state = BlochVector()
        self.k = k

    def apply_microwave_pulse(self, pulse_length, amp, phase):
        self.state.rotate(phase, pulse_length * amp * self.k)

    def apply_mixer(self, pulse_length, I, Q):
        self.apply_microwave_pulse(pulse_length, math.sqrt(I**2 + Q**2), math.atan2(Q, I))
