import pygame
from random import randint, randrange
import sys

pygame.init()

game_width = 600
game_height = 600
font = pygame.font.SysFont(None, 25)
screen = pygame.display.set_mode(size=(game_width, game_height))
screen_rect = pygame.Rect(0, 0, game_width, game_height)
clock = pygame.time.Clock()


def game_over_screen():
    screen.fill((0, 0, 0))
    msg = font.render("You Lost! Press C-Play Again or Q-Quit", True, (255, 255, 255))
    screen.blit(msg, [game_width / 6, game_height / 3])
    pygame.display.update()

class Snake:

    section_width = 10
    section_height = 10
    x1_change = 0
    y1_change = 0
    snake_length = 1

    def __init__(self):
        self.x1 = randint(0, screen.get_width())
        self.y1 = randint(0, screen.get_height())

        self.rects = [pygame.Rect(self.x1, self.y1, self.section_width, self.section_height)]

    def draw(self):
        self.x1 += self.x1_change
        self.y1 += self.y1_change

        temp_rect = pygame.Rect(self.x1, self.y1, self.section_width, self.section_height)

        self.rects.append(temp_rect)

        if len(self.rects) > self.snake_length:
            del self.rects[0]

        for rect in self.rects:
            pygame.draw.rect(screen, (255, 255, 255), rect)

    def handle_key_pressed(self, event):
        if event.key == pygame.K_UP:
            self.x1_change = 0
            self.y1_change = -self.section_height
        if event.key == pygame.K_DOWN:
            self.x1_change = 0
            self.y1_change = self.section_height
        if event.key == pygame.K_LEFT:
            self.x1_change = -self.section_width
            self.y1_change = 0
        if event.key == pygame.K_RIGHT:
            self.x1_change = self.section_width
            self.y1_change = 0
        if event.key == pygame.K_SPACE:
            self.snake_length += 1

class Food:

    food_width = 10
    food_height = 10
    color = (0, 255, 0)

    def __init__(self):
        self.x = round(randrange(0, 600 - 10) / 10.0) * 10.0
        self.y = round(randrange(0, 600 - 10) / 10.0) * 10.0
        self.food_rect = pygame.Rect(self.x, self.y, self.food_width, self.food_height)

    def position(self):
        self.x = round(randrange(0, 600 - 10) / 10.0) * 10.0
        self.y = round(randrange(0, 600 - 10) / 10.0) * 10.0
        self.food_rect.x = self.x
        self.food_rect.y = self.y

    def draw(self):
        pygame.draw.rect(screen, self.color, self.food_rect)


def game_loop():
    game_over = False
    game_close = False

    snake = Snake()
    food = Food()

    while not game_over:
        while game_close == True:
            game_over_screen()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_c:
                        game_loop()
                    if event.key == pygame.K_q:
                        sys.exit()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                snake.handle_key_pressed(event)

        screen.fill((0, 0, 0))
        food.draw()
        snake.draw()
        pygame.display.update()

        if snake.rects[-1].colliderect(food.food_rect):
            snake.snake_length += 1
            food.position()

        if not screen_rect.contains(snake.rects[-1]):
            game_close = True

        if len(snake.rects) > 1:
            if snake.rects[-1] in snake.rects[:-1]:
                game_close = True

        clock.tick(25)


game_loop()
