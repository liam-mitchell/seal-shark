import pygame

from player import Player

class Window(object):
    LEVEL1 = 0
    LEVEL2 = 1
    VEL_LEVEL1 = pygame.math.Vector2()
    VEL_LEVEL2 = pygame.math.Vector2(-Player.VEL_LEFTRIGHT,
                                     0)
    VEL_LEVEL2_UP = pygame.math.Vector2(0, Player.VEL_LEFTRIGHT)
    TIME_LEVEL2_WAIT = 5000
    BG_LEVEL1 = pygame.image.load("mock/level1-background.png")
    BG_LEVEL2 = pygame.image.load("mock/level2-background.png")
    # Responsible for drawing objects and background on the screen
    # Member variables:
    #   screen: drawing window obtained with pygame.display.set_mode()
    #   background: pygame surface with background image
    def __init__(self, width, height):
        self.screen = pygame.display.set_mode([width, height]);
        self.background = Window.BG_LEVEL1
        self.screen.blit(self.background, (0,0))
        self.camera = pygame.math.Vector2()
        self.velocity = Window.VEL_LEVEL1
        self.level = Window.LEVEL1
        self.idle_time = 0
        self.idle = False

    # render()
    # Core render function. Called once per frame from main loop.
    #
    # Draws the background onto the screen, then each of objects
    # Updates the display once finished drawing to the screen
    #
    # param entities:
    #   list of Entity objects to draw
    # param colliders:
    #   list of Collider objects to draw
    def render(self, entities, dt):
        self.move(dt)
        if self.level == Window.LEVEL1:
            self.background = Window.BG_LEVEL1.copy()
        else:
            self.background = Window.BG_LEVEL2.copy()

        for e in entities:
            self.background.blit(e.animation.next_frame(dt),
                                 (e.position.x, e.position.y))

        self.screen.blit(self.background, self.camera)
        pygame.display.update()

    def change_level(self, clock, target, duration):
        scale_x = self.background.get_rect().width / target.width
        scale_y = self.background.get_rect().height / target.height
        final_size = pygame.Rect(0, 0,
                                 self.background.get_rect().width * scale_x,
                                 self.background.get_rect().height * scale_y)
        initial_size = pygame.Rect(self.background.get_rect())

        delta_xsize = final_size.width - initial_size.width
        delta_ysize = final_size.height - initial_size.height

        delta_xdist = target.left
        delta_ydist = target.top

        time = 0
        
        while(time < duration):
            clock.tick()
            dt = clock.get_time()
            dxsize = delta_xsize * (float(dt) / duration)
            dysize = delta_ysize * (float(dt) / duration)

            dxdist = delta_xdist * (float(dt) / duration)
            dydist = delta_ydist * (float(dt) / duration)

##            print("delta_xsize: " + str(delta_xsize))
##            print("delta_ysize: " + str(delta_ysize))
##            print("delta_xdist: " + str(delta_xdist))
##            print("delta_ydist: " + str(delta_ydist))
##            print("dt: " + str(dt))
##            print("duration: " + str(duration))
##            print("time: " + str(time))
##            print("dxsize: " + str(dxsize))
##            print("dysize: " + str(dysize))
##            print("dxdist: " + str(dxdist))
##            print("dydist: " + str(dydist))
##            print("scale_x: " + str(scale_x))
##            print("scale_y: " + str(scale_y))

            newbackground = pygame.transform.smoothscale(self.background,
                                                         (self.background.get_rect().width + int(dxsize),
                                                          self.background.get_rect().height + int(dysize)))
##            print("newbackground.rect now (" +
##                  str(newbackground.get_rect().top) + ", " +
##                  str(newbackground.get_rect().left) + ")" +
##                  str(newbackground.get_rect().width) + "x" +
##                  str(newbackground.get_rect().height))

            self.background = pygame.Surface((1092, 780))
            self.background.blit(newbackground, (-dxdist * 10, -dydist * 10))

            self.screen.blit(self.background, (0, 0))
            pygame.display.update()
            time += dt

        self.background = pygame.image.load("mock/level2-background.png")
        self.velocity = Window.VEL_LEVEL2
        self.level = Window.LEVEL2
        self.camera = pygame.math.Vector2(0, -780)

    def move(self, dt):
        self.camera = self.camera + pygame.math.Vector2(self.velocity.x * dt / 1000,
                                                        self.velocity.y * dt / 1000)
        print("camera now: (" + str(self.camera.x) + ", " + str(self.camera.y))
        if self.camera.x < -(3276 - 1080) and self.level == Window.LEVEL2:
            self.velocity.x = 0
            self.camera.x = -(3276 - 1080)
            self.idle = True

        if self.camera.y > 0 and self.level == Window.LEVEL2:
            self.camera.y = 0
            self.velocity.y = 0

        if self.idle:
            self.idle_time += dt
            if self.idle_time > Window.TIME_LEVEL2_WAIT:
                self.idle = False
                self.velocity = Window.VEL_LEVEL2_UP
##            self.time += dt
##            if self.time > Window.TIME_LEVEL2_WAIT:
##                self.velocity.y = Window.VEL_LEVEL2_UP

##        if self.camera.y <= 0 and self.level == Window.LEVEL2:
##            self.camera.x = -(3276 - 1080)
##            self.camera.y = 0
##            self.velocity.y = 0
