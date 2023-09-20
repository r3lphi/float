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
    def __init__(self, world_coords, use_exported = False) -> None:
        self.file_dir = f"{world_coords[0]}_{world_coords[1]}.txt" if not use_exported else "exported_screen.txt"
        
        super().__init__(import_screen(self.file_dir))

        self.world_coords = world_coords
    def draw(self, surface):
        super().draw(surface)
        # for sprite in self.sprites():
        #     pygame.draw.rect(surface, "red", sprite.rect, 1)
    def get_at(self, position: pygame.Vector2):
        for sprite in self.sprites():
            if sprite.rect.x == position.x and sprite.rect.y == position.y:
                return sprite
    def reload(self):
        self.empty()
        self.add(import_screen(self.file_dir))

def export_screen(screen: Screen):
    with open('leveldat/exported_screen.txt', 'w') as f:
        inverted_tile_dict = list(tile_dict.values())

        for y in range(TILESCREEN_HEIGHT):
            row = ""
            
            for x in range(TILESCREEN_WIDTH):
                tile = screen.get_at(pygame.Vector2(x * 8, y * 8))
                id = inverted_tile_dict.index(tile.image) if tile else -1

                row += f"{id},"
            
            f.write(row + "\n")
        
        f.close()
        
