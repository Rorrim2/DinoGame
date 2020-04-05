import pygame
from Dino import Dino
from Background import Background
from Tree import Tree
import time
import random

from pygame.locals import (K_UP, K_DOWN, KEYDOWN, K_ESCAPE)

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

pygame.display.set_caption("Dino Run")

screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
background = Background("Assets/background.png", [0,0])


ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 750)


player = Dino()

obstacles = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

clock = pygame.time.Clock()

running = True
i = 0
while running:
    screen.fill((255, 255, 255))
    screen.blit(background.image, background.rect)
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        elif event.type == pygame.QUIT:
            running = False
        elif event.type == ADDENEMY:
            rand = random.randint(0, 100)
            if rand < 70:
                if i > 2:
                    tree = Tree()
                    obstacles.add(tree)
                    all_sprites.add(tree)
                    i = 0
                else:
                    i += 1

    pressed_keys = pygame.key.get_pressed()

    player.update_sprite(pressed_keys)
    obstacles.update()

    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)
    if pygame.sprite.spritecollideany(player, obstacles):
        player.kill()
        running = False

    pygame.display.flip()
    clock.tick(30)

pygame.quit()