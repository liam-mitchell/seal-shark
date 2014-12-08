import pygame

class Window(object):
    # Responsible for drawing objects and background on the screen
    # Member variables:
    #   screen: drawing window obtained with pygame.display.set_mode()
    #   background: pygame surface with background image
    def __init__(self, width, height):
        self.screen = pygame.display.set_mode([width, height]);
        self.background = pygame.image.load("mock/level1-background.png")
        self.screen.blit(self.background, (0,0))

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
        self.screen.blit(self.background, (0,0))

        for e in entities:
            self.screen.blit(e.animation.next_frame(dt),
                             (e.position.x, e.position.y))

        pygame.display.update()
