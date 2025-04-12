import pygame as game



def init_game():
    game.init()
    game.font.init()
    screen_info = game.display.Info()
    screen = game.display.set_mode((screen_info.current_w, screen_info.current_h))
    screen.set_alpha(None)
    return screen, (screen_info.current_w, screen_info.current_h)

def load_resources():
    return game.font.Font(None, 48), game.font.Font(None, 28), game.font.Font(None, 22), game.mixer.Sound("tick.wav")

def get_user_input():
    print("\nCustomize the block properties:")
    B1_mass = float(input("Enter mass of Block 1 (large block): "))
    B1_velocity = float(input("Enter velocity of Block 1 (e.g., -300): "))
    B2_mass = float(input("Enter mass of Block 2 (small block): "))
    B2_velocity = float(input("Enter velocity of Block 2 (e.g., 0): "))
    return B1_mass, B1_velocity, B2_mass, B2_velocity




class Block:
    def __init__(self, mass, velocity, size, x, y):
        self.m = mass
        self.v1 = velocity
        self.v2 = 0
        self.size = size
        self.x = x
        self.y = y
        
    
def handle_collision(B1, B2):
    """ Handle collision between two blocks. """
    B1.v2 = (((B1.m * B1.v1) + (B2.m * B2.v1)) - (B2.m * (B1.v1 - B2.v1))) / (B1.m + B2.m)
    B2.v2 = B1.v2 + (B1.v1 - B2.v1)
    B1.v1 = B1.v2
    B2.v1 = B2.v2




def draw_info(screen, fonts, B1, B2, collision, distance):
    font, desc_font, small_font = fonts
    white = (255, 255, 255)
    screen.fill("black")

    # Display statistics
    screen.blit(font.render(f"Collisions: {collision}", True, white), (50, 30))
    screen.blit(font.render(f"Distance: {int(distance)} px", True, white), (50, 80))

    # Block 1 Info
    screen.blit(desc_font.render("Block 1 (Big):", True, white), (50, 150))
    screen.blit(small_font.render(f"Mass: {B1.m} kg", True, white), (60, 180))
    screen.blit(small_font.render(f"Velocity: {round(B1.v1, 3)} px/s", True, white), (60, 210))
    screen.blit(small_font.render(f"Momentum: {round(B1.m * B1.v1, 3)} kg·px/s", True, white), (60, 240))
    screen.blit(small_font.render(f"KE: {round(0.5 * B1.m * B1.v1**2, 3)} J", True, white), (60, 270))
    screen.blit(small_font.render(f"X-Position: {round(B1.x, 2)} px", True, white), (60, 300))

    # Block 2 Info
    screen.blit(desc_font.render("Block 2 (Small):", True, white), (50, 350))
    screen.blit(small_font.render(f"Mass: {B2.m} kg", True, white), (60, 380))
    screen.blit(small_font.render(f"Velocity: {round(B2.v1, 3)} px/s", True, white), (60, 410))
    screen.blit(small_font.render(f"Momentum: {round(B2.m * B2.v1, 3)} kg·px/s", True, white), (60, 440))
    screen.blit(small_font.render(f"KE: {round(0.5 * B2.m * B2.v1**2, 3)} J", True, white), (60, 470))
    screen.blit(small_font.render(f"X-Position: {round(B2.x, 2)} px", True, white), (60, 500))

    # Draw blocks
    game.draw.rect(screen, white, game.Rect(B1.x, B1.y, B1.size, B1.size))
    game.draw.rect(screen, white, game.Rect(B2.x, B2.y, B2.size, B2.size))
    game.draw.line(screen, (0, 255, 0), (0, B1.y + B1.size), (screen.get_width(), B1.y + B1.size), 5)





def main():
    screen, screen_size = init_game()
    font, desc_font, small_font, tick_sound = load_resources()
    fonts = (font, desc_font, small_font)
    white = (255, 255, 255)

    B1_mass, B1_velocity, B2_mass, B2_velocity = get_user_input()

    # Create Block objects
    B1 = Block(B1_mass, B1_velocity, 200, screen_size[0] * 0.65, screen_size[1] * 0.5)
    B2 = Block(B2_mass, B2_velocity, 100, screen_size[0] * 0.4, screen_size[1] * 0.5 + 100)

    clock = game.time.Clock()
    collision = 0
    running = True
    dt = 0

    while running:
        for event in game.event.get():
            if event.type == game.QUIT:
                running = False

        distance = B1.x - (B2.x + B2.size)

        # Fast-forward edge case: high initial speed
        while abs(B2.v1) > 20000:
            if ((B2.x + B2.size) >= B1.x) and (B1.v1 <= B2.v1):
                collision += 1
                handle_collision(B1, B2)
            elif (B2.x <= 0) and (B2.v1 < 0):
                collision += 1
                B2.v1 *= -1

            B1.x += B1.v1 * dt
            B2.x += B2.v1 * dt

        # Handle regular collisions
        if ((B2.x + B2.size) >= B1.x) and (B1.v1 <= B2.v1):
            collision += 1
            game.mixer.Sound.play(tick_sound)
            handle_collision(B1, B2)

        elif (B2.x <= 0) and (B2.v1 < 0):
            collision += 1
            game.mixer.Sound.play(tick_sound)
            B2.v1 *= -1

        # Update positions
        B1.x += B1.v1 * dt
        B2.x += B2.v1 * dt

        draw_info(screen, fonts, B1, B2, collision, distance)
        game.display.flip()
        dt = clock.tick(120) / 1000  # cap at 120 FPS

    game.quit()

if __name__ == "__main__":
    main()