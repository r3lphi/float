from typing import Iterable, Union
import pygame
from pygame.sprite import Group, Sprite
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
        print("Updating!")
        if not self.animation:
            return
        
        print("Tick!")

        self.timer += 1 * dt

        if self.timer >= self.animation.frames[self.frame_index].length:
            self.frame_index += 1
            self.timer = 0
        
        self.image = self.animation.frames[self.frame_index]

class Player(Group):
    def __init__(self, starting_pos = pygame.Vector2(0, 0)):
        self.rect = Rect(starting_pos, (16, 16))

        a_char_bob = Animation([
            AnimationFrame(img_dict["player_char_idle_0"], 0.5),
            AnimationFrame(img_dict["player_char_idle_1"], 0.5)
        ])

        self.s_char = AnimableSprite(a_char_bob)

        self.s_balloon = AnimableSprite()
        self.s_balloon.image = img_dict["player_balloon_idle_0"]
        self.s_balloon.rect = self.s_balloon.image.get_rect()

        super().__init__([self.s_char, self.s_balloon])

        self.moveSpeed = 10

        from Main import SURFACE_SIZE
        self.position = starting_pos if starting_pos != pygame.Vector2(0, 0) else pygame.Vector2(
            (SURFACE_SIZE[0] / 2) - (self.rect.width / 2),
            SURFACE_SIZE[1] - self.rect.height * 2
        )

        self.velocity = pygame.Vector2(0, 0)

        self.lastDirection = 0

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

        frame_velocity = self.moveSpeed * direction * dt
        
        if keys[pygame.K_s]:
            self.velocity.x = pygame.math.lerp(self.velocity.x, 0, 2 * dt)
        else:
            self.velocity.x += frame_velocity

        if keys[pygame.K_w]:
            self.velocity.x = 2 * -self.lastDirection

        self.position.x += self.velocity.x
        self.rect.x = round(self.position.x)
        self.rect.y = round(self.position.y)
        
        for sprite in self.sprites():
            sprite.rect.x = self.rect.x
            sprite.rect.y = self.rect.y

            if directionChanged:
                sprite.image = pygame.transform.flip(sprite.image, True, False)