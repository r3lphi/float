import pygame
from pygame.sprite import Sprite
from ImageHandler import Spritesheet
from pygame import Rect

img_dict = {}
tile_dict = {}

def Init():
    global img_dict

    sheet_player = Spritesheet(filename="player.png")

    img_dict["player_idle_0"] = sheet_player.cut(Rect(0, 0, 16, 16))
    img_dict["player_idle_1"] = sheet_player.cut(Rect(16, 0, 16, 16))

    img_dict["player_deathfall"] = sheet_player.cut(Rect(32, 0, 16, 16))

    sheet_tiles = Spritesheet(filename="tiles.png")
    
    img_dict["rock"] = sheet_tiles.cut(Rect(0, 0, 8, 8), colorkey=None)
    tile_dict[0] = img_dict["rock"]

    img_dict["steel"] = sheet_tiles.cut(Rect(8, 0, 8, 8), colorkey=None)
    tile_dict[1] = img_dict["steel"]

    img_dict["cliff_flat"] = sheet_tiles.cut(Rect(16, 0, 8, 8), colorkey=None)
    tile_dict[2] = img_dict["cliff_flat"]

    img_dict["cliff_side"] = sheet_tiles.cut(Rect(24, 0, 8, 8), colorkey=None)
    tile_dict[3] = img_dict["cliff_side"]

    img_dict["cliff_corner"] = sheet_tiles.cut(Rect(0, 8, 8, 8), colorkey=None)
    tile_dict[4] = img_dict["cliff_corner"]
