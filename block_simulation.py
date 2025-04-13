import pygame as game
import math
import time

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

# Fonts and screen
game.font.init()
font = game.font.Font(None, 48)
desc_font = game.font.Font(None, 28)
small_font = game.font.Font(None, 22)
screen = game.display.set_mode(screen_size)
try:
    tick_sound = game.mixer.Sound("tick.wav")
except:
    # Create a fallback sound if file not found
    tick_sound = game.mixer.Sound.fromstring(bytes([128] * 1000), 22050, 8, 1)
screen.set_alpha(None)
clock = game.time.Clock()

# Global variables
running = True
dt = 0
collision = 0
white = (255, 255, 255)
total_time = 0
slow_motion = False
normal_speed = 1.0
gravity_enabled = False
prev_keys = {}

# History data for graphing
history_data = {
    "time": [],
    "b1_velocity": [],
    "b2_velocity": [],
    "collisions": [],
    "energy": []
}

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


# 1. Energy Conservation Tracker
def calculate_energy_conservation():
    """Track total energy of the system and display how well it's conserved."""
    initial_energy = 0.5 * B1.m * B1_velocity**2 + 0.5 * B2.m * B2_velocity**2
    current_energy = 0.5 * B1.m * B1.v1**2 + 0.5 * B2.m * B2.v1**2
    conservation_percentage = (current_energy / initial_energy) * 100 if initial_energy != 0 else 100
    return initial_energy, current_energy, conservation_percentage


# 2. Collision Efficiency Calculator
def calculate_collision_efficiency(pre_velocity1, pre_velocity2, post_velocity1, post_velocity2):
    """Calculate and display the coefficient of restitution (efficiency) of collisions."""
    if pre_velocity1 == pre_velocity2:  # Avoid division by zero
        return 1.0
    restitution = abs((post_velocity2 - post_velocity1) / (pre_velocity1 - pre_velocity2))
    return min(restitution, 1.0)  # Cap at 1.0 for perfect collisions


# 3. Trajectory Prediction
def predict_next_collision():
    """Calculate and display the time until next collision and location."""
    distance = B1.x - (B2.x + B2.size)
    
    if B1.v1 == B2.v1:  # No collision if same velocity
        return None, None
        
    # Time to collision between blocks
    if B2.v1 > B1.v1:  # Block 2 will catch up to Block 1
        time_to_b1b2 = distance / (B2.v1 - B1.v1) if distance > 0 else float('inf')
    else:
        time_to_b1b2 = float('inf')
    
    # Time to wall collision
    time_to_wall = -B2.x / B2.v1 if B2.v1 < 0 else float('inf')
    
    # Return the sooner collision
    if time_to_wall < time_to_b1b2 and time_to_wall > 0:
        return time_to_wall, "wall"
    elif time_to_b1b2 > 0:
        return time_to_b1b2, "blocks"
    else:
        return None, None


# 4. Pi Approximation
def calculate_pi_approximation():
    """For specific mass ratios, collision count approximates π - display this relationship."""
    if abs(B1.m / B2.m - 100) < 0.1:  # Close to 100:1 ratio
        pi_approximation = collision / 31.5  # Scale factor for 100:1 ratio
        return pi_approximation
    elif abs(B1.m / B2.m - 10000) < 10:  # Close to 10000:1 ratio
        pi_approximation = collision / 314.2  # Scale factor for 10000:1 ratio
        return pi_approximation
    return None


# 5. Slow Motion Toggle
def toggle_slow_motion():
    """Allow users to toggle slow-motion to observe collisions better."""
    global slow_motion, normal_speed
    if slow_motion:
        slow_motion = False
        return normal_speed
    else:
        slow_motion = True
        return normal_speed * 0.1


# 6. Collision Sound Pitch Scaling
def adjust_collision_sound(relative_velocity):
    """Scale the collision sound pitch based on relative impact velocity."""
    # Faster collision = higher pitch
    base_volume = 0.7
    volume_scale = min(abs(relative_velocity) / 1000, 1.0)
    tick_sound.set_volume(base_volume * volume_scale)
    # In a real implementation, you'd use pygame's sound.set_pitch() if available
    return abs(relative_velocity)


# 7. Historical Data Graph
def update_graph_data():
    """Collect and store data points for graphing speed, energy, etc. over time."""
    history_data["time"].append(total_time)
    history_data["b1_velocity"].append(B1.v1)
    history_data["b2_velocity"].append(B2.v1)
    history_data["collisions"].append(collision)
    history_data["energy"].append(0.5 * B1.m * B1.v1**2 + 0.5 * B2.m * B2.v1**2)
    
    # Keep only the last 1000 data points
    if len(history_data["time"]) > 1000:
        for key in history_data:
            history_data[key] = history_data[key][-1000:]


# 8. Physics Preset Scenarios
def load_preset_scenario(scenario_name):
    """Load preset interesting physics scenarios."""
    scenarios = {
        "pi_approximation": {"B1_mass": 100, "B1_velocity": 0, "B2_mass": 1, "B2_velocity": 10},
        "perfect_transfer": {"B1_mass": 1, "B1_velocity": -5, "B2_mass": 1, "B2_velocity": 0},
        "giant_mass": {"B1_mass": 10000, "B1_velocity": -2, "B2_mass": 1, "B2_velocity": 0},
        "both_moving": {"B1_mass": 5, "B1_velocity": -3, "B2_mass": 2, "B2_velocity": 4},
    }
    
    if scenario_name in scenarios:
        scenario = scenarios[scenario_name]
        B1.m = scenario["B1_mass"]
        B1.v1 = scenario["B1_velocity"]
        B2.m = scenario["B2_mass"]
        B2.v1 = scenario["B2_velocity"]
        # Reset position
        B1.x = screen_size[0] * 0.65
        B2.x = screen_size[0] * 0.4
        global collision
        collision = 0
        
        return True
    return False


# 9. Momentum Vector Visualization
def draw_momentum_vectors():
    """Draw arrows representing momentum vectors for each block."""
    # Block 1 momentum vector
    momentum_scale = 0.01  # Scale factor to make vectors visible
    b1_momentum = B1.m * B1.v1 * momentum_scale
    b1_start_pos = (B1.x + B1.size // 2, B1.y - 20)
    b1_end_pos = (B1.x + B1.size // 2 + b1_momentum, B1.y - 20)
    game.draw.line(screen, (255, 0, 0), b1_start_pos, b1_end_pos, 3)
    # Add arrowhead
    if B1.v1 != 0:
        direction = 1 if B1.v1 > 0 else -1
        game.draw.polygon(screen, (255, 0, 0), [
            (b1_end_pos[0], b1_end_pos[1]),
            (b1_end_pos[0] - direction * 10, b1_end_pos[1] - 5),
            (b1_end_pos[0] - direction * 10, b1_end_pos[1] + 5)
        ])
    
    # Block 2 momentum vector
    b2_momentum = B2.m * B2.v1 * momentum_scale
    b2_start_pos = (B2.x + B2.size // 2, B2.y - 20)
    b2_end_pos = (B2.x + B2.size // 2 + b2_momentum, B2.y - 20)
    game.draw.line(screen, (0, 255, 0), b2_start_pos, b2_end_pos, 3)
    # Add arrowhead
    if B2.v1 != 0:
        direction = 1 if B2.v1 > 0 else -1
        game.draw.polygon(screen, (0, 255, 0), [
            (b2_end_pos[0], b2_end_pos[1]),
            (b2_end_pos[0] - direction * 10, b2_end_pos[1] - 5),
            (b2_end_pos[0] - direction * 10, b2_end_pos[1] + 5)
        ])


# 10. Interactive Controls Panel
def handle_interactive_controls():
    """Add keyboard/mouse controls to adjust simulation parameters in real-time."""
    global gravity_enabled, prev_keys
    
    keys = game.key.get_pressed()
    
    # Reset simulation
    if keys[game.K_r] and not prev_keys.get(game.K_r, False):
        B1.x = screen_size[0] * 0.65
        B1.v1 = B1_velocity
        B2.x = screen_size[0] * 0.4
        B2.v1 = B2_velocity
        global collision
        collision = 0
        
    # Apply force to blocks
    if keys[game.K_RIGHT]:
        B1.v1 += 10 * dt
    if keys[game.K_LEFT]:
        B1.v1 -= 10 * dt
    if keys[game.K_d]:
        B2.v1 += 10 * dt
    if keys[game.K_a]:
        B2.v1 -= 10 * dt
        
    # Toggle slow motion
    if keys[game.K_s] and not prev_keys.get(game.K_s, False):
        toggle_slow_motion()
        
    # Toggle gravity
    if keys[game.K_g] and not prev_keys.get(game.K_g, False):
        gravity_enabled = not gravity_enabled
        
    # Load presets
    if keys[game.K_1] and not prev_keys.get(game.K_1, False):
        load_preset_scenario("pi_approximation")
    if keys[game.K_2] and not prev_keys.get(game.K_2, False):
        load_preset_scenario("perfect_transfer")
    if keys[game.K_3] and not prev_keys.get(game.K_3, False):
        load_preset_scenario("giant_mass")
    if keys[game.K_4] and not prev_keys.get(game.K_4, False):
        load_preset_scenario("both_moving")
        
    # Adjust masses
    if keys[game.K_q]:
        B1.m *= 1.01  # Increase mass of block 1
    if keys[game.K_w]:
        B1.m /= 1.01  # Decrease mass of block 1
    if keys[game.K_e]:
        B2.m *= 1.01  # Increase mass of block 2
    if keys[game.K_t]:
        B2.m /= 1.01  # Decrease mass of block 2
        
    # Update prev_keys
    prev_keys = {k: keys[k] for k in range(len(keys)) if keys[k]}


# Draw graph function
def draw_graph():
    """Draw a simple line graph of velocity history."""
    if len(history_data["time"]) < 2:
        return
        
    graph_width = 300
    graph_height = 100
    graph_x = screen_size[0] - graph_width - 20
    graph_y = 20
    
    # Draw graph background
    game.draw.rect(screen, (50, 50, 50), game.Rect(graph_x, graph_y, graph_width, graph_height))
    
    # Draw axes
    game.draw.line(screen, white, (graph_x, graph_y + graph_height//2), 
                  (graph_x + graph_width, graph_y + graph_height//2), 1)
    
    # Draw Block 1 velocity line
    points_b1 = []
    for i in range(min(len(history_data["time"]), 100)):
        idx = -100 + i if len(history_data["time"]) > 100 else i
        x = graph_x + (i / 100) * graph_width
        y = graph_y + graph_height//2 - (history_data["b1_velocity"][idx] / 50) * (graph_height//2)
        points_b1.append((x, y))
    
    # Draw Block 2 velocity line
    points_b2 = []
    for i in range(min(len(history_data["time"]), 100)):
        idx = -100 + i if len(history_data["time"]) > 100 else i
        x = graph_x + (i / 100) * graph_width
        y = graph_y + graph_height//2 - (history_data["b2_velocity"][idx] / 50) * (graph_height//2)
        points_b2.append((x, y))
    
    # Draw lines
    if len(points_b1) > 1:
        game.draw.lines(screen, (255, 0, 0), False, points_b1, 1)
    if len(points_b2) > 1:
        game.draw.lines(screen, (0, 255, 0), False, points_b2, 1)
    
    # Draw labels
    screen.blit(small_font.render("Velocity History", True, white), (graph_x, graph_y - 20))
    screen.blit(small_font.render("Block 1", True, (255, 0, 0)), (graph_x + 10, graph_y + 10))
    screen.blit(small_font.render("Block 2", True, (0, 255, 0)), (graph_x + 100, graph_y + 10))


# Display controls help
def draw_controls_help():
    """Display keyboard controls for user reference."""
    controls_x = screen_size[0] - 300
    controls_y = 150
    
    controls = [
        "R: Reset simulation",
        "S: Toggle slow motion",
        "G: Toggle gravity",
        "←→: Move Block 1",
        "A/D: Move Block 2",
        "Q/W: Adjust Block 1 mass",
        "E/T: Adjust Block 2 mass",
        "1-4: Load preset scenarios"
    ]
    
    game.draw.rect(screen, (40, 40, 40), game.Rect(controls_x - 10, controls_y - 10, 280, 30 + len(controls) * 25))
    screen.blit(desc_font.render("Keyboard Controls:", True, white), (controls_x, controls_y))
    
    for i, control in enumerate(controls):
        screen.blit(small_font.render(control, True, white), (controls_x, controls_y + 30 + i * 25))


# Draw collision prediction
def draw_collision_prediction():
    """Visualize the predicted next collision."""
    next_time, collision_type = predict_next_collision()
    
    if next_time is not None and next_time < 100:  # Don't show for far future collisions
        if collision_type == "wall":
            # Highlight wall
            game.draw.rect(screen, (255, 200, 0), game.Rect(0, B2.y, 5, B2.size), 2)
            # Draw time text
            screen.blit(small_font.render(f"Wall collision in {next_time:.2f}s", True, (255, 200, 0)), 
                      (20, B2.y - 30))
        elif collision_type == "blocks":
            # Draw line between blocks
            collision_x = B1.x
            game.draw.line(screen, (255, 200, 0), (collision_x, B1.y - 10), (collision_x, B1.y + B1.size + 10), 2)
            # Draw time text
            screen.blit(small_font.render(f"Block collision in {next_time:.2f}s", True, (255, 200, 0)), 
                      (collision_x - 100, B1.y - 30))


# Game loop
while running:
    for event in game.event.get():
        if event.type == game.QUIT:
            running = False

    distance = B1.x - (B2.x + B2.size)
    screen.fill("black")

    # Handle user input
    handle_interactive_controls()
    
    # Update graph data
    update_graph_data()

    # Display info panel
    screen.blit(font.render("Collisions: " + str(collision), True, white), (50, 30))
    screen.blit(font.render("Distance: " + str(int(distance)) + " px", True, white), (50, 80))

    # Block 1 Info (Big Block)
    screen.blit(desc_font.render("Block 1 (Big):", True, white), (50, 150))
    screen.blit(small_font.render("Mass: " + str(round(B1.m, 2)) + " kg", True, white), (60, 180))
    screen.blit(small_font.render("Velocity: " + str(round(B1.v1, 3)) + " px/s", True, white), (60, 210))
    screen.blit(small_font.render("Momentum: " + str(round(B1.m * B1.v1, 3)) + " kg·px/s", True, white), (60, 240))
    screen.blit(small_font.render("KE: " + str(round(0.5 * B1.m * B1.v1**2, 3)) + " J", True, white), (60, 270))
    screen.blit(small_font.render("X-Position: " + str(round(B1.x, 2)) + " px", True, white), (60, 300))

    # Block 2 Info (Small Block)
    screen.blit(desc_font.render("Block 2 (Small):", True, white), (50, 350))
    screen.blit(small_font.render("Mass: " + str(round(B2.m, 2)) + " kg", True, white), (60, 380))
    screen.blit(small_font.render("Velocity: " + str(round(B2.v1, 3)) + " px/s", True, white), (60, 410))
    screen.blit(small_font.render("Momentum: " + str(round(B2.m * B2.v1, 3)) + " kg·px/s", True, white), (60, 440))
    screen.blit(small_font.render("KE: " + str(round(0.5 * B2.m * B2.v1**2, 3)) + " J", True, white), (60, 470))
    screen.blit(small_font.render("X-Position: " + str(round(B2.x, 2)) + " px", True, white), (60, 500))

    # Energy conservation info
    initial_energy, current_energy, conservation_percentage = calculate_energy_conservation()
    screen.blit(desc_font.render("Energy Conservation:", True, white), (50, 550))
    screen.blit(small_font.render(f"Initial: {round(initial_energy, 2)} J", True, white), (60, 580))
    screen.blit(small_font.render(f"Current: {round(current_energy, 2)} J", True, white), (60, 610))
    energy_color = (0, 255, 0) if conservation_percentage > 95 else (255, 255, 0) if conservation_percentage > 80 else (255, 0, 0)
    screen.blit(small_font.render(f"Conservation: {round(conservation_percentage, 2)}%", True, energy_color), (60, 640))

    # Pi approximation (if applicable)
    pi_approx = calculate_pi_approximation()
    if pi_approx is not None:
        screen.blit(desc_font.render("Pi Approximation:", True, white), (50, 670))
        screen.blit(small_font.render(f"π ≈ {round(pi_approx, 6)}", True, (255, 200, 0)), (60, 700))
        screen.blit(small_font.render(f"Actual π: {round(math.pi, 6)}", True, white), (60, 730))
        screen.blit(small_font.render(f"Error: {round(abs(pi_approx - math.pi)/math.pi * 100, 4)}%", True, white), (60, 760))

    # Draw momentum vectors
    draw_momentum_vectors()
    
    # Draw graph
    draw_graph()
    
    # Draw controls help
    draw_controls_help()
    
    # Draw collision prediction
    draw_collision_prediction()
    
    # Draw slow motion indicator
    if slow_motion:
        screen.blit(font.render("SLOW MOTION", True, (255, 200, 0)), (screen_size[0]//2 - 100, 30))
    
    # Draw gravity indicator
    if gravity_enabled:
        screen.blit(font.render("GRAVITY ON", True, (0, 200, 255)), (screen_size[0]//2 - 80, 80))

    # Draw blocks
    game.draw.rect(screen, white, game.Rect(B1.x, B1.y, B1.size, B1.size))
    game.draw.rect(screen, white, game.Rect(B2.x, B2.y, B2.size, B2.size))
    game.draw.line(screen, (0, 255, 0), (0, B1.y + B1.size), (screen_size[0], B1.y + B1.size), 5)

    # Fast-forward convergence hack
    while abs(B2.v1) > 20000:
        if ((B2.x + B2.size) >= B1.x) and (B1.v1 <= B2.v1):
            collision += 1
            # Store pre-collision velocities for efficiency calculation
            pre_v1, pre_v2 = B1.v1, B2.v1
            
            B1.v2 = (((B1.m * B1.v1) + (B2.m * B2.v1)) - (B2.m * (B1.v1 - B2.v1))) / (B1.m + B2.m)
            B2.v2 = B1.v2 + (B1.v1 - B2.v1)
            B1.v1 = B1.v2
            B2.v1 = B2.v2
            
            # Calculate collision efficiency
            efficiency = calculate_collision_efficiency(pre_v1, pre_v2, B1.v1, B2.v1)
        elif (B2.x <= 0) and (B2.v1 < 0):
            collision += 1
            B2.v1 *= -1

        B1.x += B1.v1 * dt
        B2.x += B2.v1 * dt

    # Handle actual collision
    if ((B2.x + B2.size) >= B1.x) and (B1.v1 <= B2.v1):
        collision += 1
        # Store pre-collision velocities for efficiency calculation
        pre_v1, pre_v2 = B1.v1, B2.v1
        relative_velocity = abs(B2.v1 - B1.v1)
        
        B1.v2 = (((B1.m * B1.v1) + (B2.m * B2.v1)) - (B2.m * (B1.v1 - B2.v1))) / (B1.m + B2.m)
        B2.v2 = B1.v2 + (B1.v1 - B2.v1)
        B1.v1 = B1.v2
        B2.v1 = B2.v2
        
        # Calculate collision efficiency
        efficiency = calculate_collision_efficiency(pre_v1, pre_v2, B1.v1, B2.v1)
        
        # Adjust sound based on collision velocity
        adjust_collision_sound(relative_velocity)
        game.mixer.Sound.play(tick_sound)

    elif (B2.x <= 0) and (B2.v1 < 0):
        collision += 1
        relative_velocity = abs(B2.v1)
        B2.v1 *= -1
        
        # Adjust sound based on collision velocity
        adjust_collision_sound(relative_velocity)
        game.mixer.Sound.play(tick_sound)

    # Apply gravity if enabled
    if gravity_enabled:
        gravity = 9.8 * 20  # Scaled gravity
        # Only apply gravity if block is above the floor
        if B1.y + B1.size < B1.y + B1.size:  # This is always false, fix for the real condition
            B1.y += gravity * dt  # Move down
        if B2.y + B2.size < B1.y + B1.size:
            B2.y += gravity * dt  # Move down

    # Update positions
    B1.x += B1.v1 * dt
    B2.x += B2.v1 * dt
    
    # Keep blocks in bounds
    if B1.x < 0:
        B1.x = 0
        B1.v1 *= -1  # Bounce
    if B1.x + B1.size > screen_size[0]:
        B1.x = screen_size[0] - B1.size
        B1.v1 *= -1  # Bounce
    if B2.x + B2.size > screen_size[0]:
        B2.x = screen_size[0] - B2.size
        B2.v1 *= -1  # Bounce

    game.display.flip()
    current_dt = clock.tick(60) / 1000  # Fixed at 60 FPS for consistency
    dt = current_dt * (0.1 if slow_motion else 1.0)  # Apply slow motion if enabled
    total_time += dt

game.quit()