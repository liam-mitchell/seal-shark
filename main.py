import pygame
from pygame.locals import *

from block import Block
from rotatorblock import RotatorBlock
from inputmanager import InputManager
from logic import LogicManager
from physics import PhysicsEngine
from piston import Piston
from player import Player
from staticenemy import StaticEnemy
from trigger import ShutdownTrigger
from window import Window

def main():
    pygame.init()

    window = Window(1092, 780)
    input_m = InputManager()
    physics = PhysicsEngine()
    logic = LogicManager()
    clock = pygame.time.Clock()

    entities = [
    #    Player("shark-right.png", pygame.math.Vector2(0, 500)),
        Player("mock/shark-right.png", pygame.math.Vector2(900, 0)),
        Block("mock/floor.png", pygame.math.Vector2(130, 311)),
        Block("mock/box6x6.png", pygame.math.Vector2(832, 155)),
        Block("mock/box2x4.png", pygame.math.Vector2(702, 207)),
        Block("mock/box1x3.png", pygame.math.Vector2(598, 233)),
        Block("mock/box2x1.png", pygame.math.Vector2(0, 9 * 26 - 1)),
        Block("mock/box1x3.png", pygame.math.Vector2(0, 2 * 26 - 1)),
        Block("mock/box-window.png", pygame.math.Vector2(130, 208)),
        Block("mock/bottom-floor.png", pygame.math.Vector2(0, 29 * 26 - 1)),
        Piston("mock/piston.png", pygame.math.Vector2(338, 156)),
        ]

    entities.append(ShutdownTrigger("mock/trigger.png", pygame.math.Vector2(0, 208),
                                    StaticEnemy("mock/laser.png", pygame.math.Vector2(26, 285)),
                                    entities))

    rotator_center = Block("mock/box1x1.png", pygame.math.Vector2(8 * 26, 25 * 26 - 1))
    rotator_left = RotatorBlock("mock/rotatorblock.png",
                                pygame.math.Vector2(4 * 25, 25 * 26 - 1),
                                pygame.math.Vector2(rotator_center.position.x + 13,
                                                    rotator_center.position.y + 13))
    rotator_top = RotatorBlock("mock/rotatorblock.png",
                                pygame.math.Vector2(7 * 25, 22 * 26 - 1),
                                pygame.math.Vector2(rotator_center.position.x + 13,
                                                    rotator_center.position.y + 13))
    rotator_right = RotatorBlock("mock/rotatorblock.png",
                                pygame.math.Vector2(10.5 * 25, 25 * 26 - 1),
                                pygame.math.Vector2(rotator_center.position.x + 13,
                                                    rotator_center.position.y + 13))
    rotator_bottom = RotatorBlock("mock/rotatorblock.png",
                                pygame.math.Vector2(7 * 25, 28 * 26 - 1),
                                pygame.math.Vector2(rotator_center.position.x + 13,
                                                    rotator_center.position.y + 13))

    entities.append(rotator_center)
    entities.append(rotator_left)
    entities.append(rotator_top)
    entities.append(rotator_right)
    entities.append(rotator_bottom)

    running = True

    while(running):
        running = input_m.update()

        clock.tick()
        dt = clock.get_time()

        logic.update(entities, input_m, dt)
        physics.update(entities, dt)
        window.render(entities, dt)

if __name__ == "__main__":
    main()
