import pygame

class Fader:
    def __init(self):
        self.isFading = False
        self.alpha = 0

        from Main import SURFACE_SIZE

        self.veil = pygame.Surface(SURFACE_SIZE)
        self.veil.fill("black")

        self.speed = 0
        self.hangTime = 0
    
    def activate(self, speed, hangTime):
        self.speed = speed
        self.hangTime = hangTime

        self.isFading = True

    def update(self, dt):
        if not self.isFading:
            return
        
        if self.alpha < 255:
            self.alpha += self.speed * dt

    def draw(self, surface):
        self.veil.set_alpha(round(self.alpha))
        surface.blit(self.veil, (0, 0))