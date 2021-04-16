import pygame
import pygame.freetype
import random
import numpy as np
import math


# import sys
# from pympler import asizeof


class Ant:
    def __init__(self, start_x, start_y):
        self.size = 20
        self.x = start_x
        self.y = start_y
        self.image = pygame.image.load('./images/ant.png')
        self.image = pygame.transform.scale(self.image, (self.size, self.size))
        self.direction = random.uniform(0, 2 * np.pi)
        self.angle = 0.15 * np.pi
        self.emission = "home"
        self.emission_step = 10
        self.current_step = 0

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


class Pheromon:
    def __init__(self, life_expect, x, y, color: (int, int, int), image_path):
        self.life_expectancy = life_expect
        self.life = 0
        self.x, self.y = x, y
        self.color = color
        self.radius = 3
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (self.radius * 2, self.radius * 2))

    def circle_draw(self, display: pygame.Surface):
        transp = round(255 / self.life_expectancy * (self.life_expectancy - self.life))
        self.image.set_alpha(transp)
        display.blit(self.image, (self.x - self.radius, self.y - self.radius))

    def add_life(self):
        self.life += 1

    def survive(self):
        return self.life < self.life_expectancy


class Colony:
    def __init__(self, x, y, n):
        self.x, self.y = x, y
        self.ants = [Ant(x, y) for _ in range(n)]
        self.pheromons = []
        self.step = 10

    def display_ants(self, display):
        for ant in self.ants:
            ant.display_ant(display)

    def move_ants(self, display: pygame.Surface):
        for ant in self.ants:
            ant.move_random(10, display)

    def update_pheromons(self, display):
        if self.step == 10:
            self.step = 0
            for a in self.ants:
                self.pheromons.append(Pheromon(150, a.x, a.y, house_pheromon_color, './images/to_house.png'))
        temp_pheromons = []
        for i, p in enumerate(self.pheromons):
            if p.survive():
                temp_pheromons.append(p)
                p.circle_draw(display)
                p.add_life()
        self.pheromons = temp_pheromons
        self.step += 1

    def one_turn(self, display):
        self.move_ants(display)
        self.update_pheromons(display)


pygame.init()

GAME_FONT = pygame.freetype.SysFont("Arial", 24)

DISPLAY_WIDTH, DISPLAY_HEIGHT = 1280, 720
HOUSE_X, HOUSE_Y = DISPLAY_WIDTH // 2, DISPLAY_HEIGHT // 2
house_pheromon_color, food_pheromon_color = [214, 51, 255], [0, 230, 0]
n_ant = 200

ant_size = 15


gameDisplay = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
pygame.display.set_caption('Vive les fourmis')

black = (0, 0, 0)
white = (255, 255, 255)

clock = pygame.time.Clock()

crashed = False
is_pause = True

gameDisplay.fill(black)
simulation = Colony(HOUSE_X, HOUSE_Y, n_ant)

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
        simulation.display_ants(gameDisplay)
    else:
        GAME_FONT.render_to(gameDisplay, (20, 40), str(int(clock.get_fps())), white)
        simulation.one_turn(gameDisplay)
        # print(simulation.ants[0].direction * 180 / np.pi, simulation.ants[0].x, simulation.ants[0].y)
    pygame.display.update()
    # print(asizeof.asizeof(gameDisplay))
    clock.tick(20)
pygame.quit()
quit()
