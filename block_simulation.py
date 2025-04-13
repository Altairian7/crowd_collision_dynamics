import pygame as game


def calculate_energy_conservation():
    """Track total energy of the system and display how well it's conserved."""
    initial_energy = 0.5 * B1.m * B1_velocity**2 + 0.5 * B2.m * B2_velocity**2
    current_energy = 0.5 * B1.m * B1.v1**2 + 0.5 * B2.m * B2.v1**2
    conservation_percentage = (current_energy / initial_energy) * 100
    return initial_energy, current_energy, conservation_percentage


def calculate_collision_efficiency(pre_velocity1, pre_velocity2, post_velocity1, post_velocity2):
    """Calculate and display the coefficient of restitution (efficiency) of collisions."""
    if pre_velocity1 == pre_velocity2:  # Avoid division by zero
        return 1.0
    restitution = abs((post_velocity2 - post_velocity1) / (pre_velocity1 - pre_velocity2))
    return min(restitution, 1.0)  # Cap at 1.0 for perfect collisions

# Initialize pygame and get screen info
game.init()
info = game.display.Info()
screen_size = (info.current_w, info.current_h)

# Terminal input for customizing block parameters
print("\nCustomize the block properties:")
B1_mass = float(input("Enter mass of Block 1 (large block): "))
B1_velocity = float(input("Enter velocity of Block 1 (e.g., -300): "))
B2_mass = float(input("Enter mass of Block 2 (small block): "))
B2_velocity = float(input("Enter velocity of Block 2 (e.g., 0): "))


def predict_next_collision():
    """Calculate and display the time until next collision and location."""
    if B1.v1 == B2.v1:  # No collision if same velocity
        return None, None
        
    # Time to collision between blocks
    if B2.v1 < B1.v1:  # Block 2 will catch up to Block 1
        time_to_b1b2 = distance / (B2.v1 - B1.v1) if B2.v1 != B1.v1 else float('inf')
    else:
        time_to_b1b2 = float('inf')
    
    # Time to wall collision
    time_to_wall = -B2.x / B2.v1 if B2.v1 < 0 else float('inf')
    
    # Return the sooner collision
    if time_to_wall < time_to_b1b2:
        return time_to_wall, "wall"
    else:
        return time_to_b1b2, "blocks"
    
    
    
    
    
def calculate_pi_approximation():
    """For specific mass ratios, collision count approximates π - display this relationship."""
    if abs(B1.m / B2.m - 100) < 0.1:  # Close to 100:1 ratio
        pi_approximation = collision / 31.5  # Scale factor for 100:1 ratio
        return pi_approximation
    elif abs(B1.m / B2.m - 10000) < 10:  # Close to 10000:1 ratio
        pi_approximation = collision / 314.2  # Scale factor for 10000:1 ratio
        return pi_approximation
    return None

# Fonts and screen
game.font.init()
font = game.font.Font(None, 48)
desc_font = game.font.Font(None, 28)
small_font = game.font.Font(None, 22)
screen = game.display.set_mode(screen_size)
tick_sound = game.mixer.Sound("tick.wav")
screen.set_alpha(None)
clock = game.time.Clock()

running = True
dt = 0
collision = 0
white = (255, 255, 255)

# Block classes
class B1:
    m = B1_mass
    v1 = B1_velocity
    v2 = 0
    size = 200
    x = screen_size[0] * 0.65
    y = screen_size[1] * 0.5

class B2:
    m = B2_mass
    v1 = B2_velocity
    v2 = 0
    size = 100
    x = screen_size[0] * 0.4
    y = screen_size[1] * 0.5 + (B1.size - 100)





# Game loop
while running:
    for event in game.event.get():
        if event.type == game.QUIT:
            running = False

    distance = B1.x - (B2.x + B2.size)
    screen.fill("black")

    # Display info panel
    screen.blit(font.render("Collisions: " + str(collision), True, white), (50, 30))
    screen.blit(font.render("Distance: " + str(int(distance)) + " px", True, white), (50, 80))

    # Block 1 Info (Big Block)
    screen.blit(desc_font.render("Block 1 (Big):", True, white), (50, 150))
    screen.blit(small_font.render("Mass: " + str(B1.m) + " kg", True, white), (60, 180))
    screen.blit(small_font.render("Velocity: " + str(round(B1.v1, 3)) + " px/s", True, white), (60, 210))
    screen.blit(small_font.render("Momentum: " + str(round(B1.m * B1.v1, 3)) + " kg·px/s", True, white), (60, 240))
    screen.blit(small_font.render("KE: " + str(round(0.5 * B1.m * B1.v1**2, 3)) + " J", True, white), (60, 270))
    screen.blit(small_font.render("X-Position: " + str(round(B1.x, 2)) + " px", True, white), (60, 300))

    # Block 2 Info (Small Block)
    screen.blit(desc_font.render("Block 2 (Small):", True, white), (50, 350))
    screen.blit(small_font.render("Mass: " + str(B2.m) + " kg", True, white), (60, 380))
    screen.blit(small_font.render("Velocity: " + str(round(B2.v1, 3)) + " px/s", True, white), (60, 410))
    screen.blit(small_font.render("Momentum: " + str(round(B2.m * B2.v1, 3)) + " kg·px/s", True, white), (60, 440))
    screen.blit(small_font.render("KE: " + str(round(0.5 * B2.m * B2.v1**2, 3)) + " J", True, white), (60, 470))
    screen.blit(small_font.render("X-Position: " + str(round(B2.x, 2)) + " px", True, white), (60, 500))

    # Draw blocks
    game.draw.rect(screen, white, game.Rect(B1.x, B1.y, B1.size, B1.size))
    game.draw.rect(screen, white, game.Rect(B2.x, B2.y, B2.size, B2.size))
    game.draw.line(screen, (0, 255, 0), (0, B1.y + B1.size), (screen_size[0], B1.y + B1.size), 5)

    # Fast-forward convergence hack
    while abs(B2.v1) > 20000:
        if ((B2.x + B2.size) >= B1.x) and (B1.v1 <= B2.v1):
            collision += 1
            B1.v2 = (((B1.m * B1.v1) + (B2.m * B2.v1)) - (B2.m * (B1.v1 - B2.v1))) / (B1.m + B2.m)
            B2.v2 = B1.v2 + (B1.v1 - B2.v1)
            B1.v1 = B1.v2
            B2.v1 = B2.v2
        elif (B2.x <= 0) and (B2.v1 < 0):
            collision += 1
            B2.v1 *= -1

        B1.x += B1.v1 * dt
        B2.x += B2.v1 * dt

    # Handle actual collision
    if ((B2.x + B2.size) >= B1.x) and (B1.v1 <= B2.v1):
        collision += 1
        game.mixer.Sound.play(tick_sound)
        B1.v2 = (((B1.m * B1.v1) + (B2.m * B2.v1)) - (B2.m * (B1.v1 - B2.v1))) / (B1.m + B2.m)
        B2.v2 = B1.v2 + (B1.v1 - B2.v1)
        B1.v1 = B1.v2
        B2.v1 = B2.v2

    elif (B2.x <= 0) and (B2.v1 < 0):
        collision += 1
        game.mixer.Sound.play(tick_sound)
        B2.v1 *= -1

    # Update positions
    B1.x += B1.v1 * dt
    B2.x += B2.v1 * dt

    game.display.flip()
    dt = clock.tick(100000000) / 1000

game.quit()


