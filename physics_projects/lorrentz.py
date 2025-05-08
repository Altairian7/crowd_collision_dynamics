from scipy.integrate import solve_ivp

fig = plt.figure()
ax = fig.add_subplot(projection='3d')

sigma = 10
rho = 28
beta = 8/3

def lorenz(t, state):
    x, y, z = state
    dx = sigma * (y - x)
    dy = x * (rho - z) - y
    dz = x * y - beta * z
    return [dx, dy, dz]

sol = solve_ivp(lorenz, [0, 40], [1, 1, 1], t_eval=np.linspace(0, 40, 10000))

ax.plot(sol.y[0], sol.y[1], sol.y[2], lw=0.5)
plt.title("Lorenz Attractor")
plt.show()