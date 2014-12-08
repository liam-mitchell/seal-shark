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

    CD_TEETH = 1000
    CD_SHOT = 1000

    DIST_KNOCKBACK = VEL_KNOCKBACK / 10

    ANIM_FRAMELEN_WALK = 500

    ANIM_RIGHT = Animation([
        pygame.image.load("mock/shark-right.png"),
        pygame.image.load("mock/shark-right-2.png")
        ],
                           ANIM_FRAMELEN_WALK)
    ANIM_LEFT = Animation([
        pygame.image.load("mock/shark-left.png"),
        pygame.image.load("mock/shark-left-2.png")
        ],
                           ANIM_FRAMELEN_WALK)
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
        self.VEL_JUMP = math.sqrt(2 * Player.HEIGHT_JUMP
                                  * PhysicsEngine.ACCEL_GRAVITY)
        self.animation = Player.ANIM_RIGHT
        self.reset_collider()

        self.shot_cooldown = 0
        self.teeth_cooldown = 0

    def collide(self, other, axis, dt):
        if other.type == Entity.TYPE_ENEMY_STATIC \
           or other.type == Entity.TYPE_ENEMY_DYNAMIC:
            print("player collided with a " + str(type(other)))
            self.health -= other.damage

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

        if input_m.up:
            if self.can_jump:
                self.can_jump = False
                self.jumping = True
                self.velocity.y = -self.VEL_JUMP

        if input_m.z and self.shot_cooldown <= 0:
            bullet_position = pygame.math.Vector2(self.position.x, self.position.y + 26)
            bullet_direction = pygame.math.Vector2(0, 0)
            if self.animation == Player.ANIM_RIGHT:
                bullet_position.x += 4 * 26
                bullet_direction.x = Player.VEL_BULLET
            else:
                bullet_position.x -= 26
                bullet_direction.x = -Player.VEL_BULLET

            entities.append(PlayerBullet(bullet_position, bullet_direction))
            self.shot_cooldown = Player.CD_SHOT

        if input_m.x and self.teeth_cooldown <= 0:
            teeth_position = pygame.math.Vector2(self.position.x, self.position.y + 26)
            if self.animation == Player.ANIM_RIGHT:
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

    def __init__(self, position, velocity):
        self.animation = PlayerBullet.ANIM_BULLET
        self.position = position
        self.velocity = velocity
        self.type = Entity.TYPE_PLAYER_RANGED
        self.reset_collider()
        self.dead = False

    def collide(self, other, axis, dt):
        other.take_damage(PlayerBullet.DMG_BULLET, self)
        self.dead = True

    def update_logic(self, input_m, entities, dt):
        if self.dead:
            entities.remove(self)

class PlayerTeeth(Entity):
    ANIM_TEETH = Animation([pygame.image.load("mock/teeth.png")], 0)
    DURATION_TEETH = 100
    DMG_TEETH = 1

    def __init__(self, position):
        self.animation = PlayerTeeth.ANIM_TEETH
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
