import pygame._view

import pygame
from pygame.locals import *

from animation import Animation, PlayOnceAnimation
from block import Block, BreakableBlock, TimedBlock
from chameleon import Chameleon
from chester import Chester
from rotatorblock import RotatorBlock
from inputmanager import InputManager
from logic import LogicManager
from newlevel import NewLevelException, ResetLevelException
from physics import PhysicsEngine
from piston import Piston
from player import Player
from potion import Potion
from staticenemy import StaticEnemy
from trigger import ShutdownTrigger, FireTrigger
from window import Window

def spawn_entities_level_one():
    player = Player("mock/shark-right.png", pygame.math.Vector2(900, 0))

    entities = [
    #    Player("shark-right.png", pygame.math.Vector2(0, 500)),
        player,
        Block("mock/floor.png", pygame.math.Vector2(130, 311)),
        Block("mock/box6x6.png", pygame.math.Vector2(832, 155)),
        Block("mock/box2x4.png", pygame.math.Vector2(702, 207)),
        Block("mock/box1x3.png", pygame.math.Vector2(598, 233)),
        Block("mock/box2x1.png", pygame.math.Vector2(0, 9 * 26 - 1)),
        Block("mock/box1x3.png", pygame.math.Vector2(0, 2 * 26 - 1)),
        Block("mock/box-window.png", pygame.math.Vector2(130, 208)),
        Block("mock/bottom-floor.png", pygame.math.Vector2(0, 29 * 26 - 1)),
        Block("mock/box-trans-3.png", pygame.math.Vector2(17 * 26, 22 * 26 - 1)),
        Block("mock/box-trans-3.png", pygame.math.Vector2(10 * 26, 22 * 26 - 1)),
        Block("mock/box-trans-5.png", pygame.math.Vector2(13 * 26, 19 * 26 - 1)),
        StaticEnemy("mock/coil.png", pygame.math.Vector2(16 * 26 - 13, 19 * 26 - 1), 1),
        Block("mock/stove.png", pygame.math.Vector2(14 * 26, 25 * 26 - 1)),
        Piston("mock/piston.png", pygame.math.Vector2(338, 104)),
        Potion("mock/potion.png", pygame.math.Vector2(832, 140)),
        Potion("mock/potion.png", pygame.math.Vector2(27 * 26, 28 * 26 - 13)),
        ]

    laser = StaticEnemy("mock/laser.png", pygame.math.Vector2(26, 285))
    laser.animation = Animation([
        pygame.image.load("mock/laser.png"),
        pygame.image.load("mock/laser-2.png"),
        pygame.image.load("mock/laser-3.png"),
        ],
                                100)
    entities.append(ShutdownTrigger("mock/trigger.png", pygame.math.Vector2(0, 208),
                                    laser,
                                    entities))
    entities.append(FireTrigger("mock/trigger-left.png",
                                pygame.math.Vector2(14 * 26 - 13, 28 * 26),
                                entities))

    rotator_center = pygame.math.Vector2(6 * 26, 25 * 26 - 1)
    rotator_left = RotatorBlock("mock/rotatorblock.png",
                                pygame.math.Vector2(2 * 25, 25 * 26 - 1),
                                pygame.math.Vector2(rotator_center.x + 13,
                                                    rotator_center.y + 13))
    rotator_top = RotatorBlock("mock/rotatorblock.png",
                                pygame.math.Vector2(5 * 25, 22 * 26 - 1),
                                pygame.math.Vector2(rotator_center.x + 13,
                                                    rotator_center.y + 13))
    rotator_right = RotatorBlock("mock/rotatorblock.png",
                                pygame.math.Vector2(8.5 * 25, 25 * 26 - 1),
                                pygame.math.Vector2(rotator_center.x + 13,
                                                    rotator_center.y + 13))
    rotator_bottom = RotatorBlock("mock/rotatorblock.png",
                                pygame.math.Vector2(5 * 25, 28 * 26 - 1),
                                pygame.math.Vector2(rotator_center.x + 13,
                                                    rotator_center.y + 13))

    entities.append(rotator_left)
    entities.append(rotator_top)
    entities.append(rotator_right)
    entities.append(rotator_bottom)

    doctor_animation = PlayOnceAnimation([
        pygame.image.load("mock/doctor-man.png"),
        pygame.image.load("mock/doctor-man.png"),
        pygame.image.load("mock/doctor-man.png"),
        pygame.image.load("mock/doctor-man.png"),
        pygame.image.load("mock/doctor-man.png"),
        pygame.image.load("mock/doctor-man.png"),
        pygame.image.load("mock/doctor-man.png"),
        pygame.image.load("mock/doctor-man.png"),
        pygame.image.load("mock/doctor-man.png"),
        pygame.image.load("mock/doctor-man.png"),
        pygame.image.load("mock/doctor-man.png"),
        pygame.image.load("mock/doctor-man.png"),
        pygame.image.load("mock/doctor-man.png"),
        pygame.image.load("mock/doctor-man.png"),
        pygame.image.load("mock/doctor-man.png"),
        pygame.image.load("mock/doctor-man.png"),
        pygame.image.load("mock/doctor-man.png"),
        pygame.image.load("mock/doctor-man.png"),
        pygame.image.load("mock/doctor-man.png"),
        pygame.image.load("mock/doctor-man.png"),
        pygame.image.load("mock/doctor-man.png"),
        pygame.image.load("mock/doctor-man.png"),
        pygame.image.load("mock/doctor-man.png"),
        pygame.image.load("mock/doctor-man.png"),
        pygame.image.load("mock/doctor-man.png"),
        pygame.image.load("mock/doctor-man.png"),
        pygame.image.load("mock/doctor-man.png"),
        pygame.image.load("mock/doctor-drink-2.png"),
        pygame.image.load("mock/doctor-drink-3.png"),
        pygame.image.load("mock/doctor-drink-4.png"),
        pygame.image.load("mock/doctor-drink-5.png"),
        pygame.image.load("mock/doctor-drink-6.png"),
        pygame.image.load("mock/box-trans-3.png"),
        ],
                                 100)
    doctor = TimedBlock(doctor_animation, pygame.math.Vector2(25 * 26, 26 * 26), 10000)
    
    entities.append(doctor)

    return entities

def spawn_entities_level_two():
    entities = [
        Player("mock/shark-right.png", pygame.math.Vector2(800, 50 * 26)),
        Block("mock/level2-floor.png", pygame.math.Vector2(0, 59 * 26)),
        Block("mock/box-level2.png", pygame.math.Vector2(624, 1486)),
        Block("mock/box2-level2.png", pygame.math.Vector2(858, 1486)),
        Block("mock/box-level2.png", pygame.math.Vector2(1040, 1486)),
        Block("mock/box3-level2.png", pygame.math.Vector2(1040, 1434)),
        Block("mock/box-level2.png", pygame.math.Vector2(1350, 1486)),
        Block("mock/box2-level2.png", pygame.math.Vector2(1586, 1486)),
        Block("mock/box3-level2.png", pygame.math.Vector2(1586, 1408)),
        Block("mock/box3-level2.png", pygame.math.Vector2(1586, 1330)),
        Block("mock/box2-level2.png", pygame.math.Vector2(1742, 1486)),
        Block("mock/box-level2.png", pygame.math.Vector2(1742, 1408)),
        Block("mock/box3-level2.png", pygame.math.Vector2(1742, 1330)),
        Block("mock/box2-level2.png", pygame.math.Vector2(1534, 1408)),
        Block("mock/box3-level2.png", pygame.math.Vector2(1508, 1486)),
        Block("mock/box-level2.png", pygame.math.Vector2(2054, 1486)),
        Block("mock/box-level2.png", pygame.math.Vector2(2288, 1382)),
        BreakableBlock("mock/beaker.png", pygame.math.Vector2(1260, 700 + 30 * 26)),
        BreakableBlock("mock/beaker.png", pygame.math.Vector2(1350, 1408)),
        BreakableBlock("mock/beaker.png", pygame.math.Vector2(1350, 1330)),
        BreakableBlock("mock/beaker.png", pygame.math.Vector2(2054, 1408)),
        BreakableBlock("mock/beaker.png", pygame.math.Vector2(2288, 1460)),
        Block("mock/tree-platform.png", pygame.math.Vector2(3276 - 10 * 26, 1560 - 3 * 26)),
        Block("mock/tree-platform.png", pygame.math.Vector2(3276 - 7 * 26, 1560 - 6 * 26)),
        Block("mock/tree-platform.png", pygame.math.Vector2(3276 - 6 * 26, 1560 - 9 * 26)),
        Block("mock/tree-platform.png", pygame.math.Vector2(3276 - 3 * 26, 1560 - 11 * 26)),
        Block("mock/tree-platform.png", pygame.math.Vector2(3276 - 9 * 26, 1560 - 14 * 26)),
        Block("mock/tree-platform.png", pygame.math.Vector2(3276 - 10 * 26, 1560 - 17 * 26)),
        Block("mock/tree-platform.png", pygame.math.Vector2(3276 - 12 * 26, 1560 - 20 * 26)),
        Block("mock/tree-platform.png", pygame.math.Vector2(3276 - 6 * 26, 1560 - 23 * 26)),
        Block("mock/tree-platform.png", pygame.math.Vector2(3276 - 5 * 26, 1560 - 26 * 26)),
        Block("mock/tree-platform.png", pygame.math.Vector2(3276 - 10 * 26, 1560 - 28 * 26)),
        Block("mock/tree-platform.png", pygame.math.Vector2(3276 - 13 * 26, 1560 - 22 * 26)),
        Block("mock/tree-platform.png", pygame.math.Vector2(3276 - 16 * 26, 1560 - 25 * 26)),
        Block("mock/tree-platform.png", pygame.math.Vector2(3276 - 16 * 26, 1560 - 31 * 26)),
        Block("mock/tree-platform.png", pygame.math.Vector2(3276 - 19 * 26, 1560 - 34 * 26)),
        Block("mock/tree-platform.png", pygame.math.Vector2(3276 - 21 * 26, 1560 - 37 * 26)),
        Block("mock/tree-platform.png", pygame.math.Vector2(3276 - 22 * 26, 1560 - 40 * 26)),
        Block("mock/tree-platform.png", pygame.math.Vector2(3276 - 17 * 26, 1560 - 45 * 26)),
        Block("mock/tree-platform.png", pygame.math.Vector2(3276 - 19 * 26, 1560 - 44 * 26)),
        Block("mock/tree-platform.png", pygame.math.Vector2(3276 - 12 * 26, 1560 - 36 * 26)),
        Block("mock/box-trans-14.png", pygame.math.Vector2(3276 - 36 * 26, 1565 - 42 * 26)),
        StaticEnemy("mock/screw.png", pygame.math.Vector2(1196, 1512)),
        StaticEnemy("mock/screw.png", pygame.math.Vector2(1235, 1512)),
        StaticEnemy("mock/screw.png", pygame.math.Vector2(1660, 1512)),
        StaticEnemy("mock/screw.png", pygame.math.Vector2(1699, 1512)),
        StaticEnemy("mock/screw.png", pygame.math.Vector2(2522, 1512)),
        StaticEnemy("mock/screw.png", pygame.math.Vector2(2678, 1512)),
        StaticEnemy("mock/screw.png", pygame.math.Vector2(2834, 1512)),
        Chester("mock/chester.png"),
        Chameleon("mock/chameleon.png", pygame.math.Vector2(2350 + 3 * 26, 418)),
        ]

    return entities
    

def main():
    pygame.init()

    window = Window(1092, 780)
    input_m = InputManager()
    physics = PhysicsEngine()
    logic = LogicManager()
    clock = pygame.time.Clock()
    entities = spawn_entities_level_one()
    running = True
    level = 1

    while(running):
        try:
            running = input_m.update()
            clock.tick()
            dt = clock.get_time()
            logic.update(entities, input_m, dt)
            physics.update(entities, dt)
            window.render(entities, dt)
        except NewLevelException:
            window.change_level(clock,
                                pygame.Rect(650, 480, 100, 100),
                                3000)
            entities = spawn_entities_level_two()
            level = 2
        except ResetLevelException:
            if level == 2:
                entities = spawn_entities_level_two()
                window.enter_level2()
            else:
                entities = spawn_entities_level_one()
            

if __name__ == "__main__":
    main()
