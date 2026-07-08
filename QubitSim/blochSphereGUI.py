import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons

from qubitSystem import QubitSystem

ANIMATION_STEPS = 40
FRAME_PAUSE = 0.02


class BlochSphereGUI:
    def __init__(self):
        self.qubit = QubitSystem(2 * math.pi)
        self.mode = "manual"

        self.fig = plt.figure(figsize=(13, 9.5))
        self.ax = self.fig.add_axes([0.03, 0.34, 0.48, 0.62], projection="3d")

        self._draw_static_sphere()
        self.trail_line, = self.ax.plot([], [], [], color="tab:red", linewidth=1)
        self.axis_line, = self.ax.plot([], [], [], color="tab:blue", linewidth=1.5, linestyle="--")
        self.preview_arc, = self.ax.plot([], [], [], color="tab:orange", linewidth=2, linestyle=":")
        self.arrow = None
        self.trail = []
        self._draw_state()

        self._build_iq_axes()
        self._build_controls()
        self._set_mode("Manual I/Q")

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
        if self.mode == "manual":
            phase = math.atan2(self.slider_q.val, self.slider_i.val)
        else:
            phase = self.slider_angle_phase.val
        axis_len = 1.3
        dx, dy = axis_len * math.cos(phase), axis_len * math.sin(phase)
        self.axis_line.set_data([-dx, dx], [-dy, dy])
        self.axis_line.set_3d_properties([0, 0])
        self.fig.canvas.draw_idle()

    def _update_rotation_preview(self, event=None):
        if self.mode != "angle":
            self.preview_arc.set_data([], [])
            self.preview_arc.set_3d_properties([])
            self.fig.canvas.draw_idle()
            return

        rot_phase = self.slider_rot_phase.val
        angle_phase = self.slider_angle_phase.val

        v0 = np.array(self.qubit.state.get_state(), dtype=float)
        n = np.array([math.cos(angle_phase), math.sin(angle_phase), 0.0])
        cross_nv = np.cross(n, v0)
        dot_nv = np.dot(n, v0)

        thetas = np.linspace(0, rot_phase, 60)
        cos_t = np.cos(thetas)
        sin_t = np.sin(thetas)
        points = (v0[None, :] * cos_t[:, None]
                  + cross_nv[None, :] * sin_t[:, None]
                  + n[None, :] * dot_nv * (1 - cos_t)[:, None])

        self.preview_arc.set_data(points[:, 0], points[:, 1])
        self.preview_arc.set_3d_properties(points[:, 2])
        self.fig.canvas.draw_idle()

    def _build_iq_axes(self):
        self.ax_i_plot = self.fig.add_axes([0.66, 0.70, 0.31, 0.22])
        self.ax_q_plot = self.fig.add_axes([0.66, 0.42, 0.31, 0.22])
        self.ax_amp_plot = self.fig.add_axes([0.66, 0.16, 0.31, 0.22])

        self.line_i, = self.ax_i_plot.plot([], [], color="tab:blue")
        self.line_q, = self.ax_q_plot.plot([], [], color="tab:green")
        self.line_amp, = self.ax_amp_plot.plot([], [], color="tab:purple")

        self.ax_i_plot.set_ylabel("I")
        self.ax_q_plot.set_ylabel("Q")
        self.ax_amp_plot.set_ylabel("Amplitude")
        self.ax_amp_plot.set_xlabel("Stage")

        self.iq_plot_axes = [self.ax_i_plot, self.ax_q_plot, self.ax_amp_plot]
        self._clear_iq_plots()

    def _clear_iq_plots(self):
        for ax, line in ((self.ax_i_plot, self.line_i), (self.ax_q_plot, self.line_q), (self.ax_amp_plot, self.line_amp)):
            line.set_data([], [])
            ax.set_xlim(0, 1)
            ax.set_ylim(-1, 1)

    def _build_controls(self):
        axcolor = "whitesmoke"

        ax_mode = self.fig.add_axes([0.02, 0.18, 0.12, 0.12])
        self.mode_radio = RadioButtons(ax_mode, ("Manual I/Q", "Angle Pulse"))
        self.mode_radio.on_clicked(self._set_mode)

        ax_k = self.fig.add_axes([0.24, 0.25, 0.26, 0.03], facecolor=axcolor)
        self.slider_k = Slider(ax_k, "Coupling k", 0.0, 4 * math.pi, valinit=2 * math.pi)
        self.slider_k.on_changed(self._on_k_changed)

        ax_i = self.fig.add_axes([0.24, 0.20, 0.26, 0.03], facecolor=axcolor)
        ax_q = self.fig.add_axes([0.24, 0.15, 0.26, 0.03], facecolor=axcolor)
        ax_dur = self.fig.add_axes([0.24, 0.10, 0.26, 0.03], facecolor=axcolor)
        self.slider_i = Slider(ax_i, "I", -1.0, 1.0, valinit=1.0)
        self.slider_q = Slider(ax_q, "Q", -1.0, 1.0, valinit=0.0)
        self.slider_dur = Slider(ax_dur, "Duration", 0.0, 1.0, valinit=0.25)
        self.slider_i.on_changed(self._update_axis_line)
        self.slider_q.on_changed(self._update_axis_line)

        ax_apply = self.fig.add_axes([0.24, 0.03, 0.25, 0.05])
        self.btn_apply = Button(ax_apply, "Apply Pulse")
        self.btn_apply.on_clicked(self._on_apply)

        ax_rot_phase = self.fig.add_axes([0.24, 0.20, 0.26, 0.03], facecolor=axcolor)
        ax_angle_phase = self.fig.add_axes([0.24, 0.15, 0.26, 0.03], facecolor=axcolor)
        self.slider_rot_phase = Slider(ax_rot_phase, "Rotation angle", -2 * math.pi, 2 * math.pi, valinit=math.pi / 2)
        self.slider_angle_phase = Slider(ax_angle_phase, "Axis angle", -2 * math.pi, 2 * math.pi, valinit=0.0)
        self.slider_rot_phase.on_changed(self._update_axis_line)
        self.slider_angle_phase.on_changed(self._update_axis_line)
        self.slider_rot_phase.on_changed(self._update_rotation_preview)
        self.slider_angle_phase.on_changed(self._update_rotation_preview)

        ax_send = self.fig.add_axes([0.24, 0.03, 0.25, 0.05])
        self.btn_send = Button(ax_send, "Send Pulse")
        self.btn_send.on_clicked(self._on_send_pulse)

        ax_reset = self.fig.add_axes([0.55, 0.03, 0.25, 0.05])
        self.btn_reset = Button(ax_reset, "Reset")
        self.btn_reset.on_clicked(self._on_reset)

        self.manual_widgets = [self.slider_i, self.slider_q, self.slider_dur, self.btn_apply]
        self.angle_widgets = [self.slider_rot_phase, self.slider_angle_phase, self.btn_send]

    def _set_mode(self, label):
        self.mode = "manual" if label == "Manual I/Q" else "angle"
        is_manual = self.mode == "manual"

        # Overlapping widgets keep responding to clicks/drags even while their axes
        # is hidden (Axes.set_visible does not gate AxesWidget.ignore()), so the
        # inactive mode's widgets must also be explicitly deactivated.
        for w in self.manual_widgets:
            w.ax.set_visible(is_manual)
            w.set_active(is_manual)
        for w in self.angle_widgets:
            w.ax.set_visible(not is_manual)
            w.set_active(not is_manual)
        for ax in self.iq_plot_axes:
            ax.set_visible(not is_manual)

        self._update_axis_line()
        self._update_rotation_preview()
        self.fig.canvas.draw()

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

    def _on_send_pulse(self, event):
        rot_phase = self.slider_rot_phase.val
        angle_phase = self.slider_angle_phase.val
        if rot_phase == 0:
            return

        start_state = self.qubit.state.state.copy()
        self.qubit.rotate_anl(rot_phase, angle_phase)

        I_data = self.qubit.pulses_I.copy()
        Q_data = self.qubit.pulses_Q.copy()
        amp_data = np.sqrt(I_data ** 2 + Q_data ** 2)
        stages = self.qubit.stages
        t = np.arange(stages) * self.qubit.stage_period

        self.qubit.state.state = start_state
        self._configure_time_axis(self.ax_i_plot, t, I_data)
        self._configure_time_axis(self.ax_q_plot, t, Q_data)
        self._configure_time_axis(self.ax_amp_plot, t, amp_data)
        self.line_i.set_data([], [])
        self.line_q.set_data([], [])
        self.line_amp.set_data([], [])

        for i in range(stages):
            self.qubit.apply_mixer(self.qubit.stage_period, I_data[i], Q_data[i])
            self._draw_state()
            self.line_i.set_data(t[:i + 1], I_data[:i + 1])
            self.line_q.set_data(t[:i + 1], Q_data[:i + 1])
            self.line_amp.set_data(t[:i + 1], amp_data[:i + 1])
            plt.pause(FRAME_PAUSE)

        self._update_rotation_preview()
        self.fig.canvas.draw()

    @staticmethod
    def _configure_time_axis(ax, t, y_data, margin_frac=0.1):
        y_min, y_max = float(np.min(y_data)), float(np.max(y_data))
        if y_min == y_max:
            pad = 0.1 if y_min == 0 else abs(y_min) * 0.1
            y_min, y_max = y_min - pad, y_max + pad
        else:
            pad = (y_max - y_min) * margin_frac
            y_min, y_max = y_min - pad, y_max + pad

        ax.set_xlim(float(t[0]), float(t[-1]) if len(t) > 1 else float(t[0]) + 1)
        ax.set_ylim(y_min, y_max)

    def _on_k_changed(self, value):
        self.qubit.k = value

    def _on_reset(self, event):
        self.qubit = QubitSystem(self.slider_k.val)
        self.trail = []
        self._draw_state()
        self._clear_iq_plots()
        self._update_rotation_preview()
        self.fig.canvas.draw()

    def show(self):
        plt.show()


def run():
    BlochSphereGUI().show()


if __name__ == "__main__":
    run()
