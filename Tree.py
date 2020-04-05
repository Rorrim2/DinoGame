import pygame
import random
from pygame.locals import (K_UP, K_DOWN)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

class Tree(pygame.sprite.Sprite):
    def __init__(self):
        super(Tree, self).__init__()
        self.surf = pygame.image.load("Assets/CACTUS1.png")
        self.rect = self.surf.get_rect(
            center=(
                SCREEN_WIDTH + 20,
                380,
            )
        )
        self.speed = 5


    def update(self):

        self.rect.move_ip(-self.speed, 0)

        if self.rect.right < 0:
            self.kill()