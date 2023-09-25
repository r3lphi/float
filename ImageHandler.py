import pygame

def load_image(filename):
    image = pygame.image.load(f"Assets/{filename}").convert()

    return image

class Spritesheet:
    def __init__(self, image = None, filename = None):
        self.sheet = image if image else load_image(filename) if filename else pygame.Surface((50, 50))
    def cut(self, rect, scale = 1, colorkey = -1):
        image = pygame.Surface(rect.size).convert()
        image.blit(self.sheet, (0, 0), rect)

        if scale != 1:
            image = pygame.transform.scale(image, (image.get_width() * scale, image.get_height() * scale))

        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, pygame.RLEACCEL)

        return image
