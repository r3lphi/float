import pygame
from enum import Enum

pygame.font.init()

class Fonts(Enum):
    DEFAULT = pygame.font.Font("Assets/Fonts/rainyhearts.ttf", 16)

def draw_text(surface, text, position, font = Fonts.DEFAULT.value, color_fg = (255, 255, 255), color_bg = (128, 128, 128)):
    rendered = font.render(text, True, color_fg, color_bg)
    rect = rendered.get_rect()
    rect.center = position

    surface.blit(rendered, rect)
