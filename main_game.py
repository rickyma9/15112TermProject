from editor import *
from play_game import *
from objects import *
import pygame
import pygamegame
import random

# WIP: main game where you can choose to play or edit

class main_game(pygamegame.PygameGame):
    def init(self, screen):

        self.screen = screen

        self.mode = "start"

        self.audio = None
        # pick a random song to play
        songs = os.listdir("music")
        numSongs = len(songs)
        pick = random.randint(0, numSongs-1)
        print(songs, numSongs, pick)
        self.audio = pygame.mixer.Sound("music" + "\\" + songs[pick])


        self.font = pygame.font.SysFont("Berlin Sans FB", 50)

        self.changeW = 3*self.height//4
        self.changeH = 3*self.height//4


        self.background = pygame.image.load("images\\background.jpg").convert_alpha()
        self.background = pygame.transform.smoothscale(self.background, (self.width, self.height))

        self.time = 0
        self.otherTime = 0

        self.changeR = 2*self.height//5


    def mousePressed(self, x, y):

        pygame.mixer.Sound.fadeout(self.audio, 1000)

        if 0 <= x < self.width/2:
            self.mode = "play"
            game = play()
            game.run()
            print(self.mode)

        else:
            self.mode = "edit"
            game = Editor()
            game.run()
            print(self.mode)

    def timerFired(self, dt):

        if self.otherTime == 50:
            pygame.mixer.Sound.set_volume(self.audio, 0.1)
            pygame.mixer.Sound.play(self.audio, 0)

        self.otherTime += 1
        self.time += dt/1000

        if self.time >= 0.5:
            self.changeR = 2*self.height//5

            self.time = 0
        else:
            self.changeR += 1



    def redrawAll(self, screen):

        screen.blit(self.background, (0, 0))

        pygame.draw.circle(self.screen, (200, 220, 255), (self.width//2, self.height//2), self.changeR)
        pygame.draw.circle(self.screen, (225, 240, 255), (self.width//2, self.height//2), 2*self.changeR//3)
        pygame.draw.circle(self.screen, (255, 255, 255), (self.width//2, self.height//2), self.changeR//3)

        pygame.draw.circle(self.screen, (200, 200, 200), (self.width//2, self.height//2), self.changeR, 10)
        pygame.draw.circle(self.screen, (200, 200, 200), (self.width//2, self.height//2), self.changeR//3, 10)
        pygame.draw.circle(self.screen, (200, 200, 200), (self.width//2, self.height//2), 2*self.changeR//3, 10)

        pygame.draw.line(self.screen, (140, 140, 140), (self.width//2, 0), (self.width//2, self.height), 2)


        play = "Play!"
        edit = "Edit!"

        playRender = self.font.render(play, True, (50, 50, 50))
        editRender = self.font.render(edit, True, (50, 50, 50))

        screen.blit(playRender, (self.width/2-200, self.height/2-25))
        screen.blit(editRender, (self.width/2+100, self.height/2-25))

game = main_game()

game.run()
    