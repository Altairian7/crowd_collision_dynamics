import pygame
import math

class Body:
    def __init__(self, x, y, mass, radius, color, name=""):
        self.x = x
        self.y = y
        self.mass = mass
        self.radius = radius
        self.color = color
        self.name = name
        self.vx = 0
        self.vy = 0
        self.trail = []

    def attract(self, other):
        dx = other.x - self.x
        dy = other.y - self.y
        distance = math.hypot(dx, dy)
        if distance == 0:
            return
        force = G * self.mass * other.mass / distance**2
        angle = math.atan2(dy, dx)
        fx = math.cos(angle) * force
        fy = math.sin(angle) * force
        self.vx += fx / self.mass * dt
        self.vy += fy / self.mass * dt

    def update(self):
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.trail.append((int(self.x), int(self.y)))
        if len(self.trail) > 100:
            self.trail.pop(0)

    def draw(self, screen, font):
        # Draw trail
        for point in self.trail:
            pygame.draw.circle(screen, self.color, point, 2)
        # Draw body
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
        # Draw info
        info_text = f"{self.name} v=({self.vx:.1f},{self.vy:.1f})"
        text = font.render(info_text, True, (255, 255, 255))
        screen.blit(text, (self.x + self.radius + 5, self.y - self.radius - 5))

# Pygame setup
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Gravity Simulation GUI")
font = pygame.font.SysFont("Arial", 14)
clock = pygame.time.Clock()

# Constants
G = 6.67430e-1
dt = 0.1

# Body initialization
bodies = [
    Body(400, 300, 10000, 20, (255, 255, 0), "Sun"),
    Body(500, 300, 1, 5, (0, 0, 255), "Blue"),
    Body(300, 300, 1, 5, (255, 0, 0), "Red")
]
bodies[1].vy = 5
bodies[2].vy = -5

# Main loop
running = True
while running:
    screen.fill((0, 0, 0))
    fps = int(clock.get_fps())

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    for body in bodies:
        for other in bodies:
            if body != other:
                body.attract(other)

    for body in bodies:
        body.update()
        body.draw(screen, font)

    # Display simulation info
    sim_info = font.render(f"FPS: {fps}", True, (255, 255, 255))
    screen.blit(sim_info, (10, 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
