import pygame

from animation import Animation
from entity import Entity
from player import Player

class Chester(Entity):

    def __init__(self, image_path):
        self.type = Entity.TYPE_ENEMY_DYNAMIC
        self.animation = Animation([
            pygame.image.load(image_path)
            ],
                                   0)
        self.position = pygame.math.Vector2(0, 780 - 5 * 26)
        self.velocity = pygame.math.Vector2(Player.VEL_LEFTRIGHT, 0)
        self.damage = 3
        self.reset_collider()

    def collide(self, other, axis, dt):
        other.take_damage(self.damage, self)

    def update_logic(self, input_m, entities, dt):
        print("chester updatin' at " +
              str(self.position.x) + ", "
              + str(self.position.y) + ")")
