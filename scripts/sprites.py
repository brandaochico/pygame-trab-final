""" Sprites para entidades e animações de entidades """

import pygame

from settings import *

class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(topleft = pos)

class AnimatedSprite(Sprite):
    def __init__(self, frames, pos, groups):
        self.frames, self.frame_index, self.animation_speed = frames, 0, 5
        super().__init__(pos, self.frames[self.frame_index], groups)

    def animate(self, dt):
        self.frame_index += self.animation_speed * dt
        self.image = self.frames[int(self.frame_index) % len(self.frames)]

class Player(AnimatedSprite):
    def __init__(self, pos, groups, collision_sprites, frames):
        super().__init__(frames, pos, groups)

        # Movement & collision
        self.direction = pygame.Vector2()
        self.speed = 150
        self.gravity = 1200
        self.on_floor = False

        self.collision_sprites = collision_sprites

        # Animation
        self.flip = True

    def update(self, dt):
        self.check_floor()
        self.input()
        self.move(dt)
        self.animate(dt)

    def input(self):
        keys = pygame.key.get_pressed()

        self.direction.x = int(keys[pygame.K_RIGHT] or keys[pygame.K_d]) - int(keys[pygame.K_LEFT] or keys[pygame.K_a])

        if keys[pygame.K_SPACE] and self.on_floor:
            self.direction.y = -350

    def move(self, dt):
        self.rect.x += self.direction.x * self.speed * dt
        self.collision('h')

        self.direction.y += self.gravity * dt
        self.rect.y += self.direction.y * dt
        self.collision('v')

    def check_floor(self):
        if self.direction.y >= 0:
            bottom_rect = pygame.FRect((0,0), (self.rect.width, 0.1)).move_to(midtop = self.rect.midbottom)
            level_rects = [sprite.rect for sprite in self.collision_sprites]
            self.on_floor = bottom_rect.collidelist(level_rects) >= 0
        else:
            self.on_floor = False

    def collision(self, direction):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.rect):
                if direction == 'h':
                    if self.direction.x > 0: self.rect.right = sprite.rect.left
                    if self.direction.x < 0: self.rect.left = sprite.rect.right
                if direction == 'v':
                    if self.direction.y > 0: self.rect.bottom = sprite.rect.top
                    if self.direction.y < 0: self.rect.top = sprite.rect.bottom
                    self.direction.y = 0

    def animate(self, dt):
        if self.direction.x:
            self.frame_index += self.animation_speed * dt
            self.flip = self.direction.x > 0
        else: self.frame_index = 0

        self.frame_index = 1 if not self.on_floor else self.frame_index
        self.image = self.frames[int(self.frame_index) % len(self.frames)]
        self.image = pygame.transform.flip(self.image, self.flip, False)

class Bat(AnimatedSprite):
    def __init__(self, frames, pos, groups):
        super().__init__(frames, pos, groups)

    def update(self, dt):
        self.animate(dt)
