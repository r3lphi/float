import pygame

class EventHandler:
    def __init__(self):
        self.events = pygame.event.get()
    def update(self):
        self.event = pygame.event.get()