import pygame
import pygame.freetype
import random

pygame.init()

GAME_FONT = pygame.freetype.SysFont("Arial", 24)

DISPLAY_WIDTH = 1280
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
antImg = pygame.image.load('./images/ant.png', )
antImg = pygame.transform.scale(antImg, (16, 18))

is_pause = True


class Ant:
    def __init__(self, start_x, start_y):
        self.size = 15
        self.x = start_x
        self.y = start_y
        self.image = pygame.image.load('./images/ant.png')
        self.image = pygame.transform.scale(self.image, (self.size, self.size))

    def move_ant(self, display: pygame.Surface):
        display.blit(self.image, (self.x - self.size // 2, self.y + self.size // 2))

    def update_x(self, new_x):
        self.x = new_x

    def update_y(self, new_y):
        self.y = new_y

    def move_random(self, dist):
        self.update_x((random.randint(-dist, dist) + self.x) % DISPLAY_WIDTH)
        self.update_y((random.randint(-dist, dist) + self.y) % DISPLAY_HEIGHT)


def move_colony(colony, display: pygame.Surface):
    for ant in colony:
        ant.move_random(10)
        ant.move_ant(display)


gameDisplay.fill(black)
colonies = []
for i in range(n_ant):
    colonies.append(Ant(HOUSE_X, HOUSE_Y))

for ant in colonies:
    ant.move_ant(gameDisplay)

x = (DISPLAY_WIDTH * 0.5)
y = (DISPLAY_HEIGHT * 0.5)

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
        move_colony(colonies, gameDisplay)
    pygame.display.update()
    clock.tick(20)
pygame.quit()
quit()
