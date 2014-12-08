import pygame

class Entity(object):
    TYPE_PLAYER = 0
    TYPE_OBJECT = 1
    TYPE_OBJECT_DYNAMIC = 2
    TYPE_ENEMY_STATIC = 3
    TYPE_ENEMY_DYNAMIC = 4
    TYPE_PLAYER_MELEE = 5
    TYPE_PLAYER_RANGED = 6

    # Parent class of all entities in the game
    #
    # Member variables:
    #   Surface image
    #   Rect collider
    #   Vec2 position
    #   Vec2 velocity
    #   int type (TYPE_[PLAYER,OBJECT,ENEMY])
    #   Animation animation
    #
    # Abstract methods:
    #   __init__()
    #   collide()
    #   update_logic()

    def __init__(self):
        raise NotImplementedError("Attempt to instantiate abstract entity")

    def update_logic(self, input_m, entities, dt):
        raise NotImplementedError()

    def collide(self, other, axis):
        raise NotImplementedError()

    def collides_with(self, other):
        if self == other:
            return False

        for c in self.colliders():
            for o in other.colliders():
                if c.colliderect(o):
                    return True

        return False

    def die():
        pass

    def take_damage(self, damage, source):
        pass

    def match(self, other, axis):
        if axis == 'y':
            print("self y: " + str(self.position.y)
                  + " other y: " + str(other.position.y))
##            if self.position.y < other.position.y:
##                self.match_bottom(other)
##            else:
##                self.match_top(other)
            if self.velocity.y < 0:
                self.match_top(other)
            else:
                self.match_bottom(other)
            self.velocity.y = 0
        else:
            if self.velocity.x < 0:
                self.match_right(other)
            else:
                self.match_left(other)
            self.velocity.x = 0

    def resolve_collision(self, other, axis, dt):
        if axis == 'y':
            if self.type == Entity.TYPE_PLAYER \
               and self.velocity.y > 0:
                self.can_jump = True
            self.position.y -= self.velocity.y * dt / 1000
            self.velocity.y = 0
        else:
            self.position.x -= self.velocity.x * dt / 1000
            self.velocity.x = 0

    def match_top(self, other):
        print("matching top")
        self.position.y = other.position.y + other.animation.current_frame().get_height()
        self.reset_collider()
        print("self position now (" +
              str(self.position.x) + ", " +
              str(self.position.y) + ")")

    def match_bottom(self, other):
        print("matching bottom")
        self.position.y = other.position.y - self.animation.current_frame().get_height()
        if self.type == Entity.TYPE_PLAYER:
            self.can_jump = True
        self.reset_collider()

    def match_left(self, other):
        print("matching left")
        self.position.x = other.position.x - self.animation.current_frame().get_width()
        self.reset_collider()
        print("self position now (" +
              str(self.position.x) + ", " +
              str(self.position.y) + ")")        

    def match_right(self, other):
        print("matching right")
        self.position.x = other.position.x + other.animation.current_frame().get_width()
        self.reset_collider()
        print("self position now (" +
              str(self.position.x) + ", " +
              str(self.position.y) + ")")

    def colliders(self):
        return [self.collider]

    def reset_collider(self):
        self.collider = pygame.Rect(self.position.x, self.position.y,
                                    self.animation.current_frame().get_width(),
                                    self.animation.current_frame().get_height())
