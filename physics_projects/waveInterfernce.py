import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Slider, CheckButtons

# Constants
x = np.linspace(0, 4 * np.pi, 1000)
t_vals = np.linspace(0, 2 * np.pi, 300)

# Default params
amp1_init = 1.0
amp2_init = 1.0
freq1_init = 1.0
freq2_init = 1.0
phase_init = 0.0

# Create figure and subplots
fig, axs = plt.subplots(3, 1, figsize=(10, 8), sharex=True)
plt.subplots_adjust(left=0.25, bottom=0.35)

(line1,) = axs[0].plot(x, np.zeros_like(x), label="Wave 1", color='blue')
axs[0].set_title("Wave 1")

(line2,) = axs[1].plot(x, np.zeros_like(x), label="Wave 2", color='green')
axs[1].set_title("Wave 2")

(line_sum,) = axs[2].plot(x, np.zeros_like(x), label="Interference", color='red')
axs[2].set_title("Superposition (Wave 1 + Wave 2)")

for ax in axs:
    ax.set_ylim(-3, 3)
    ax.grid(True)

# Widgets
ax_amp1 = plt.axes([0.25, 0.25, 0.65, 0.03])
ax_amp2 = plt.axes([0.25, 0.20, 0.65, 0.03])
ax_freq1 = plt.axes([0.25, 0.15, 0.65, 0.03])
ax_freq2 = plt.axes([0.25, 0.10, 0.65, 0.03])
ax_phase = plt.axes([0.25, 0.05, 0.65, 0.03])

slider_amp1 = Slider(ax_amp1, 'Amplitude 1', 0, 2, valinit=amp1_init)
slider_amp2 = Slider(ax_amp2, 'Amplitude 2', 0, 2, valinit=amp2_init)
slider_freq1 = Slider(ax_freq1, 'Frequency 1', 0.5, 5, valinit=freq1_init)
slider_freq2 = Slider(ax_freq2, 'Frequency 2', 0.5, 5, valinit=freq2_init)
slider_phase = Slider(ax_phase, 'Phase Diff (rad)', -np.pi, np.pi, valinit=phase_init)

check_ax = plt.axes([0.05, 0.5, 0.15, 0.15])
check = CheckButtons(check_ax, ['Wave 1', 'Wave 2'], [True, True])

# State flags
show_wave1 = True
show_wave2 = True

def toggle_visibility(label):
    global show_wave1, show_wave2
    if label == 'Wave 1':
        show_wave1 = not show_wave1
    elif label == 'Wave 2':
        show_wave2 = not show_wave2

check.on_clicked(toggle_visibility)

# Animation function
def update(frame):
    t = t_vals[frame]
    a1 = slider_amp1.val
    a2 = slider_amp2.val
    f1 = slider_freq1.val
    f2 = slider_freq2.val
    phi = slider_phase.val

    wave1 = a1 * np.sin(f1 * x - t)
    wave2 = a2 * np.sin(f2 * x + t + phi)
    superposed = wave1 + wave2

    line1.set_ydata(wave1 if show_wave1 else np.zeros_like(x))
    line2.set_ydata(wave2 if show_wave2 else np.zeros_like(x))
    line_sum.set_ydata(superposed)

    return line1, line2, line_sum

ani = FuncAnimation(fig, update, frames=len(t_vals), interval=30, blit=False)
plt.show()
