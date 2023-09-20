import pygame
from typing import Any, Iterable
from pygame.sprite import AbstractGroup, Group, DirtySprite
from pygame import Rect
from AssetsHandler import tile_dict

TILESCREEN_WIDTH = 40
TILESCREEN_HEIGHT = 23

def import_screen(coords: tuple):
        tile_data = []

        with open(f'leveldat/{coords[0]}_{coords[1]}.txt') as f:
            contents = f.read()

            raw_data = contents.replace("\n", "").split(",")
            
            for y in range(TILESCREEN_HEIGHT):
                for x in range(TILESCREEN_WIDTH):
                    id = raw_data[TILESCREEN_WIDTH * y + x]
                    if not id.lstrip("-").isnumeric() or id == "-1":
                        continue

                    tile = DirtySprite()
                    tile.image = tile_dict[int(id)]
                    tile.rect = Rect(x * 8, y * 8, 8, 8)

                    tile_data.append(tile)

            return tile_data

def create_tile(id, tiledPosition = pygame.Vector2(0, 0)):
    tile = DirtySprite()
    tile.image = tile_dict[int(id)]
    tile.rect = Rect(tiledPosition.x * 8, tiledPosition.y * 8, 8, 8)

    return tile

class Screen(Group):
    def __init__(self, world_coords) -> None:
        super().__init__(import_screen(world_coords))

        self.world_coords = world_coords
    def draw(self, surface):
        super().draw(surface)
        # for sprite in self.sprites():
        #     pygame.draw.rect(surface, "red", sprite.rect, 1)
    def get_at(self, coords: tuple):
        for sprite in self.sprites():
            print(sprite.rect)

def export_screen(screen : Screen):
    for y in range(TILESCREEN_HEIGHT):
        row = ""

        for x in range(TILESCREEN_WIDTH):
            tile = screen.get_at((x * 8, y * 8))

            if not tile:
                row += "0,"
                continue

            row += f"{list(tile_dict.values()).index(tile.image)},"
        
        print(row)


