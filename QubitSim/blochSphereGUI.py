import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button

from qubitSystem import QubitSystem

ANIMATION_STEPS = 40
FRAME_PAUSE = 0.02


class BlochSphereGUI:
    def __init__(self):
        self.qubit = QubitSystem(2 * math.pi)

        self.fig = plt.figure(figsize=(8, 9.5))
        self.ax = self.fig.add_subplot(111, projection="3d")
        self.fig.subplots_adjust(bottom=0.37)

        self._draw_static_sphere()
        self.trail_line, = self.ax.plot([], [], [], color="tab:red", linewidth=1)
        self.axis_line, = self.ax.plot([], [], [], color="tab:blue", linewidth=1.5, linestyle="--")
        self.arrow = None
        self.trail = []
        self._draw_state()

        self._build_controls()
        self._update_axis_line()

    def _draw_static_sphere(self):
        ax = self.ax
        u, v = np.mgrid[0:2 * np.pi:40j, 0:np.pi:20j]
        x = np.cos(u) * np.sin(v)
        y = np.sin(u) * np.sin(v)
        z = np.cos(v)
        ax.plot_wireframe(x, y, z, color="lightgray", linewidth=0.5, alpha=0.5)

        theta = np.linspace(0, 2 * np.pi, 200)
        ax.plot(np.cos(theta), np.sin(theta), np.zeros_like(theta), color="gray", linewidth=0.8)
        ax.plot(np.cos(theta), np.zeros_like(theta), np.sin(theta), color="gray", linewidth=0.5, alpha=0.4)
        ax.plot(np.zeros_like(theta), np.cos(theta), np.sin(theta), color="gray", linewidth=0.5, alpha=0.4)

        axis_len = 1.3
        ax.plot([-axis_len, axis_len], [0, 0], [0, 0], color="black", linewidth=0.7)
        ax.plot([0, 0], [-axis_len, axis_len], [0, 0], color="black", linewidth=0.7)
        ax.plot([0, 0], [0, 0], [-axis_len, axis_len], color="black", linewidth=0.7)

        ax.text(axis_len, 0, 0, "X", fontsize=10)
        ax.text(0, axis_len, 0, "Y", fontsize=10)
        ax.text(0, 0, axis_len + 0.1, "|0>", fontsize=10)
        ax.text(0, 0, -axis_len - 0.15, "|1>", fontsize=10)

        ax.set_box_aspect([1, 1, 1])
        ax.set_xlim(-1.4, 1.4)
        ax.set_ylim(-1.4, 1.4)
        ax.set_zlim(-1.4, 1.4)
        ax.set_axis_off()
        ax.set_title("Qubit Bloch Sphere")

    def _draw_state(self):
        x, y, z = self.qubit.state.get_state()

        if self.arrow is not None:
            self.arrow.remove()
        self.arrow = self.ax.quiver(0, 0, 0, x, y, z, color="tab:red", linewidth=2, arrow_length_ratio=0.12)

        self.trail.append((x, y, z))
        trail_arr = np.array(self.trail)
        self.trail_line.set_data(trail_arr[:, 0], trail_arr[:, 1])
        self.trail_line.set_3d_properties(trail_arr[:, 2])

    def _update_axis_line(self, event=None):
        I = self.slider_i.val
        Q = self.slider_q.val
        phase = math.atan2(Q, I)
        axis_len = 1.3
        dx, dy = axis_len * math.cos(phase), axis_len * math.sin(phase)
        self.axis_line.set_data([-dx, dx], [-dy, dy])
        self.axis_line.set_3d_properties([0, 0])
        self.fig.canvas.draw_idle()

    def _build_controls(self):
        axcolor = "whitesmoke"
        ax_i = self.fig.add_axes([0.15, 0.27, 0.7, 0.03], facecolor=axcolor)
        ax_q = self.fig.add_axes([0.15, 0.22, 0.7, 0.03], facecolor=axcolor)
        ax_dur = self.fig.add_axes([0.15, 0.17, 0.7, 0.03], facecolor=axcolor)
        ax_k = self.fig.add_axes([0.15, 0.12, 0.7, 0.03], facecolor=axcolor)

        self.slider_i = Slider(ax_i, "I", -1.0, 1.0, valinit=1.0)
        self.slider_q = Slider(ax_q, "Q", -1.0, 1.0, valinit=0.0)
        self.slider_dur = Slider(ax_dur, "Duration", 0.0, 1.0, valinit=0.25)
        self.slider_k = Slider(ax_k, "Coupling k", 0.0, 4 * math.pi, valinit=2 * math.pi)

        ax_apply = self.fig.add_axes([0.15, 0.03, 0.3, 0.05])
        ax_reset = self.fig.add_axes([0.55, 0.03, 0.3, 0.05])
        self.btn_apply = Button(ax_apply, "Apply Pulse")
        self.btn_reset = Button(ax_reset, "Reset")

        self.btn_apply.on_clicked(self._on_apply)
        self.btn_reset.on_clicked(self._on_reset)
        self.slider_i.on_changed(self._update_axis_line)
        self.slider_q.on_changed(self._update_axis_line)
        self.slider_k.on_changed(self._on_k_changed)

    def _on_apply(self, event):
        I = self.slider_i.val
        Q = self.slider_q.val
        duration = self.slider_dur.val
        if duration <= 0:
            return

        step_duration = duration / ANIMATION_STEPS
        for _ in range(ANIMATION_STEPS):
            self.qubit.apply_mixer(step_duration, I, Q)
            self._draw_state()
            plt.pause(FRAME_PAUSE)

    def _on_k_changed(self, value):
        self.qubit.k = value

    def _on_reset(self, event):
        self.qubit = QubitSystem(self.slider_k.val)
        self.trail = []
        self._draw_state()
        plt.draw()

    def show(self):
        plt.show()


def run():
    BlochSphereGUI().show()

if __name__ == '__main__':
    run()
