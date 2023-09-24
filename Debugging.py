import pygame
from TextRenderer import draw_text
from WorldTypes import create_tile
from AssetsHandler import tile_dict
from pygame.sprite import DirtySprite

class Selector:
    def __init__(self, id, position = pygame.Vector2(0, 0)):
        self.id = id
        self.position = position
        self.lastMovedBy = pygame.Vector2(0, 0)
        self.highlightColor = "blue"
    def move(self, move_by, screen):
        from Main import SURFACE_SIZE

        futurePos = self.position + move_by
        
        if (futurePos.x < 0 or futurePos.x >= SURFACE_SIZE[0]) or (futurePos.y < 0 or futurePos.y > SURFACE_SIZE[1]):
            return

        self.position = futurePos
        self.lastMovedBy = move_by

        self.highlightColor = "red" if screen.get_at(self.position) else "blue"

class MapEditor:
    def __init__(self, currentScreen):
        self.screen = currentScreen
        self.selector = Selector(-1)
    def update(self, dt, events):
        for event in events:
            if event.type != pygame.KEYDOWN:
                return
            if event.key == pygame.K_n:
                self.selector.id = 0
            if event.key == pygame.K_ESCAPE:
                self.selector.id = -1
            if event.key == pygame.K_RETURN and self.selector.id >= 0 and not self.screen.get_at(self.selector.position):
                tile = DirtySprite()
                tile.image = tile_dict[self.selector.id]
                tile.rect = pygame.Rect(self.selector.position, (8, 8))

                self.screen.add(tile)

                self.selector.move(self.selector.lastMovedBy, self.screen)
            
            if event.key == pygame.K_F4:
                self.screen.reload()
            if event.key == pygame.K_F7:
                from WorldTypes import export_screen
                export_screen(self.screen)
            if event.key == pygame.K_SPACE:
                if self.selector.id >= 0:
                    self.selector.id = (self.selector.id + 1) % len(tile_dict)
            if event.key == pygame.K_F9:
                self.screen.empty()
            
            match event.key:
                case pygame.K_UP:
                    self.selector.move(pygame.Vector2(0, -8), self.screen)
                case pygame.K_DOWN:
                    self.selector.move(pygame.Vector2(0, 8), self.screen)
                case pygame.K_LEFT:
                    self.selector.move(pygame.Vector2(-8, 0), self.screen)
                case pygame.K_RIGHT:
                    self.selector.move(pygame.Vector2(8, 0), self.screen)
                case pygame.K_d:
                    selectedSpace = self.screen.get_at(self.selector.position)
                    
                    if selectedSpace:
                        self.screen.remove(selectedSpace)

    def render(self, surface):
        from Main import SURFACE_SIZE

        draw_text(surface, "EDIT MODE", (SURFACE_SIZE[0] - 50, 20))
        draw_text(surface, str(self.selector.id if self.selector else "None"), (SURFACE_SIZE[0] - 50, 40))

        if self.selector.id >= 0:
            surface.blit(tile_dict[self.selector.id], self.selector.position)
        pygame.draw.rect(surface, self.selector.highlightColor, pygame.Rect(self.selector.position, (8, 8)), 1)
