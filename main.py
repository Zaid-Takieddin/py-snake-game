import random
import time
import pygame
from pygame.locals import *

SIZE = 24
DISPLAY_X = 480
DISPLAY_Y = 360


class Game:

    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        pygame.display.set_caption("Snakey!")
        self.background = pygame.display.set_mode((DISPLAY_X, DISPLAY_Y))
        # self.background.fill((255, 255, 255))
        self.snake = Snake(self.background, 1)
        self.snake.draw()
        self.apple = Apple(self.background)
        self.apple.draw()

    def is_collision(self, x1, y1, x2, y2):
        if x2 <= x1 < x2 + SIZE:
            if y2 <= y1 < y2 + SIZE:
                return True
        return False

    def display_score(self):
        font = pygame.font.SysFont('Impact', 16)
        score = font.render(f'Score: {self.snake.length}', True, (0, 0, 0))
        self.background.blit(score, (DISPLAY_X - score.get_width() - 10, 0))

    def render_background(self):
        bg = pygame.image.load('resources/background.jpg')
        self.background.blit(bg, (0, 0))

    def show_game_over(self):
        font = pygame.font.SysFont("Impact", 20)
        message = font.render(f'Game is over! Your Score is {self.snake.length}.', True, (0, 0, 0))
        message2 = font.render('To play another game press Enter.', True, (0, 0, 0))
        message3 = font.render('To exit press ESC', True, (0, 0, 0))
        self.background.blit(message, (((DISPLAY_X / 2) - (message.get_width() / 2)), (DISPLAY_Y / 2) - (message.get_height() / 2)))
        self.background.blit(message2, (((DISPLAY_X / 2) - (message2.get_width() / 2)), (DISPLAY_Y / 2) + 30 - (message2.get_height() / 2)))
        self.background.blit(message3, (((DISPLAY_X / 2) - (message3.get_width() / 2)), (DISPLAY_Y / 2) + 60 - (message3.get_height() / 2)))
        pygame.display.flip()

    def play(self):
        self.render_background()
        self.snake.walk()
        self.apple.draw()
        self.display_score()
        pygame.display.flip()
        if self.is_collision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
            self.snake.increase_length()
            self.apple.re_render()
            pygame.mixer.Sound("resources/powerup.mp3").play()
        for i in range(2, self.snake.length):
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                raise "Collision Occurred"

    def reset(self):
        self.snake = Snake(self.background, 1)
        self.apple = Apple(self.background)

    def run(self):
        self.render_background()
        pygame.mixer.music.load("resources/background.mp3")
        pygame.mixer.music.play()
        running = True
        pause = False
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                    if event.key == K_RETURN:
                        pause = False
                        pygame.mixer.music.play()
                    if event.key == K_UP:
                        self.snake.move_up()
                    if event.key == K_DOWN:
                        self.snake.move_down()
                    if event.key == K_RIGHT:
                        self.snake.move_right()
                    if event.key == K_LEFT:
                        self.snake.move_left()
            try:
                if not pause:
                    self.play()
            except Exception as e:
                pygame.mixer.Sound("resources/game_over.wav").play()
                pygame.mixer.music.stop()
                pause = True
                self.show_game_over()
                self.reset()
            time.sleep(0.25)


class Snake:

    def __init__(self, parent_class, length):
        self.length = length
        self.parent_class = parent_class
        self.block = pygame.image.load("resources/snake.png")
        self.x = [random.randint(0, ((DISPLAY_X / SIZE) - 1)) * SIZE] * length
        self.y = [random.randint(0, ((DISPLAY_Y / SIZE) - 1)) * SIZE] * length
        self.directions = ['up', 'down', 'left', 'right']
        self.direction = self.directions[random.randint(0, 3)]

    def draw(self):
        for i in range(self.length):
            self.parent_class.blit(self.block, (self.x[i], self.y[i]))
        pygame.display.flip()

    def increase_length(self):
        self.length += 1
        self.x.append(0)
        self.y.append(0)

    def move_up(self):
        self.direction = 'up'

    def move_down(self):
        self.direction = 'down'

    def move_right(self):
        self.direction = 'right'

    def move_left(self):
        self.direction = 'left'

    def walk(self):

        for i in range(self.length - 1, 0, -1):
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]
        match self.direction:
            case 'up':
                self.y[0] -= SIZE
            case 'down':
                self.y[0] += SIZE
            case 'left':
                self.x[0] -= SIZE
            case 'right':
                self.x[0] += SIZE
        self.draw()


class Apple:

    def __init__(self, parent_class):
        self.parent_class = parent_class
        self.block = pygame.image.load('resources/apple-24.png')
        self.x = random.randint(0, ((DISPLAY_X / SIZE) - 1)) * SIZE
        self.y = random.randint(0, ((DISPLAY_Y / SIZE) - 1)) * SIZE

    def draw(self):
        self.parent_class.blit(self.block, (self.x, self.y))
        pygame.display.flip()

    def re_render(self):
        self.x = random.randint(0, ((DISPLAY_X / SIZE) - 1)) * SIZE
        self.y = random.randint(0, ((DISPLAY_Y / SIZE) - 1)) * SIZE


if __name__ == "__main__":
    game = Game()
    game.run()


