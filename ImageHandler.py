import pygame

def load_image(filename):
    image = pygame.image.load(f"Assets/{filename}").convert()

    return image

def rescale(image, scale):
    return pygame.transform.scale(image, (image.get_size()[0] * scale, image.get_size()[1] * scale))

def scale_with_screen(image, newRes, oldRes):
    sw = newRes[0] / oldRes[0]
    sh = newRes[1] / oldRes[1]

    print((sw, sh))

    return pygame.transform.scale(image, (image.get_size()[0] * sw, image.get_size()[1] * sh))

class Spritesheet:
    def __init__(self, image = None, filename = None):
        self.sheet = image if image else load_image(filename) if filename else pygame.Surface((50, 50))
    def cut(self, rect, scale = 1, colorkey = None):
        image = pygame.Surface(rect.size).convert()
        image.blit(self.sheet, (0, 0), rect)

        if scale != 1:
            image = rescale(image, scale)

        if not colorkey:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, pygame.RLEACCEL)

        return image
