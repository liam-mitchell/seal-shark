import pygame

from animation import Animation
from entity import Entity

class Trigger(Entity):
    def __init__(self, image_path, position, entity, entities):
        self.entity = entity
        self.entities = entities
        self.entities.append(entity)
        self.position = position
        self.velocity = pygame.math.Vector2()
        self.type = Entity.TYPE_OBJECT
        self.animation = Animation([pygame.image.load(image_path)], 0)
        self.reset_collider()

class ShutdownTrigger(Trigger):
    def update_logic(self, input_m, entities, dt):
        pass

    def collide(self, other, axis, dt):
        if other.type == Entity.TYPE_PLAYER_MELEE \
           or other.type == Entity.TYPE_PLAYER_RANGED:
                self.die()

    def take_damage(self, damage, source):
        print("trigger taking damage from a " + str(type(source)))
        self.die()

    def die(self):
        if self.entity in self.entities:
            print("trigger removing a " + str(type(self.entity)))
            self.entities.remove(self.entity)
        self.animation = Animation([pygame.image.load("trigger-broken.png")],
                                   0)

        
