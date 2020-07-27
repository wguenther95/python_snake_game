import sys
import pygame
from random import randint

pygame.init()

clock = pygame.time.Clock()


class Application:
    background_color = (0, 0, 0)
    rect_color = (255, 255, 255)
    screen_width = 600
    screen_height = 600
    offset = 20
    rect_width = screen_width - offset
    rect_height = screen_height - offset
    game_over_bool = False
    game_over_font = pygame.font.SysFont(None, 48)
    restart_font = pygame.font.SysFont(None, 24)
    game_over_img = game_over_font.render("Game Over", True, (0, 0, 255))
    restart_img = restart_font.render("Press spacebar to restart", True, (0, 0, 255))

    bound_collide = pygame.USEREVENT + 1

    def __init__(self):
        self.screen = pygame.display.set_mode(size=(self.screen_width, self.screen_height))
        self.screen.fill(self.background_color)
        self.game_area = pygame.Rect(0 + self.offset / 2, 0 + self.offset / 2, self.rect_width, self.rect_height)
        self.snake = Snake(self)
        self.draw()

    def draw(self):
        pygame.draw.rect(self.screen, self.rect_color, self.game_area)
        self.snake.update_pos()
        pygame.draw.rect(self.screen, self.snake.color, self.snake.head)
        self.handle_collision()

    def game_over(self):
        self.game_over_bool = True

        while self.game_over_bool == True:
            self.screen.fill(self.background_color)
            pygame.draw.rect(self.screen, self.rect_color, self.game_area)
            self.screen.blit(self.game_over_img, (self.game_area.centerx - self.game_over_img.get_width() / 2,
                                                  self.game_area.centery - self.game_over_img.get_height() / 2))
            self.screen.blit(self.restart_img, (self.game_area.centerx - self.restart_img.get_width() / 2,
                                                self.game_area.centery + self.game_over_img.get_height() / 2))
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.snake.restart()
                        self.game_over_bool = False

    def handle_collision(self):
        if not self.game_area.contains(self.snake.head):
            bound_collide_event = pygame.event.Event(self.bound_collide, message='Collision with game boundary!')
            pygame.event.post(bound_collide_event)


class Snake:
    width = 10
    height = 10
    x1_change = 0
    y1_change = 0
    color = (0, 255, 0)

    bound_collide = pygame.USEREVENT + 1

    def __init__(self, app):
        self.screen = app.screen
        self.game_area = app.game_area
        self.x1 = randint(self.game_area.x, self.game_area.x + self.game_area.width)
        self.y1 = randint(self.game_area.y, self.game_area.y + self.game_area.height)
        self.head = pygame.Rect(self.x1, self.y1, self.width, self.height)

    def add_section(self):
        pass

    def update_pos(self):
        self.x1 += self.x1_change
        self.y1 += self.y1_change

        self.head.x = self.x1
        self.head.y = self.y1

    def restart(self):
        self.x1 = randint(self.game_area.x, self.game_area.x + self.game_area.width)
        self.y1 = randint(self.game_area.y, self.game_area.y + self.game_area.height)
        self.head = pygame.Rect(self.x1, self.y1, self.width, self.height)
        self.x1_change = 0
        self.y1_change = 0
        pygame.draw.rect(self.screen, self.color, self.head)

    def handle_key_event(self, event):
        if event.key == pygame.K_DOWN:
            self.y1_change = 5
            self.x1_change = 0
        if event.key == pygame.K_UP:
            self.y1_change = -5
            self.x1_change = 0
        if event.key == pygame.K_RIGHT:
            self.y1_change = 0
            self.x1_change = 5
        if event.key == pygame.K_LEFT:
            self.y1_change = 0
            self.x1_change = -5

    # def handle_collision(self):
    #     if not self.game_area.contains(self.head):
    #         bound_collide_event = pygame.event.Event(self.bound_collide, message='Collision with game boundary!')
    #         pygame.event.post(bound_collide_event)


app = Application()

# snake = Snake(app)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            app.snake.handle_key_event(event)
        if event.type == app.bound_collide:
            app.game_over()

    app.draw()
    # snake.draw()
    pygame.display.flip()

    clock.tick(30)
