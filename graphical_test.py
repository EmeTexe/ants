import pygame
import pygame.freetype
import random
import numpy as np


class Ant:
    def __init__(self, start_x, start_y):
        self.size = 15
        self.x = start_x
        self.y = start_y
        self.image = pygame.image.load('./images/ant.png')
        self.image = pygame.transform.scale(self.image, (self.size, self.size))
        self.direction = random.uniform(0, 2 * np.pi)
        self.angle = 0.25 * np.pi

    def display_ant(self, display: pygame.Surface):
        display.blit(self.image, (self.x - self.size // 2, self.y + self.size // 2))

    def update_x(self, new_x):
        self.x = new_x

    def update_y(self, new_y):
        self.y = new_y

    def move_random(self, dist, display: pygame.Surface):
        self.new_random_direction()
        self.update_x((random.randint(-dist, dist) + self.x) % DISPLAY_WIDTH)
        self.update_y((random.randint(-dist, dist) + self.y) % DISPLAY_HEIGHT)
        self.display_ant(display)

    def new_random_direction(self):
        self.direction = (random.uniform(-self.angle, self.angle) + self.direction) % (2 * np.pi)


class Colony:
    def __init__(self, x, y, n):
        self.x, self.y = x, y
        self.ants = [Ant(x, y) for _ in range(n)]

    def display_ants(self, display):
        for ant in self.ants:
            ant.display_ant(display)

    def move_ants(self, display: pygame.Surface):
        for ant in self.ants:
            ant.move_random(10, display)


pygame.init()

GAME_FONT = pygame.freetype.SysFont("Arial", 24)

DISPLAY_WIDTH = 1290
DISPLAY_HEIGHT = 720
HOUSE_X = DISPLAY_WIDTH // 2
HOUSE_Y = DISPLAY_HEIGHT // 2
n_ant = 2000

gameDisplay = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
pygame.display.set_caption('Vive les fourmis')

black = (0, 0, 0)
white = (255, 255, 255)

clock = pygame.time.Clock()

crashed = False
is_pause = True

gameDisplay.fill(black)
simulation = Colony(HOUSE_X, HOUSE_Y, 200)

while not crashed:
    gameDisplay.fill(black)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                is_pause = not is_pause
    if is_pause:
        GAME_FONT.render_to(gameDisplay, (20, 40), "To unpause game press spacebar", white)
    else:
        Colony.move_ants(gameDisplay)
    pygame.display.update()
    clock.tick(20)
pygame.quit()
quit()
