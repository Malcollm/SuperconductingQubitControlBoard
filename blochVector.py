import numpy as np


class BlochVector:
    def __init__(self, rabi_freq, init_state=None):
        if init_state is None:
            init_state = np.array([ [0], [0], [1] ])
        self.state = []
        for item in init_state:
            self.state.append(item)
        self.state = np.array(self.state)

        self.rabi_freq = rabi_freq

    def rotate_x(self, angle):
        r = np.array([
            [1, 0, 0],
            [0, np.cos(angle), -np.sin(angle)],
            [0, np.sin(angle), np.cos(angle)]
        ])

        self.state = r @ self.state

    def rotate_y(self, angle):
        r = np.array([
            [np.cos(angle), 0, np.sin(angle)],
            [0, 1, 0],
            [-np.sin(angle), 0, np.cos(angle)]
        ])

        self.state = r @ self.state

    def get_state(self):
        output = []
        for item in self.state:
            output.append(item[0])
        return output

    def rotate(self, phase, pulse_length):
        theta = self.rabi_freq * pulse_length
        r = np.array([
            [np.cos(theta) + np.cos(phase) ** 2 * (1 - np.cos(theta)), np.cos(phase) * np.sin(phase) * (1 - np.cos(theta)), np.sin(phase) * np.sin(theta)],
            [np.cos(phase) * np.sin(phase) * (1 - np.cos(theta)), np.cos(theta) + np.sin(phase) ** 2 * (1 - np.cos(theta)), -np.cos(phase) * np.sin(theta)],
            [-np.sin(phase) * np.sin(theta), np.cos(phase) * np.sin(theta), np.cos(theta)]
        ])

        self.state = r @ self.state
