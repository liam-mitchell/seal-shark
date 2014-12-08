import pygame

from block import Block
from entity import Entity

class RotatorBlock(Block):
    VEL_UP = pygame.math.Vector2(0, -1)
    VEL_RIGHT = pygame.math.Vector2(1, 0)
    VEL_LEFT = pygame.math.Vector2(-1, 0)
    VEL_DOWN = pygame.math.Vector2(0, 1)

    TIME_ROTATION = 25

    def __init__(self, image_path, position, center, collider=None):
        Block.__init__(self, image_path, position, collider)
        self.center = center
        self.this_center = pygame.math.Vector2(self.position.x
                                               + self.animation.current_frame().get_width() / 2,
                                               self.position.y
                                               + self.animation.current_frame().get_height() / 2)
        self.distance = self.this_center - self.center
        self.type = Entity.TYPE_OBJECT_DYNAMIC

    def update_logic(self, input_m, entities, dt):
        self.distance.rotate_ip(float(dt) / RotatorBlock.TIME_ROTATION)
        self.update_velocity(dt)

    def update_velocity(self, dt):
        self.this_center = self.center + self.distance
        self.next_position = pygame.math.Vector2(self.this_center.x
                                                 - self.animation.current_frame().get_width() / 2,
                                                 self.this_center.y
                                                 - self.animation.current_frame().get_height() / 2)
        self.velocity = self.next_position - self.position

    def collide(self, other, axis, dt):
        if other.type == Entity.TYPE_PLAYER:
            if axis == 'y':
                if self.velocity.y > 0:
                    other.match_top(self)
                else:
                    other.match_bottom(self)
                other.velocity.y = self.velocity.y
            else:
                if self.velocity.x < 0:
                    other.match_left(self)
                else:
                    other.match_right(self)
                other.velocity.x = self.velocity.x
        other.reset_collider()
