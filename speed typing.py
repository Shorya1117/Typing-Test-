import pygame
from pygame.locals import *
import sys
import time
import random

class Game:
    def __init__(self):
        self.w = 1280
        self.h = 720
        self.reset = True
        self.active = False
        self.input_text = ''
        self.word = ''
        self.time_start = 0
        self.total_time = 0
        self.accuracy = '0%'
        self.results = 'Time:0 Accuracy:0 % Wpm:0 '
        self.wpm = 0
        self.end = False
        self.HEAD_C = (255, 213, 102)
        self.TEXT_C = (240, 240, 240)
        self.RESULT_C = (255, 70, 70)
        
        pygame.init()
        self.font = pygame.font.Font(None, 32)
        self.open_img = pygame.image.load('type-speed-open.png')
        self.open_img = pygame.transform.scale(self.open_img, (self.w, self.h))

        self.bg = pygame.image.load('background.jpg')
        self.bg = pygame.transform.scale(self.bg, (self.w, self.h))

        self.screen = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Type Speed Test')

        # Input box dimensions
        self.base_rect_width = 650  # Initial width
        self.rect_height = 50
        self.rect_width = self.base_rect_width

        # Centered position calculations
        self.rect_x = (self.w - self.rect_width) // 2
        self.rect_y = (self.h - self.rect_height) // 2

    def draw_text(self, screen, msg, y, fsize, color):
        font = pygame.font.Font(None, fsize)
        text = font.render(msg, 1, color)
        text_rect = text.get_rect(center=(self.w / 2, y))
        screen.blit(text, text_rect)
        pygame.display.update()

    def get_sentence(self):
        with open('sentences.txt', 'r') as f:
            sentences = f.read().split('\n')
        return random.choice(sentences)

    def show_results(self, screen):
        if not self.end:
            self.total_time = time.time() - self.time_start
            count = sum(1 for i, c in enumerate(self.word) if i < len(self.input_text) and self.input_text[i] == c)
            self.accuracy = count / len(self.word) * 100
            self.wpm = len(self.input_text) * 60 / (5 * self.total_time)
            self.end = True

            self.results = f'Time: {round(self.total_time)} secs   Accuracy: {round(self.accuracy)}%   Wpm: {round(self.wpm)}'

            self.time_img = pygame.image.load('icon.png')
            self.time_img = pygame.transform.scale(self.time_img, (150, 150))
            screen.blit(self.time_img, (self.w / 2 - 75, self.h - 140))
            self.draw_text(screen, "Reset", self.h - 70, 26, (100, 100, 100))

            pygame.display.update()

    def adjust_input_box(self):
        """Adjust the size of the input box based on the length of the input text."""
        text_surface = self.font.render(self.input_text, True, (250, 250, 250))
        text_width = text_surface.get_width() + 20  # Adding padding

        # Expand the box if the text exceeds the initial width, but not beyond the screen width
        self.rect_width = max(self.base_rect_width, text_width)
        if self.rect_width > self.w - 100:  # Prevent overflow with 100px margin
            self.rect_width = self.w - 100

        # Recalculate X position to keep the box centered
        self.rect_x = (self.w - self.rect_width) // 2

    def run(self):
        self.reset_game()

        self.running = True
        while self.running:
            clock = pygame.time.Clock()
            self.screen.fill((0, 0, 0), (self.rect_x - 5, self.rect_y - 5, self.rect_width + 10, self.rect_height + 10))

            # Adjust input box size based on input
            self.adjust_input_box()

            # Draw the dynamically resized input box
            pygame.draw.rect(self.screen, self.HEAD_C, (self.rect_x, self.rect_y, self.rect_width, self.rect_height), 2)

            # Render and draw the text inside the box
            text_surface = self.font.render(self.input_text, True, (250, 250, 250))
            self.screen.blit(text_surface, (self.rect_x + 10, self.rect_y + 10))

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == QUIT:
                    self.running = False
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONUP:
                    x, y = pygame.mouse.get_pos()
                    if self.rect_x <= x <= self.rect_x + self.rect_width and self.rect_y <= y <= self.rect_y + self.rect_height:
                        self.active = True
                        self.input_text = ''
                        self.time_start = time.time()
                    if self.w / 2 - 100 <= x <= self.w / 2 + 100 and self.h - 140 <= y <= self.h - 90 and self.end:
                        self.reset_game()

                elif event.type == pygame.KEYDOWN:
                    if self.active and not self.end:
                        if event.key == pygame.K_RETURN:
                            self.show_results(self.screen)
                            self.draw_text(self.screen, self.results, self.rect_y + 100, 28, self.RESULT_C)
                        elif event.key == pygame.K_BACKSPACE:
                            self.input_text = self.input_text[:-1]
                        else:
                            self.input_text += event.unicode

            clock.tick(60)

    def reset_game(self):
        self.screen.blit(self.open_img, (0, 0))
        pygame.display.update()
        time.sleep(1)

        self.reset = False
        self.end = False
        self.input_text = ''
        self.word = self.get_sentence()
        self.time_start = 0
        self.total_time = 0
        self.wpm = 0

        self.screen.fill((0, 0, 0))
        self.screen.blit(self.bg, (0, 0))

        self.draw_text(self.screen, "Typing Speed Test", 80, 80, self.HEAD_C)
        pygame.draw.rect(self.screen, (255, 192, 25), (self.rect_x, self.rect_y, self.rect_width, self.rect_height), 2)
        self.draw_text(self.screen, self.word, self.rect_y - 50, 28, self.TEXT_C)

        pygame.display.update()


Game().run()
