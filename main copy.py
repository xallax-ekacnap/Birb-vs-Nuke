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

WIDTH, HEIGHT = 800, 800

screen = pygame.display.set_mode((WIDTH, HEIGHT))

class Player(pygame.sprite.Sprite):
    def __init__(self, size):
        # super(Player, self).__init__()
        # self.ID = 'player'
        # self.teleportTime = time.time()
        # self.surface = pygame.image.load('Birb.png')
        # self.surface.set_colorkey((255, 255, 255), RLEACCEL)
        # self.surface = pygame.transform.scale(self.surface, (size, size))
        # self.rect = self.surface.get_rect()
        # self.rect.move_ip((WIDTH / 2, HEIGHT / 2))
        # self.flipped = False
        # self.lsurface = pygame.transform.flip(self.surface, True, False)
        super(Player, self).__init__()
        self.ID = 'player'
        self.surface = pygame.image.load('Birb.png')
        self.surface.set_colorkey((255, 255, 255), RLEACCEL)
        self.surface = pygame.transform.scale(self.surface, (size, size))
        self.rect = self.surface.get_rect()
        self.rect.move_ip((WIDTH / 2, HEIGHT / 2))
        self.flipped = False
        self.surface_lflipped = pygame.transform.flip(self.surface, True, False)
        self.position = pygame.Vector2(self.rect.center)
        self.target_position = pygame.Vector2(self.rect.center)
        self.speed = 0.1  # The rate of movement, adjust for desired speed
    
    def move(self, screen):
        # if pressed_keys[pygame.K_SPACE]:
        #     self.teleportTime = time.time()
        #     if pressed_keys[K_UP]:
        #         self.rect.move_ip(0, -30)
        #     if pressed_keys[K_DOWN]:
        #         self.rect.move_ip(0, 30)
        #     if pressed_keys[K_LEFT]:
        #         self.rect.move_ip(-30, 0)
        #         self.flipped = True
        #     if pressed_keys[K_RIGHT]:
        #         self.rect.move_ip(30, 0)
        #         self.flipped = False
        # else:
        #     if pressed_keys[K_UP]:
        #         self.rect.move_ip(0, -5)
        #     if pressed_keys[K_DOWN]:
        #         self.rect.move_ip(0, 5)
        #     if pressed_keys[K_LEFT]:
        #         self.rect.move_ip(-5, 0)
        #         self.flipped = True
        #     if pressed_keys[K_RIGHT]:
        #         self.rect.move_ip(5, 0)
        #         self.flipped = False
            
        # if self.rect.right > WIDTH:
        #     self.rect.right = WIDTH
        # if self.rect.left < 0:
        #     self.rect.left = 0
        # if self.rect.top < 0:
        #     self.rect.top = 0
        # if self.rect.bottom > HEIGHT:
        #     self.rect.bottom = HEIGHT

        # if self.flipped:
        #     screen.blit(self.lsurface, self.rect)
        # else:
        #     screen.blit(self.surface, self.rect)
        mouse_pos = pygame.mouse.get_pos()
        self.target_position.update(mouse_pos)

        # Calculate the direction vector towards the target position
        direction = self.target_position - self.position

        # Apply a fraction of the distance (speed) to the position to create smooth movement
        if direction.length() > 10  :
            direction.scale_to_length(self.speed * direction.length())
            self.position += direction

        # Update the rect center to the new position
        self.rect.center = self.position

        # Determine the direction of the player (flipping the sprite)
        if direction.x < 0:
            self.flipped = True
        elif direction.x > 0:
            self.flipped = False

        if self.flipped:
            screen.blit(self.surface_lflipped, self.rect)
        else:
            screen.blit(self.surface, self.rect)
        
    def create(self):
        pass

class Turret(pygame.sprite.Sprite):
    def __init__(self, xpos, ypos):
        super(Turret, self).__init__()
        self.ID = 'turret'
        self.surface = pygame.image.load("turret.png")
        self.surface.set_colorkey((255, 255, 255), RLEACCEL)
        self.surface = pygame.transform.scale(self.surface, (25, 25))
        self.rect = self.surface.get_rect()
        self.rect.move_ip((xpos, ypos))
    
    def move(self, screen):
        pass

    def create(self):
        pass


class Invader(pygame.sprite.Sprite):
    def __init__(self, isShooter=False):
        super(Invader, self).__init__()
        self.ID = 'invader'
        self.isShooter = isShooter
        self.orientation = random.randint(0, 3)
        self.location = random.randint(0, HEIGHT)
        self.surface = pygame.image.load("Invader.jpg")
        print(self.orientation)
        if isShooter:
            self.surface = pygame.image.load("Invader_Shooter.jpg")
        self.surface.set_colorkey((255, 255, 255), RLEACCEL)
        self.surface = pygame.transform.scale(self.surface, (75, 25))
        toRotate = 0 if self.orientation == 0 else 180 if self.orientation == 1 else 270 if self.orientation == 2 else 90
        print(toRotate)
        self.surface = pygame.transform.rotate(self.surface, toRotate)
        self.rect = self.surface.get_rect()
        self.speed = random.randint(2, 10)

        # 0 = right, 1 = left, 2 = down, 3 = up
        
        self.rect.move_ip((0, self.location) if self.orientation == 0 else (WIDTH, self.location) if self.orientation == 1 else (self.location, 0) if self.orientation == 2 else (WIDTH, self.location))
        self.hitbox = self.rect
    
    def create(self, invadertime=0):
        alarm = pygame.image.load("danger.png")
        alarm.set_colorkey((255, 255, 255), RLEACCEL)
        alarm = pygame.transform.scale(alarm, (25, 25))
        screen.blit(alarm, (self.rect.x, self.rect.y))
        while time.time() - invadertime < 1:
            pygame.display.flip()

    def move(self, screen):
        self.hitsurf = pygame.Surface((25, 40))
        self.hitsurf.fill((40, 123, 75))
        if self.orientation == 0:
            self.rect.move_ip((self.speed, 0))
        elif self.orientation == 1:
            self.rect.move_ip((-self.speed, 0))
        elif self.orientation == 2:
            self.rect.move_ip((0, self.speed))
        elif self.orientation == 3:
            self.rect.move_ip((0, -self.speed))
        screen.blit(self.surface, self.rect)
        
class Beam(pygame.sprite.Sprite):
    def __init__(self):
        super(Beam, self).__init__()
        self.ID = 'beam'
        side = random.randint(0, 1)
        if side == 0:
            num = random.randint(0, WIDTH)
        else:
            num = random.randint(0, HEIGHT)
        self.position = (0 if side == 1 else num, 0 if side == 0 else num)
        

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

    def move(self, screen):
        self.rect.move_ip((0, self.speed))
        screen.blit(self.surface, self.rect)
    
    def create(self):
        pass

class Cracked_Egg(pygame.sprite.Sprite):
    def __init__(self, xcoord):
        super(Cracked_Egg, self).__init__()
        self.ID = 'cracked_egg'
        self.surface = pygame.transform.scale(pygame.image.load("cracked_egg.jpeg"), (50, 50))
        self.surface.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surface.get_rect().move((xcoord, HEIGHT - 40))
        self.createtime = time.time()

    def create(self):
        pass

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, orientation, type):
        super(Bullet, self).__init__()
        self.ID = type
        if (type == 'invader_bullet'):
            self.surface = pygame.transform.scale(pygame.image.load("Invader_bullet.png"), (10, 10))
        elif (type == 'turret_bullet'):
            self.surface = pygame.transform.scale(pygame.image.load("Turret_bullet.png"), (10, 10))
        self.surface = pygame.transform.rotate(self.surface, orientation * 45)
        self.surface.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surface.get_rect().move((x, y))
        self.hitbox = self.rect
        self.orientation = orientation
    
    def move(self, screen):
        if self.orientation > 0 and self.orientation < 4:
            self.rect.move_ip((random.randint(0, 3), 0))
        elif self.orientation > 4 and self.orientation < 8:
            self.rect.move_ip((-random.randint(0, 3), 0))
        if self.orientation > 2 and self.orientation < 6:
            self.rect.move_ip((0, random.randint(0, 3)))
        elif self.orientation == 7 or self.orientation == 8 or self.orientation == 1:
            self.rect.move_ip((0, -random.randint(0, 3)))
        screen.blit(self.surface, self.rect)
    
    def create(self):
        pass

        # (-1, -1) (0, -1) (1, -1)
        # (-1, 0)          (1, 0)
        # (-1, 1)  (0, 1)  (1, 1)

# class Danger(pygame.sprite.Sprite, Invader):
#     def __init__(self, xpos, ypos):
#         super(Danger, self).__init__()
#         self.ID = 'danger'
#         self.surface = pygame.transform.scale(pygame.image.load("danger.png"), (25, 25))
#         self.surface.set_colorkey((255, 255, 255), RLEACCEL)
#         self.rect = self.surface.get_rect()
#         self.rect.move_ip((xpos, ypos))
    
#     def create(self):
#         pass

#     def move(self, screen, pressed_keys):
#         pass



def is_out_of_bounds(sprite):
    return sprite.rect.left < 0 or sprite.rect.right > WIDTH or sprite.rect.top < 0 or sprite.rect.bottom > HEIGHT


player = Player(50)
white = (255, 255, 255)

n_invaders = 5
invader_group = pygame.sprite.Group()
for i in range(n_invaders):
    invader_group.add(Invader(False))
all_sprites = pygame.sprite.Group(player, invader_group)
all_sprites.add(Turret(random.randint(0, WIDTH), random.randint(0, HEIGHT)))
all_sprites.add(Turret(random.randint(0, WIDTH), random.randint(0, HEIGHT)))
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
eggtime = starttime
bullettime = starttime
turrettime = starttime
invadertime = starttime

for sprite in all_sprites:
    sprite.create()

running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
    
    for sprite in all_sprites:
        if (sprite.ID == 'invader' or sprite.ID == 'invader_bullet') and player.rect.colliderect(sprite.hitbox):
            died.play()
            time.sleep(3)
            running = False
    
    if (time.time() - eggtime) > random.randint(2, 7):
        new_egg = Egg()
        all_sprites.add(new_egg)
        egg_group.add(new_egg)
        eggtime = time.time()

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
        if is_out_of_bounds(sprite):
            if sprite.ID == 'invader':
                has_bullets = True if random.randint(0, 5) == 1 else False
                new_sprite = Invader(has_bullets)
                invader_group.add(new_sprite)
                all_sprites.add(new_sprite)
            if sprite.ID == 'egg':
                egg_cracked_list.append(sprite.rect[0])
            sprite.kill()
        sprite.move(screen)
    
    for egg in egg_cracked_list:
        current_cracked_eggs.append(Cracked_Egg(egg))
        crack_sound.play()
    
    for egg in current_cracked_eggs:
        if time.time() - egg.createtime < 1.5:
            screen.blit(egg.surface, egg.rect)

    if time.time() - bullettime > 3:
        bullettime = time.time()
        for invader in invader_group:
            if invader.isShooter:
                for i in range (8):
                    new_bullet = Bullet(invader.rect[0], invader.rect[1], i + 1, "invader_bullet")
                    all_sprites.add(new_bullet)

    screen.fill(white)

    if (time.time() - turrettime) > 3:
        for sprite in all_sprites:
            if sprite.ID == 'turret':
                all_sprites.add(Bullet(sprite.rect[0], sprite.rect[1], random.randint(0, 8), "turret_bullet"))
                all_sprites.add(Bullet(sprite.rect[0], sprite.rect[1], random.randint(0, 8), "turret_bullet"))
                all_sprites.add(Bullet(sprite.rect[0], sprite.rect[1], random.randint(0, 8), "turret_bullet"))
                all_sprites.add(Bullet(sprite.rect[0], sprite.rect[1], random.randint(0, 8), "turret_bullet"))
                all_sprites.add(Bullet(sprite.rect[0], sprite.rect[1], random.randint(0, 8), "turret_bullet"))
                all_sprites.add(Bullet(sprite.rect[0], sprite.rect[1], random.randint(0, 8), "turret_bullet"))
        turrettime = time.time()

    for sprite in all_sprites:
        screen.blit(sprite.surface, sprite.rect)

    screen.blit(text, textrect)
    pygame.display.flip()