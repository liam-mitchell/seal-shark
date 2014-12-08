import pygame

from entity import Entity

class PhysicsEngine(object):
    # Responsible for maintaining lists of static colliders and moving entities
    # During each frame, loops over moving entities in turn, colliding them with
    # all other entities and colliders and calling their collide() function
    # if a collision is detected.

    ACCEL_GRAVITY = 2000.0

    def update(self, entities, dt):
        for e in entities:
            self.add_gravity(e, dt)
            self.step(e, dt, entities)

    def add_gravity(self, entity, dt):
        if entity.type == Entity.TYPE_PLAYER:
            entity.velocity.y += self.ACCEL_GRAVITY * dt / 1000

    def step(self, entity, dt, entities):
        if entity.type != Entity.TYPE_OBJECT \
           and entity.type != Entity.TYPE_ENEMY_STATIC:
            self.step_y(entity, dt, entities)
            entity.reset_collider()
            self.step_x(entity, dt, entities)
            entity.reset_collider()
            if entity.type == Entity.TYPE_PLAYER:
                print("player at (" + str(entity.position.x)
                      + ", " + str(entity.position.y) + ") vel ("
                      + str(entity.velocity.x) + ", "
                      + str(entity.velocity.y) + ")")

    def step_y(self, entity, dt, entities):
        delta = entity.velocity.y * dt / 1000
        entity.position.y += delta
        self.collide_with_all(entity, entities, 'y', dt)

    def step_x(self, entity, dt, entities):
        delta = entity.velocity.x * dt / 1000
        entity.position.x += delta
        self.collide_with_all(entity, entities, 'x', dt)

    def collide_with_all(self, entity, entities, axis, dt):
        entity.reset_collider()
        if entity.type == Entity.TYPE_PLAYER and entity.jumping:
            return
          
        for e in entities:
            if entity.collides_with(e):
                entity.collide(e, axis, dt)
                
