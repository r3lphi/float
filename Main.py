import pygame
from pygame import time
from States import *
import AssetsHandler
import KeyHandler

from pygame.constants import SCALED

pygame.init()

pygame.display.set_caption("Float")

SURFACE_SIZE = (640, 360)

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
    KeyHandler.update()

    if KeyHandler.check(pygame.K_F11):
        toggle_fullscreen()

    clock.tick(frame_rate)

    now = time.get_ticks()
    dt = (now - last_time) / 1000
    last_time = now

    active_state.update(dt)

    # print(clock.get_fps())

    surface.fill("cyan")
    active_state.draw(surface)
    pygame.display.flip()

pygame.quit()