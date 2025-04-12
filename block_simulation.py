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
