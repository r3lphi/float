import pygame
from TextRenderer import draw_text
from WorldTypes import create_tile
from AssetsHandler import tile_dict
from pygame.sprite import DirtySprite

class GhostTile:
    def __init__(self, id, position = pygame.Vector2(0, 0)):
        self.id = id
        self.position = position
        self.lastMovedBy = pygame.Vector2(0, 0)
        self.highlightColor = "blue"
    def move(self, move_by, screen):
        self.position += move_by
        self.lastMovedBy = move_by

        self.highlightColor = "red" if screen.get_at(self.position) else "blue"

class MapEditor:
    def __init__(self, currentScreen):
        self.screen = currentScreen
        self.ghostTile = None
    def update(self, dt, events):
        for event in events:
            if event.type != pygame.KEYDOWN:
                return
            if event.key == pygame.K_n:
                self.ghostTile = GhostTile(0)
            if event.key == pygame.K_ESCAPE:
                self.ghostTile = None
            if event.key == pygame.K_RETURN and self.ghostTile and not self.screen.get_at(self.ghostTile.position):
                tile = DirtySprite()
                tile.image = tile_dict[self.ghostTile.id]
                tile.rect = pygame.Rect(self.ghostTile.position, (8, 8))

                self.screen.add(tile)

                self.ghostTile.move(self.ghostTile.lastMovedBy, self.screen)
            
            if event.key == pygame.K_F4:
                self.screen.reload()
            if event.key == pygame.K_F7:
                from WorldTypes import export_screen
                export_screen(self.screen)
            
            if not self.ghostTile:
                return
            
            match event.key:
                case pygame.K_UP:
                    self.ghostTile.move(pygame.Vector2(0, -8), self.screen)
                case pygame.K_DOWN:
                    self.ghostTile.move(pygame.Vector2(0, 8), self.screen)
                case pygame.K_LEFT:
                    self.ghostTile.move(pygame.Vector2(-8, 0), self.screen)
                case pygame.K_RIGHT:
                    self.ghostTile.move(pygame.Vector2(8, 0), self.screen)
    def render(self, surface):
        from Main import SURFACE_SIZE

        draw_text(surface, "EDIT MODE", (SURFACE_SIZE[0] - 50, 20))
        draw_text(surface, str(self.ghostTile.id if self.ghostTile else "None"), (SURFACE_SIZE[0] - 50, 40))

        if not self.ghostTile:
            return
        
        surface.blit(tile_dict[self.ghostTile.id], self.ghostTile.position)
        pygame.draw.rect(surface, self.ghostTile.highlightColor, pygame.Rect(self.ghostTile.position, (8, 8)), 1)
