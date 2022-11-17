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

pygame.mixer.init()
pygame.init()

pygame.mixer.music.load("Mercury.mp3")
pygame.mixer.music.set_volume(0.125)
pygame.mixer.music.play(loops=-1)

WIDTH, HEIGHT = 500, 800

screen = pygame.display.set_mode((WIDTH, HEIGHT))

class Player(pygame.sprite.Sprite):
    def __init__(self, size):
        super(Player, self).__init__()
        self.ID = 'player'
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
        self.ID = 'invader'
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
        self.hitsurf = pygame.Surface((25, 40))
        self.hitsurf.fill((40, 123, 75))
        self.hitbox = self.hitsurf.get_rect().move((self.rect[0], self.rect[1] + 25))
        screen.blit(self.surface, self.rect)
        

class Egg(pygame.sprite.Sprite):
    def __init__(self):
        super(Egg, self).__init__()
        self.ID = 'egg'
        self.surface = pygame.transform.rotate(pygame.image.load("egg.jpeg"), 90)
        self.surface.set_colorkey((255, 255, 255), RLEACCEL)
        self.surface = pygame.transform.rotate(self.surface, 270)
        self.surface = pygame.transform.scale(self.surface, (50, 75))
        self.rect = self.surface.get_rect()
        self.speed = random.randint(2, 10)
        self.rect.move_ip((random.randint(0, WIDTH), 0))

    def move(self, screen, pressed_keys):
        self.rect.move_ip((0, self.speed))
        screen.blit(self.surface, self.rect)

class Cracked_Egg(pygame.sprite.Sprite):
    def __init__(self, xcoord):
        super(Cracked_Egg, self).__init__()
        self.ID = 'cracked_egg'
        self.surface = pygame.transform.scale(pygame.image.load("cracked_egg.jpeg"), (50, 50))
        self.surface.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surface.get_rect().move((xcoord, HEIGHT - 40))
        self.createtime = time.time()

player = Player(75)
white = (255, 255, 255)

n_invaders = 8
invader_group = pygame.sprite.Group()
for i in range(n_invaders):
    invader_group.add(Invader())
all_sprites = pygame.sprite.Group(player, invader_group)
egg_group = pygame.sprite.Group()

nice = pygame.mixer.Sound('nioce.mp3')
crack_sound = pygame.mixer.Sound('egg_crack.mp3')
died = pygame.mixer.Sound('died.mp3')

points = 0
font = pygame.font.Font('freesansbold.ttf', 32)
text = font.render(str(points), True, (0, 0, 0))
textrect = text.get_rect()
textrect.move_ip((10, 10))
current_cracked_eggs = []

starttime = time.time()

running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
    
    for invader in invader_group:
        if player.rect.colliderect(invader.hitbox):
            died.play()
            time.sleep(3)
            running = False
    
    if (time.time() - starttime) > random.randint(2, 7):
        new_egg = Egg()
        all_sprites.add(new_egg)
        egg_group.add(new_egg)
        starttime = time.time()

    pressed_keys = pygame.key.get_pressed()

    text = font.render(str(points), True, (0, 0, 0))

    clock = pygame.time.Clock()
    clock.tick(50)

    for egg in egg_group:
        if player.rect.colliderect(egg.rect):
            points += 1
            nice.play()
            egg.kill()

    egg_cracked_list = []
    screen.fill(white)
    for sprite in all_sprites:
        if sprite.rect[1] > HEIGHT:
            if sprite.ID == 'invader':
                new_sprite = Invader()
                invader_group.add(new_sprite)
                all_sprites.add(new_sprite)
            if sprite.ID == 'egg':
                egg_cracked_list.append(sprite.rect[0])
            sprite.kill()
        sprite.move(screen, pressed_keys)
    
    for egg in egg_cracked_list:
        current_cracked_eggs.append(Cracked_Egg(egg))
        crack_sound.play()
    
    for egg in current_cracked_eggs:
        if time.time() - egg.createtime < 1.5:
            screen.blit(egg.surface, egg.rect)


    screen.blit(text, textrect)
    pygame.display.flip()