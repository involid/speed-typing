from multiprocessing.connection import answer_challenge
import sys
import random
import time
import pygame
import colors

class game:
    def __init__(self):
        self.WIDTH = 700
        self.HEIGHT = 480
        self.FPS = 30

        self.programIcon = pygame.image.load('icon.png')
        pygame.display.set_icon(self.programIcon)

        pygame.init()
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Typing test")
        self.clock = pygame.time.Clock()

        self.background = pygame.image.load('background.jpg')
        self.background = pygame.transform.scale(self.background, (self.WIDTH, self.HEIGHT))
        self.playing_background = pygame.image.load('playing_background.jpg')
        self.playing_background = pygame.transform.scale(self.playing_background, (self.WIDTH, self.HEIGHT))

        self.textCoordinates = (50, 150)


    def text_to_screen(self, text, coordinates, size = 50,
                color = colors.white, font_type = None):
        font = pygame.font.Font(font_type, size)
        text = font.render(text, True, color)
        #text_rect = text.get_rect(center = coordinates)
        self.screen.blit(text, coordinates)
    
    
    def text_to_screen(self, text, coordinates, size = 50,
                color = colors.white, center = False, font_type = None):
        font = pygame.font.Font(font_type, size)
        text = font.render(text, True, color)
        if center:
            text_rect = text.get_rect(center = coordinates)
            self.screen.blit(text, text_rect)
            return
        self.screen.blit(text, coordinates)


    def get_text_metrics(self, text):
        font = pygame.freetype.Font(None, 50)
        font.origin = True
        return font.get_metrics(text)

    def GetText(self):
        with open('texts') as f:
            lines = [line for line in f.read().split('\n') if line.strip() != '']
        return random.choice(lines)

    def showText(self):
        self.text_to_screen(self.text, self.textCoordinates)
        self.text_to_screen(self.text[:self.right_input_lenght], self.textCoordinates, 50, colors.black)

    def showTypedText(self):
        self.text_to_screen(self.input_text, (50, 250), 50, colors.red)
        self.text_to_screen(self.input_text[:self.right_input_lenght], (50, 250))

    def showTimer(self):
        self.timer = int(int(time.time() - self.start_time))
        self.text_to_screen(str(self.timer), (50, 50))

    def showScore(self):
        self.text_to_screen(str(self.mistakes), (650, 50), 50, colors.red)
        self.text_to_screen(str(self.score), (650, 100), 50, colors.blue)

    def typing_process(self):
        self.start_time = time.time()
        self.input_text = ''
        self.right_input_lenght = 0
        self.mistakes = 0
        self.score = 0
        self.text = self.GetText()
        while time.time() - self.start_time <= 15:
            self.screen.blit(self.playing_background, (0, 0))
            self.showText()
            self.showTypedText()
            self.showTimer()
            self.showScore()
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        if self.right_input_lenght == len(self.input_text) and self.right_input_lenght > 0:
                            self.right_input_lenght -= 1
                            self.score -= 1
                        self.input_text = self.input_text[:-1]
                    else:
                        try:
                            self.input_text += event.unicode
                            if self.input_text[-1] == self.text[self.right_input_lenght]:
                                self.right_input_lenght += 1
                                self.score += 1
                            else:
                                self.mistakes += 1
                        except:
                            pass
                    if self.text == self.input_text:
                        self.text = self.GetText()
                        self.input_text = ''
                        self.right_input_lenght = 0


    def showResults(self):
        while True:
            self.screen.blit(self.background, (0, 0))
            self.text_to_screen("SCORE : " + str(self.score), (self.WIDTH / 2, self.HEIGHT / 3), 100, colors.blue, True)
            self.text_to_screen("MISTAKES : " + str(self.mistakes), (self.WIDTH / 2, self.HEIGHT / 1.5), 70, colors.red, True)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONUP:
                    return                


    def run(self):
        self.start_time = time.time()
        self.running = True
        while self.running:
            self.text = 'START'
            self.input_text = ''
            self.screen.blit(self.background, (0, 0))
            self.text_to_screen(self.text, (self.WIDTH / 2, self.HEIGHT / 2), 200, colors.orange, True)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONUP:
                    x,y = pygame.mouse.get_pos()
                    self.text = self.GetText()
                    self.typing_process()
                    self.showResults()

game().run()
