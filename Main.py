import pygame
from pygame import time
from States import *
import AssetsHandler

from pygame.constants import SCALED

pygame.init()

pygame.display.set_caption("Float")

SURFACE_SIZE = (320, 180)

surface = pygame.display.set_mode(SURFACE_SIZE, SCALED, vsync=1)

AssetsHandler.Init()

isRunning = 1
clock = pygame.time.Clock()
frame_rate = 60

last_time = time.get_ticks()
dt = 0

states = {
    "GAMEPLAY" : GameplayState()
}

active_state = states["GAMEPLAY"]

def toggle_fullscreen():
    from pygame.constants import FULLSCREEN
    if not pygame.display.is_fullscreen():
        surface = pygame.display.set_mode(SURFACE_SIZE, FULLSCREEN | SCALED, vsync=1)
        return
    
    surface = pygame.display.set_mode(SURFACE_SIZE, SCALED, vsync=1)

while(isRunning):
    events = pygame.event.get()

    for event in events:
        if event.type == pygame.QUIT:
            isRunning = 0
        if event.type == pygame.KEYDOWN:
            match event.key:
                case pygame.K_F11:
                    toggle_fullscreen()

    clock.tick(frame_rate)

    now = time.get_ticks()
    dt = (now - last_time) / 1000
    last_time = now

    active_state.update(dt, events)
    
    # print(clock.get_fps())

    surface.fill("#F3B05A")
    active_state.draw(surface)
    pygame.display.flip()

pygame.quit()