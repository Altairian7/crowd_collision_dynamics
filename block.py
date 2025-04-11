import pygame
import math

class Square(object):
    def __init__(self, size, XY, mass, velocity):
        self.x = XY[0]
        self.y = XY[1]
        self.mass = mass
        self.v = velocity
        self.size = size

    def collision(self, otherblock):
        return not (self.x + self.size < otherblock.x or self.x > otherblock.x + otherblock.size)

    def NewVelocity(self, otherblock):
        sumM = self.mass + otherblock.mass
        newV = (self.mass - otherblock.mass)/sumM * self.v
        newV += (2 * otherblock.mass / sumM) * otherblock.v
        return newV

    def collide_wall(self):
        if self.x <= 0:
            self.v *= -1
            return True
        return False

    def update(self):
        self.x += self.v

    def draw(self, background, otherblock):
        if self.x < 10:
            pygame.draw.rect(background, red, [10, self.y , self.size, self.size])
        else:
            pygame.draw.rect(background, red, [self.x, self.y , self.size, self.size])
        pygame.draw.rect(background, red, [otherblock.x, otherblock.y , otherblock.size, otherblock.size])

def redraw():
    background.fill(white)
    pygame.draw.rect(background, gray, [0 , 0, 800, 250])
    SquareBig.draw(background, SquareSmall)
    font = pygame.font.SysFont(None, 30)
    text = font.render(f"Collisions: {count}", True, (0,0,0))
    background.blit(text, [20, 260])
    background.blit(font.render(f"Big Mass: {SquareBig.mass:.1e}, Velocity: {SquareBig.v:.2f}", True, (0,0,0)), [20, 290])
    background.blit(font.render(f"Small Mass: {SquareSmall.mass}, Velocity: {SquareSmall.v:.2f}", True, (0,0,0)), [20, 320])
    background.blit(font.render("W/S: Big Mass | A/D: Big Vel | I/K: Small Mass | J/L: Small Vel", True, (0,0,0)), [20, 350])
    pygame.display.update()

width, height = 800, 400
white = (255,255,255)
gray = (190,190,190)
red = (200,0,0)

pygame.init()
power = math.pow(100, 5)
background = pygame.display.set_mode((width, height))

SquareBig = Square(50, (320,200), power, -0.9/10000)
SquareSmall = Square(10, (100, 240), 1, 0)

count = 0
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                SquareBig.mass *= 1.1
            elif event.key == pygame.K_s:
                SquareBig.mass /= 1.1
            elif event.key == pygame.K_a:
                SquareBig.v -= 0.01
            elif event.key == pygame.K_d:
                SquareBig.v += 0.01
            elif event.key == pygame.K_i:
                SquareSmall.mass *= 1.1
            elif event.key == pygame.K_k:
                SquareSmall.mass /= 1.1
            elif event.key == pygame.K_j:
                SquareSmall.v -= 0.01
            elif event.key == pygame.K_l:
                SquareSmall.v += 0.01

    for i in range(10000):
        if SquareSmall.collision(SquareBig):
            count += 1
            v1 = SquareSmall.NewVelocity(SquareBig)
            v2 = SquareBig.NewVelocity(SquareSmall)
            SquareBig.v = v2
            SquareSmall.v = v1

        if SquareSmall.collide_wall():
            count += 1

        SquareBig.update()
        SquareSmall.update()

    redraw()
    clock.tick(60)
