import pygame
import math

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Refraction Simulator")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 16)

# Constants
ref_index_air = 1.0
ref_index_glass = 1.5
incident_start = [200, 100]
boundary_point = [400, 300]

def draw_text(text, pos, color=(255, 255, 255)):
    screen.blit(font.render(text, True, color), pos)

running = True
dragging = False

while running:
    screen.fill((0, 0, 0))

    # Event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if math.hypot(event.pos[0] - incident_start[0], event.pos[1] - incident_start[1]) < 20:
                dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            dragging = False
        elif event.type == pygame.MOUSEMOTION and dragging:
            incident_start = list(event.pos)

    # Background layers
    pygame.draw.rect(screen, (135, 206, 235), (0, 0, 800, 300))     # Air
    pygame.draw.rect(screen, (0, 0, 139), (0, 300, 800, 300))       # Glass

    draw_text("Air (n = 1.0)", (10, 10))
    draw_text("Glass (n = 1.5)", (10, 310))

    # Normal line
    pygame.draw.line(screen, (100, 100, 100), (400, 0), (400, 600), 1)

    # Incident ray
    pygame.draw.line(screen, (255, 255, 255), incident_start, boundary_point, 2)

    # Calculate incident and refracted angles
    dx = boundary_point[0] - incident_start[0]
    dy = boundary_point[1] - incident_start[1]
    incidence_angle = math.atan2(dx, dy)  # relative to normal

    try:
        sin_refraction = ref_index_air / ref_index_glass * math.sin(incidence_angle)
        if abs(sin_refraction) > 1:
            raise ValueError("Total internal reflection")
        refraction_angle = math.asin(sin_refraction)

        # Refracted ray
        x2 = boundary_point[0] + 200 * math.sin(refraction_angle)
        y2 = boundary_point[1] + 200 * math.cos(refraction_angle)
        pygame.draw.line(screen, (255, 255, 0), boundary_point, (x2, y2), 2)

        draw_text(f"Incidence Angle: {math.degrees(incidence_angle):.1f}°", (550, 10))
        draw_text(f"Refraction Angle: {math.degrees(refraction_angle):.1f}°", (550, 30))

    except ValueError:
        draw_text("Total Internal Reflection!", (520, 30), (255, 0, 0))
        pygame.draw.line(screen, (255, 0, 0), boundary_point,
                         (boundary_point[0] + dx, boundary_point[1] - dy), 2)

    # Draw draggable point
    pygame.draw.circle(screen, (0, 255, 0), incident_start, 6)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
