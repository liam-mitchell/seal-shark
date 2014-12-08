import pygame

from animation import Animation
from entity import Entity

class Piston(Entity):
    PISTON_DIST = 5 * 26

    PISTON_SPEED = 150

    def __init__(self, image_path, position):
        self.type = Entity.TYPE_OBJECT_DYNAMIC
        self.position = position
        self.start = pygame.math.Vector2(position.x, position.y)
        self.velocity = pygame.math.Vector2(0, Piston.PISTON_SPEED)
        self.top = None
        self.second = None
        self.bottom = None
        self.turning = False
        self.reset_collider()
        self.animation = Animation([pygame.image.load(image_path)], 0)

    def update_logic(self, input_m, entities, dt):
        if self.turning:
            self.turning = False
            return

        if self.position.y - self.start.y > Piston.PISTON_DIST \
           or self.position.y - self.start.y < 0:
            self.velocity.y = -self.velocity.y
            self.turning = True

    def collide(self, other, axis, dt):
        if other.type == Entity.TYPE_PLAYER:
            if self.velocity.y < 0:
                other.match_bottom(self)
            else:
                other.match_top(self)

    def colliders(self):
        return self.collider_list

    def reset_collider(self):
        self.top = pygame.Rect(self.position.x,
                               self.position.y,
                               7 * 26,
                               1 * 26)
        self.second = pygame.Rect(self.position.x + 26,
                                  self.position.y + 26,
                                  5 * 26,
                                  1 * 26)
        self.bottom = pygame.Rect(self.position.x + 26,
                                  self.position.y + 9 * 26,
                                  4 * 26,
                                  26)
        self.collider_list = [self.top, self.second, self.bottom]
