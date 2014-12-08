import pygame

from animation import Animation
from entity import Entity

class Potion(Entity):
    def __init__(self, image_path, position):
        self.position = position
        self.velocity = pygame.math.Vector2()
        self.type = Entity.TYPE_POTION
        self.animation = Animation([
            pygame.image.load(image_path)
            ],
                                   0)
        self.reset_collider()
        self.active = True

    def collide(self, other, axis, dt):
        pass

    def update_logic(self, input_m, entities, dt):
        pass
