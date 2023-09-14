import pygame
from ImageHandler import Spritesheet

class Player():
    def __init__(self, position = pygame.Vector2(0, 0)):
        self.sheet = Spritesheet(filename="player.png")

        from Main import surface

        self.images = [
            self.sheet.cut(pygame.Rect(0, 0, 16, 16), 2),
            self.sheet.cut(pygame.Rect(0, 16, 16, 16), 2)
        ]

        self.rect = pygame.Rect((0, 0), self.images[0].get_rect().size)
        self.rect.center = (
            surface.get_rect().centerx - (self.images[0].get_rect().width / 2),
            surface.get_rect().centery - (self.images[0].get_rect().height / 2)
        )

        self.position = pygame.Vector2(self.rect.topleft)

        self.moveSpeed = 200

    def get_input_direction(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_d]:
            return 1
        if keys[pygame.K_a]:
            return -1
        
        return 0

    def update(self, dt):
        keys = pygame.key.get_pressed()
        input_direction = self.get_input_direction()

        self.position.x += self.moveSpeed * input_direction * dt
        self.rect.x = round(self.position.x)

    def draw(self, surface):
        for image in self.images:
            surface.blit(image, self.rect)