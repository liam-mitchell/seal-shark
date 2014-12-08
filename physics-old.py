import pygame

from entity import Entity

class PhysicsEngine(object):
    # Responsible for maintaining lists of static colliders and moving entities
    # During each frame, loops over moving entities in turn, colliding them with
    # all other entities and colliders and calling their collide() function
    # if a collision is detected.

    ACCEL_GRAVITY = 1000.0

    def add_entity(self, entity):
        entities.append(entity)

    def update(self, entities, dt):
        for e in entities:
            self.add_gravity(e, dt)
            self.step(e, dt, entities)

    def add_gravity(self, entity, dt):
        if entity.type != Entity.TYPE_OBJECT \
           and entity.type != Entity.TYPE_ENEMY_STATIC:
            entity.velocity.y += self.ACCEL_GRAVITY * dt / 1000

    def step(self, entity, dt, entities):
        if entity.type != Entity.TYPE_OBJECT \
           and entity.type != Entity.TYPE_ENEMY_STATIC:
            dy = self.step_y(entity, dt, entities)
            dx = self.step_x(entity, dt, entities)
            entity.position.x += dx
            entity.position.y += dy
            entity.reset_collider()

    def step_y(self, entity, dt, entities):
        delta = entity.velocity.y * dt / 1000
        entity.position.y += delta
        collision = self.collide_with_all(entity, entities)
        entity.position.y -= delta

        if collision:
            print("collision on y")
            if entity.velocity.y < 0:
                delta = self.match_top(entity, collision)
            else:
                delta = self.match_bottom(entity, collision)

        return delta


    def step_x(self, entity, dt, entities):
        print("entity velocity x: " + str(entity.velocity.x))
        delta = entity.velocity.x * dt / 1000
        entity.position.x += delta
        collision = self.collide_with_all(entity, entities)
        entity.position.x -= delta

        if collision:
            print("collision on x")
            if entity.velocity.x < 0:
                delta = self.match_right(entity, collision)
            else:
                delta = self.match_left(entity, collision)

        return delta

    def match_top(self, entity, other):
        position = other.position.y + other.image.get_height()
        entity.velocity.y = 0
        return entity.position.y - position

    def match_bottom(self, entity, other):
        position = other.position.y - entity.image.get_height()
        entity.velocity.y = 0
        if entity.type == Entity.TYPE_PLAYER:
            entity.can_jump = True
        return entity.position.y - position

    def match_left(self, entity, other):
        position = other.position.x - entity.image.get_width()
        entity.velocity.x = 0
        return entity.position.x - position

    def match_right(self, entity, other):
        position = other.position.x + other.image.get_width()
        entity.velocity.x = 0
        return entity.position.x - position

    def collide_with_all(self, entity, entities):
        collision = None
        if entity.type == Entity.TYPE_PLAYER and entity.jumping:
            return collision
        for e in entities:
            if entity.collider.colliderect(e.collider) and e != entity:
                entity.collide(e)
                collision = e
        return collision
