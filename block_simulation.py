import pygame as game
import math

# Initialize everything
game.init()
game.font.init()

# Screen setup
info = game.display.Info()
screen_size = (info.current_w, info.current_h)
screen = game.display.set_mode(screen_size)
screen.set_alpha(None)
clock = game.time.Clock()

# Load sound
tick_sound = game.mixer.Sound("tick.wav")

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
CYAN = (0, 200, 200)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BG = (10, 10, 10)

# Fonts
font = game.font.Font(None, 48)
desc_font = game.font.Font(None, 28)
small_font = game.font.Font(None, 22)

# State variables
collision_count = 0
paused = False
elastic = True

# Setup inputs
def get_user_inputs():
    print("\n🎮 Customize the block properties:")
    B1_mass = float(input("Mass of Block 1 (big): "))
    B1_velocity = float(input("Velocity of Block 1 (e.g., -300): "))
    B2_mass = float(input("Mass of Block 2 (small): "))
    B2_velocity = float(input("Velocity of Block 2 (e.g., 0): "))
    return B1_mass, B1_velocity, B2_mass, B2_velocity

# Block class with trail support
class Block:
    def __init__(self, mass, velocity, size, x, y):
        self.mass = mass
        self.v = velocity
        self.v2 = 0
        self.size = size
        self.x = x
        self.y = y
        self.trail = []

    def momentum(self):
        return self.mass * self.v

    def ke(self):
        return 0.5 * self.mass * self.v ** 2

    def update_trail(self):
        self.trail.append((self.x, self.y))
        if len(self.trail) > 25:
            self.trail.pop(0)

# Draw block with optional trail and velocity arrow
def draw_block(screen, block, color, show_trail=True):
    if show_trail:
        for point in block.trail:
            game.draw.rect(screen, CYAN, game.Rect(point[0], point[1], 4, 4))

    game.draw.rect(screen, color, game.Rect(block.x, block.y, block.size, block.size))
    arrow_len = 40 * (block.v / 100)
    game.draw.line(screen, YELLOW, (block.x + block.size // 2, block.y + block.size // 2),
                   (block.x + block.size // 2 + arrow_len, block.y + block.size // 2), 4)

# Physics update
def update_positions(B1, B2, dt):
    B1.x += B1.v * dt
    B2.x += B2.v * dt
    B1.update_trail()
    B2.update_trail()

# Handle collisions
def handle_collision(B1, B2):
    global collision_count
    if (B2.x + B2.size) >= B1.x and B1.v <= B2.v:
        game.mixer.Sound.play(tick_sound)
        collision_count += 1
        if elastic:
            total_mass = B1.mass + B2.mass
            B1.v2 = ((B1.mass - B2.mass) * B1.v + 2 * B2.mass * B2.v) / total_mass
            B2.v2 = ((B2.mass - B1.mass) * B2.v + 2 * B1.mass * B1.v) / total_mass
        else:  # perfectly inelastic
            v_final = (B1.mass * B1.v + B2.mass * B2.v) / (B1.mass + B2.mass)
            B1.v2 = B2.v2 = v_final
        B1.v, B2.v = B1.v2, B2.v2

    if B2.x <= 0 and B2.v < 0:
        game.mixer.Sound.play(tick_sound)
        collision_count += 1
        B2.v *= -1

# Draw UI panel
def draw_panel(screen, B1, B2, distance):
    screen.blit(font.render(f"Collisions: {collision_count}", True, WHITE), (50, 30))
    screen.blit(font.render(f"Distance: {int(distance)} px", True, WHITE), (50, 80))

    # Big block info
    screen.blit(desc_font.render("Block 1 (Big):", True, WHITE), (50, 140))
    screen.blit(small_font.render(f"Mass: {B1.mass} kg", True, WHITE), (60, 170))
    screen.blit(small_font.render(f"Velocity: {round(B1.v, 2)} px/s", True, WHITE), (60, 195))
    screen.blit(small_font.render(f"Momentum: {round(B1.momentum(), 2)}", True, WHITE), (60, 220))
    screen.blit(small_font.render(f"KE: {round(B1.ke(), 2)} J", True, WHITE), (60, 245))

    # Small block info
    screen.blit(desc_font.render("Block 2 (Small):", True, WHITE), (50, 290))
    screen.blit(small_font.render(f"Mass: {B2.mass} kg", True, WHITE), (60, 320))
    screen.blit(small_font.render(f"Velocity: {round(B2.v, 2)} px/s", True, WHITE), (60, 345))
    screen.blit(small_font.render(f"Momentum: {round(B2.momentum(), 2)}", True, WHITE), (60, 370))
    screen.blit(small_font.render(f"KE: {round(B2.ke(), 2)} J", True, WHITE), (60, 395))

# Keyboard controls
def handle_keys(event):
    global paused, elastic, collision_count
    if event.type == game.KEYDOWN:
        if event.key == game.K_SPACE:
            paused = not paused
        elif event.key == game.K_r:
            collision_count = 0
            reset_blocks()
        elif event.key == game.K_e:
            elastic = not elastic

# Reset blocks to initial state
def reset_blocks():
    B1.x = screen_size[0] * 0.65
    B2.x = screen_size[0] * 0.4
    B1.v = B1_init_v
    B2.v = B2_init_v
    B1.trail.clear()
    B2.trail.clear()

# Main program setup
B1_mass, B1_init_v, B2_mass, B2_init_v = get_user_inputs()
B1 = Block(B1_mass, B1_init_v, 200, screen_size[0] * 0.65, screen_size[1] * 0.5)
B2 = Block(B2_mass, B2_init_v, 100, screen_size[0] * 0.4, screen_size[1] * 0.5 + 100)
reset_blocks()

# Main loop
running = True
while running:
    dt = clock.tick(60) / 1000
    for event in game.event.get():
        if event.type == game.QUIT:
            running = False
        handle_keys(event)

    if not paused:
        handle_collision(B1, B2)
        update_positions(B1, B2, dt)

    distance = B1.x - (B2.x + B2.size)
    screen.fill(BG)
    draw_panel(screen, B1, B2, distance)
    draw_block(screen, B1, RED)
    draw_block(screen, B2, GREEN)
    game.draw.line(screen, (0, 100, 255), (0, B1.y + B1.size), (screen_size[0], B1.y + B1.size), 4)

    game.display.flip()

game.quit()
