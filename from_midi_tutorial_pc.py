import pygame
import mido
import rtmidi
import time
from mido import MidiFile
import threading
import random
import os
import sys
import keyboard

paused = False
outputs = mido.get_output_names()
print(outputs)
port = mido.open_output("Microsoft GS Wavetable Synth 0")
# port = mido.open_output('2- MK USB OUT  1 1')
FILE = os.path.join(sys.path[0], "MIDI/demo1.mid")
mid = MidiFile(FILE, clip=True)
# print(mid)
BLACK = [0, 0, 0]
WHITE = [255, 255, 255]
note_list = []
note_list_off = []

SIZE = [1900, 980]
RECT_SIZE = 25

done = False


def readMidi():
    for msg in MidiFile(FILE).play():
        if not msg.is_meta:
            try:
                # time.sleep(msg.time)
                # print(msg)
                n = msg.note
                x = (n - 35) * 30
                r = random.randint(0, 255)
                g = random.randint(0, 255)
                b = random.randint(0, 255)
                rgb = [r, g, b]
                # rgb = [0,0,255]

                if msg.velocity > 0:
                    note_list.append([x, 0, rgb, msg])
                else:
                    note_list_off.append([x, 0, msg])
            except:
                continue


# readMidi()
threading.Thread(target=readMidi).start()

screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption("Python MIDI Program")

image = pygame.image.load(os.path.join(sys.path[0], "piano.png"))
screen.blit(image, (30, SIZE[1] - 120))

clock = pygame.time.Clock()
while done == False:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    if not paused:
        for i in range(len(note_list)):
            if note_list[i][1] < (SIZE[1]):
                pygame.draw.rect(
                    screen,
                    note_list[i][2],
                    pygame.Rect(
                        note_list[i][0], note_list[i][1] - 150, RECT_SIZE, RECT_SIZE
                    ),
                )
                note_list[i][1] += 1
            elif note_list[i][1] == (SIZE[1]):
                note_list[i][1] += 1
                port.send(note_list[i][3])
                paused = True
        pygame.display.flip()

        for i in range(len(note_list_off)):
            if note_list_off[i][1] < (SIZE[1]):
                pygame.draw.rect(
                    screen,
                    BLACK,
                    pygame.Rect(
                        note_list_off[i][0],
                        note_list_off[i][1] - 150,
                        RECT_SIZE,
                        RECT_SIZE,
                    ),
                )
                note_list_off[i][1] += 1
            elif note_list_off[i][1] == (SIZE[1]):
                note_list_off[i][1] += 1
                port.send(note_list_off[i][2])
    while paused:
        if keyboard.is_pressed("k"):
            paused = False

    clock.tick(200)
pygame.quit()
