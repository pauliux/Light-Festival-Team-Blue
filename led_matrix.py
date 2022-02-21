# Importing the library
import pygame
import threading

class led_matrix:
    def __init__(self, rows = 10, columns = 10, led_size = 10, padding_coef = 1.1):
        pygame.init()
        self.offColor = (50,50,50)
        self.rows = rows
        self.columns = columns
        self.led_size = led_size
        self.padding_coef = padding_coef
        self.surface = pygame.display.set_mode((self.columns*self.led_size*2*self.padding_coef,self.rows*self.led_size*2*self.padding_coef))
        self.pixels = self.setPixels()

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
 