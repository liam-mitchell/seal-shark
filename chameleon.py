import pygame

from animation import Animation
from entity import Entity
from player import Player
from staticenemy import DynamicEnemy, DoctorMan, StaticEnemy

class Chameleon(Entity):
    TONGUE_TIME = 1500
    TONGUE_DELAY = 500
    TONGUE_DURATION = 1000

    LASER_TIME = 0
    LASER_DELAY = 500
    LASER2_DELAY = 100
    LASER_DURATION = 1000

    STATE_IDLE = 0
    STATE_TONGUE = 1
    STATE_LASERS = 2

    OFFSET_TONGUE = pygame.math.Vector2(4.5 * 26, 0)
    OFFSET_LASER = pygame.math.Vector2(5 * 26, 0)
    OFFSET_DOCTOR = pygame.math.Vector2(1 * 26, -1.5 * 26)

    ANIM_TONGUE = Animation([
        pygame.image.load("mock/nanomeleon-tongue-1.png"),
        pygame.image.load("mock/nanomeleon-tongue-2.png"),
        pygame.image.load("mock/nanomeleon-tongue-2.png"),
        pygame.image.load("mock/nanomeleon-tongue-2.png"),
        pygame.image.load("mock/nanomeleon-tongue-3.png"),
        ],
                            (TONGUE_DELAY + TONGUE_DURATION) / 5)
    ANIM_LASER = Animation([
        pygame.image.load("mock/nanomeleon-laser-1.png"),
        pygame.image.load("mock/nanomeleon-laser-2.png"),
        pygame.image.load("mock/nanomeleon-laser-2.png"),
        pygame.image.load("mock/nanomeleon-laser-2.png"),
        pygame.image.load("mock/nanomeleon-laser-3.png"),
        ],
                           (LASER_DELAY + LASER2_DELAY + LASER_DURATION) / 5)

    ANIM_IDLE = Animation([
        pygame.image.load("mock/nanomeleon-walk-1.png"),
        pygame.image.load("mock/nanomeleon-walk-2.png"),
        pygame.image.load("mock/nanomeleon-walk-3.png"),
        pygame.image.load("mock/nanomeleon-walk-4.png"),
        pygame.image.load("mock/nanomeleon-walk-5.png"),
        pygame.image.load("mock/nanomeleon-walk-6.png"),
        pygame.image.load("mock/nanomeleon-walk-7.png"),
        ],
                          100)

    ANIM_OBJ_TONGUE = Animation([
        pygame.image.load("mock/tongue-1.png"),
        pygame.image.load("mock/tongue-2.png"),
        pygame.image.load("mock/tongue-3.png"),
        pygame.image.load("mock/tongue-4.png"),
        pygame.image.load("mock/tongue-4.png"),
        pygame.image.load("mock/tongue-4.png"),
        pygame.image.load("mock/tongue-4.png"),
        pygame.image.load("mock/tongue-4.png"),
        ],
                                TONGUE_DURATION / 8)
    VEL_LEFTRIGHT = 100
    DIST_LEFTRIGHT = 26 * 3

    def __init__(self, image_path, position):
        self.type = Entity.TYPE_CHAMELEON
        self.animation = Animation([
            pygame.image.load(image_path),
            ],
                                   0)
        self.position = position
        self.start = pygame.math.Vector2(position.x, position.y)
        self.velocity = pygame.math.Vector2(Chameleon.VEL_LEFTRIGHT, 0)
        self.damage = 1
        self.reset_collider()
        self.tongue = None
        self.laser = None
        self.laser2 = None
        self.jumped = False
        self.dead = False
        self.state = Chameleon.STATE_IDLE
        self.state_time = 0
        self.doctor = DoctorMan(self.position + Chameleon.OFFSET_DOCTOR)

    def collide(self, other, axis, dt):
        if other.type == Entity.TYPE_PLAYER or other.type == Entity.TYPE_OBJECT:
            other.take_damage(self.damage, self)
            self.resolve_collision(other, axis, dt)

    def update_logic(self, input_m, entities, dt):
        if self.doctor.dead:
            self.velocity = pygame.math.Vector2()
            self.animation = Chameleon.ANIM_IDLE
            return

        if not self.doctor in entities:
            entities.insert(0, self.doctor)

        self.state_time += dt
        if self.state == Chameleon.STATE_IDLE:
            self.update_idle(dt)
        elif self.state == Chameleon.STATE_TONGUE:
            self.update_tongue(dt, entities)
        else:
            self.update_laser(dt, entities)

        self.update_doctor()

    def update_idle(self, dt):
        if self.position.x - self.start.x > Chameleon.DIST_LEFTRIGHT:
            self.velocity.x = -Chameleon.VEL_LEFTRIGHT
        elif self.position.x - self.start.x < -Chameleon.DIST_LEFTRIGHT:
            self.velocity.x = Chameleon.VEL_LEFTRIGHT

        if self.animation != Chameleon.ANIM_IDLE:
            self.animation = Chameleon.ANIM_IDLE
            self.animation.frame_number = 0
            self.animation.current_time = 0
        if self.state_time > Chameleon.TONGUE_TIME:
            self.state = Chameleon.STATE_TONGUE
            self.state_time = 0

    def update_tongue(self, dt, entities):
        if self.animation != Chameleon.ANIM_TONGUE:
            self.animation = Chameleon.ANIM_TONGUE
            self.animation.frame_number = 0
            self.animation.current_time = 0
        if self.tongue:
            self.tongue.position = self.position + Chameleon.OFFSET_TONGUE
        if self.state_time > Chameleon.TONGUE_DELAY and not self.tongue:
            Chameleon.ANIM_OBJ_TONGUE.frame_number = 0
            Chameleon.ANIM_OBJ_TONGUE.current_time = 0
            self.tongue = DynamicEnemy("mock/chameleon-tongue.png",
                                       self.position + Chameleon.OFFSET_TONGUE,
                                       pygame.math.Vector2(),
                                       3,
                                       Chameleon.ANIM_OBJ_TONGUE)
            print("tongue is a " + str(type(self.tongue)) + " with damage " + str(self.tongue.damage))
            entities.append(self.tongue)
        elif self.state_time > Chameleon.TONGUE_DELAY + Chameleon.TONGUE_DURATION:
            self.state_time = 0
            self.state = Chameleon.STATE_LASERS
            if self.tongue in entities:
                entities.remove(self.tongue)

            self.tongue = None

    def update_laser(self, dt, entities):
        if self.animation != Chameleon.ANIM_LASER:
            self.animation = Chameleon.ANIM_LASER
            self.animation.frame_number = 0
            self.animation.current_time = 0
        if self.state_time > Chameleon.LASER_DELAY and not self.jumped:
            self.jump()
            self.jumped = True

        if self.state_time > Chameleon.LASER_DELAY and not self.laser:
            self.laser = DynamicEnemy("mock/chameleon-laser.png",
                                      self.position + Chameleon.OFFSET_LASER,
                                      pygame.math.Vector2(Player.VEL_BULLET, 0),
                                      3)
            entities.append(self.laser)
        if self.state_time > Chameleon.LASER_DELAY + Chameleon.LASER2_DELAY \
           and not self.laser2:
            self.laser2 = DynamicEnemy("mock/chameleon-laser.png",
                                       self.position + Chameleon.OFFSET_LASER,
                                       pygame.math.Vector2(Player.VEL_BULLET, 0),
                                       3)
            entities.append(self.laser2)
        elif self.state_time > Chameleon.LASER_DELAY \
             + Chameleon.LASER_DURATION \
             + Chameleon.LASER2_DELAY:
            if self.laser in entities:
                entities.remove(self.laser)
            if self.laser2 in entities:
                entities.remove(self.laser2)
            self.laser = None
            self.laser2 = None
            self.jumped = False
            self.state_time = 0
            self.state = Chameleon.STATE_IDLE

    def jump(self):
        self.velocity = pygame.math.Vector2(0, -Player.VEL_JUMP)

    def update_doctor(self):
        self.doctor.position = self.position + Chameleon.OFFSET_DOCTOR
        print("chameleon now at (" + str(self.position.x) + ", "
              + str(self.position.y) + ")")
        print("doctor now at (" + str(self.doctor.position.x)
              + ", " + str(self.doctor.position.y) + ")")
