from led_matrix import led_matrix
from PIL import Image
import time
import os
import sys

path = os.path.join(sys.path[0], "animations/splash-30x50") # splash effect for 30x50 matrix
animationImages = os.listdir(path)

rows = 30
columns = 50
led_matrix = led_matrix(rows = rows, columns = columns, led_size = 10)
led_matrix.begin()

def imageAnimation():
    for img in animationImages:
        im = Image.open(path+"/"+img) # Can be many different formats.
        pix = im.load()
        led_matrix.imageToPixels(pix)
        time.sleep(0.02)

    led_matrix.turnOffPixels()      


imageAnimation()
imageAnimation()
imageAnimation()

for y in range(0, columns, 5):    
    for x in range(rows): 
        led_matrix.setPixelColor(y,rows-1-x,(255,255,255))
        time.sleep(0.02)
    led_matrix.turnOffPixels()    