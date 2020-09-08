import pygame
import math

# all the objects that are used in making the game and playing it

# add time parameter, so the thing knows what time to come in
class Circle(pygame.sprite.Sprite):
    def __init__(self, x, y, r, screen):
        self.x = x
        self.y = y
        self.r = r
        self.screen = screen
        self.approachR = r * 3

        self.isClicked = False

        self.hitCircle = pygame.image.load("images\\hitcircle.png").convert_alpha()
        self.hitCircleOverlay = pygame.image.load("images\\hitcircleoverlay.png").convert_alpha()
        self.hitCircle = pygame.transform.smoothscale(self.hitCircle, (self.r*2, self.r*2))
        self.hitCircleOverlay = pygame.transform.smoothscale(self.hitCircle, (self.r*2, self.r*2))

        self.purple = (150, 100, 230)
        self.lightpurple = (200, 140, 230)

        self.fade1 = 200
        self.fade2 = 200
        self.fade3 = 200

    def __repr__(self):
        return "circle"

    #change approach circle and sliderball movement with smallTime, figure out how to represent the number of objects I need to show at one time on the screen (mostly use smalltime i g)
    def approachCircle(self, rate):
        self.approachR -= rate
        if self.approachR - self.r <= 1:
            self.approachR = self.r + 1

    def draw(self):

        self.screen.blit(self.hitCircle, (self.x-self.r, self.y-self.r))
        pygame.draw.circle(self.screen, (255, 255, 255), [self.x, self.y], self.r, 4)
        pygame.draw.circle(self.screen, (0, 0, 0), [self.x, self.y], self.r, 1)
  
        pygame.draw.circle(self.screen, (200, 200, 200), [self.x, self.y], self.approachR, 4)

        if self.isClicked == True:
            color = (self.fade1, self.fade2, self.fade3)
            pygame.draw.circle(self.screen, color, (self.x, self.y), self.r-5)
            if self.fade1 < 255:
                self.fade1 += 1
                self.fade2 += 1
                self.fade3 += 1


class ghostCircle(Circle):

    def __repr__(self):
        return "ghost circle"

    def draw(self):
        self.screen.blit(self.hitCircle, (self.x-self.r, self.y-self.r))

        pygame.draw.circle(self.screen, (0, 0, 0), [self.x, self.y], self.r, 1)


class bigCircle(Circle):

    def draw(self):
        pygame.draw.circle(self.screen, (0, 0, 0), [self.x, self.y], self.r, 3)




class Slider(pygame.sprite.Sprite):
    def __init__(self, startCircle, endCircle, screen):
        self.startCircle = startCircle
        self.endCircle = ghostCircle(endCircle.x, endCircle.y, endCircle.r, screen)

        self.startx = startCircle.x
        self.starty = startCircle.y
        self.endx = endCircle.x
        self.endy = endCircle.y
        self.r = startCircle.r

        self.screen = screen

        # contains the circles that make up the slider
        self.sliderBall = ghostCircle(self.startx, self.starty, self.r*2, screen)

        # approach rate
        self.approachR = self.r * 3
        self.move = False

        # determines if you will break combo at the point of release
        self.comboBreak = True

        # determines if the cursor is in the sliderball range
        self.inside = False


    def __repr__(self):
        return "slider"

    def draw(self):

        self.startCircle.draw()
        self.endCircle.draw()


        # approach circle
        if self.move == False:
            pygame.draw.circle(self.screen, (200, 200, 200), [self.startx, self.starty],
                self.approachR, 1)

        # slider ball
        if self.move == True:
            if self.inside == True:
                pygame.draw.circle(self.screen, (200, 200, 200), [self.sliderBall.x, self.sliderBall.y],
                    self.sliderBall.r, 1)
            pygame.draw.circle(self.screen, (200, 200, 200), [self.sliderBall.x, self.sliderBall.y],
                self.r, 5)


        r = self.connectCircles(self.startx, self.starty, self.endx, self.endy)

        pygame.draw.line(self.screen, (0, 0, 0), [self.startx+r[0], self.starty+r[1]],
            [self.endx+r[0], self.endy+r[1]], 2)
        pygame.draw.line(self.screen, (0, 0, 0), [self.startx-r[0], self.starty-r[1]],
            [self.endx-r[0], self.endy-r[1]], 2)

    # make speed * time to determine where the slider should be at the time
    def inSlider(self, x, y):
        pass

    def isClicked(self):
        self.move = True

    def approachCircle(self, rate):
        self.approachR -= rate

        if self.approachR - self.r <= 1:
            self.approachR = self.r + 1

        if self.approachR == self.r + 1:
            self.move = True

        self.startCircle.approachR = self.approachR




    # inslider can just see if the cursor is in the slider ball
    def updateSliderBall(self, speed):
        if self.move == True:
            connectingSlope = (self.endy - self.starty)/(self.endx - self.startx)
            angle = math.atan(connectingSlope)

            speedX = (self.endx - self.startx)/speed
            speedY = (self.endy - self.starty)/speed

            self.sliderBall.x += int(speedX)
            self.sliderBall.y += int(speedY)

            # determine if you will combo break
            if self.sliderBall.x - self.endx <= 20 and self.sliderBall.y - self.endy <= 20:
                self.comboBreak = False

    # finding the angle of the lines connecting the sliders
    def connectCircles(self, startx, starty, endx, endy):
        connectingSlope = (endy - starty)/(endx - startx)
        perpendicular = -1 / connectingSlope
        angle = math.atan(perpendicular)
        return (self.r * math.cos(angle), self.r * math.sin(angle))


