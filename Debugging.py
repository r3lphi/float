import pygame
from AdvancedRendering import draw_text
from WorldTypes import create_tile
from AssetsHandler import tile_dict
from pygame.sprite import DirtySprite

class GhostTile:
    def __init__(self, id, position = pygame.Vector2(0, 0)):
        self.id = id
        self.position = position

class MapEditor:
    def __init__(self, currentScreen):
        self.screen = currentScreen
        self.ghostTile = None
        self.lastDirection = None
    def update(self, dt, events):
        for event in events:
            if event.type != pygame.KEYDOWN:
                return
            if event.key == pygame.K_n:
                self.ghostTile = GhostTile(0)
            if event.key == pygame.K_ESCAPE:
                self.ghostTile = None
            if event.key == pygame.K_RETURN and self.ghostTile:
                tile = DirtySprite()
                tile.image = tile_dict[self.ghostTile.id]
                tile.rect = pygame.Rect(self.ghostTile.position, (8, 8))

                self.screen.add(tile)

                self.ghostTile.position += self.lastDirection
            if event.key == pygame.K_UP and self.ghostTile:
                self.ghostTile.position.y -= 8
                self.lastDirection = pygame.Vector2(0, -8)
            if event.key == pygame.K_DOWN and self.ghostTile:
                self.ghostTile.position.y += 8
                self.lastDirection = pygame.Vector2(0, 8)
            if event.key == pygame.K_LEFT and self.ghostTile:
                self.ghostTile.position.x -= 8
                self.lastDirection = pygame.Vector2(-8, 0)
            if event.key == pygame.K_RIGHT and self.ghostTile:
                self.ghostTile.position.x += 8
                self.lastDirection = pygame.Vector2(8, 0)

    def render(self, surface):
        from Main import SURFACE_SIZE

        draw_text(surface, "EDIT MODE", (SURFACE_SIZE[0] - 50, 20))
        draw_text(surface, str(self.ghostTile), (SURFACE_SIZE[0] - 50, 40))

        if not self.ghostTile:
            return
        
        surface.blit(tile_dict[self.ghostTile.id], self.ghostTile.position)
        pygame.draw.rect(surface, "red", pygame.Rect(self.ghostTile.position, (8, 8)), 1)
