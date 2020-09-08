import pygame
#from objects import *
#from test_game import *
import pygamegame
import os

# possibly add os functions to find the beatmap files
#class Beatmap(test):
#    def init(self, songName, width=1000, height=600, fps=50, title="112 Pygame Game"):
#        self.audio = songName
'''    def init(self, songName): #add audio parameter
        self.circles = []
        self.sliders = []

        self.width = 1000
        self.height = 700
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.audio = pygame.mixer.Sound(songName)
        self.time = 0

        self.circleSize = 4
        self.approachRate = 9
        self.hpDrain = 7

        self.currentObject = None

    # if you clickin the box of circles, you can make circles lol
    def mousePressed(self, x, y):
        pass

    def redrawAll(self, screen):
        for circle in self.circles:
            circle.draw()

    def timerFired(self, dt):
        if self.time == 0:
            pygame.mixer.Sound.play(self.audio)

        # fadeout
        if self.time == 100:
            pygame.mixer.Sound.fadeout(self.audio, 10000)'''



#game = Beatmap("billy.wav")
#game.run()

for song in os.listdir("music"):
    print(song)






