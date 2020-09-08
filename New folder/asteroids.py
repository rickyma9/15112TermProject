'''
GameObject.py

implements the base GameObject class, which defines the wraparound motion
Lukas Peraza, 2015 for 15-112 Pygame Lecture
'''
import pygame

class GameObject(pygame.sprite.Sprite):
    def __init__(self, x, y, image, radius):
        super(GameObject, self).__init__()
        # x, y define the center of the object
        self.x, self.y, self.image, self.radius = x, y, image, radius
        self.baseImage = image.copy()  # non-rotated version of image
        w, h = image.get_size()
        self.updateRect()
        self.velocity = (0, 0)
        self.angle = 0

    def updateRect(self):
        # update the object's rect attribute with the new x,y coordinates
        w, h = self.image.get_size()
        self.width, self.height = w, h
        self.rect = pygame.Rect(self.x - w / 2, self.y - h / 2, w, h)

    def update(self, screenWidth, screenHeight):
        self.image = pygame.transform.rotate(self.baseImage, self.angle)
        vx, vy = self.velocity
        self.x += vx
        self.y += vy
        self.updateRect()
        # wrap around, and update the rectangle again
        if self.rect.left > screenWidth:
            self.x -= screenWidth + self.width
        elif self.rect.right < 0:
            self.x += screenWidth + self.width
        if self.rect.top > screenHeight:
            self.y -= screenHeight + self.height
        elif self.rect.bottom < 0:
            self.y += screenHeight + self.height
        self.updateRect()

import pygame
import math
#from GameObject import GameObject

class Ship(GameObject):
    # we only need to load the image once, not for every ship we make!
    #   granted, there's probably only one ship...
    @staticmethod
    def init():
        Ship.shipImage = pygame.transform.rotate(pygame.transform.scale(
            pygame.image.load('C:\\Users\\memor\\Documents\\15112\\tp\\spaceship.png').convert_alpha(),
            (60, 100)), -90)  # rotate -90 because ship is pointing up, but 0 = right

    def __init__(self, x, y):
        super(Ship, self).__init__(x, y, Ship.shipImage, 30)
        self.power = 1
        self.drag = 0.9
        self.angleSpeed = 5
        self.angle = 0  # starts pointing straight up
        self.maxSpeed = 20

    def update(self, keysDown, screenWidth, screenHeight):
        if keysDown(pygame.K_LEFT):
            self.angle += self.angleSpeed

        if keysDown(pygame.K_RIGHT):
            # not elif! if we're holding left and right, don't turn
            self.angle -= self.angleSpeed

        if keysDown(pygame.K_UP):
            self.thrust(self.power)
        else:
            vx, vy = self.velocity
            self.velocity = self.drag * vx, self.drag * vy

        super(Ship, self).update(screenWidth, screenHeight)

    def thrust(self, power):
        angle = math.radians(self.angle)
        vx, vy = self.velocity
        # distribute the thrust in x and y directions based on angle
        vx += power * math.cos(angle)
        vy -= power * math.sin(angle)
        speed = math.sqrt(vx ** 2 + vy ** 2)
        if speed > self.maxSpeed:
            factor = self.maxSpeed / speed
            vx *= factor
            vy *= factor
        self.velocity = (vx, vy)
#C:\Users\memor\Documents\15112\tp\asteroids.png
#C:\Users\memor\Documents\15112\tp\spaceship.png

import pygame
#from Ship import Ship
from pygamegame import PygameGame


class Game(PygameGame):
    def init(self):
        Ship.init()
        self.shipGroup = pygame.sprite.Group(Ship(self.width, self.height))

    def timerFired(self, dt):
        self.shipGroup.update(self.isKeyPressed, self.width, self.height)

    def redrawAll(self, screen):
        self.shipGroup.draw(screen)

Game(600, 600).run()