from typing import Iterable, Union
import pygame
from pygame.sprite import AbstractGroup, Group, Sprite
from pygame.rect import Rect
from pygame.math import clamp
from ImageHandler import Spritesheet
from AssetsHandler import img_dict

class AnimationFrame():
    def __init__(self, image, length):
        self.image = image
        self.length = length

class Animation():
    def __init__(self, frames: []):
        self.frames = frames

class AnimableSprite(Sprite):
    def __init__(self, starting_animation = None, *groups: Group) -> None:
        super().__init__(*groups)

        self.animation = starting_animation
        self.timer = 0
        self.frame_index = 0

        if starting_animation:
            self.image = starting_animation.frames[0].image
            self.rect = self.image.get_rect()
    
    def update(self, dt):
        if not self.animation:
            return

        self.timer += 1 * dt

        if self.timer >= self.animation.frames[self.frame_index].length:
            self.frame_index = (self.frame_index + 1) % len(self.animation.frames)
            self.timer = 0
        
        self.image = self.animation.frames[self.frame_index].image
    def change_anim(self, newAnim):
        if self.animation == newAnim:
            return

        self.timer = 0
        self.frame_index = 0

        self.animation = newAnim

class Object(Sprite):
    def __init__(self, sprite, position = pygame.Vector2(0, 0)):
        super().__init__()

        self.image = sprite
        self.rect = self.image.get_rect()

        self.position = position
        self.velocity = pygame.Vector2(0, 0)
        
        self.rect.x = self.position.x
        self.rect.y = self.position.y
    
    def update(self, dt, events):
        self.velocity.y += 9.81 * dt
        self.position.y += self.velocity.y
        self.rect.y = round(self.position.y)

class Player(Group):
    def __init__(self, starting_pos = pygame.Vector2(0, 0)):
        self.rect = Rect(starting_pos, (16, 16))

        self.a_idle = Animation([
            AnimationFrame(img_dict["player_idle_0"], 0.5),
            AnimationFrame(img_dict["player_idle_1"], 0.5)
        ])
        self.a_fall = Animation([
            AnimationFrame(img_dict["player_deathfall"], 60)
        ])

        self.s_charcacter = AnimableSprite(self.a_idle)

        super().__init__([self.s_charcacter])

        self.moveSpeed = 5

        self.riseSpeed = -0.5
        self.fallSpeed = 9.81

        from Main import SURFACE_SIZE
        self.position = starting_pos if starting_pos != pygame.Vector2(0, 0) else pygame.Vector2(
            (SURFACE_SIZE[0] / 2) - (self.rect.width / 2),
            SURFACE_SIZE[1] - self.rect.height * 2
        )

        self.velocity = pygame.Vector2(0, 0)

        self.lastDirection = 0

        self.noRiseBuffer = 0

        self.collisionSubject = None

        self.isDead = False

    def get_direction(self, keys):
        if keys[pygame.K_d]:
            return 1
        if keys[pygame.K_a]:
            return -1
        return 0
    
    def update(self, dt, events):
        keys = pygame.key.get_pressed()

        direction = self.get_direction(keys)
        directionChanged = 0

        if direction != 0:
            if (self.lastDirection == 0 and direction != 1) or (self.lastDirection != 0 and direction != self.lastDirection):
                directionChanged = 1
            self.lastDirection = direction

        frame_velocity = pygame.Vector2(self.moveSpeed * direction * dt, self.velocity.y)
        
        if keys[pygame.K_s]:
            self.velocity.x = pygame.math.lerp(self.velocity.x, 0, 3 * dt)
        else:
            self.velocity.x += frame_velocity.x
        
        if keys[pygame.K_w]:
            self.s_charcacter.change_anim(self.a_fall)

            frame_velocity.y += self.fallSpeed * dt
        else:
            self.s_charcacter.change_anim(self.a_idle)

            frame_velocity.y = pygame.math.lerp(frame_velocity.y, self.riseSpeed, 5 * dt)

        # for event in events:
        #     if event.type != pygame.KEYDOWN:
        #         continue
        #     if event.key == pygame.K_w:
        #         self.velocity.x = (2 * self.moveSpeed) * -(self.velocity.x / abs(self.velocity.x)) if self.velocity.x != 0 else 0

        self.velocity.y = frame_velocity.y if self.noRiseBuffer == 0 else 0

        self.position += self.velocity

        self.rect.x = round(self.position.x)
        self.rect.y = round(self.position.y)

        if self.noRiseBuffer > 0:
            self.noRiseBuffer = pygame.math.clamp(self.noRiseBuffer - (1 * dt), 0, 100)
        
        for sprite in self.sprites():
            from Main import SURFACE_SIZE
            sprite.rect.x = self.rect.x
            sprite.rect.y = self.rect.y

            # if directionChanged:
            #     sprite.image = pygame.transform.flip(sprite.image, True, False)
            
            sprite.update(dt)

    def draw(self, surface):
        for sprite in self.sprites():
            surface.blit(sprite.image, sprite.rect)
        for y in range(4):
            pygame.draw.rect(surface, "black", Rect(self.s_charcacter.rect.x + 10, self.s_charcacter.rect.y + 14 + y, 1, 1))