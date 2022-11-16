# https://realpython.com/pygame-a-primer/

import pygame
import time
import random

from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

pygame.init()

WIDTH, HEIGHT = 500, 800

screen = pygame.display.set_mode((WIDTH, HEIGHT))

class Player(pygame.sprite.Sprite):
    def __init__(self, size):
        super(Player, self).__init__()
        self.surface = pygame.image.load('Birb.png')
        self.surface.set_colorkey((255, 255, 255), RLEACCEL)
        self.surface = pygame.transform.scale(self.surface, (size, size))
        self.rect = self.surface.get_rect()
        self.rect.move_ip((WIDTH / 2, HEIGHT - 20))
        self.flipped = False
        self.lsurface = pygame.transform.flip(self.surface, True, False)

    def move(self, screen, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
            self.flipped = True
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)
            self.flipped = False
            
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

        if self.flipped:
            screen.blit(self.lsurface, self.rect)
        else:
            screen.blit(self.surface, self.rect)


class Invader(pygame.sprite.Sprite):
    def __init__(self):
        super(Invader, self).__init__()
        self.surface = pygame.image.load("Invader.jpg")
        self.surface.set_colorkey((255, 255, 255), RLEACCEL)
        self.surface = pygame.transform.rotate(self.surface, 270)
        self.surface = pygame.transform.scale(self.surface, (25, 75))
        self.rect = self.surface.get_rect()
        self.speed = random.randint(2, 10)
        self.rect.move_ip((random.randint(0, WIDTH), 0))
        self.hitbox = self.rect

    def move(self, screen, pressed_keys):
        self.rect.move_ip((0, self.speed))
        self.hitsurf = pygame.Surface((25, 50))
        self.hitsurf.fill((40, 123, 75))
        self.hitbox = self.hitsurf.get_rect().move((self.rect.topleft[0], self.rect.topleft[1] + 25))
        print(self.rect, self.hitbox)
        screen.blit(self.surface, self.rect)
        
    
      
player = Player(75)
white = (255, 255, 255)

n_invaders = 10
all_sprites = pygame.sprite.Group(player)
for i in range(n_invaders):
    all_sprites.add(Invader())

for i in reversed(range(1, 3)):
    time.sleep(1)
    print(i)

running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    invader_group = pygame.sprite.Group.copy(all_sprites)
    pygame.sprite.Group.remove(invader_group, player)
    
    for invader in invader_group:
        if player.rect.colliderect(invader.hitbox):
            running = False
    
    pressed_keys = pygame.key.get_pressed()

    clock = pygame.time.Clock()
    clock.tick(50)


    
    screen.fill(white)
    for sprite in all_sprites:
        if sprite.rect[1] > HEIGHT:
            sprite.kill()
            all_sprites.add(Invader())
        sprite.move(screen, pressed_keys)
    pygame.display.flip()
            