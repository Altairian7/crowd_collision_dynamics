import pygame as game

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
screen = game.display.set_mode(screen_size)
tick_sound = game.mixer.Sound("tick.wav")
screen.set_alpha(None)
clock = game.time.Clock()

running = True
dt = 0
collision = 0
white = (255, 255, 255)

# Remove right wall bounce
infinite_collision = False  # Change this to False to disable right wall collision

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

    # Display info
    text_surface = font.render("Collision : " + str("{:,}".format(collision)), True, white)
    distance_text = font.render("Distance : " + str("{:,}".format(int(distance))), True, white)
    b1_mass = desc_font.render(str("{:,}".format(B1.m)) + " kg", True, white)
    b1_velocity = desc_font.render(str(round(B1.v1, 10)) + " px/s", True, white)
    b2_mass = desc_font.render(str("{:,}".format(B2.m)) + " kg", True, white)
    b2_velocity = desc_font.render(str(round(B2.v1, 10)) + " px/s", True, white)

    screen.blit(text_surface, (50, 50))
    screen.blit(distance_text, (50, 100))
    screen.blit(b1_mass, (B1.x, B1.y - 50))
    screen.blit(b2_mass, (B2.x, B2.y - 50))
    screen.blit(b1_velocity, (B1.x, B1.y - 25))
    screen.blit(b2_velocity, (B2.x, B2.y - 25))

    # Draw blocks
    game.draw.rect(screen, white, game.Rect(B1.x, B1.y, B1.size, B1.size))
    game.draw.rect(screen, white, game.Rect(B2.x, B2.y, B2.size, B2.size))
    game.draw.line(screen, (0, 255, 0), (0, B1.y + B1.size), (screen_size[0], B1.y + B1.size), 5)

    # High-speed convergence hack
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

    # Commented out right wall collision
    # elif (B1.x + B1.size >= screen_size[0]) and (B1.v1 > 0):
    #     if infinite_collision:
    #         collision += 1
    #         game.mixer.Sound.play(tick_sound)
    #         B1.v1 *= -1

    # Update positions
    B1.x += B1.v1 * dt
    B2.x += B2.v1 * dt

    game.display.flip()
    dt = clock.tick(100000000) / 1000

game.quit()
