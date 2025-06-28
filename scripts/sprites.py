""" Sprites para entidades e animações de entidades """

import pygame
from settings import *
from math import sin
from random import randint

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

class Enemy(AnimatedSprite):
    def __init__(self, frames, pos, groups):
        super().__init__(frames, pos, groups)

    def update(self, dt):
        self.move(dt)
        self.animate(dt)
        self.constraint()

class Player(AnimatedSprite):
    def __init__(self, pos, groups, collision_sprites, stairs_sprites, collectable_sprites, frames):
        super().__init__(frames, pos, groups)

        # Movement & collision
        self.direction = pygame.Vector2()
        self.speed = 150
        self.gravity = 1200
        self.on_floor = False

        self.collision_sprites = collision_sprites
        self.stairs_sprites = stairs_sprites
        self.on_stairs = False
        self.collectable_sprites = collectable_sprites
        self.won = False

        # Animation
        self.flip = True

    def update(self, dt):
        self.check_floor()
        self.check_stairs()
        self.check_collectable()
        self.input()
        self.move(dt)
        self.animate(dt)

    def input(self):
        keys = pygame.key.get_pressed()

        self.direction.x = int(keys[pygame.K_RIGHT] or keys[pygame.K_d]) - int(keys[pygame.K_LEFT] or keys[pygame.K_a])

        if self.on_stairs:
            if keys[pygame.K_w] or keys[pygame.K_UP]:
                self.direction.y = -150
            elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
                self.direction.y = 150
            else:
                self.direction.y = 0
        else:
            if keys[pygame.K_SPACE] and self.on_floor:
                self.direction.y = -350

    def move(self, dt):
        self.rect.x += self.direction.x * self.speed * dt
        self.collision('h')

        if not self.on_stairs:
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

    def check_stairs(self):
        self.on_stairs = any(sprite.rect.colliderect(self.rect) for sprite in self.stairs_sprites)

    def check_collectable(self):
        collided = pygame.sprite.spritecollideany(self, self.collectable_sprites)
        if collided:
            collided.kill()
            self.won = True

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

class Bat(Enemy):
    def __init__(self, frames, pos, groups, speed):
        super().__init__(frames, pos, groups)
        self.speed = speed
        self.amplitude = randint(200, 450)
        self.frequency = randint(300, 600)

    def move(self, dt):
        self.rect.x -=  self.speed * dt
        self.rect.y += sin(pygame.time.get_ticks() / self.frequency) * self.amplitude * dt

    def constraint(self):
        if self.rect.x <= 0: self.kill()
