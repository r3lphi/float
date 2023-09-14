import pygame
from pygame import time
from States import *

from pygame.constants import SCALED

pygame.init()

pygame.display.set_caption("Float")

surface_size = (360, 640)

surface = pygame.display.set_mode(surface_size, SCALED, vsync=1)

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
    if not pygame.display.is_fullscreen():
        surface = pygame.display.set_mode((0, 0), SCALED, vsync=1)
        return
    
    surface = pygame.display.set_mode(surface_size, SCALED, vsync=1)

while(isRunning):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = 0
        # if event.type == pygame.KEYDOWN:
        #     if event.key == pygame.K_F11:
        #         toggle_fullscreen()


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