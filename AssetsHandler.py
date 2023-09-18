import pygame
from pygame.sprite import Sprite
from ImageHandler import Spritesheet
from pygame import Rect

img_dict = {}
tile_dict = {}

def Init():
    global img_dict

    sheet_player = Spritesheet(filename="player.png")

    img_dict["player_char_idle_0"] = sheet_player.cut(Rect(0, 0, 16, 16))
    img_dict["player_char_idle_1"] = sheet_player.cut(Rect(16, 0, 16, 16))
    img_dict["player_balloon_idle_0"] = sheet_player.cut(Rect(0, 16, 16, 16))
    img_dict["player_balloon_idle_1"] = sheet_player.cut(Rect(16, 16, 16, 16))
    img_dict["player_balloon_idle_2"] = sheet_player.cut(Rect(32, 16, 16, 16))

    sheet_tiles = Spritesheet(filename="tiles.png")
    
    img_dict["rock"] = sheet_tiles.cut(Rect(0, 0, 8, 8), colorkey=None)
    tile_dict[0] = img_dict["rock"]
