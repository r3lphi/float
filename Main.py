import pygame
from States import *

pygame.init()

pygame.display.set_caption("Float")

surface_size = (1280, 720)
surface = pygame.display.set_mode(surface_size)

isRunning = 1
clock = pygame.time.Clock()
frame_rate = 60

dt = 0

states = {
    "GAMEPLAY" : GameplayState()
}

active_state = states["GAMEPLAY"]

def toggle_fullscreen():
    if not pygame.display.is_fullscreen():
        from pygame.locals import FULLSCREEN, DOUBLEBUF
        surface = pygame.display.set_mode((0, 0), FULLSCREEN | DOUBLEBUF)
        return
    
    surface = pygame.display.set_mode(surface_size)

while(isRunning):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = 0
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F11:
                toggle_fullscreen()
    
    dt = clock.tick(frame_rate) * 0.001
    # print(clock.get_fps())

    active_state.update(dt)

    surface.fill("cyan")
    active_state.draw(surface)
    pygame.display.flip()

pygame.quit()