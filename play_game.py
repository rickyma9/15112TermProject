import pygame
import pygamegame
from objects import *
import os
import string
import main_game

# run this file to play the game

class play(pygamegame.PygameGame):
    def init(self, screen):
        self.beatmapName = None

        self.screen = screen

        self.path = "beatmaps"
        self.musicPath = "music"

        self.channel = pygame.mixer.Channel(0)
        self.audio = None
        self.audioLength = None
        self.hitsound = pygame.mixer.Sound("drum-hitclap.wav")
        pygame.mixer.Sound.set_volume(self.hitsound, 0.3)

        self.selectScreenAudio = None
        self.selectScreenAudioPlaying = False

        self.background = pygame.image.load("images\\background.jpg").convert_alpha()
        self.background = pygame.transform.smoothscale(self.background, (self.width, self.height))

        self.timeline = {}

        self.clock = pygame.time.Clock()
        self.smallTime = 0
        self.time = 0

        self.font = pygame.font.SysFont("gillsans", 25) 
        self.scoreFont = pygame.font.SysFont("gillsans", 75) 

        self.combo = 0
        self.maxCombo = 0
        self.score = 0
        self.num300s = 0
        self.num100s = 0
        self.num50s = 0
        self.numMisses = 0

        self.pause = False
        self.drag = False

        self.inSlider = False
        self.curSlider = None

        self.fixedCircle1 = bigCircle(self.width//2, self.height//2, self.height//6, self.screen)
        self.fixedCircle2 = bigCircle(self.width//2, self.height//2, self.height//2, self.screen)

        self.playing = False
        self.scoreScreen = False

        self.hoveredArea = None
        self.clickedArea = None

    # open the music for the beatmap
    def openMusic(self, name):
        self.audio = pygame.mixer.Sound(self.musicPath + "\\" + name)
        self.audioLength = int(pygame.mixer.Sound.get_length(self.audio))

    # open the beatmap you want to play
    def openBeatmap(self, name):
        with open(self.path + "\\" + name, "rt") as f:
            contents = f.read()

        self.openMusic(contents.splitlines()[0])

        for line in contents.splitlines()[1:]:
            obj = line.split(" ")
            index = int(obj[0])

            if len(obj) > 5:
                circle1 = Circle(int(obj[1]), int(obj[2]), int(obj[3]), self.screen)
                circle2 = Circle(int(obj[4]), int(obj[5]), int(obj[6]), self.screen)
                self.timeline[index] = Slider(circle1, circle2, self.screen)
            elif len(obj) == 1:
                self.timeline[index] = None
            else:
                self.timeline[index] = Circle(int(obj[1]), int(obj[2]), int(obj[3]), self.screen)


    def mousePressed(self, x, y):

        if self.selectScreenAudio != None:
            self.selectScreenAudio.stop()

        if self.scoreScreen == True:
            self.init(self.screen)

        # actions you can take when paused
        if self.pause == True:
            if self.width/2-self.width/6 <= x <= self.width/2+self.width/6 and\
               self.height/2-self.height/32 <= y <= self.height/2-self.height/32+self.height/16:


                self.channel.unpause()
                self.pause = False

            elif self.width/2-self.width/6 <= x <= self.width/2+self.width/6 and\
                 self.height/2-self.height/32+40 <= y <= self.height/2-self.height/32+40+self.height/16:


                self.channel.stop()
                self.pause = False
                self.openBeatmap(self.beatmapName)
                self.time = 0
                self.smallTime = 0
                self.channel.play(self.audio)

            elif self.width/2-self.width/6 <= x <= self.width/2+self.width/6 and\
                 self.height/2-self.height/32+80 <= y <= self.height/2-self.height/32+80+self.height/16:

                self.init(self.screen)

        # actions when not paused lol
        else:

            # pick a beatmap to play
            if self.playing == False:
                beatmaps = os.listdir(self.path)
                numBeatmaps = len(beatmaps)

                for i in range(0, numBeatmaps):

                    if 10 <= x <= self.width-20 and 10 + 10*i + i*(self.height-20)/16 <= y <= 10 + 10*i + (i+1)*(self.height-20)/16:

                        self.clickedArea = (10, 10 + 10*i + (i)*(self.height-20)/16, self.width-20,  
                                        (self.height-20)/16)

                        self.beatmapName = beatmaps[i]
                        self.openBeatmap(self.beatmapName)
                        self.playing = True


            # play the game
            else:

                self.drag = True

                # scoring for circles
                if isinstance(self.timeline[self.time], Circle):
                    circle = self.timeline[self.time]

                    if circle.x - circle.r <= x <= circle.x + circle.r and \
                       circle.y - circle.r <= y <= circle.y + circle.r:
                        #toRemove.append(circle)
                        self.combo += 1
                        if 1 <= circle.approachR - circle.r <= 10:
                            self.score += 300*self.combo
                            self.num300s += 1
                            circle.isClicked = True
                            pygame.mixer.Sound.play(self.hitsound)

                        elif circle.approachR - circle.r <= 1 and circle.isClicked != True:
                            self.numMisses += 1

                        elif 11 <= circle.approachR - circle.r <= 25:
                            self.score +=100*self.combo
                            self.num100s += 1
                            circle.isClicked = True
                            pygame.mixer.Sound.play(self.hitsound)

                        elif 26 <= circle.approachR - circle.r <= 30:
                            self.score +=50*self.combo
                            self.num50s += 1
                            circle.isClicked = True
                            pygame.mixer.Sound.play(self.hitsound)

                        else:
                            #pygame.mixer.Sound.play(self.combobreak)
                            if self.combo > self.maxCombo:
                                self.maxCombo = self.combo
                            self.numMisses += 1
                            self.combo = 0

                # slider behaviors, like the sliderball, circle, movement, etc
                elif isinstance(self.timeline[self.time], Slider):
                    slider = self.timeline[self.time]

                    if slider.startx - slider.r <= x <= slider.startx + slider.r and\
                       slider.starty - slider.r <= y <= slider.starty + slider.r:
                        self.curSlider = slider
                        self.inSlider = True
                        self.curSlider.inside = True
                        slider.isClicked()



    def mouseReleased(self, x, y):

        # controlling for comboing in sliders
        if self.inSlider == True:
            self.combo = 0
            self.curSlider.inside = False
            self.inSlider = False

        self.drag = False

    def mouseMotion(self, x, y):

        self.clickedArea = None
        self.hoveredArea = None

        if self.pause == True:
            if self.width/2-self.width/6 <= x <= self.width/2+self.width/6 and\
               self.height/2-self.height/32 <= y <= self.height/2-self.height/32+self.height/16:

                self.hoveredArea = (self.width/2-self.width/6, self.height/2-self.height/32,
                                    self.width/3, self.height/16)


            elif self.width/2-self.width/6 <= x <= self.width/2+self.width/6 and\
                 self.height/2-self.height/32+40 <= y <= self.height/2-self.height/32+40+self.height/16:

                self.hoveredArea = (self.width/2-self.width/6, self.height/2-self.height/32+40,
                                    self.width/3, self.height/16)

            elif self.width/2-self.width/6 <= x <= self.width/2+self.width/6 and\
                 self.height/2-self.height/32+80 <= y <= self.height/2-self.height/32+80+self.height/16:

                self.hoveredArea = (self.width/2-self.width/6, self.height/2-self.height/32+80,
                                    self.width/3, self.height/16)


        # actions when not paused lol
        else:

            # pick a beatmap to play
            if self.playing == False and self.scoreScreen == False:
                beatmaps = os.listdir(self.path)
                numBeatmaps = len(beatmaps)

                for i in range(0, numBeatmaps):

                    if 10 <= x <= self.width-20 and 10 + 10*i + i*(self.height-20)/16 <= y <= 10 + 10*i + (i+1)*(self.height-20)/16:

                        self.hoveredArea = (10, 10 + 10*i + (i)*(self.height-20)/16, self.width-20,  
                                        (self.height-20)/16)

                        if i != self.selectScreenAudioPlaying and self.selectScreenAudio != None:
                            self.selectScreenAudio.stop()
                            self.selectScreenAudio = None

                        if self.selectScreenAudio == None:  
                            self.selectScreenAudioPlaying = i

                            with open(self.path + "\\" + beatmaps[i], "rt") as f:
                                contents = f.read()

                            songName = contents.splitlines()[0]
                            self.selectScreenAudio = pygame.mixer.Sound(self.musicPath + "\\" + songName)
                            self.selectScreenAudio.set_volume(0.1)
                            self.selectScreenAudio.play()


    def mouseDrag(self, x, y):

        # comboing for sliders, determining if you're inside a slider, etc
        if self.inSlider == True:
            r = self.curSlider.sliderBall.r
            sX = self.curSlider.sliderBall.x
            sY = self.curSlider.sliderBall.y
            # if you go out of sliderball, break combo
            if x not in range(sX-r, sX+r) or y not in range (sY-r, sY+r) and \
               self.curSlider.comboBreak == True:
                

                if self.combo > self.maxCombo:
                    self.maxCombo = self.combo
                self.combo = 0
                #self.sliders.remove(self.curSlider)
                self.inSlider = False
                self.curSlider.inside = False

        # if you are still dragging and go back in sliderball range, draw the big sliderball again (possibly start adding combo again!!)
        #if self.drag == True:
        #    r = self.curSlider.sliderBall.r
        #    sX = self.curSlider.sliderBall.x
        #    sY = self.curSlider.sliderBall.y
        #    
        #    if x in range(sX-r, sX+r) and y in range (sY-r, sY+r):
        #        self.inSlider = True # -> call the original if statement again, which determines if you go back out, breaking combo again
        #        self.curSlider.inside = True

    def keyPressed(self, keyCode, modifier):

        if keyCode == pygame.K_ESCAPE:
            if self.audio != None:
                self.audio.stop()
                self.audio = None
            if self.selectScreenAudio != None:
                self.selectScreenAudio.stop()
                self.selectScreenAudio =  None

            game = main_game.main_game()
            game.run()

        # pausing and unpausing!!
        if keyCode == pygame.K_BACKQUOTE:
            self.pause = not self.pause
            if self.pause == True:
                self.channel.pause()
            else:
                self.channel.unpause()
        
        # skip to score screen
        if keyCode ==  pygame.K_u:
            self.time = self.audioLength-1
            self.smallTime = self.audioLength-1
            self.scoreScreen = True

    def timerFired(self, dt):

        # controls time-based things while playing
        if self.playing == True:

            # play the song
            if self.smallTime == 0:
                pygame.mixer.Sound.set_volume(self.audio, 0.1)
                #pygame.mixer.Sound.play(self.audio)
                self.channel.play(self.audio)

            # when beatmap is over, stop the song
            if self.time >= self.audioLength:
                self.channel.stop()
                self.playing = False
                self.scoreScreen = True

            # when not paused, do this
            if self.pause == False:

                self.smallTime += dt/1000
                self.time = int(self.smallTime)

                # # decreasing the approach circles
                for time in self.timeline:

                    if self.timeline[time] != None and self.time == time:
                        self.timeline[time].approachCircle(int(((1/30) * (self.timeline[time].r * 3)))) # decrease evenly over the span of 1 second(which is based on frames per second)

                        if self.timeline[time].approachR - self.timeline[time].r <= 0:
                            self.timeline[time] = None

                    # updating sliderball 
                    if isinstance(self.timeline[time], Slider):
                        self.timeline[time].updateSliderBall(10) # try to make it update enough over the span of 1 second
                        # slider combos
                        if self.inSlider == True:
                            self.combo += 1

                            slider = self.timeline[time]
                            if abs(slider.sliderBall.x - slider.endx <= 10) and\
                               abs(slider.sliderBall.y - slider.endy <= 10):
                                pygame.mixer.Sound.play(self.hitsound)
                                self.timeline[time] = None

            else:
                pass

    def redrawAll(self, screen):

        screen.blit(self.background, (0, 0))

        if self.hoveredArea != None:
            x, width, y, height = self.hoveredArea
            pygame.draw.rect(self.screen, (200, 200, 200), (x, width, y, height))

        if self.clickedArea != None:
            x, width, y, height = self.clickedArea
            pygame.draw.rect(self.screen, (150, 150, 150), (x, width, y, height))

        #screen.fill((240, 240, 240))

        # what to draw when the beatmap is not over
        if self.scoreScreen == False:
            
            # what's drawn when playing
            if self.playing == True:

                # progress bar
            
                pygame.draw.rect(self.screen, (190, 190, 190), (100, 20, self.width/20, (self.height-40)))
                pygame.draw.rect(self.screen, (255, 255, 255), (100, 20, self.width/20, (self.height-40)*(self.audioLength-self.time)/self.audioLength))
                pygame.draw.rect(self.screen, (100, 100, 100), (100, 20, self.width/20, (self.height-40)), 2)

                self.fixedCircle1.draw()
                self.fixedCircle2.draw()

                comboText = self.font.render(str(self.combo), True, (0, 0, 0))
                scoreText = self.font.render(str(self.score), True, (0, 0, 0))

                # combo and score
                screen.blit(comboText, (30, self.height-50))
                screen.blit(scoreText, (self.width-100, 50))

                if self.timeline[self.time] != None:
                    self.timeline[self.time].draw()

                # drawing of the pause screen
                if self.pause == True:
                    pygame.draw.rect(self.screen, (230, 230, 230), (self.width/2-self.width/6, self.height/2-self.height/32, self.width/3, self.height/16))
                    pygame.draw.rect(self.screen, (0, 0, 0), (self.width/2-self.width/6, self.height/2-self.height/32, self.width/3, self.height/16), 1)
                    pygame.draw.rect(self.screen, (230, 230, 230), (self.width/2-self.width/6, self.height/2-self.height/32+40, self.width/3, self.height/16))
                    pygame.draw.rect(self.screen, (0, 0, 0), (self.width/2-self.width/6, self.height/2-self.height/32+40, self.width/3, self.height/16), 1)
                    pygame.draw.rect(self.screen, (230, 230, 230), (self.width/2-self.width/6, self.height/2-self.height/32+80, self.width/3, self.height/16))
                    pygame.draw.rect(self.screen, (0, 0, 0), (self.width/2-self.width/6, self.height/2-self.height/32+80, self.width/3, self.height/16), 1)

                    paused = "Continue"
                    retry = "Retry"
                    quit = "Quit"

                    pausedRender = self.font.render(paused, True, (0, 0, 0))
                    retryRender = self.font.render(retry, True, (0, 0, 0))
                    quitRender = self.font.render(quit, True, (0, 0, 0))

                    screen.blit(pausedRender, (self.width/2-30, self.height/2-self.height/32+10))
                    screen.blit(retryRender, (self.width/2-22, self.height/2-self.height/32+10+40))
                    screen.blit(quitRender, (self.width/2-20, self.height/2-self.height/32+10+80))

            # what's drawn when you're picking a map to play
            else:
                numBeatmaps = len(os.listdir(self.path))

                i = 0
                for beatmap in os.listdir(self.path):
                    pygame.draw.rect(self.screen, (0, 0, 0), (10, 10 + 10*i + i*(self.height-20)/16, self.width-20, (self.height-20)/16), 1)

                    name = beatmap[:-4]

                    beatmapRender = self.font.render(name, True, (0, 0, 0)) 

                    screen.blit(beatmapRender, (10+8, (10 + 10*i + i*(self.height-20)/16)+8))

                    i += 1

        # score screen!
        else:
            pygame.draw.rect(self.screen, (0, 0, 0), (self.width/4, 50, self.width/2, self.height-80), 1)
            pygame.draw.rect(self.screen, (0, 0, 0), (self.width/4, 50, self.width/2, self.height/5), 1)

            score = str(self.score)
            maxCombo = str(self.maxCombo)
            num300s = str(self.num300s)
            threehundo = "300:"
            num100s = str(self.num100s)
            onehundo = "100:"
            num50s = str(self.num50s)
            fiftyo = "50:"
            misses = str(self.numMisses)
            misseso = "Misses:"
            tryAgain = "Click anywhere to pick another beatmap!"

            scoreRender = self.scoreFont.render(score, True, (0, 0, 0))
            maxComboRender = self.scoreFont.render(maxCombo, True, (0, 0, 0))
            num300sRender = self.scoreFont.render(num300s, True, (0, 0, 0))
            num100sRender = self.scoreFont.render(num100s, True, (0, 0, 0))
            num50sRender = self.scoreFont.render(num50s, True, (0, 0, 0))
            missesRender = self.scoreFont.render(misses, True, (0, 0, 0))
            threehundoRender = self.scoreFont.render(threehundo, True, (0, 0, 0))
            onhundoRender = self.scoreFont.render(onehundo, True, (0, 0, 0))
            fiftyoRender = self.scoreFont.render(fiftyo, True, (0, 0, 0))
            missesoRender = self.scoreFont.render(misseso, True, (0, 0, 0))
            tryAgainRender = self.font.render(tryAgain, True, (0, 0, 0))

            screen.blit(scoreRender, (self.width/4 + 20, 50+20))
            screen.blit(num300sRender, (self.width/4 + self.width/2 - 150, 50 + self.height/5 + 30))
            screen.blit(num100sRender, (self.width/4 + self.width/2 - 150, 50 + self.height/5 + 120))
            screen.blit(num50sRender, (self.width/4 + self.width/2 - 150, 50 + self.height/5 + 210))
            screen.blit(missesRender, (self.width/4 + self.width/2 - 150, 50 + self.height/5 + 300))
            screen.blit(threehundoRender, (self.width/4 + 30, 50 + self.height/5 + 30))
            screen.blit(onhundoRender, (self.width/4 + 30, 50 + self.height/5 + 120))
            screen.blit(fiftyoRender, (self.width/4 + 30, 50 + self.height/5 + 210))
            screen.blit(missesoRender, (self.width/4 + 30, 50 + self.height/5 + 300))
            screen.blit(tryAgainRender, (10, 10))
            
