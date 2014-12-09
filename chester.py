import pygame

from animation import Animation
from entity import Entity
from player import Player

class Chester(Entity):
    def __init__(self, image_path):
        self.type = Entity.TYPE_ENEMY_DYNAMIC
        self.animation = Animation([
            pygame.image.load("mock/chester-1.png"),
            pygame.image.load("mock/chester-2.png"),
            pygame.image.load("mock/chester-3.png"),
            pygame.image.load("mock/chester-4.png"),
            ],
                                   100)
        self.position = pygame.math.Vector2(0, 1560 - 9 * 26)
        self.velocity = pygame.math.Vector2(Player.VEL_LEFTRIGHT, 0)
        self.damage = 3
        self.reset_collider()

    def collide(self, other, axis, dt):
        other.take_damage(self.damage, self)

    def update_logic(self, input_m, entities, dt):
        if self.position.x > 2900:
            self.velocity.x = 0
            if len(self.animation.frames) > 2:
                self.animation = Animation([
                    pygame.image.load("mock/chester-tired-1.png"),
                    pygame.image.load("mock/chester-tired-2.png"),
                    ],
                                           500)
