import pygame
import math

pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

light_angle = math.radians(45)
ref_index_air = 1.0
ref_index_glass = 1.5

running = True
while running:
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.draw.rect(screen, (0, 0, 255), (0, 300, 800, 300))
    pygame.draw.line(screen, (255, 255, 255), (200, 100), (400, 300), 2)

    incidence_angle = light_angle
    refraction_angle = math.asin(ref_index_air / ref_index_glass * math.sin(incidence_angle))
    x2 = 400 + 200 * math.sin(refraction_angle)
    y2 = 300 + 200 * math.cos(refraction_angle)
    pygame.draw.line(screen, (255, 255, 0), (400, 300), (x2, y2), 2)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()