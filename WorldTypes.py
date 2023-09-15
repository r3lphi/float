import pygame
from pygame.sprite import Group, Sprite
from pygame import Rect
from ImageHandler import Spritesheet

def import_screen(coords: tuple):
        with open(f'leveldat/{coords[0]}_{coords[1]}.txt') as f:
            contents = f.read()
            
            tile_data = []

            x = 0
            y = 0

            for char in contents:
                if char == "\n":
                    y += 1
                    continue
                if char == ",":
                    x += 1
                    continue
                if char.isspace():
                    continue
                tile = Sprite()
                tile.image = TilesDict[int(char)]
                tile.rect = Rect(x * 8, y * 8, 8, 8)

                tile_data.append(tile)
            
            return tile_data

class Screen(Group):
    def __init__(self, world_coords):
        self.add(import_screen(world_coords))

