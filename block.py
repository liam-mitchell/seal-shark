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

class BreakableBlock(Block):
    def __init__(self, image_path, position):
        Block.__init__(self, image_path, position)
        self.dead = False

    def take_damage(self, damage, source):
        self.dead = True

    def update_logic(self, input_m, entities, dt):
        if self.dead:
            entities.remove(self)

class TimedBlock(Block):
    def __init__(self, animation, position, time):
        self.time = time
        self.current_time = 0
        self.animation = animation
        self.type = Entity.TYPE_OBJECT
        self.position = position
        self.velocity = pygame.math.Vector2()
        self.reset_collider()

    def update_logic(self, input_m, entities, dt):
        self.current_time += dt
        if self.current_time > self.time and self in entities:
            entities.remove(self)
