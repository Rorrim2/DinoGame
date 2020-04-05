import pygame

from pygame.locals import (K_UP, K_DOWN)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

class Dino(pygame.sprite.Sprite):

    def __init__(self):
        super(Dino, self).__init__()
        self.surf = pygame.image.load("Assets/jump.png")
        # self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.jumping = False
        self.jumSpeedConst = 20
        self.jumSpeed = self.jumSpeedConst
        self.gravity = 1.25
        self.rect = self.surf.get_rect(center = (80, 380))

    def update_sprite(self, pressed_keys):
        if pressed_keys[K_UP] and self.jumping == False:
            self.jumping = True
            self.rect.move_ip(0, -self.jumSpeed)
        elif self.jumping == True:
            self.jumSpeed = self.jumSpeed - self.gravity
            self.rect.move_ip(0, -self.jumSpeed)
            if self.jumSpeed == -self.jumSpeedConst:
                self.jumping = False
                self.jumSpeed = self.jumSpeedConst


            # if pressed_keys[K_DOWN]:
            #     self.rect.move_ip(0, 5)

        if self.rect.top <= 0:
            self.rect.top = 0

        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT


