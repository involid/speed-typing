from multiprocessing.connection import answer_challenge
import sys
import random
import time
import pygame
from pygame.locals import *
import colors
from datetime import datetime


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
        self.playing_time = 5

        self.background = pygame.image.load('background.jpg')
        self.background = pygame.transform.scale(self.background, (self.WIDTH, self.HEIGHT))
        self.playing_background = pygame.image.load('playing_background.jpg')
        self.playing_background = pygame.transform.scale(self.playing_background, (self.WIDTH, self.HEIGHT))

        self.textCoordinates = (50, 150)

        self.makeLines()
        self.results = [line for line in open('results').read().split('\n') if line != '']
        with open('record') as f:
            self.record = int(f.read())

    def text_to_screen(self, text, coordinates, size = 50,
                color = colors.white, center = False, font_type = None):
        font = pygame.font.Font(font_type, size)
        text = font.render(text, True, color)
        if center:
            text_rect = text.get_rect(center = coordinates)
            self.screen.blit(text, text_rect)
            return
        self.screen.blit(text, coordinates)

    def makeLines(self):
        with open('texts') as f:
            self.lines = [line for line in f.read().split('\n') if line.strip() != '']
        random.shuffle(self.lines)
        self.line_number = -1

    def GetText(self):
        self.line_number += 1
        return self.lines[self.line_number]

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

    def rect_to_screen(self, color, left_border, up_border, width, height, border_width = 0):
        pygame.draw.rect(self.screen, color, (left_border, up_border, width, height), border_width)

    def show_start_buttom(self):
        self.rect_to_screen(colors.black, self.WIDTH * 11 / 40, self.HEIGHT / 4, self.WIDTH * 18 / 40, 120, 4)
        self.text_to_screen('START', (self.WIDTH / 2, self.HEIGHT / 4 + 60), 120, colors.green, True)

    def show_scores_buttom(self):
        self.rect_to_screen(colors.black, self.WIDTH / 3, self.HEIGHT * 23 / 40, self.WIDTH / 3, 70, 4)
        self.text_to_screen('SCORES', (self.WIDTH / 2, self.HEIGHT * 13 / 20), 70, colors.gray, True)

    def showFirstScreen(self):
        self.text = 'START'
        self.screen.blit(self.background, (0, 0))
        self.show_start_buttom()
        self.show_scores_buttom()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONUP:
                x, y = pygame.mouse.get_pos()
                if x >= self.WIDTH * 11 / 40 and x <= self.WIDTH * 29 / 40 and y >= self.HEIGHT / 4 and y <= self.HEIGHT / 4 + 120:
                    self.game_status = 'playing'
                elif x >= self.WIDTH / 3 and x <= self.WIDTH * 2 / 3 and y >= self.HEIGHT * 23 / 40 and y <= self.HEIGHT * 23 / 40 + 70:
                    self.game_status = 'showing_scores'

    def reset_results(self):
        open('results', 'w').close()
        with open('record', 'w') as f:
            f.write('0')
        self.record = 0
        self.results = []

    def save_result(self):
        self.current_time = datetime.now().strftime('%d/%m/%Y    %H:%M')
        self.points = max(0, self.score * 3 - self.mistakes * 7)
        self.results.append(f'{self.current_time}    {self.points}')
        with open('results', 'a') as f:
            f.write(f'{self.results[-1]}\n')

    def typingProcess(self):
        self.start_time = time.time()
        self.input_text = ''
        self.right_input_lenght = 0
        self.mistakes = 0
        self.score = 0
        self.text = self.GetText()
        while time.time() - self.start_time <= self.playing_time:
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
                    if event.key == pygame.K_ESCAPE:
                        self.game_status = 'begining'
                        return
                    elif event.key == pygame.K_BACKSPACE:
                        if self.right_input_lenght == len(self.input_text) and self.right_input_lenght > 0:
                            self.right_input_lenght -= 1
                            self.score -= 1
                        self.input_text = self.input_text[:-1]
                    else:
                        try:
                            self.input_text += event.unicode
                            if self.input_text[-1] == self.text[self.right_input_lenght] and self.right_input_lenght + 1 == len(self.input_text):
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
        self.save_result()
        self.setted_record = False
        self.game_status = 'showing_results'

    def show_reset_buttom(self):
        self.rect_to_screen(colors.black, self.WIDTH / 14, self.HEIGHT / 14, self.WIDTH / 3, 40, 4)
        self.text_to_screen('RESET SCORES', (self.WIDTH * 29 / 120, self.HEIGHT / 14 + 20), 40, colors.red, True)

    def showScores(self):
        self.screen.blit(self.background, (0, 0))
        self.result_height = self.HEIGHT / 5
        self.text_to_screen("PRESS ESC TO RETURN", (self.WIDTH * 3 / 4, self.HEIGHT / 10), 30, colors.red, True)
        self.show_reset_buttom()
        self.text_to_screen("DATE             TIME    POINTS", (self.WIDTH / 10, self.result_height))
        for result in self.results[::-1]:
            self.result_height += 50
            self.text_to_screen(result, (self.WIDTH / 10, self.result_height), 50, colors.gray)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game_status = 'begining'
                    return
            elif event.type == pygame.MOUSEBUTTONUP:
                x, y = pygame.mouse.get_pos()
                if x >= self.WIDTH / 14 and x <= self.WIDTH * (1 / 14 + 1 / 3) and y >= self.HEIGHT / 14 and y <= self.HEIGHT / 14 + 40:
                    self.reset_results()

    def showResults(self):
        self.screen.blit(self.background, (0, 0))
        if self.points > self.record:
            self.setted_record = True
        if self.setted_record:
            self.record = self.points
            with open('record', 'w') as f:
                f.write(str(self.points))
            self.score_height = self.HEIGHT * 13 / 20
            self.mistakes_height = self.HEIGHT * 16 / 20
            self.points_height = self.HEIGHT * 10 / 20
            self.points_size = 70
            self.text_to_screen("NEW RECORD!", (self.WIDTH / 2, self.HEIGHT / 3), 100, colors.yellow, True)
        else:
            self.score_height = self.HEIGHT * 3 / 5
            self.mistakes_height = self.HEIGHT * 4 / 5
            self.points_height = self.HEIGHT / 3
            self.points_size = 100
        self.text_to_screen(f"POINTS : {str(self.points)}", (self.WIDTH / 2, self.points_height), self.points_size, colors.blue, True)
        self.text_to_screen(f"SCORE : {str(self.score)}", (self.WIDTH / 2, self.score_height), 70, colors.blue, True)
        self.text_to_screen(f"MISTAKES : {str(self.mistakes)}", (self.WIDTH / 2, self.mistakes_height), 70, colors.red, True)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONUP:
                self.game_status = 'begining'        

    def run(self):
        self.running = True
        self.game_status = 'begining'
        while self.running:
            if self.game_status == 'begining':
                self.showFirstScreen()
            elif self.game_status == 'quit':
                self.running = False
            elif self.game_status == 'playing':
                self.typingProcess()
            elif self.game_status == 'showing_scores':
                self.showScores()
            elif self.game_status == 'showing_results':
                self.showResults()
            pygame.display.update()


game().run()
