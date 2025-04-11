import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, Ellipse
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Slider
import matplotlib.gridspec as gridspec

class CollidingBlocksSimulation:
    def __init__(self):
        self.m1 = 1.0
        self.m2 = 100.0
        self.v1 = 0.0
        self.v2 = -1.0
        self.e = 1.0

        self.block_width1 = 1.0
        self.block_height1 = 1.0
        self.block_width2 = 1.0
        self.block_height2 = 1.0
        self.x1 = 2.0
        self.x2 = 4.0
        self.wall_position = 0

        self.t = 0
        self.dt = 0.01
        self.collision_count = 0

        self.v1_trajectory = []
        self.v2_trajectory = []

        self.setup_figure()
        self.ani = FuncAnimation(self.fig, self.update, interval=10)
        plt.show()

    def setup_figure(self):
        self.fig = plt.figure(figsize=(12, 10))
        gs = gridspec.GridSpec(3, 2, height_ratios=[2, 1, 1])

        self.ax_sim = plt.subplot(gs[0, :])
        self.ax_sim.set_xlim(-1, 30)
        self.ax_sim.set_ylim(-1, 5)
        self.ax_sim.set_title('Counting π')
        self.wall = Rectangle((self.wall_position, 0), 0.1, 3, color='black')
        self.ax_sim.add_patch(self.wall)

        self.block1 = Rectangle((self.x1, 0), self.block_width1, self.block_height1, color='cyan')
        self.block2 = Rectangle((self.x2, 0), self.block_width2, self.block_height2, color='blueviolet')
        self.ax_sim.add_patch(self.block1)
        self.ax_sim.add_patch(self.block2)

        self.velocity1_text = self.ax_sim.text(0.1, 0.9, '', transform=self.ax_sim.transAxes, color='cyan')
        self.velocity2_text = self.ax_sim.text(0.1, 0.85, '', transform=self.ax_sim.transAxes, color='blueviolet')
        self.collision_text = self.ax_sim.text(0.8, 0.9, '', transform=self.ax_sim.transAxes)
        self.time_text = self.ax_sim.text(0.8, 0.85, '', transform=self.ax_sim.transAxes)

        self.ax_vphase = plt.subplot(gs[1, 0])
        self.ax_vphase.set_xlim(-10, 10)
        self.ax_vphase.set_ylim(-10, 10)
        self.ax_vphase.set_title('Velocity Phase Space')
        self.vphase_point = self.ax_vphase.plot([], [], 'ko')[0]
        self.vphase_trace = self.ax_vphase.plot([], [], 'orange', alpha=0.7)[0]

        self.ax_trans_vphase = plt.subplot(gs[2, 0])
        self.ax_trans_vphase.set_xlim(-10, 10)
        self.ax_trans_vphase.set_ylim(-10, 10)
        self.ax_trans_vphase.set_title('Transformed Velocity Phase Space')
        self.trans_vphase_point = self.ax_trans_vphase.plot([], [], 'ko')[0]
        self.trans_vphase_trace = self.ax_trans_vphase.plot([], [], 'orange', alpha=0.7)[0]

        # Sliders
        slider_ax_m2 = plt.axes([0.2, 0.05, 0.2, 0.02], facecolor='lightgoldenrodyellow')
        self.mass2_slider = Slider(slider_ax_m2, 'Mass 2', 1, 1000, valinit=self.m2, valstep=1)
        self.mass2_slider.on_changed(self.update_mass2)

        slider_ax_v2 = plt.axes([0.5, 0.05, 0.2, 0.02], facecolor='lightgoldenrodyellow')
        self.velocity2_slider = Slider(slider_ax_v2, 'Initial Velocity 2', -10, 10, valinit=self.v2)
        self.velocity2_slider.on_changed(self.update_velocity2)

        slider_ax_v1 = plt.axes([0.8, 0.05, 0.2, 0.02], facecolor='lightgoldenrodyellow')
        self.velocity1_slider = Slider(slider_ax_v1, 'Initial Velocity 1', -10, 10, valinit=self.v1)
        self.velocity1_slider.on_changed(self.update_velocity1)

        plt.subplots_adjust(left=0.05, right=0.95, top=0.95, bottom=0.12)

    def update_mass2(self, val):
        self.m2 = val
        self.reset()

    def update_velocity1(self, val):
        self.v1 = val
        self.reset()

    def update_velocity2(self, val):
        self.v2 = val
        self.reset()

    def reset(self):
        self.x1 = 2.0
        self.x2 = 4.0
        self.t = 0
        self.collision_count = 0
        self.v1_trajectory.clear()
        self.v2_trajectory.clear()

    def update(self, frame):
        # Handle wall collision for block1
        if self.x1 <= self.wall_position and self.v1 < 0:
            self.v1 = -self.v1
            self.collision_count += 1

        # Handle block collision
        if self.x1 + self.block_width1 >= self.x2:
            u1, u2 = self.v1, self.v2
            self.v1 = ((self.m1 - self.m2) * u1 + 2 * self.m2 * u2) / (self.m1 + self.m2)
            self.v2 = ((self.m2 - self.m1) * u2 + 2 * self.m1 * u1) / (self.m1 + self.m2)
            self.collision_count += 1

        self.x1 += self.v1 * self.dt
        self.x2 += self.v2 * self.dt
        self.t += self.dt

        # Update rectangles
        self.block1.set_xy((self.x1, 0))
        self.block2.set_xy((self.x2, 0))

        # Update text
        self.velocity1_text.set_text(f'Velocity 1 : {self.v1:.4f}')
        self.velocity2_text.set_text(f'Velocity 2 : {self.v2:.4f}')
        self.collision_text.set_text(f'Collisions : {self.collision_count}')
        self.time_text.set_text(f'Time : {self.t:.3f}')

        # Update phase space
        self.v1_trajectory.append(self.v1)
        self.v2_trajectory.append(self.v2)

        self.vphase_point.set_data([self.v2], [self.v1])
        self.vphase_trace.set_data(self.v2_trajectory, self.v1_trajectory)

        v1t = self.v1 * np.sqrt(self.m1)
        v2t = self.v2 * np.sqrt(self.m2)
        self.trans_vphase_point.set_data([v2t], [v1t])
        trans_v1_traj = np.array(self.v1_trajectory) * np.sqrt(self.m1)
        trans_v2_traj = np.array(self.v2_trajectory) * np.sqrt(self.m2)
        self.trans_vphase_trace.set_data(trans_v2_traj, trans_v1_traj)

if __name__ == '__main__':
    CollidingBlocksSimulation()
