import pygame
import math
import sys
import random
from pygame.locals import *

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 800
CENTER = (WIDTH // 2, HEIGHT // 2)
RADIUS = 300

# Colors
BACKGROUND = (0, 0, 0)
LINE_COLOR = (255, 255, 255)
TEXT_COLOR = (255, 255, 255)
HIGHLIGHT_COLORS = [
    (255, 0, 0),    # Red
    (0, 255, 0),    # Green
    (0, 0, 255),    # Blue
    (255, 255, 0),  # Yellow
    (255, 0, 255),  # Magenta
    (0, 255, 255),  # Cyan
    (255, 128, 0),  # Orange
    (128, 0, 255),  # Purple
]

# Create window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Musical Harmonics with Collision")

# Font
font = pygame.font.SysFont('Arial', 20)
title_font = pygame.font.SysFont('Arial', 32)

class Particle:
    def __init__(self, x, y, radius=10):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = random.choice(HIGHLIGHT_COLORS)
        self.vx = random.uniform(-2, 2)
        self.vy = random.uniform(-2, 2)
        self.mass = self.radius ** 2  # Mass proportional to area
        
    def move(self):
        self.x += self.vx
        self.y += self.vy
        
        # Bounce off walls
        if self.x - self.radius < 0:
            self.x = self.radius
            self.vx = -self.vx
        elif self.x + self.radius > WIDTH:
            self.x = WIDTH - self.radius
            self.vx = -self.vx
            
        if self.y - self.radius < 0:
            self.y = self.radius
            self.vy = -self.vy
        elif self.y + self.radius > HEIGHT:
            self.y = HEIGHT - self.radius
            self.vy = -self.vy
    
    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)
        
    def distance(self, other):
        dx = self.x - other.x
        dy = self.y - other.y
        return math.sqrt(dx**2 + dy**2)
    
    def check_collision(self, other):
        distance = self.distance(other)
        if distance < self.radius + other.radius:
            return True
        return False
    
    def resolve_collision(self, other):
        # Calculate direction vector
        dx = other.x - self.x
        dy = other.y - self.y
        distance = math.sqrt(dx**2 + dy**2)
        
        # Normalize direction vector
        if distance == 0:  # Avoid division by zero
            dx, dy = 1, 0
        else:
            dx, dy = dx/distance, dy/distance
            
        # Calculate relative velocity
        dvx = self.vx - other.vx
        dvy = self.vy - other.vy
        
        # Calculate velocity along the normal direction
        velocity_along_normal = dvx * dx + dvy * dy
        
        # If particles are moving away from each other, no collision response
        if velocity_along_normal > 0:
            return
        
        # Calculate impulse scalar
        restitution = 1.0  # Perfect elasticity
        impulse_scalar = -(1 + restitution) * velocity_along_normal
        impulse_scalar /= 1/self.mass + 1/other.mass
        
        # Apply impulse
        self.vx -= impulse_scalar * dx / self.mass
        self.vy -= impulse_scalar * dy / self.mass
        other.vx += impulse_scalar * dx / other.mass
        other.vy += impulse_scalar * dy / other.mass
        
        # Separate the particles to avoid sticking
        overlap = (self.radius + other.radius - distance) / 2.0
        self.x -= overlap * dx
        self.y -= overlap * dy
        other.x += overlap * dx
        other.y += overlap * dy

class HarmonicVisualizer:
    def __init__(self):
        self.num_points = 60  # Number of points around the circle
        self.current_multiplier = 2  # Start with ratio 2:1 (octave)
        self.show_lines = True
        self.animate = False
        self.animation_speed = 0.01
        self.animation_value = 2.0
        self.animation_direction = 1
        self.mode = "harmonic"  # "harmonic" or "collision"
        
        # Create particles for collision mode
        self.particles = []
        self.num_particles = 40
        self.create_particles()
        
    def create_particles(self):
        self.particles = []
        for _ in range(self.num_particles):
            radius = random.randint(5, 15)
            # Create particles away from edges
            x = random.randint(radius, WIDTH - radius)
            y = random.randint(radius, HEIGHT - radius)
            self.particles.append(Particle(x, y, radius))
    
    def update_collision(self):
        # Move all particles
        for particle in self.particles:
            particle.move()
        
        # Check for collisions
        for i in range(len(self.particles)):
            for j in range(i+1, len(self.particles)):
                if self.particles[i].check_collision(self.particles[j]):
                    self.particles[i].resolve_collision(self.particles[j])
    
    def draw_collision(self):
        screen.fill(BACKGROUND)
        
        # Draw title
        title_text = "Particle Collision Simulation"
        title_surf = title_font.render(title_text, True, TEXT_COLOR)
        screen.blit(title_surf, (WIDTH // 2 - title_surf.get_width() // 2, 30))
        
        # Draw particles
        for particle in self.particles:
            particle.draw(screen)
        
        # Draw instructions
        instructions = [
            "Controls:",
            "M: Switch between modes",
            "C: Add more particles",
            "R: Reset particles",
            "Space: Toggle line display (in harmonic mode)",
            "A: Toggle animation (in harmonic mode)"
        ]
        
        for i, text in enumerate(instructions):
            text_surf = font.render(text, True, TEXT_COLOR)
            screen.blit(text_surf, (20, HEIGHT - 150 + i * 25))
    
    def draw_harmonic(self):
        screen.fill(BACKGROUND)
        
        # Draw title
        if self.animate:
            title_text = f"Musical Harmonics - Ratio: 1:{self.animation_value:.2f}"
        else:
            title_text = f"Musical Harmonics - Ratio: 1:{self.current_multiplier}"
        title_surf = title_font.render(title_text, True, TEXT_COLOR)
        screen.blit(title_surf, (WIDTH // 2 - title_surf.get_width() // 2, 30))
        
        # Draw instructions
        instructions = [
            "Controls:",
            "M: Switch between modes",
            "1-9: Set multiplier",
            "Up/Down: Change number of points",
            "Space: Toggle line display",
            "A: Toggle animation",
            "Left/Right: Adjust animation speed"
        ]
        
        for i, text in enumerate(instructions):
            text_surf = font.render(text, True, TEXT_COLOR)
            screen.blit(text_surf, (20, HEIGHT - 170 + i * 25))
        
        # Draw circle
        pygame.draw.circle(screen, LINE_COLOR, CENTER, RADIUS, 1)
        
        # Draw points around the circle
        points = []
        for i in range(self.num_points):
            angle = 2 * math.pi * i / self.num_points
            x = CENTER[0] + RADIUS * math.cos(angle)
            y = CENTER[1] + RADIUS * math.sin(angle)
            points.append((x, y))
            pygame.draw.circle(screen, LINE_COLOR, (int(x), int(y)), 3)
            
            # Draw point number
            if self.num_points <= 60:  # Only show numbers if not too crowded
                num_text = font.render(str(i), True, TEXT_COLOR)
                text_x = CENTER[0] + (RADIUS + 20) * math.cos(angle)
                text_y = CENTER[1] + (RADIUS + 20) * math.sin(angle)
                screen.blit(num_text, (text_x - num_text.get_width() // 2, text_y - num_text.get_height() // 2))
        
        # Draw lines between points based on the multiplier
        if self.show_lines:
            multiplier = self.current_multiplier
            if self.animate:
                multiplier = self.animation_value
                
            for i in range(self.num_points):
                start_point = points[i]
                # Calculate the destination point using the multiplier
                dest_index = (i * int(multiplier)) % self.num_points
                end_point = points[dest_index]
                
                # Use a color based on the starting point for visual interest
                color_index = i % len(HIGHLIGHT_COLORS)
                pygame.draw.line(screen, HIGHLIGHT_COLORS[color_index], start_point, end_point, 1)
    
    def draw(self):
        if self.mode == "harmonic":
            self.draw_harmonic()
        else:  # collision mode
            self.draw_collision()
        
        # Update the display
        pygame.display.flip()
    
    def update_animation(self):
        if self.mode == "harmonic" and self.animate:
            self.animation_value += self.animation_speed * self.animation_direction
            
            # Reverse direction or reset if hitting bounds
            if self.animation_value <= 1.0:
                self.animation_value = 1.0
                self.animation_direction = 1
            elif self.animation_value >= 13.0:
                self.animation_value = 13.0
                self.animation_direction = -1
        elif self.mode == "collision":
            self.update_collision()

    def handle_events(self, event):
        if event.type == KEYDOWN:
            # Switch between modes
            if event.key == K_m:
                self.mode = "collision" if self.mode == "harmonic" else "harmonic"
            
            # Mode-specific controls
            if self.mode == "harmonic":
                # Number keys to set multiplier
                if event.key in range(K_1, K_9 + 1):
                    self.current_multiplier = event.key - K_0
                    self.animation_value = self.current_multiplier
                    self.animate = False
                
                # Adjust number of points
                elif event.key == K_UP:
                    self.num_points = min(self.num_points + 1, 150)
                elif event.key == K_DOWN:
                    self.num_points = max(self.num_points - 1, 10)
                
                # Toggle line display
                elif event.key == K_SPACE:
                    self.show_lines = not self.show_lines
                
                # Toggle animation
                elif event.key == K_a:
                    self.animate = not self.animate
                    if not self.animate:
                        self.current_multiplier = round(self.animation_value)
                
                # Adjust animation speed
                elif event.key == K_LEFT:
                    self.animation_speed = max(self.animation_speed - 0.005, 0.001)
                elif event.key == K_RIGHT:
                    self.animation_speed = min(self.animation_speed + 0.005, 0.1)
            
            elif self.mode == "collision":
                # Add more particles
                if event.key == K_c:
                    for _ in range(5):
                        radius = random.randint(5, 15)
                        x = random.randint(radius, WIDTH - radius)
                        y = random.randint(radius, HEIGHT - radius)
                        self.particles.append(Particle(x, y, radius))
                        
                # Reset particles
                elif event.key == K_r:
                    self.create_particles()

def main():
    visualizer = HarmonicVisualizer()
    clock = pygame.time.Clock()
    
    # Main game loop
    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            visualizer.handle_events(event)
        
        # Update animation/physics if active
        visualizer.update_animation()
        
        # Draw everything
        visualizer.draw()
        
        # Cap the frame rate
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()