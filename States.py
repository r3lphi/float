import pygame
from Entities import Player
from WorldTypes import Screen

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

        # world = World()

        # self.screen = Screen((0, 0))

    def update(self, dt):
        self.player.update(dt)
    
    def draw(self, surface):
        self.player.draw(surface)