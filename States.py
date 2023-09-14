import pygame
from Entities import Player

class State:
    def __init__(self):
        pass
    def update(dt):
        pass
    def draw(surface):
        pass

class GameplayState(State):
    def __init__(self):
        super().__init__()

        self.player = Player()

        import World
        World.import_screen(coords=(0, 0))

    def update(self, dt):
        self.player.update(dt)
    
    def draw(self, surface):
        self.player.draw(surface)
    