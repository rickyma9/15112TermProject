import pygame
from objects import *
#from test_game import *
import pygamegame

# possibly add os functions to find the beatmap files
class Beatmap(pygamegame.PygameGame):
    def __init__(self): #add audio parameter
        self.circles = []
        self.sliders = []
        self.audio = pygame.mixer.Sound("LilyScarlet_Rose.wav")
        self.time = 0
        self.circleSize = 4
        self.approachRate = 9
        self.hpDrain = 7

    def mousePressed(self, x, y):

        toRemove = []
        for circle in self.circles:
            if circle.x - circle.r <= x <= circle.x + circle.r and \
               circle.y - circle.r <= y <= circle.y + circle.r:
                toRemove.append(circle)

        for circle in range(len(toRemove)-1, -1, -1):
            self.circles.remove(toRemove[circle])
            break

    def redrawAll(self, screen):
        for circle in self.circles:
            circle.draw()

    def timerFired(self, dt):
        if self.time == 0:
            pygame.mixer.Sound.play(self.audio)

        # fadeout
        if self.time == 100:
            pygame.mixer.Sound.fadeout(self.audio, 10000)

game = Beatmap()
game.run()







