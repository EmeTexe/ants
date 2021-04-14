import pygame
import pygame.freetype
import random
import numpy as np
import sys
from pympler import asizeof


class Ant:
    def __init__(self, start_x, start_y):
        self.size = 50
        self.x = start_x
        self.y = start_y
        self.image = pygame.image.load('./images/ant.png')
        self.image = pygame.transform.scale(self.image, (self.size, self.size))
        self.direction = random.uniform(0, 2 * np.pi)
        self.angle = 0.25 * np.pi

    def display_ant(self, display: pygame.Surface):
        new_image = pygame.transform.rotate(self.image, self.direction * 180 / np.pi)
        new_rectangle = new_image.get_rect(center=(self.x, self.y))
        display.blit(new_image, new_rectangle.topleft)

    def update_x(self, new_x):
        self.x = new_x

    def update_y(self, new_y):
        self.y = new_y

    def move_random(self, dist, display: pygame.Surface):
        self.new_random_direction()
        distance = (random.randint(0, dist))
        self.update_x(round(distance * np.cos(self.direction)) + self.x % DISPLAY_WIDTH)
        self.update_y(round(distance * -np.sin(self.direction)) + self.y % DISPLAY_HEIGHT)
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
            ant.move_random(60, display)


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
simulation = Colony(HOUSE_X, HOUSE_Y, 1)

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
        simulation.move_ants(gameDisplay)
        # print(simulation.ants[0].direction * 180 / np.pi, simulation.ants[0].x, simulation.ants[0].y)
    pygame.display.update()
    # print(asizeof.asizeof(gameDisplay))
    clock.tick(2)
pygame.quit()
quit()
