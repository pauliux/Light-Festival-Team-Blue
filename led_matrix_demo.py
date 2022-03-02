from led_matrix import led_matrix
from PIL import Image
import time
from mido import MidiFile
import os
import sys
import math
import random
import mido
import rtmidi # py -m pip install python-rtmidi

def get_tempo(mid):
     for track in mid.tracks:
         for msg in track:
             if msg.type == 'set_tempo':
                 return msg.tempo
     else:
         # Default tempo.
         return 500000

def shortestNoteTime(mid):
    min = 10000
    for msg in mid:
        if not msg.is_meta:
            try:
                if msg.time < min and msg.time > 0.02:
                    min = msg.time
            except:
                continue
    if min == 10000:
        min = 0.02        
    return min

def readMidi(mid, note_list, note_list_off):
    yCoordinate = 0
    
    timeForOnePixel = shortestNoteTime(mid)

    # smallest note is thirty-second note, then sixteenth note then eighth note and quarter note. 
    # thirty-second note = 1 led pixel
    # quarterNoteLengthInSec = get_tempo(mid)/1000000
    # timeForOnePixel = quarterNoteLengthInSec / 2**3   

    for msg in mid:
        if not msg.is_meta:
            try:
                # print(msg)
                # time.sleep(msg.time)
                n = msg.note
                numOfPixels = int(math.ceil(msg.time / timeForOnePixel))
                yCoordinate -= numOfPixels
                x = n-30
                r = random.randint(0, 255)
                g = random.randint(0, 255)
                b = random.randint(0, 255)
                rgb = (r, g, b)
 
                if msg.velocity > 0:
                    note_list.append([x, yCoordinate, rgb, msg])
                else:
                    note_list_off.append([x, yCoordinate, msg])   
            except:
                continue

def playAnimation(led_matrix, folder):
    path = os.path.join(sys.path[0], "animations/"+folder) # splash effect for 30x50 matrix
    animationImages = os.listdir(path)
    led_matrix.begin()
    imageAnimation(animationImages, path)

def playMidiFile(led_matrix, file, delay, tutorial):
    note_list = []
    note_list_off = []
    mid = MidiFile(os.path.join(sys.path[0], "MIDI/"+file), clip=True)
    # outputs = mido.get_output_names()
    # print(outputs)
    port = mido.open_output("Microsoft GS Wavetable Synth 0")
    readMidi(mid, note_list, note_list_off)

    led_matrix.playMidi(note_list, note_list_off, port, tutorial = tutorial, delay = delay) 
        
def imageAnimation(animationImages, path):
    for img in animationImages:
        im = Image.open(path+"/"+img) # Can be many different formats.
        pix = im.load()
        led_matrix.imageToPixels(pix)
        time.sleep(0.02)
    led_matrix.turnOffPixels()      

def customFunction(led_matrix, rows, columns):
    led_matrix.begin()
    for y in range(0, columns, 5):    
        for x in range(rows): 
            led_matrix.setPixelColor(y,rows-1-x,(255,255,255))
            time.sleep(0.02)
        led_matrix.turnOffPixels() 


if __name__ == "__main__":
    rows = 30
    columns = 65
    led_matrix = led_matrix(rows = rows, columns = columns, led_size = 10)

    # customFunction(led_matrix, rows, columns)

    # playAnimation(led_matrix = led_matrix, folder = "splash-30x50") # matrix dimensions must be the same as image's (rows X columns) 

    playMidiFile(led_matrix = led_matrix, file = "pirates.mid", tutorial = False, delay = 0.02)
                
