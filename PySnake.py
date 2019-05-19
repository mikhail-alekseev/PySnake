import sys
import random
import pygame
from pygame.locals import *

WIDTH = 20
HEIGHT = 15

BACKGROUND_COLOR = (0, 0, 0)  # Black
TEXT_COLOR = (255, 255, 255)  # White
SNAKE_COLOR = (255, 69, 0)  # Orange
APPLE_COLOR = (0, 255, 0)  # Green

TILE = 40  # Size of a tile in px
WIN_WIDTH = TILE * WIDTH  # 800px
WIN_HEIGHT = TILE * HEIGHT  # 600px

FPS = 10

# Directions
LEFT = (-1, 0)
UP = (0, -1)
RIGHT = (1, 0)
DOWN = (0, 1)


class SnakeGame:

    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Snake')
        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT), 0, 32)
        self.font = pygame.font.SysFont('Arial', 70)
        self.timer = pygame.time.Clock()
        self.new_game()
        self.gameloop()

    def new_game(self):
        self.snake = [(11, 7), (10, 7), (9, 7)]
        self.direction = RIGHT
        self.apple = self.get_new_apple()

    def gameloop(self):
        while True:
            self.handle_events()
            self.update()
            self.render()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_LEFT and self.direction != RIGHT:
                    self.direction = LEFT
                elif event.key == K_RIGHT and self.direction != LEFT:
                    self.direction = RIGHT
                elif event.key == K_UP and self.direction != DOWN:
                    self.direction = UP
                elif event.key == K_DOWN and self.direction != UP:
                    self.direction = DOWN

    def update(self):
        head = self.snake[0]
        new_x, new_y = head[0] + self.direction[0], head[1] + self.direction[1]

        # Wrap around the screen
        if new_x < 0:
            new_x = WIDTH - 1
        elif new_x >= WIDTH:
            new_x = 0
        if new_y < 0:
            new_y = HEIGHT - 1
        elif new_y >= HEIGHT:
            new_y = 0

        self.snake.insert(0, (new_x, new_y))

        if self.apple == self.snake[0]:
            # We have just "eaten" the apple so we need a new one
            self.apple = self.get_new_apple()
        else:
            self.snake.pop()

        if self.snake[0] in self.snake[1:]:
            self.gameover()

        self.render()
        pygame.display.update()
        self.timer.tick(FPS)

    def render(self):
        self.screen.fill(BACKGROUND_COLOR)
        for segment in self.snake:
            pygame.draw.rect(self.screen, SNAKE_COLOR,
                             pygame.Rect(segment[0] * TILE,
                                         segment[1] * TILE,
                                         TILE, TILE))

        pygame.draw.rect(self.screen, APPLE_COLOR,
                         pygame.Rect(self.apple[0] * TILE,
                                     self.apple[1] * TILE,
                                     TILE, TILE))

    def gameover(self):
        self.draw_text('GAME OVER', TEXT_COLOR, 250, 250)
        pygame.display.update()
        pygame.time.delay(2000)
        self.new_game()

    def draw_text(self, text, color, x, y):
        textimg = self.font.render(text, 1, color)
        self.screen.blit(textimg, (x, y))

    def get_new_apple(self):
        while True:
            apple = (random.randint(0, WIDTH-1), random.randint(0, HEIGHT-1))
            if apple not in self.snake:
                return apple


if __name__ == '__main__':
    SnakeGame()
