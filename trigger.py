import pygame

from animation import Animation
from entity import Entity
from staticenemy import StaticEnemy
from block import Block

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
        self.animation = Animation([pygame.image.load("mock/trigger-broken.png")],
                                   0)

        
class FireTrigger(ShutdownTrigger):
    FIRE_ON_TIME = 500
    FIRE_OFF_TIME = 750

    ANIM_GLOWY = Animation([
        pygame.image.load("mock/stove-glowy.png"),
        pygame.image.load("mock/stove-glowy-2.png"),
        pygame.image.load("mock/stove-glowy-3.png"),
        ],
                           FIRE_OFF_TIME / 3)
    ANIM_FIRE = Animation([
        pygame.image.load("mock/stove-fire.png"),
        pygame.image.load("mock/stove-fire-2.png"),
        ],
                          FIRE_ON_TIME / 2)

    def __init__(self, image_path, position, entities):
        self.entities = entities
        self.fire = [
            StaticEnemy("mock/stove-fire.png",
                        pygame.math.Vector2(20 * 26, 22 * 26 - 1), 1,
                        FireTrigger.ANIM_FIRE),
            StaticEnemy("mock/stove-fire.png",
                        pygame.math.Vector2(14 * 26, 22 * 26 - 1), 1,
                        FireTrigger.ANIM_FIRE),
            StaticEnemy("mock/stove-fire.png",
                        pygame.math.Vector2(17 * 26, 22 * 26 - 1), 1,
                        FireTrigger.ANIM_FIRE),
            ]
        self.glowies = [
            StaticEnemy("mock/stove-glowy.png",
                        pygame.math.Vector2(20 * 26, 25 * 26 - 1), 1,
                        FireTrigger.ANIM_GLOWY),
            StaticEnemy("mock/stove-glowy.png",
                        pygame.math.Vector2(14 * 26, 25 * 26 - 1), 1,
                        FireTrigger.ANIM_GLOWY),
            StaticEnemy("mock/stove-glowy.png",
                        pygame.math.Vector2(17 * 26, 25 * 26 - 1), 1,
                        FireTrigger.ANIM_GLOWY),
            ]

        self.position = position
        self.animation = Animation([pygame.image.load("mock/trigger.png")], 0)
        self.type = Entity.TYPE_OBJECT
        self.reset_collider()
        self.time = 0
        self.on = False
        self.current = 0
        self.dead = False

    def update_logic(self, input_m, entities, dt):
        if self.dead:
            return
        print("updating fire trigger")
        if self.on:
            if self.time > FireTrigger.FIRE_ON_TIME:
                self.on = False
                self.time = 0

                if self.current == len(self.fire):
                    self.turn_off_all(self.fire)
                else:
                    self.turn_off(self.fire[self.current])

                self.current += 1

                if self.current > len(self.fire):
                    self.current = 0

                if self.current == len(self.fire):
                    self.turn_on_all(self.glowies)
                else:
                    self.turn_on(self.glowies[self.current])
        else:
            if self.time > FireTrigger.FIRE_OFF_TIME:
                self.on = True
                self.time = 0

                if self.current == len(self.fire):
                    self.turn_off_all(self.glowies)
                    self.turn_on_all(self.fire)

                else:
                    self.turn_off(self.glowies[self.current])
                    self.turn_on(self.fire[self.current])

        self.time += dt

    def turn_on_all(self, entities):
        for e in entities:
            self.turn_on(e)

    def turn_on(self, entity):
        self.entities.append(entity)

    def turn_off_all(self, entities):
        for e in entities:
            self.turn_off(e)

    def turn_off(self, entity):
        if entity in self.entities:
            self.entities.remove(entity)
            entity.animation.current_time = 0
            entity.animation.frame_number = 0

    def die(self):
        self.dead = True
        self.turn_off_all(self.fire)
        self.turn_off_all(self.glowies)
