import pygame as game
import math
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

# Init
game.init()
info = game.display.Info()
screen_size = (info.current_w, info.current_h)
screen = game.display.set_mode(screen_size)
clock = game.time.Clock()

# Fonts
font = game.font.Font(None, 32)

# Sound
tick_sound = game.mixer.Sound("tick.wav")

# Colors
WHITE = (255, 255, 255)
BG = (20, 20, 20)

# Block Class
class Block:
    def __init__(self, mass, velocity, size, x, y):
        self.mass = mass
        self.v = velocity
        self.size = size
        self.x = x
        self.y = y
        self.v2 = 0

    def momentum(self): return self.mass * self.v
    def ke(self): return 0.5 * self.mass * self.v ** 2

# Graph Class
class RealTimePlot:
    def __init__(self, title):
        self.fig, self.ax = plt.subplots(figsize=(3, 2), dpi=100)
        self.canvas = FigureCanvas(self.fig)
        self.title = title
        self.x_data, self.y_data = [], []
        self.ax.set_title(title)
        self.ax.grid(True)

    def update(self, x_val, y_val):
        self.x_data.append(x_val)
        self.y_data.append(y_val)
        self.ax.cla()
        self.ax.set_title(self.title)
        self.ax.plot(self.x_data[-100:], self.y_data[-100:], color='cyan')
        self.ax.grid(True)

    def draw(self):
        self.canvas.draw()
        raw_data = self.canvas.buffer_rgba()
        size = self.canvas.get_width_height()
        return game.image.frombuffer(raw_data, size, "RGBA")

# Setup
B1_mass, B1_velocity = 100, -300
B2_mass, B2_velocity = 1, 0
B1 = Block(B1_mass, B1_velocity, 200, screen_size[0] * 0.65, screen_size[1] * 0.5)
B2 = Block(B2_mass, B2_velocity, 100, screen_size[0] * 0.3, screen_size[1] * 0.5)

# Graphs
graph_momentum = RealTimePlot("Total Momentum")
graph_ke = RealTimePlot("Total Kinetic Energy")
graph_v = RealTimePlot("B1 & B2 Velocity")

# Simulation Vars
collision_count = 0
paused = False
elastic = True
time_step = 0

# Main loop
running = True
while running:
    dt = clock.tick(60) / 1000
    time_step += dt

    for event in game.event.get():
        if event.type == game.QUIT:
            running = False
        if event.type == game.KEYDOWN:
            if event.key == game.K_SPACE:
                paused = not paused
            if event.key == game.K_e:
                elastic = not elastic

    if not paused:
        # Movement
        B1.x += B1.v * dt
        B2.x += B2.v * dt

        # Collisions
        if (B2.x + B2.size) >= B1.x and B1.v <= B2.v:
            game.mixer.Sound.play(tick_sound)
            collision_count += 1
            if elastic:
                total_mass = B1.mass + B2.mass
                B1.v2 = ((B1.mass - B2.mass) * B1.v + 2 * B2.mass * B2.v) / total_mass
                B2.v2 = ((B2.mass - B1.mass) * B2.v + 2 * B1.mass * B1.v) / total_mass
            else:
                v_final = (B1.mass * B1.v + B2.mass * B2.v) / (B1.mass + B2.mass)
                B1.v2 = B2.v2 = v_final
            B1.v, B2.v = B1.v2, B2.v2

        if B2.x <= 0 and B2.v < 0:
            game.mixer.Sound.play(tick_sound)
            collision_count += 1
            B2.v *= -1

    # Graph updates
    total_momentum = B1.momentum() + B2.momentum()
    total_ke = B1.ke() + B2.ke()
    graph_momentum.update(time_step, total_momentum)
    graph_ke.update(time_step, total_ke)
    graph_v.update(time_step, B1.v)
    graph_v.update(time_step, B2.v)

    # Drawing
    screen.fill(BG)

    game.draw.rect(screen, (255, 0, 0), game.Rect(B1.x, B1.y, B1.size, B1.size))
    game.draw.rect(screen, (0, 255, 0), game.Rect(B2.x, B2.y, B2.size, B2.size))

    # Text Info
    screen.blit(font.render(f"Collisions: {collision_count}", True, WHITE), (50, 30))
    screen.blit(font.render(f"KE: {round(total_ke, 2)}", True, WHITE), (50, 70))
    screen.blit(font.render(f"Momentum: {round(total_momentum, 2)}", True, WHITE), (50, 110))
    screen.blit(font.render(f"Elastic: {elastic}", True, WHITE), (50, 150))

    # Render graphs to surface
    screen.blit(graph_momentum.draw(), (screen_size[0] - 320, 20))
    screen.blit(graph_ke.draw(), (screen_size[0] - 320, 240))
    screen.blit(graph_v.draw(), (screen_size[0] - 320, 460))

    game.display.flip()

game.quit()
