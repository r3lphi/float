import pygame
from collections import defaultdict

keys = defaultdict()

def update():
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            keys[event.key.key_code] = 1
        if event.type == pygame.KEYUP:
            keys[event.key.key_code] = 0
        
def check(key):
    return keys[key]