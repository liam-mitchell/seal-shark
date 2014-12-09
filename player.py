import math
import pygame

from animation import Animation
from entity import Entity
from newlevel import NewLevelException
from physics import PhysicsEngine

class Player(Entity):
    HEIGHT_JUMP = 104

    VEL_LEFTRIGHT = 200
    VEL_KNOCKBACK = VEL_LEFTRIGHT
    VEL_BULLET = 500
    VEL_JUMP = math.sqrt(2 * HEIGHT_JUMP * PhysicsEngine.ACCEL_GRAVITY)

    CD_TEETH = 250
    CD_SHOT = 250

    DIST_KNOCKBACK = VEL_KNOCKBACK / 10

    ANIM_FRAMELEN_WALK = 100

    ANIM_RIGHT = Animation([
        pygame.image.load("mock/shark-right-1.png"),
        pygame.image.load("mock/shark-right-2.png"),
        pygame.image.load("mock/shark-right-3.png"),
        pygame.image.load("mock/shark-right-4.png"),
        pygame.image.load("mock/shark-right-5.png"),
        pygame.image.load("mock/shark-right-6.png"),
        ],
                           ANIM_FRAMELEN_WALK)
    ANIM_LEFT = Animation([
        pygame.image.load("mock/shark-left-1.png"),
        pygame.image.load("mock/shark-left-2.png"),
        pygame.image.load("mock/shark-left-3.png"),
        pygame.image.load("mock/shark-left-4.png"),
        pygame.image.load("mock/shark-left-5.png"),
        pygame.image.load("mock/shark-left-6.png")
        ],
                           ANIM_FRAMELEN_WALK)
    ANIM_IDLE_RIGHT = Animation([
        pygame.image.load("mock/shark-right-1.png")
        ],
                                0)
    ANIM_IDLE_LEFT = Animation([
        pygame.image.load("mock/shark-left-1.png")
        ],
                               0)
    ANIM_DEAD = Animation([
        pygame.image.load("mock/shark-dead.png")
        ],
                          0)

    def __init__(self, image_path, position):
        self.position = position
        self.velocity = pygame.math.Vector2()
        self.type = Entity.TYPE_PLAYER
        self.health = 3
        self.can_jump = False
        self.jumping = False
        self.dead = False
        self.stunned = 10
        self.animation = Player.ANIM_RIGHT
        self.reset_collider()

        self.shot_cooldown = 0
        self.teeth_cooldown = 0

    def collide(self, other, axis, dt):
        if other.type == Entity.TYPE_ENEMY_STATIC \
           or other.type == Entity.TYPE_ENEMY_DYNAMIC \
           or other.type == Entity.TYPE_CHAMELEON:
            self.health -= other.damage
            print("collided with enemy")

            if other.damage > 0:
                if axis == 'y':
                    self.velocity.y = -self.velocity.y
                else:
                    self.velocity.x = -self.velocity.x
                self.stunned = 10

            if self.health < 1:
                self.die()
        elif other.type == Entity.TYPE_POTION and other.active:
            other.active = False
            raise NewLevelException()
        else:
            self.resolve_collision(other, axis, dt)
            self.reset_collider()

    def take_damage(self, damage, source):
        self.health -= damage
        if self.health < 1:
            self.die()

    def die(self):
        self.animation = Player.ANIM_DEAD
        self.dead = True

    def update_logic(self, input_m, entities, dt):
        if self.dead:
            return

        if self.stunned > 0:
            self.stunned -= 1
            return

        if self.jumping:
            self.jumping = False

        if input_m.left:
            self.velocity.x = -Player.VEL_LEFTRIGHT
            self.animation = Player.ANIM_LEFT
        elif input_m.right:
            self.velocity.x = Player.VEL_LEFTRIGHT
            self.animation = Player.ANIM_RIGHT
        else:
            self.velocity.x = 0
            if self.animation == Player.ANIM_LEFT \
               or self.animation == Player.ANIM_IDLE_LEFT:
                self.animation = Player.ANIM_IDLE_LEFT
            else:
                self.animation = Player.ANIM_IDLE_RIGHT

        if input_m.up:
            if self.can_jump:
                self.can_jump = False
                self.jumping = True
                self.velocity.y = -self.VEL_JUMP

        if input_m.z and self.shot_cooldown <= 0:
            bullet_position = pygame.math.Vector2(self.position.x, self.position.y + 52)
            bullet_direction = pygame.math.Vector2(0, 0)
            if self.animation == Player.ANIM_RIGHT \
               or self.animation == Player.ANIM_IDLE_RIGHT:
                bullet_position.x += 2.5 * 26
                bullet_direction.x = Player.VEL_BULLET
            else:
                bullet_direction.x = -Player.VEL_BULLET

            entities.append(PlayerBullet(bullet_position, bullet_direction))
            self.shot_cooldown = Player.CD_SHOT

        if input_m.x and self.teeth_cooldown <= 0:
            teeth_position = pygame.math.Vector2(self.position.x, self.position.y + 26)
            if self.animation == Player.ANIM_RIGHT \
               or self.animation == Player.ANIM_IDLE_RIGHT:
                teeth_position.x += 3 * 26
            else:
                teeth_position.x -= 26
        
            entities.append(PlayerTeeth(teeth_position))
            self.teeth_cooldown = Player.CD_TEETH

        if self.shot_cooldown > 0:
            self.shot_cooldown -= dt
        if self.teeth_cooldown > 0:
            self.teeth_cooldown -= dt

    def reset_collider(self):
        dx = 19
        dy = 26

        self.collider = pygame.Rect(self.position.x + dx,
                                    self.position.y + dy,
                                    self.animation.current_frame().get_width() - 39,
                                    self.animation.current_frame().get_height() - 26)

class PlayerBullet(Entity):
    VEL_BULLET = 500                                         
    ANIM_BULLET = Animation([pygame.image.load("mock/bullet.png")], 0)
    DMG_BULLET = 1
    TIME_BULLET = 5000

    def __init__(self, position, velocity):
        self.animation = PlayerBullet.ANIM_BULLET
        self.position = position
        self.velocity = velocity
        self.type = Entity.TYPE_PLAYER_RANGED
        self.reset_collider()
        self.dead = False
        self.time = 0

    def collide(self, other, axis, dt):
        other.take_damage(PlayerBullet.DMG_BULLET, self)
        print("bullet hit a " + str(type(other)))
        self.dead = True

    def update_logic(self, input_m, entities, dt):
        self.time += dt
        if self.time > PlayerBullet.TIME_BULLET:
            self.dead = True
        if self.dead:
            entities.remove(self)

class PlayerTeeth(Entity):

    DURATION_TEETH = 100
    ANIM_TEETH = Animation([
        pygame.image.load("mock/shark-bite-1.png"),
        pygame.image.load("mock/shark-bite-2.png"),
        pygame.image.load("mock/shark-bite-3.png"),
        pygame.image.load("mock/shark-bite-4.png"),
        ], DURATION_TEETH / 4)
    DMG_TEETH = 1

    def __init__(self, position):
        self.animation = PlayerTeeth.ANIM_TEETH
        self.animation.frame_number = 0
        self.animation.current_time = 0
        self.position = position
        self.velocity = pygame.math.Vector2()
        self.type = Entity.TYPE_PLAYER_MELEE
        self.reset_collider()
        self.duration = 0
        self.dead = False

    def collide(self, other, axis, dt):
        other.take_damage(PlayerTeeth.DMG_TEETH, self)
        self.dead = True

    def update_logic(self, input_m, entities, dt):
        self.duration += dt
        if self.duration > PlayerTeeth.DURATION_TEETH:
            self.dead = True
        if self.dead:
            entities.remove(self)
