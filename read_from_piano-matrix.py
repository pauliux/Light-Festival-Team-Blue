import pygame
import mido
import rtmidi
from led_matrix import led_matrix

pygame.init()

BLACK = [  0,   0,   0]
WHITE = [255, 255, 255]
note_list = []
note_list_off = []

# outport=mido.open_output()
inputs = mido.get_input_names()
print(inputs)
rows = 30
columns = 65
led_matrix = led_matrix(rows = rows, columns = columns, led_size = 10)

inport=mido.open_input()
led_matrix.readFromPiano(inport = inport, rows = rows, delay = 0.02)
