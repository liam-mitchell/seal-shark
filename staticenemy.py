import pygame

from animation import Animation
from entity import Entity

class StaticEnemy(Entity):

    def __init__(self, image_path, position, damage=1, animation=None):
        self.type = Entity.TYPE_ENEMY_STATIC
        if not animation:
            self.animation = Animation([pygame.image.load(image_path)], 0)
        else:
            self.animation = animation
        self.position = position
        self.velocity = pygame.math.Vector2()
        self.collider = pygame.Rect(position.x, position.y,
                                    self.animation.current_frame().get_width(),
                                    self.animation.current_frame().get_height())
        self.damage = damage

    def collide(self, other, axis, dt):
        pass

    def update_logic(self, input_m, entities, dt):
        pass

class DynamicEnemy(StaticEnemy):
    def __init__(self, image_path, position, velocity, damage=1, animation=None):
        StaticEnemy.__init__(self, image_path, position, damage, animation)
        self.velocity = velocity
        print("created dynamic enemy with vel (" +
              str(self.velocity.x) + ", " + str(self.velocity.y) + ")")
        self.reset_collider()
        self.type = Entity.TYPE_ENEMY_DYNAMIC
        self.dead = False

    def collide(self, other, axis, dt):
        if other.type == Entity.TYPE_PLAYER:
            self.dead = True
            other.take_damage(self.damage, self)

    def update_logic(self, input_m, entities, dt):
        if self.dead and self in entities:
            entities.remove(self)

class DoctorMan(StaticEnemy):
    def __init__(self, position):
        StaticEnemy.__init__(self, "mock/doctor-man.png", position)
        self.health = 5
        self.dead = False

    def collide(self, other, axis, dt):
        pass

    def take_damage(self, damage, source):
        print("doctor hit by a " + str(type(source)))
        if source.type == Entity.TYPE_PLAYER_MELEE \
           or source.type == Entity.TYPE_PLAYER_RANGED:
            self.health -= 1
            if self.health < 1:
                self.dead = True

    def update_logic(self, input_m, entities, dt):
        if self.dead and self in entities:
            entities.remove(self)
