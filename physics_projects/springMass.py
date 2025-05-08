import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
from matplotlib.animation import FuncAnimation

# Initial values
k_init = 5
x0_init = 1
t = np.linspace(0, 10, 500)

# Create the main figure and axis
fig, ax = plt.subplots(figsize=(8, 5))
plt.subplots_adjust(left=0.1, bottom=0.35)
line, = ax.plot(t, x0_init * np.cos(np.sqrt(k_init) * t), lw=2, color='deepskyblue')
ax.set_ylim(-2, 2)
ax.set_xlabel("Time (s)")
ax.set_ylabel("Displacement (x)")
ax.set_title("🎯 Interactive Spring-Mass Oscillator", fontsize=14)

# Sliders for k and x0
ax_k = plt.axes([0.1, 0.2, 0.8, 0.03])
ax_x0 = plt.axes([0.1, 0.15, 0.8, 0.03])
slider_k = Slider(ax_k, 'Spring Constant k', 1, 10, valinit=k_init, color='orange')
slider_x0 = Slider(ax_x0, 'Initial Displacement x₀', -2, 2, valinit=x0_init, color='limegreen')

# Reset button
reset_ax = plt.axes([0.8, 0.05, 0.1, 0.04])
reset_button = Button(reset_ax, 'Reset', color='lightcoral', hovercolor='salmon')

# Update function for sliders
def update(val):
    k = slider_k.val
    x0 = slider_x0.val
    line.set_ydata(x0 * np.cos(np.sqrt(k) * t))
    fig.canvas.draw_idle()

slider_k.on_changed(update)
slider_x0.on_changed(update)

# Reset functionality
def reset(event):
    slider_k.reset()
    slider_x0.reset()

reset_button.on_clicked(reset)

plt.show()
