import pygame
import pygame.freetype
import random
import numpy as np
import time
import math


class Ant:
    def __init__(self, start_x, start_y):
        self.x = start_x
        self.y = start_y
        self.size = 3
        self.direction = random.uniform(0, 2 * np.pi)
        self.emission = "home"
        self.sense = ANT_SENSE
        self.max_move = 3
        self.surf = pygame.Surface((self.size, self.size))
        self.surf.fill(ANT_COLOR)
        self.dist = 100

    def display_ant(self, display: pygame.Surface):
        display.blit(self.surf, (self.x - 1, self.y - 1))

    def move(self, x, y, display):
        self.find_and_set_angle(x, y)
        d1, d2 = pygame.math.Vector2(), pygame.math.Vector2()
        d1.xy = x, y
        d2.xy = self.x, self.y
        dist = d1.distance_to(d2)
        if dist > self.max_move:
            self.x = round(self.max_move * np.cos(self.direction)) + self.x % DISPLAY_WIDTH
            self.y = round(self.max_move * -np.sin(self.direction)) + self.y % DISPLAY_HEIGHT
        else:
            self.x, self.y = x, y
        self.display_ant(display)

    def move_random(self, display: pygame.Surface):
        self.new_random_direction()
        distance = (random.randint(0, self.max_move))
        # self.x = round(distance * np.cos(self.direction)) + self.x % DISPLAY_WIDTH
        # self.y = round(distance * -np.sin(self.direction)) + self.y % DISPLAY_HEIGHT
        newx = round(distance * np.cos(self.direction)) + self.x
        newy = round(distance * -np.sin(self.direction)) + self.y
        if newx < 1 or newx > DISPLAY_WIDTH or newy < 1 or newy > DISPLAY_HEIGHT:
            self.direction += np.pi
        if newx < 1: newx = 1
        if newy < 1: newy = 1
        if newx > DISPLAY_WIDTH: newx = DISPLAY_WIDTH
        if newy > DISPLAY_HEIGHT: newy = DISPLAY_HEIGHT
        self.x, self.y = newx, newy
        self.dist -= 1
        self.display_ant(display)

    def new_random_direction(self):
        # self.direction = (random.uniform(-self.angle, self.angle) + self.direction) % (2 * np.pi)
        self.direction = random.vonmisesvariate(self.direction, 80)

    def is_sensible(self, x, y):
        d1, d2 = pygame.math.Vector2(), pygame.math.Vector2()
        d1.xy = x, y
        d2.xy = self.x, self.y
        return d1.distance_to(d2) <= self.sense

    def find_and_set_angle(self, x, y):
        diffx, diffy = x - self.x, self.y - y
        self.direction = np.arctan2(diffy, diffx)


class Pheromon:
    def __init__(self, life_expect, x, y, color: (int, int, int)):
        self.life_expectancy = life_expect
        self.life = 0
        self.display_time = 60 / 100 * life_expect
        self.x, self.y = x, y
        self.color = color
        self.size = 2
        self.surf = pygame.Surface((self.size, self.size))
        self.surf.fill(self.color)

    def circle_draw(self, display: pygame.Surface):
        if self.life >= self.display_time:
            return
        # transp = round(255 / self.display_time * (self.display_time - self.life))
        # surf = pygame.Surface((self.size, self.size))
        self.surf.set_alpha(self.display_time - self.life)
        # self.surf.fill(self.color)
        display.blit(self.surf, (self.x, self.y))

    def add_life(self):
        self.life += 1

    def survive(self):
        return self.life < self.life_expectancy


class Food:
    def __init__(self, x, y, n, image, radius):
        self.x, self.y = x, y
        self.max_nutrition = n
        self.remaining_nutrition = n
        self.image = image
        self.radius = radius

    def display_food(self, display: pygame.Surface):
        transp = round(235 / self.max_nutrition * self.remaining_nutrition + 20)
        self.image.set_alpha(transp)
        display.blit(self.image, (self.x - self.radius, self.y - self.radius))


class Colony:
    def __init__(self, x, y, n, n_tile):
        self.x, self.y = x, y
        self.ants = [Ant(x, y) for _ in range(n)]
        self.ants_surface = pygame.Surface((DISPLAY_WIDTH, DISPLAY_HEIGHT))
        self.tiles = list(range(0, n_tile))
        self.pheromons = {i: [] for i in self.tiles}
        self.pheromons_radius = 2
        self.pheromons_surface = pygame.Surface((DISPLAY_WIDTH, DISPLAY_HEIGHT))
        self.step = 7
        self.foods = []
        self.foods_radius = 10
        self.foods_image = pygame.image.load('./images/apple.png')
        self.foods_image = pygame.transform.scale(self.foods_image,
                                                  (self.foods_radius * 2, self.foods_radius * 2))

    def display_ants(self, display):
        for ant in self.ants:
            ant.display_ant(display)

    def move_ants(self, display: pygame.Surface):
        for ant in self.ants:
            for f in self.foods:
                if ant.is_sensible(f.x, f.y):
                    ant.move(f.x, f.y, display)
                    break
            else:
                ant.move_random(display)

    def update_pheromons(self, display):
        if self.step == 7:
            self.step = 0
            for a in self.ants:
                # self.pheromons.append(Pheromon(250, a.x, a.y, house_pheromon_color))
                self.pheromons[(a.x - 1) // TILE_SIZE + ((a.y - 1) // TILE_SIZE * N_WIDTH)].append(
                    Pheromon(250, a.x, a.y, house_pheromon_color))
        temp_pheromons = {}
        for t in self.pheromons:
            temp_pheromons[t] = []
            for p in self.pheromons[t]:
                if p.survive():
                    temp_pheromons[t].append(p)
                    p.circle_draw(display)
                    p.add_life()
        self.pheromons = temp_pheromons
        self.step += 1

    def one_turn(self, display):
        t1 = time.time()
        self.update_pheromons(display)
        for f in self.foods:
            f.display_food(display)
        t2 = time.time()
        self.move_ants(display)
        t3 = time.time()
        print(f"move ants : {t3 - t2}, pheromons : {t2 - t1}")

    def add_food(self, x, y, display):
        food = Food(x, y, 150, self.foods_image, self.foods_radius)
        self.foods.append(food)
        food.display_food(display)

    def remove_food(self, x, y):
        temp_food = []
        for f in self.foods:
            if x >= f.x + self.foods_radius or x <= f.x - self.foods_radius or y >= f.y + self.foods_radius or y <= f.y - self.foods_radius:
                temp_food.append(f)
        self.foods = temp_food


if __name__ == "__main__":

    pygame.init()

    GAME_FONT = pygame.freetype.SysFont("Arial", 16)

    DISPLAY_WIDTH, DISPLAY_HEIGHT = 1040, 800
    TILE_SIZE = ANT_SENSE = 40
    DISPLAY_WIDTH = math.floor(DISPLAY_WIDTH / TILE_SIZE) * TILE_SIZE
    DISPLAY_HEIGHT = math.floor(DISPLAY_HEIGHT / TILE_SIZE) * TILE_SIZE
    N_WIDTH, N_HEIGHT = DISPLAY_WIDTH // TILE_SIZE, DISPLAY_HEIGHT // TILE_SIZE
    n_tile = N_WIDTH * N_HEIGHT

    HOUSE_X, HOUSE_Y = DISPLAY_WIDTH // 2, DISPLAY_HEIGHT // 2
    black = (0, 0, 0)
    white = (255, 255, 255)
    house_pheromon_color, food_pheromon_color = [214, 51, 255], [0, 230, 0]
    ANT_COLOR = white
    n_ant = 4000

    ant_size = 15

    gameDisplay = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
    pygame.display.set_caption('Vive les fourmis')

    clock = pygame.time.Clock()

    crashed = False
    is_pause = True

    gameDisplay.fill(black)
    simulation = Colony(HOUSE_X, HOUSE_Y, n_ant, n_tile)

    while not crashed:
        t2 = time.time()
        gameDisplay.fill(black)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                crashed = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    is_pause = not is_pause
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                if event.button == 1:
                    simulation.add_food(pos[0], pos[1], gameDisplay)
                elif event.button == 3:
                    simulation.remove_food(pos[0], pos[1])
        if is_pause:
            GAME_FONT.render_to(gameDisplay, (20, 40), "To unpause game press spacebar", white)
            # simulation.display_ants(gameDisplay)
        else:
            # GAME_FONT.render_to(gameDisplay, (20, 40), str(int(clock.get_fps())), white)
            simulation.one_turn(gameDisplay)
        GAME_FONT.render_to(gameDisplay, (10, 10), f"{str(int(clock.get_fps()))} fps", white)
        pygame.display.update()
        # print("turn time :", time.time()-t2)
        clock.tick(30)
    pygame.quit()
    quit()
