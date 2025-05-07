from matplotlib.widgets import Slider

fig, ax = plt.subplots()
plt.subplots_adjust(bottom=0.25)
t = np.linspace(0, 10, 500)
k = 5
x0 = 1

line, = ax.plot(t, x0 * np.cos(np.sqrt(k) * t))
ax.set_ylim(-2, 2)

ax_k = plt.axes([0.25, 0.1, 0.65, 0.03])
slider_k = Slider(ax_k, 'k', 1, 10, valinit=k)


def update(val):
    k = slider_k.val
    line.set_ydata(x0 * np.cos(np.sqrt(k) * t))
    fig.canvas.draw_idle()

slider_k.on_changed(update)
plt.title("Spring-Mass Oscillator")
plt.show()
