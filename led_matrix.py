# Importing the library
from matplotlib.pyplot import pause
import pygame
import time
import threading
import mido
import rtmidi
import keyboard
import random
import os
import sys

class led_matrix:
    def __init__(self, rows = 10, columns = 10, led_size = 10, padding_coef = 1.1):
        pygame.init()
        self.offColor = (50,50,50)
        self.rows = rows
        self.columns = columns
        self.led_size = led_size
        self.padding_coef = padding_coef
        self.surface = pygame.display.set_mode((self.columns*self.led_size*2*self.padding_coef,self.rows*self.led_size*2*self.padding_coef+95))
        self.pixels = self.setPixels()
        self.image = pygame.image.load(os.path.join(sys.path[0], "piano_matrix.png"))
        self.surface.blit(self.image, (0,self.rows*self.led_size*2*self.padding_coef))

    def setPixels(self):
        return [[self.offColor for c in range(self.rows)] for r in range(self.columns)]

    def turnOffPixels(self):
        for x in range(self.columns):
                for y in range(self.rows):
                    self.setPixelColor(x, y, self.offColor)

    def setPixelColor(self, x, y, color):
        self.pixels[x][y] = color

    def getPixelPosition(self, x, y):
        return (x*self.led_size*2*self.padding_coef + self.led_size, y*self.led_size*2*self.padding_coef + self.led_size)

    def imageToPixels(self, pixels):
         for x in range(self.columns):
                for y in range(self.rows):
                    color = (pixels[x,y][0], pixels[x,y][1], pixels[x,y][2])
                    self.setPixelColor(x, y, color)

    def start(self):
        run = True
        while run:
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    run = False

            for x in range(self.columns):
                for y in range(self.rows):
                    pygame.draw.circle(self.surface, self.pixels[x][y], self.getPixelPosition(x, y), self.led_size)
            pygame.display.flip()
        pygame.quit()

    def begin(self):
        threading.Thread(target=self.start).start()
 
    def playMidi(self, note_list, note_list_off, port, inport, tutorial, delay):
        clock = pygame.time.Clock()
        run = True
        paused = False
        ShouldBePressedKeys = []

        for x in range(self.columns):
                for y in range(self.rows):
                    pygame.draw.circle(self.surface, self.pixels[x][y], self.getPixelPosition(x, y), self.led_size)
        pygame.display.flip()
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            # if not paused:        
            for i in range(len(note_list)):
                if note_list[i][1] < (self.rows):
                    if note_list[i][1] >= 0:
                        pygame.draw.circle(self.surface, note_list[i][2], self.getPixelPosition(note_list[i][0], note_list[i][1]), self.led_size)
                    note_list[i][1] += 1
                elif note_list[i][1] == (self.rows):
                    note_list[i][1] += 1
                    if tutorial:
                        paused = True
                        ShouldBePressedKeys.append(note_list[i][0])
                    else:                         
                        port.send(note_list[i][3])    
            pygame.display.flip()
            
            if tutorial and paused: 
                print(ShouldBePressedKeys)
                pressedMessages = []
                playedNotes = []     
                pressedNotes = []  
                releasedMessages = [] 
                while paused:
                    # print("Before")
                    # time.sleep(1)
                    
                    for msg in inport.iter_pending():
                        if msg.type == 'note_on':
                            pressedMessages.append(msg)
                            playedNotes.append(False)
                            pressedNotes.append(msg.note)
                        else:
                            try:
                                releasedMessages.append(msg)
                                index = pressedNotes.index(msg.note)
                                del playedNotes[index]
                                del pressedMessages[index]
                                del pressedNotes[index]
                            except:
                                continue
                            
                    if keyboard.is_pressed("k"):
                        paused = False  

                    copyPressed = ShouldBePressedKeys.copy() 
                    if(len(pressedMessages) > 0): 
                        print(pressedMessages) 

                    for msg in releasedMessages:
                        port.send(msg)
                        releasedMessages.remove(msg)    
                    for msg in pressedMessages:
                        index = pressedMessages.index(msg)
                        if playedNotes[index] == False:
                            port.send(msg)
                            playedNotes[index] = True

                        # print(msg.note - 36)
                        if msg.note - 36 in ShouldBePressedKeys:
                            copyPressed.remove(msg.note - 36)

                    if len(copyPressed) == 0:
                        paused = False        

                ShouldBePressedKeys = []
                
            

            for i in range(len(note_list_off)):
                if note_list_off[i][1] < (self.rows):
                    if note_list_off[i][1] >= 0:
                        pygame.draw.circle(self.surface, self.offColor, self.getPixelPosition(note_list_off[i][0], note_list_off[i][1]), self.led_size)
                    note_list_off[i][1] += 1
                elif note_list_off[i][1] == (self.rows):
                    note_list_off[i][1] += 1
                    port.send(note_list_off[i][2])
                    
            time.sleep(delay)    
                # clock.tick(10)
        pygame.quit()    

    def readFromPiano(self, inport, rows, delay):
        note_list = []
        note_list_off = []
        clock = pygame.time.Clock()
        done = False

        # paint empty LED matrix
        for x in range(self.columns):
                for y in range(self.rows):
                    pygame.draw.circle(self.surface, self.pixels[x][y], self.getPixelPosition(x, y), self.led_size)
        pygame.display.flip()

        while done == False:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done=True

            # iterate through incomming MIDI messages
            for msg in inport.iter_pending():
                n = msg.note
                x = n - 36
                if msg.velocity > 0 and msg.type == 'note_on':
                    r = random.randint(0, 255)
                    g = random.randint(0, 255)
                    b = random.randint(0, 255)
                    rgb = (r, g, b)
                    note_list.append([x, rows, rgb])
                else:       
                    note_list_off.append([x, rows])    

            # iterate through note_on list and show in matrix
            for i in range(len(note_list)):
                pygame.draw.circle(self.surface, note_list[i][2], self.getPixelPosition(note_list[i][0], note_list[i][1]), self.led_size)       
                if note_list[i][1] >= 0:
                    note_list[i][1] -= 1

            # iterate through note_off list and show in matrix
            for i in range(len(note_list_off)):
                pygame.draw.circle(self.surface, self.offColor, self.getPixelPosition(note_list_off[i][0], note_list_off[i][1]), self.led_size)
                if note_list_off[i][1] >= 0:
                    note_list_off[i][1] -= 1  
            pygame.display.flip()
            time.sleep(delay) 
            # clock.tick(200)
        pygame.quit()