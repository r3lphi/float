import pygame
from AdvancedRendering import draw_text
from WorldTypes import create_tile

class MapEditor:
    def __init__(self, currentScreen):
        self.screen = currentScreen
    def update(self, dt):
        for event in pygame.event.get():
            if event.type != pygame.KEYDOWN:
                return
            if event.key == pygame.K_n:
                print("Hey")
                self.screen.add(create_tile(0))
    def render(self, surface):
        from Main import SURFACE_SIZE

        draw_text(surface, "EDIT MODE", (SURFACE_SIZE[0] - 50, 20))