import pygame
from pygame.locals import *

class InputManager(object):
    def __init__(self):
        self.left = False
        self.right = False
        self.up = False
        self.down = False
        self.z = False
        self.x = False

    def update(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                return False

            elif event.type == KEYDOWN:
                if event.key == K_RIGHT:
                    self.right = True
                elif event.key == K_LEFT:
                    self.left = True
                elif event.key == K_UP:
                    self.up = True
                elif event.key == K_DOWN:
                    self.down = True
                elif event.key == K_z:
                    self.z = True
                elif event.key == K.x:
                    self.x = True

            elif event.type == KEYUP:
                if event.key == K_RIGHT:
                    self.right = False
                elif event.key == K_LEFT:
                    self.left = False
                elif event.key == K_UP:
                    self.up = False
                elif event.key == K_DOWN:
                    self.down = False
                elif event.key == K_z:
                    self.z = False
                elif event.key == K.x:
                    self.x = False
