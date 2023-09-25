import pygame
from Entities import Player
from WorldTypes import Screen
from Debugging import MapEditor

class State:
    def __init__(self):
        pass
    def update(dt, events):
        pass
    def draw(surface):
        pass

class GameplayState(State):
    def __init__(self):
        super().__init__()

        self.player = Player()
        self.screens = {}

        import os
        for file in os.scandir('leveldat'):
            coords = file.name.split("_")
            coords[1] = coords[1].replace(".txt", "")

            x = int(coords[0])
            y = int(coords[1])

            self.screens[(x, y)] = Screen((x, y))
        
        from Entities import Camera
        self.camera = Camera(pygame.Vector2(0, 0), 3)

        self.isEditMode = False

    def update(self, dt, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F3:
                    self.isEditMode = not self.isEditMode
        
        self.camera.update(dt, self.player.position)
        
        if self.player.isDead:
            return

        if self.player.collisionSubject:
            self.player.isDead = True

            from Entities import Object
            from AssetsHandler import img_dict

            self.deathDummy = Object(img_dict["player_deathfall"], self.player.position)
            return
        
        self.player.update(dt, events)
    
    def draw(self, surface):
        for x in range(int(self.player.coordinates.x - 1), int(self.player.coordinates.x + 1)):
            for y in range(int(self.player.coordinates.y - 1), int(self.player.coordinates.y + 1)):
                if not self.screens.get((x, y)):
                    continue

                self.screens[(x, y)].draw(surface, self.camera.position)

        if self.player.isDead:
            return

        self.player.draw(surface)

        from TextRenderer import draw_text

        draw_text(surface, "COLLIDING" if self.player.collisionSubject else "NOT COLLIDING", pygame.Vector2(60, 10))