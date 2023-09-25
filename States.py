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

        self.simplifiedCoords = pygame.Vector2(0, 0)

        self.primaryScreen = Screen((0, 0), False)
        self.additiveScreen = None

        self.isEditMode = False
        self.isTransitioningScenes = False

        self.globalScreenOffset = pygame.Vector2(0, 0)
        
        self.map_editor = MapEditor(self.primaryScreen)
    
    def begin_scene_transition(self, dif, player_relocation):
        self.simplifiedCoords += dif
        self.additiveScreen = Screen((self.simplifiedCoords.x, self.simplifiedCoords.y), False)

        self.player.position = player_relocation

        self.isTransitioningScenes = True

    def check_screen_transition(self):
        from Main import SURFACE_SIZE

        if self.player.position.y < -self.player.rect.height:
            self.begin_scene_transition(pygame.Vector2(0, 1), pygame.Vector2(self.player.rect.x, SURFACE_SIZE[1]))

        if self.player.position.y > SURFACE_SIZE[1]:
            self.begin_scene_transition(pygame.Vector2(0, -1), pygame.Vector2(self.player.rect.x, -self.player.rect.height))
    
    def update_scene_transition(self, dt):
        from pygame.math import lerp

        target = pygame.Vector2(
            -self.additiveScreen.worldCoords.x if self.additiveScreen.worldCoords.x != 0 else 0,
            -self.additiveScreen.worldCoords.y if self.additiveScreen.worldCoords.y != 0 else 0
        )

        if self.globalScreenOffset.x != target.x or self.globalScreenOffset.y != target.y:
            self.globalScreenOffset.x = lerp(self.globalScreenOffset.x, target.x, 10 * dt) if abs(self.globalScreenOffset.x - target.x) > 0.1 else target.x
            self.globalScreenOffset.y = lerp(self.globalScreenOffset.y, target.y, 10 * dt) if abs(self.globalScreenOffset.y - target.y) > 0.1 else target.y

            return
        
        self.isTransitioningScenes = False

        temp = self.additiveScreen
        self.primaryScreen = temp
        self.additiveScreen = None

        self.map_editor = MapEditor(self.primaryScreen)

    def update(self, dt, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F3:
                    self.isEditMode = not self.isEditMode
        
        if self.isEditMode:
            self.map_editor.update(dt, events)
            return
        
        self.primaryScreen.update(dt, events)
        if self.additiveScreen:
            self.additiveScreen.update(dt, events)
        
        if self.player.isDead:
            return

        if self.player.collisionSubject:
            self.player.isDead = True

            from Entities import Object
            from AssetsHandler import img_dict

            self.deathDummy = Object(img_dict["player_deathfall"], self.player.position)

            self.primaryScreen.add(self.deathDummy)
            return
        
        self.player.update(dt, events)

        if self.isTransitioningScenes:
            self.update_scene_transition(dt)

            return

        self.check_screen_transition()

        # Collision
        for tile in self.primaryScreen.sprites():
            if pygame.sprite.collide_rect(tile, self.player):
                self.player.collisionSubject = tile
                return
            
        self.player.collisionSubject = None
    
    def draw(self, surface):
        self.primaryScreen.draw(surface, self.globalScreenOffset)
        if self.additiveScreen:
            self.additiveScreen.draw(surface, self.globalScreenOffset)

        if self.isEditMode:
            self.map_editor.render(surface)
            return

        if self.player.isDead:
            return

        self.player.draw(surface)

        from TextRenderer import draw_text

        draw_text(surface, "COLLIDING" if self.player.collisionSubject else "NOT COLLIDING", pygame.Vector2(60, 10))