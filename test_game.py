import pygame
import pygamegame #the framework
import random
#from beatmap import *
from objects import *
import math


# TODO: make Sound s for hitsounds and beatmaps, make a beatmap object?,
# maybe import images for the circles and approach circles
# add scoring for sliders, combo for each second you're in the sldier?
# 

# plan:
# have different classes for different states: beatmap, start screen,
# song selection screen, fail screen, editor. they all have different controller functions.

class test(pygamegame.PygameGame):

    # inherits self.width and self.height
    def init(self, screen):
        #self.width = width
        #self.height = height
        #self.screen = pygame.display.set_mode((self.width, self.height))
        self.screen = screen

        self.clock = pygame.time.Clock()
        self.smallTime = 0
        self.time = 0

        self.audio = pygame.mixer.Sound("billy.wav")
        self.l = int(pygame.mixer.Sound.get_length(self.audio))
        self.hitsound = pygame.mixer.Sound("drum-hitclap.wav")
        #self.combobreak = pygame.mixer.Sound("combobreak.wav")
        self.image = pygame.image.load("billy_image.jpg")

        self.circles = []
        self.sliders = []

        self.font = pygame.font.SysFont(None, 25)
        self.combo = 0
        self.score = 0

        self.pause = False
        self.drag = False

        self.inSlider = False
        self.curSlider = None

        #self.test = Circle(self.width//2, self.height//2, 20, self.screen)

        # score = 300/100/50/0 * combo, determine 300/100 by how far the radius is from the actual radius


    #def mousePressed(self, x, y):

    #    circle = Circle(x, y, 20, self.screen)
     #   self.circles.append(circle)

    def mousePressed(self, x, y):

        self.drag = True

        toRemove = []
        print("click")
        for circle in self.circles:
            print(circle.x)

            if circle.x - circle.r <= x <= circle.x + circle.r and \
               circle.y - circle.r <= y <= circle.y + circle.r:
                toRemove.append(circle)
                self.combo += 1
                if 1 <= circle.approachR - circle.r <= 10:
                    self.score += 300*self.combo
                    pygame.mixer.Sound.play(self.hitsound)
                elif 11 <= circle.approachR - circle.r <= 25:
                    self.score +=100*self.combo
                    pygame.mixer.Sound.play(self.hitsound)
                elif 26 <= circle.approachR - circle.r <= 30:
                    self.score +=50*self.combo
                    pygame.mixer.Sound.play(self.hitsound)
                else:
                    #pygame.mixer.Sound.play(self.combobreak)
                    self.combo = 0



        #for circle in range(len(toRemove)-1, -1, -1):
        for circle in toRemove:
            self.circles.remove(circle)
            break

        for slider in self.sliders:
            if slider.startx - slider.r <= x <= slider.startx + slider.r and\
               slider.starty - slider.r <= y <= slider.starty + slider.r:
                self.curSlider = slider
                self.inSlider = True
                self.curSlider.inside = True
                slider.isClicked()

                # make the big circle appear again?
                #r = self.curSlider.sliderBall.r
                #sX = self.curSlider.sliderBall.x
                #sY = self.curSlider.sliderBall.y
                #if x in range(sX-r, sX+r) and y in range (sY-r, sY+r):
                #    self.inSlider = True # -> call the original if statement again, which determines if you go back out, breaking combo again
                #    self.curSlider.inside = True
                


    def mouseReleased(self, x, y):
        if self.inSlider == True:
            self.combo = 0
            self.curSlider.inside = False
            self.inSlider = False

        self.drag = False

    def mouseDrag(self, x, y):
        #self.test = Circle(x, y, 20, self.screen)

        if self.inSlider == True:
            r = self.curSlider.sliderBall.r
            sX = self.curSlider.sliderBall.x
            sY = self.curSlider.sliderBall.y
            # if you go out of sliderball, break combo
            if x not in range(sX-r, sX+r) or y not in range (sY-r, sY+r) and \
               self.curSlider.comboBreak == True:
                self.combo = 0
                #self.sliders.remove(self.curSlider)
                self.inSlider = False
                self.curSlider.inside = False

        # if you are still dragging and go back in sliderball range, draw the big sliderball again (possibly start adding combo again!!)
        if self.drag == True:
            r = self.curSlider.sliderBall.r
            sX = self.curSlider.sliderBall.x
            sY = self.curSlider.sliderBall.y
            
            if x in range(sX-r, sX+r) and y in range (sY-r, sY+r):
                self.inSlider = True # -> call the original if statement again, which determines if you go back out, breaking combo again
                self.curSlider.inside = True

    #def mouseMotion(self, x, y):




    def keyPressed(self, keyCode, modifier):
        if keyCode == pygame.K_p:
            self.pause = not self.pause
        
        if keyCode ==  pygame.K_u:
            self.audio.close()

    def timerFired(self, dt):

        if self.smallTime == 0:
            pygame.mixer.Sound.set_volume(self.audio, 0.1)
            pygame.mixer.Sound.play(self.audio)

        if self.l - self.smallTime < 3:
            pygame.mixer.Sound.fadeout(3000)
        # fadeout
        #if self.time == 100:
        #    pygame.mixer.Sound.fadeout(self.audio, 10000)

        # create circles
        if self.time % 100 == 0:
            x = random.randint(50, self.width-50)
            y = random.randint(50, self.height-50)
            x1 = random.randint(50, self.width-50)
            y1 = random.randint(50, self.width-50)
            circle = Circle(x, y, 50, self.screen)
            circle2 = Circle(x1, y1, 50, self.screen)
            slider = Slider(circle, circle2, self.screen)
            self.circles.append(circle)
            self.sliders.append(slider)

        # the rate at which the sliderball updates
        if self.time % 20 == 0:

            # slider combos
            if self.inSlider == True:
                self.combo += 1
            
            # remove sliders
            toRemove = []
            for slider in self.sliders:
                # maybe change the loction of this according to the speed at which the slider is supposed to move
                slider.updateSliderBall(10)
                if ((abs(slider.sliderBall.x - slider.endx) <= 10) and 
                    (abs(slider.sliderBall.y - slider.endy) <= 10)):
                    print(slider.sliderBall.x, slider.endx, slider.sliderBall.y, slider.endy)
                    print("a")
                    toRemove.append(slider)

            # remove sliders
            for slider in toRemove:
                self.sliders.remove(slider)

            
        # everything relating to approach circles
        if self.time % 2 == 0:
            # approach circle - change the hardcoded value to vary based on approach rate
            toRemoveC = []
            for circle in self.circles:
                circle.approachCircle(2)
                if circle.approachR - circle.r <= 0:
                    toRemoveC.append(circle)
                    #pygame.mixer.Sound.play(self.combobreak)
                    self.combo = 0

            for circle in toRemoveC:
                self.circles.remove(circle)


            toRemoveS = []
            for slider in self.sliders:
                slider.approachCircle(2)
          

        self.smallTime += self.clock.tick(50) / 1000
        
        self.time = int(self.smallTime)


    def redrawAll(self, screen):
        comboText = self.font.render(str(self.combo), True, (0, 0, 0))
        scoreText = self.font.render(str(self.score), True, (0, 0, 0))
        screen.blit(comboText, (50, self.height-50))
        screen.blit(scoreText, (self.width-50, 50))
        #screen.blit(self.image, (0, 0))

        #self.test.draw()

        for circle in self.circles:
            circle.draw()

        for slider in self.sliders:
            slider.draw()


#creating and running the game
game = test()
game.run()

######################################
'''if slider.startx > slider.endx and slider.starty > slider.endy:

                print("a")
            if slider.startx < slider.endx and slider.starty > slider.endy:

                print("b")
            if slider.startx > slider.endx and slider.starty < slider.endy:

                print("c")

            if slider.startx < slider.endx and slider.starty < slider.endy:
  
                print("d")'''


'''
        toRemove = []
        for slider in self.sliders:
            print(slider.startx, slider.endx, slider.starty, slider.endy, x, y)
            if slider.startx > slider.endx and slider.starty > slider.endy:
                if x in range(slider.startx + slider.r, slider.endx - slider.r) and \
                   y in range(slider.starty + slider.r, slider.endy - slider.r):
                    print("a")
                    toRemove.append(slider)
            if slider.startx < slider.endx and slider.starty > slider.endy:
                if x in range(slider.endx + slider.r, slider.startx - slider.r) and \
                   y in range(slider.starty + slider.r, slider.endy - slider.r):
                    print("a")
                    toRemove.append(slider)
            if slider.startx > slider.endx and slider.starty < slider.endy:
                if x in range(slider.startx + slider.r, slider.endx - slider.r) and \
                   y in range(slider.endy + slider.r, slider.starty - slider.r):
                    print("a")
                    toRemove.append(slider)
            if slider.startx < slider.endx and slider.starty < slider.endy:
                if x in range(slider.endx + slider.r, slider.startx - slider.r) and \
                   y in range(slider.endy + slider.r, slider.starty - slider.r):
                    print("a")
                    toRemove.append(slider)

            r = slider.connectCircles(slider.startx, slider.starty, slider.endx, slider.endy)

            if slider.startx > slider.endx and slider.starty > slider.endy:
                if x in range(slider.endx, slider.startx) and \
                   y in range(slider.endy, slider.starty):
                    print("a")
                    toRemove.append(slider)
            if slider.startx < slider.endx and slider.starty > slider.endy:
                if x in range(slider.startx, slider.endx) and \
                   y in range(slider.endy, slider.starty):
                    print("a")
                    toRemove.append(slider)
            if slider.startx > slider.endx and slider.starty < slider.endy:
                if x in range(slider.endx, slider.startx) and \
                   y in range(slider.starty, slider.endy):
                    print("a")
                    toRemove.append(slider)
            if slider.startx < slider.endx and slider.starty < slider.endy:
                if x in range(slider.startx, slider.endx) and \
                   y in range(slider.starty, slider.endy):
                    print("a")
                    toRemove.append(slider)




        for slider in range(len(toRemove)-1, -1, -1):
            self.sliders.remove(toRemove[slider])
            break
'''

