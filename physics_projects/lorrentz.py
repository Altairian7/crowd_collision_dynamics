import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
from scipy.integrate import solve_ivp

# Initial parameters
sigma_init = 10
rho_init = 28
beta_init = 8 / 3

# Lorenz system definition
def lorenz(t, state, sigma, rho, beta):
    x, y, z = state
    dx = sigma * (y - x)
    dy = x * (rho - z) - y
    dz = x * y - beta * z
    return [dx, dy, dz]

# Solve and plot the Lorenz attractor
def update_plot(val=None):
    sigma = s_sigma.val
    rho = s_rho.val
    beta = s_beta.val

    sol = solve_ivp(
        lambda t, y: lorenz(t, y, sigma, rho, beta),
        [0, 40],
        [1, 1, 1],
        t_eval=np.linspace(0, 40, 10000)
    )
    
    ax.cla()
    ax.plot(sol.y[0], sol.y[1], sol.y[2], lw=0.5)
    ax.set_title("Lorenz Attractor")
    fig.canvas.draw_idle()

# Create figure and 3D axis
fig = plt.figure(figsize=(10, 6))
ax = fig.add_subplot(111, projection='3d')
plt.subplots_adjust(left=0.25, bottom=0.35)

# Create sliders
ax_sigma = plt.axes([0.25, 0.25, 0.65, 0.03])
ax_rho = plt.axes([0.25, 0.2, 0.65, 0.03])
ax_beta = plt.axes([0.25, 0.15, 0.65, 0.03])

s_sigma = Slider(ax_sigma, 'Sigma (σ)', 0.1, 30.0, valinit=sigma_init)
s_rho = Slider(ax_rho, 'Rho (ρ)', 0.1, 50.0, valinit=rho_init)
s_beta = Slider(ax_beta, 'Beta (β)', 0.1, 10.0, valinit=beta_init)

# Create update button
ax_button = plt.axes([0.4, 0.05, 0.2, 0.04])
button = Button(ax_button, 'Update Plot', color='lightblue', hovercolor='skyblue')
button.on_clicked(update_plot)

# Initial plot
update_plot()

plt.show()
