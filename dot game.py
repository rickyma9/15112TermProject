import pygame
import random
class Dot(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Dot, self).__init__()
        self.radius = random.randint(5, 20)
        self.x, self.y = x, y
        self.xSpeed = random.randint(-10, 10)
        self.ySpeed = random.randint(-10, 10)
        self.rect = pygame.Rect(x - self.radius, y - self.radius,
                                2 * self.radius, 2 * self.radius)
        self.image = pygame.Surface((2 * self.radius, 2 * self.radius),
                                    pygame.SRCALPHA)  # make it transparent
        self.image = self.image.convert_alpha()
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        pygame.draw.circle(self.image, (r, g, b),
                           (self.radius, self.radius), self.radius)

    def getRect(self):  # GET REKT
        self.rect = pygame.Rect(self.x - self.radius, self.y - self.radius,
                                2 * self.radius, 2 * self.radius)

    def update(self, screenWidth, screenHeight):
        self.x += self.xSpeed
        self.y += self.ySpeed
        if self.x < 0:
            self.x = screenWidth
        elif self.x > screenWidth:
            self. x = 0
        if self.y < 0:
            self.y = screenHeight
        elif self.y > screenHeight:
            self.y = 0
        self.getRect()

pygame.init()
screen = pygame.display.set_mode((500, 500))
clock = pygame.time.Clock()

dots = pygame.sprite.Group()
playing = True
while playing:
    clock.tick(50)
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            d = Dot(*event.pos)
            dots.add(d)
        elif event.type == pygame.QUIT:
            playing = False
    dots.update(500, 500)
    screen.fill((255, 255, 255))
    dots.draw(screen)
    pygame.display.flip()
pygame.quit()