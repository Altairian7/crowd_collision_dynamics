import pygame
import math

class Body:
    def __init__(self, x, y, mass, radius, color):
        self.x = x
        self.y = y
        self.mass = mass
        self.radius = radius
        self.color = color
        self.vx = 0
        self.vy = 0

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

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

pygame.init()
screen = pygame.display.set_mode((800, 600))
G = 6.67430e-1
dt = 0.1
clock = pygame.time.Clock()

bodies = [
    Body(400, 300, 10000, 20, (255, 255, 0)),
    Body(500, 300, 1, 5, (0, 0, 255)),
    Body(300, 300, 1, 5, (255, 0, 0))
]
bodies[1].vy = 5
bodies[2].vy = -5

running = True
while running:
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    for body in bodies:
        for other in bodies:
            if body != other:
                body.attract(other)

    for body in bodies:
        body.update()
        body.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()