import pygame

from pygame.locals import (K_UP, K_DOWN)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

class Dino(pygame.sprite.Sprite):

    def __init__(self):
        super(Dino, self).__init__()
        self.surf = pygame.image.load("Assets/jump.png")
        self.jumping = False
        self.jumSpeedConst = 20
        self.jumSpeed = self.jumSpeedConst
        self.gravity = 2
        self.rect = self.surf.get_rect(center = (80, 380))
        self.x = 80
        self.y = 380
        self.counter = 0

    def update_sprite(self, pressed_keys):
        if pressed_keys[K_UP] and self.jumping == False:
            self.jumping = True
            self.rect.move_ip(0, -self.jumSpeed)
            self.y = self.y - self.jumSpeed

        elif self.jumping == True:
            self.jumSpeed = self.jumSpeed - self.gravity
            self.rect.move_ip(0, -self.jumSpeed)
            self.y = self.y - self.jumSpeed

            if self.jumSpeed <= -self.jumSpeedConst:
                self.jumping = False
                self.jumSpeed = self.jumSpeedConst
                self.rect = self.surf.get_rect(center = (80, 380))
                self.y = 380

        if self.rect.top <= 0:
            self.rect.top = 0

        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

    def update_sprite_ai(self, key):
        if key == K_UP and self.jumping == False:
            self.jumping = True
            self.rect.move_ip(0, -self.jumSpeed)
            self.y = self.y - self.jumSpeed

        elif self.jumping == True:
            self.jumSpeed = self.jumSpeed - self.gravity
            self.rect.move_ip(0, -self.jumSpeed)
            self.y = self.y - self.jumSpeed

            if self.jumSpeed <= -self.jumSpeedConst:
                self.jumping = False
                self.jumSpeed = self.jumSpeedConst
                self.rect = self.surf.get_rect(center=(80, 380))
                self.y = 380

        if self.rect.top <= 0:
            self.rect.top = 0

        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT




