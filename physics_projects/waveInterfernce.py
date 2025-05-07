import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

x = np.linspace(0, 4 * np.pi, 1000)
t = np.linspace(0, 2 * np.pi, 200)

fig, ax = plt.subplots()
line, = ax.plot(x, np.sin(x))
ax.set_ylim(-2, 2)

wave1 = lambda x, t: np.sin(x - t)
wave2 = lambda x, t: np.sin(x + t)


def update(i):
    y = wave1(x, t[i]) + wave2(x, t[i])
    line.set_ydata(y)
    return line,

ani = FuncAnimation(fig, update, frames=len(t), interval=30)
plt.title("Wave Interference")
plt.xlabel("x")
plt.ylabel("Amplitude")
plt.grid(True)
plt.show()