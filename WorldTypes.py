import pygame
from typing import Any, Iterable
from pygame.sprite import AbstractGroup, Group, DirtySprite
from pygame import Rect
from AssetsHandler import tile_dict

TILESCREEN_WIDTH = 40
TILESCREEN_HEIGHT = 23

def import_screen(filename):
    tile_data = []

    with open(f"leveldat/{filename}") as f:
        contents = f.read()

        raw_data = contents.replace("\n", "").replace(" ", "").split(",")
        
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
    def __init__(self, coords, use_exported = False) -> None:
        self.file_dir = f"{int(coords[0])}_{int(coords[1])}.txt" if not use_exported else "exported_screen.txt"
        
        super().__init__(import_screen(self.file_dir))

        from Main import SURFACE_SIZE

        self.simplifiedCoords = coords
        self.worldCoords = pygame.Vector2(SURFACE_SIZE[0] * self.simplifiedCoords[0], SURFACE_SIZE[1] * -self.simplifiedCoords[1])

    def draw(self, surface, globalOffset):
        for sprite in self.sprites():
            surface.blit(sprite.image, Rect(
                sprite.rect.x + self.worldCoords.x + globalOffset.x,
                sprite.rect.y + self.worldCoords.y + globalOffset.y,
                sprite.rect.width,
                sprite.rect.height
            ))
        # for sprite in self.sprites():
        #     pygame.draw.rect(surface, "red", sprite.rect, 1)
    def get_at(self, position: pygame.Vector2):
        for sprite in self.sprites():
            if sprite.rect.x == position.x and sprite.rect.y == position.y:
                return sprite
    def reload(self):
        self.empty()
        self.add(import_screen(self.file_dir))

def tile_to_id(sprite):
    inverted_tile_dict = list(tile_dict.values())
    return inverted_tile_dict.index(sprite.image) if sprite else -1

def export_screen(screen: Screen):
    with open('leveldat/exported_screen.txt', 'w') as f:
        for y in range(TILESCREEN_HEIGHT):
            row = ""
            
            for x in range(TILESCREEN_WIDTH):
                tile = screen.get_at(pygame.Vector2(x * 8, y * 8))
                id = tile_to_id(tile)

                row += f"{id},"
            
            f.write(row + "\n")
        
        f.close()
        
