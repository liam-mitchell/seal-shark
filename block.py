import pygame

from animation import Animation
from entity import Entity

class Block(Entity):
    def __init__(self, image_path, position, collider=None):
        self.type = Entity.TYPE_OBJECT
        self.animation = Animation([pygame.image.load(image_path)], 0)
        self.position = position
        self.velocity = pygame.math.Vector2()
        self.collider = pygame.Rect(position.x, position.y,
                                    self.animation.current_frame().get_width(),
                                    self.animation.current_frame().get_height())

    def collide(self, other, axis, dt):
        pass

    def update_logic(self, input_m, entities, dt):
        pass
