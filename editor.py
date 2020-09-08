import pygame
from objects import *
import pygamegame
import math
import os
import main_game 

# run this to make your own beatmap

class Editor(pygamegame.PygameGame):

    def init(self, screen):
        self.screen = screen

        self.path = "beatmaps"
        self.musicPath = "music"

        self.hasMusic = False
        self.songName = None
        self.audio = None
        self.audioLength = None

        self.selectScreenAudio = None
        self.selectScreenAudioPlaying = False

        self.background = pygame.image.load("images\\background.jpg").convert_alpha()
        self.background = pygame.transform.smoothscale(self.background, (self.width, self.height))

        # controls the squares for making objects and saving
        self.makeC = (0, 0, self.width//6, self.height//3)
        self.makeS = (0, self.height//3, self.width//6, self.height//3)
        self.save = (0, 2*self.height//3, self.width//6, self.height//3)

        self.clickedArea = None
        self.hoveredArea = None

        self.font = pygame.font.SysFont(None, 25)

        self.currentTime = 0  
        
        # controlling the time/passage of time in the editor
        self.pause = True
        self.clock = pygame.time.Clock()
        self.time = 0
        self.smallTime = 0
        self.preciseTime = 0

        # controlling all the objects
        self.timeline = {}
        # initialize so that each seconds currently has no object placed on it

        self.fixedCircle1 = bigCircle(self.width//2, self.height//2, self.height//6, self.screen)
        self.fixedCircle2 = bigCircle(self.width//2, self.height//2, self.height//2, self.screen)

        self.midpoint = (self.height//2 + self.height//6) // 2

        # making sliders
        self.currentObject = None
        self.makeSlider = False
        self.prevCircle = None

        # controls saving in different ways
        self.saving = False
        self.hasSaved = False
        self.saveTimer = 0

        self.beatmapName = ""
        self.sameName = False
        self.noName = False
        self.attemptSpace = False


    # writefile frome the course notes
    def saveBeatmap(self, path):
        contents = ""
        contents += self.songName + "\n"
        
        # save the beatmap as the coordinates of all the objects
        for key in self.timeline:
            obj = self.timeline[key]
            # maybe just make __repr__ do this...
            if isinstance(obj, Circle):
                contents += (str(key) + " " + str(obj.x) + " " + str(obj.y) + " " + str(obj.r) + "\n")
            elif isinstance(obj, Slider):
                contents += (str(key) + " " + str(obj.startx) + " " + str(obj.starty) + " " + str(obj.r) + " " + str(obj.endx) + " " + str(obj.endy) + " " + str(obj.r) + "\n")
            else:
                contents += str(key) + "\n"

        # if the user has saved before, it saves without asking for a name
        if self.beatmapName not in os.listdir(path):

            with open(path + "\\" + self.beatmapName + ".txt", "wt") as f:
                f.write(contents)

        elif self.hasSaved == True:
            print(self.hasSaved)
            with open(path + "\\" + self.beatmapName + ".txt", "wt") as f:
                f.write(contents)
        else:
            pass # maybe make it so you can't have two maps of the same name later


    # create variable for whether or not a box should show up

    # alculates the distance between two circles
    def distance(self, x, y, cX, cY):
        return ((cX-x)**2 + (cY-y)**2)**0.5

    def mousePressed(self, x, y):

        if self.selectScreenAudio != None:
            self.selectScreenAudio.stop()

        if self.hasMusic == False:
            songs = os.listdir(self.musicPath)
            numSongs = len(songs)

            for i in range(0, numSongs):

                if 10 <= x <= self.width-20 and 10 + 10*i + i*(self.height-20)/16 <= y <= 10 + 10*i + (i+1)*(self.height-20)/16:
                    self.clickedArea = (10, 10 + 10*i + (i)*(self.height-20)/16, self.width-20,  
                                        (self.height-20)/16)

                    self.songName = songs[i]
                    self.audio = pygame.mixer.Sound("music" + "\\" + songs[i])
                    self.audioLength = int(pygame.mixer.Sound.get_length(self.audio)) + 1
                    for i in range(0, self.audioLength):
                        self.timeline[i] = None
                    self.hasMusic = True

        # else, edit the song you've picked
        else:

        
            if x in range(self.save[0], self.save[2]) and y in range(self.save[1], self.save[3]*3):

                self.clickedArea = (self.save[0], self.save[1], self.save[2], self.save[3])
                
                self.saving = True
                if self.hasSaved == True:
                    self.saveBeatmap(self.path)

            # if self.saving is true, you can click on buttons for save or cancel
            if self.saving == True:

                # press "cancel"
                if self.width/3 + self.width/3 - self.height/15 <= x <= self.width/3 + self.width/3 + self.height/15 and\
                   self.height/2 + self.height/6 <= y <= self.height/2 + self.height/6 + self.height/15:

                   #(self.width/3 + self.width/3 - self.height/15, self.height/2 + self.height/6, self.width/15, self.height/15)

                    self.clickedArea = (self.width/3 + self.width/3 - self.height/15, self.height/2 + self.height/6,
                                        2*self.height/15, self.height/15)
                    self.saving = False

                # press "save"
                elif self.width/3 <= x <= self.width/3 + self.width/15 and\
                     self.height/2 + self.height/6 <= y <= self.height/2 + self.height/6 + self.height/15:

                     #(self.width/3, self.height/2, self.width/3, self.height/15)

                    self.clickedArea = (self.width/3, self.height/2 + self.height/6,
                                        2*self.height/15, self.height/15)


                    if self.beatmapName == "":
                        self.noName = True
                        #print(self.noName)
                    else:
                        self.hasSaved = True
                        #print(self.hasSaved)
                        self.saveBeatmap(self.path)
                        self.saving = False

            # making objects
            elif self.prevCircle != None:
                print(self.prevCircle, self.currentObject.x)
                self.timeline[self.currentTime] = Slider(self.prevCircle, self.currentObject, self.screen)

            # making circles
            if isinstance(self.currentObject, Circle):
                if self.makeSlider == False:
                    self.timeline[self.currentTime] = self.currentObject

                # creating the first circle in the slider
                if self.makeSlider == True and self.prevCircle == None:
                    self.timeline[self.currentTime] = self.currentObject
                    self.prevCircle = self.currentObject
                    self.currentObject = ghostCircle(x, y, 50, self.screen)
            

            # makes it so that when you draw it at first, it gets fixed to the circle
            cX, cY = self.fixedCircle1.x, self.fixedCircle1.y
            tmpX, tmpY = int(self.fixedCircle2.r*math.cos(math.pi)) + cX, int(self.fixedCircle2.r*math.sin(math.pi)) + cY

            # make it so that you can only have one object per second using the dictionary
            # controls what object you will place
            if x in range(self.makeC[0], self.makeC[2]) and y in range(self.makeC[1], self.makeC[3]):
                self.clickedArea = (self.makeC[0], self.makeC[1], self.makeC[2], self.makeC[3])
                
                self.makeSlider = False
                self.timeline[self.currentTime] = None
                self.prevCircle = None
                self.currentObject = Circle(tmpX, tmpY, 50, self.screen)

            elif x in range(self.makeS[0], self.makeS[2]) and y in range(self.makeS[1], self.makeS[3]*2):
                self.clickedArea = (self.makeS[0], self.makeS[1], self.makeS[2], self.makeS[3])

                self.timeline[self.currentTime] = None
                self.prevCircle = None  # whether i want to make it so that sliders are created in constantly new positions vs always have the same starting position
                self.currentObject = Circle(tmpX, tmpY, 50, self.screen)
                self.makeSlider = True


        print(self.clickedArea)
        #self.clickedArea = None


    def mouseReleased(self, x, y):

        self.clickedArea = None
        

    def mouseMotion(self, x, y):
        self.clickedArea = None
        self.hoveredArea = None

        # make it so that the current object isn't drawn when saving
        if x in range(0, self.width//6) and\
           y in range(2*self.height//3, self.height):
            self.currentObject = None

        # make it so that the object you're placing is fixed to the circles
        if self.currentObject != None:

            fixX, fixY = x, y
            cX, cY = self.fixedCircle1.x, self.fixedCircle1.y
            d = self.distance(x, y, cX, cY)
            angle = math.atan2((cY-y),(x-cX))

            if d > self.midpoint:
                fixX, fixY = int(self.fixedCircle2.r*math.cos(angle)), int(self.fixedCircle2.r*math.sin(angle))
            else:
                fixX, fixY = int(self.fixedCircle1.r*math.cos(angle)), int(self.fixedCircle1.r*math.sin(angle))

            if self.prevCircle != None:
                self.currentObject = ghostCircle(fixX+cX, cY-fixY, 50, self.screen)
            else:
                self.currentObject = Circle(fixX+cX, cY-fixY, 50, self.screen)


        # change color when mouse hovers over area
        if self.hasMusic == False:
            songs = os.listdir(self.musicPath)
            numSongs = len(songs)

            for i in range(0, numSongs):

                if 10 <= x <= self.width-20 and 10 + 10*i + i*(self.height-20)/16 <= y <= 10 + 10*i + (i+1)*(self.height-20)/16:
                    self.hoveredArea = (10, 10 + 10*i + (i)*(self.height-20)/16, self.width-20,  
                                        (self.height-20)/16)

                    if i != self.selectScreenAudioPlaying and self.selectScreenAudio != None:
                        
                        self.selectScreenAudio.stop()
                        self.selectScreenAudio = None

                    if self.selectScreenAudio == None:  
                        self.selectScreenAudioPlaying = i

                        self.selectScreenAudio = pygame.mixer.Sound(self.musicPath + "\\" + songs[i])
                        self.selectScreenAudio.set_volume(0.1)
                        self.selectScreenAudio.play()


        # else, edit the song you've picked
        else:

            if x in range(self.save[0], self.save[2]) and y in range(self.save[1], self.save[3]*3):
                
                self.hoveredArea = (self.save[0], self.save[1], self.save[2], self.save[3])

            elif x in range(self.makeC[0], self.makeC[2]) and y in range(self.makeC[1], self.makeC[3]):
                self.hoveredArea = (self.makeC[0], self.makeC[1], self.makeC[2], self.makeC[3])

            elif x in range(self.makeS[0], self.makeS[2]) and y in range(self.makeS[1], self.makeS[3]*2):
                self.hoveredArea = (self.makeS[0], self.makeS[1], self.makeS[2], self.makeS[3])

            # if self.saving is true, you can click on buttons for save or cancel
            if self.saving == True:

                # press "cancel"
                if self.width/3 + self.width/3 - self.height/15 <= x <= self.width/3 + self.width/3 + self.height/15 and\
                   self.height/2 + self.height/6 <= y <= self.height/2 + self.height/6 + self.height/15:

                    self.hoveredArea = (self.width/3 + self.width/3 - self.height/15, self.height/2 + self.height/6,
                                        2*self.height/15-15, self.height/15)

                # press "save"
                elif self.width/3 <= x <= self.width/3 + self.width/15 and\
                     self.height/2 + self.height/6 <= y <= self.height/2 + self.height/6 + self.height/15:

                    self.hoveredArea = (self.width/3, self.height/2 + self.height/6,
                                        2*self.height/15-15, self.height/15)
        
            
    def keyPressed(self, keyCode, modifier):
        # left and right change time, press space to let it play out

        if keyCode == pygame.K_ESCAPE:

            if self.selectScreenAudio != None:
                self.selectScreenAudio.stop()
                self.selectScreenAudio =  None

            game = main_game.main_game()
            game.run()

        # reset the editor
        if self.saving == False:
            if keyCode == pygame.K_BACKQUOTE:
                self.init(self.screen)

        if self.saving == True:
            if keyCode == pygame.K_BACKSPACE:
                self.attemptSpace = False
                self.beatmapName = self.beatmapName[:-1]
            elif keyCode == pygame.K_SPACE:
                self.attemptSpace = True
            elif keyCode <= 127:
                self.beatmapName += chr(keyCode)
                self.noName = False
                self.attemptSpace = False
            elif keycode == pygame.K_RETURN:
                pass # do the save beatmap stuff
            
        # edit the beatmap based on timestamps
        else:
            self.prevCircle = None

            if keyCode != pygame.K_p:
                for time in self.timeline:
                    if self.timeline[time] != None:
                        self.timeline[time].approachR = self.timeline[time].r * 3

            if keyCode == pygame.K_RIGHT:
                if self.currentTime < self.audioLength:
                    self.currentTime += 1
                    print(self.currentTime)

            if keyCode == pygame.K_LEFT:
                if self.currentTime > 0:

                    self.currentTime -= 1
                    print(self.currentTime)

            if keyCode == pygame.K_p:
                self.currentObject = None
                self.smallTime = self.currentTime
                self.pause = not self.pause


    def timerFired(self, dt):

        #if self.pause 

        # draw the "saved!" text
        if self.hasSaved == True and self.saving == True:
            self.saveTimer += 1
            if self.saveTimer % 100 == 0:
                self.saving = False

        # see how the map will play out
        if self.pause == False:
            
            self.smallTime += dt/1000
            self.currentTime = int(self.smallTime)

            for time in self.timeline:
                if self.timeline[time] != None and self.currentTime == time:
                    self.timeline[time].approachCircle(int(((1/60) * (self.timeline[time].r * 3)))) # decrease evenly over the span of 1 second(which is based on frames per second)
                if isinstance(self.timeline[time], Slider):
                    self.timeline[time].updateSliderBall(10)


    def redrawAll(self, screen):

        screen.blit(self.background, (0, 0))

        #screen.fill((0, 0, 0))
        if self.hoveredArea != None:
            x, width, y, height = self.hoveredArea
            pygame.draw.rect(self.screen, (200, 200, 200), (x, width, y, height))

        if self.clickedArea != None:
            x, width, y, height = self.clickedArea
            pygame.draw.rect(self.screen, (100, 100, 100), (x, width, y, height))

        # drawing for when you need to pick a song to edit
        if self.hasMusic == False:

            i = 0
            for song in os.listdir(self.musicPath):
                pygame.draw.rect(self.screen, (0, 0, 0), (10, 10 + 10*i + i*(self.height-20)/16, self.width-20, (self.height-20)/16), 1)

                name = song[:-4]

                beatmapRender = self.font.render(name, True, (0, 0, 0)) 

                screen.blit(beatmapRender, (10+8, (10 + 10*i + i*(self.height-20)/16)+8))

                i += 1

        # drawing for the editor
        else:
            
            pygame.draw.rect(self.screen, (0, 0, 0), self.makeC, 3)
            pygame.draw.rect(self.screen, (0, 0, 0), self.makeS, 3)
            pygame.draw.rect(self.screen, (0, 0, 0), self.save, 3)


            makeCircle = "Make Circle"
            makeSlider = "Make Slider"
            makeSave = "Save Beatmap"

            makeCircleRender = self.font.render(makeCircle, True, (0, 0, 0))
            makeSliderRender = self.font.render(makeSlider, True, (0, 0, 0))
            makeSaveRender = self.font.render(makeSave, True, (0, 0, 0))

            screen.blit(makeCircleRender, (self.makeC[0] + 10, self.makeC[1] + 10))
            screen.blit(makeSliderRender, (self.makeS[0] + 10, self.makeS[1] + 10))
            screen.blit(makeSaveRender, (self.save[0] + 10, self.save[1] + 10))

            #pygame.draw.rect(self.screen, (190, 190, 190), (self.width-100, 20, self.width/20, (self.height-40)*self.currentTime/self.audioLength))
            pygame.draw.rect(self.screen, (190, 190, 190), (self.width-100, 20, self.width/20, (self.height-40)))
            pygame.draw.rect(self.screen, (255, 255, 255), (self.width-100, 20, self.width/20, (self.height-40)*(self.audioLength-self.currentTime)/self.audioLength))
            pygame.draw.rect(self.screen, (100, 100, 100), (self.width-100, 20, self.width/20, (self.height-40)), 2)

            if isinstance(self.timeline[self.currentTime], Circle):
                objAtTime = "Circle"
            elif isinstance(self.timeline[self.currentTime], Slider):
                objAtTime = "Slider"
            else:
                objAtTime = "No Object"

            objAtTimeRender = self.font.render(objAtTime, True, (0, 0, 0))
            screen.blit(objAtTimeRender, (self.width-200, 20))


            self.fixedCircle1.draw()
            self.fixedCircle2.draw()

            if self.currentObject != None:
                self.currentObject.draw()


            # possibly show the objects before and after (only if tier permits)
            for time in self.timeline:
                
                if self.timeline[time] != None and self.currentTime == time:
                    self.timeline[time].draw()
                    break
                    
            # drawing for when you're saving
            if self.saving == True:
                
                # dialog box for saving
                if self.hasSaved == False:
                    pygame.draw.rect(self.screen, (255, 255, 255), (self.width/4, self.height/4, self.width/2, self.height/2))
                    pygame.draw.rect(self.screen, (0, 0, 0), (self.width/4, self.height/4, self.width/2, self.height/2), 1)

                    # box for entering text, i guess
                    pygame.draw.rect(self.screen, (255, 255, 255), (self.width/3, self.height/2, self.width/3, self.height/15))
                    pygame.draw.rect(self.screen, (0, 0, 0), (self.width/3, self.height/2, self.width/3, self.height/15), 1)

                    if self.hoveredArea != None:
                        x, width, y, height = self.hoveredArea
                        pygame.draw.rect(self.screen, (200, 200, 200), (x, width, y, height))

                    if self.clickedArea != None:
                        x, width, y, height = self.clickedArea
                        pygame.draw.rect(self.screen, (100, 100, 100), (x, width, y, height))

                    # box for saving
                    pygame.draw.rect(self.screen, (0, 0, 0), (self.width/3, self.height/2 + self.height/6, self.width/15, self.height/15), 1)
                    # box for cancelling
                    pygame.draw.rect(self.screen, (0, 0, 0), (self.width/3 + self.width/3 - self.height/15, self.height/2 + self.height/6, self.width/15, self.height/15), 1)


                    # text
                    question = "What do you want to name your beatmap?"
                    confirm = "Save"
                    cancel = "Cancel"
                    noname = "Your beatmap has no name!"
                    samename = "Another beatmap has this name. Do you want to override it?"
                    space = "No spaces allowed!"

                    # render the text as surfaces
                    questionRender = self.font.render(question, True, (0, 0, 0))
                    confirmRender = self.font.render(confirm, True, (0, 0, 0))
                    cancelRender = self.font.render(cancel, True, (0, 0, 0))
                    nameRender = self.font.render(self.beatmapName, True, (0, 0, 0))
                    nonameRender = self.font.render(noname, True, (255, 0, 0))
                    samenameRender = self.font.render(samename, True, (255, 0, 0))
                    spaceRender = self.font.render(space, True, (255, 0, 0))

                    # blit text onto screen
                    screen.blit(questionRender, (self.width/2 - self.width/6, self.height/2 - 50))
                    screen.blit(confirmRender, (self.width/3 + 5, self.height/2 + self.height/6 + 10))
                    screen.blit(cancelRender, (self.width/3 + self.width/3 - self.height/15 + 4, self.height/2 + self.height/6 + 10))
                    screen.blit(nameRender, (self.width/3 + 5, self.height/2 + 10))
                    if self.noName == True:
                        screen.blit(nonameRender, (self.width/2 - self.width/6, self.height/2 - 100))
                    elif self.attemptSpace == True:
                        screen.blit(spaceRender, (self.width/2 - self.width/6, self.height/2 - 100))
                    elif self.sameName == True:
                        screen.blit(samenameRender, (self.width/2 - self.width/6, self.height/2 - 100))

                    

                # simply print saved if you've saved before
                else:
                    saved = "Saved!"

                    savedRender = self.font.render(saved, True, (0, 0, 0))

                    screen.blit(savedRender, (self.width/2-50, self.height/2-20))

