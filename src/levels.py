import pygame

import constants
import platforms
import animate
from carrot import Token
from carrot import Gate
from enemy import Mob

class Level():
    """ This is a generic super-class used to define a level.
        Create a child class for each level with level-specific
        info. """

    # Lists of sprites used in all levels. Add or remove
    # lists as needed for your game. """
    platform_list = None
    enemy_list = None
    ladder_list = None
    token_list = None
    gate_list = None

    # Not used in level 1
    background_assets = None

    # Level Music
    music = None

    # Background image
    background = None
    intro_text = None
    coin_total = None

    # How far this world has been scrolled left/right
    world_shift = 0
    level_limit = -1000

    def __init__(self, player):
        """ Constructor. Pass in a handle to player. Needed for when moving platforms
            collide with the player. """
        self.platform_list = pygame.sprite.Group()
        self.ladder_list = pygame.sprite.Group()
        self.token_list = pygame.sprite.Group()
        self.enemy_list = pygame.sprite.Group()
        self.gate_list = pygame.sprite.Group()
        self.background_assets = pygame.sprite.Group()
        self.player = player

    # Update everything on this level
    def update(self):
        """ Update everything in this level."""
        self.platform_list.update()
        self.token_list.update()
        self.enemy_list.update()
        self.ladder_list.update()
        self.background_assets.update()
        self.gate_list.update()

    def draw(self, screen):
        """ Draw everything on this level. """

        # Draw the background
        screen.blit(self.background,(self.world_shift // 3,0))

        # Draw all the sprite lists that we have
        self.background_assets.draw(screen)
        self.token_list.draw(screen)
        self.platform_list.draw(screen)
        self.enemy_list.draw(screen)
        self.ladder_list.draw(screen)
        self.gate_list.draw(screen)

    def shift_world(self, shift_x):
        """ When the user moves left/right and we need to scroll everything: """

        # Keep track of the shift amount
        self.world_shift += shift_x

        # Go through all the sprite lists and shift
        for platform in self.platform_list:
            platform.rect.x += shift_x

        for enemy in self.enemy_list:
            enemy.rect.x += shift_x

        for ladder in self.ladder_list:
            ladder.rect.x += shift_x

        for token in self.token_list:
            token.rect.x += shift_x
        
        for gate in self.gate_list:
            gate.rect.x += shift_x
        
        for asset in self.background_assets:
            asset.rect.x += shift_x

class Level_01(Level):
    """ Definition for level 1. """

    def __init__(self, player):
        """ Create level 1. """

        # Call the parent constructor
        Level.__init__(self, player)

        self.background = pygame.image.load("images/back_01.png").convert()
        self.background.set_colorkey(constants.WHITE)
        self.intro_text = "Dungeon of the Dead"
        self.music = "music/backgroundmusic01.wav"
        self.player = player
        self.start_pos_x = 200
        self.start_pos_y = 500

        # How far the shift_world can go
        self.level_limit = -2500

        # Array with type of platform, and x, y location of the platform.
        level_plat = [ 
                # Platforms
                [platforms.DUNG_PLATFORM_MIDDLE, 500, 500],# platform 3-1h
                [platforms.DUNG_PLATFORM_MIDDLE, 100, 360], # platform 1-2h
                [platforms.DUNG_PLATFORM_MIDDLE, 450, 120], # platform 2-3h
                [platforms.DUNG_PLATFORM_MIDDLE, 850, 180], # platform 1-2h
                [platforms.DUNG_PLATFORM_MIDDLE, 2400, 200], # platform 1-2h
                [platforms.DUNG_PLATFORM_MIDDLE, 2800, 300], # platform 1-2h
                [platforms.DUNG_PLATFORM_MIDDLE, 3200, 350], # platform 1-2h
                [platforms.DUNG_PLATFORM_MIDDLE, 3800, 350], # platform 1-2h
                [platforms.DUNG_PLATFORM_MIDDLE, 4100, 350], # platform 1-2h
                [platforms.DUNG_PLATFORM_MIDDLE, 4400, 350], # platform 1-2h

                # Pillars
                [platforms.DUNG_PLATFORM_PILLAR, 800, 540],
                [platforms.DUNG_PLATFORM_PILLAR, 800, 480],
                [platforms.DUNG_PLATFORM_PILLAR, 800, 420],
                [platforms.DUNG_PLATFORM_PILLAR, 800, 360],
                [platforms.DUNG_PLATFORM_PILLAR, 800, 300],
                [platforms.DUNG_PLATFORM_PILLAR, 800, 240],
                [platforms.DUNG_PLATFORM_PILLAR, 800, 180],
                [platforms.DUNG_PLATFORM_PILLAR, 800, 0],

                [platforms.DUNG_PLATFORM_PILLAR, 2200, 540],
                [platforms.DUNG_PLATFORM_PILLAR, 2200, 480],
                [platforms.DUNG_PLATFORM_PILLAR, 2200, 420],
                [platforms.DUNG_PLATFORM_PILLAR, 2200, 360],
                [platforms.DUNG_PLATFORM_PILLAR, 2200, 300],
                [platforms.DUNG_PLATFORM_PILLAR, 2200, 240],
                [platforms.DUNG_PLATFORM_PILLAR, 2200, 180],
                [platforms.DUNG_PLATFORM_PILLAR, 2200, 0],

                [platforms.DUNG_PLATFORM_PILLAR, 3800, 540],
                [platforms.DUNG_PLATFORM_PILLAR, 3800, 480],
                [platforms.DUNG_PLATFORM_PILLAR, 3800, 420],
                [platforms.DUNG_PLATFORM_PILLAR, 3800, 360],
                [platforms.DUNG_PLATFORM_PILLAR, 3800, 300],
                [platforms.DUNG_PLATFORM_PILLAR, 3800, 240],
                [platforms.DUNG_PLATFORM_PILLAR, 3800, 180],
                [platforms.DUNG_PLATFORM_PILLAR, 3800, 0],
                ]
        
        # Array with all the ladders of the level
        level_lad = [
            [platforms.LADDER_SPRITE, 400, 120],
            [platforms.LADDER_SPRITE, 1160, 330],
            [platforms.LADDER_SPRITE, 1160, 180],
        ]

        # Array with all the coins of the level
        level_coins = [
            Token(100, 550),
            Token(300, 550),
            Token(120, 338),
            Token(470, 98),
            Token(610, 98),
            Token(5000, 576),
            Token(5100, 576)
        ]

        # Adding a straight line of coins
        for i in range(11):
            level_coins.append(Token((900 + i * 120), 576))

        for i in range(4):
            level_coins.append(Token((4000 + i * 160), 328))

        for i in range(4):
            level_coins.append(Token((3950 + i * 160), 576))
        
        for i in range(7):
            level_coins.append(Token((2500 + i * 160), 576))
        
        # Array with all the enemies of the level
        level_enemies = [
            Mob(200, 300, self, "images/skeleton_sheet.png", 100, 370),
            Mob(900, 558, self, "images/wolf_sheet.png", 900, 1400, "wolf"),
            Mob(1400, 558, self, "images/wolf_sheet.png", 1400, 2100, "wolf"),
            Mob(2400, 542, self, "images/goblin_sheet.png", 2400, 2800, "goblin"),
            Mob(2800, 558, self, "images/wolf_sheet.png", 2800, 3500, "wolf"),
            Mob(2790, 245, self, "images/skeleton_sheet.png", 2790, 3050),
            Mob(4100, 558, self, "images/wolf_sheet.png", 4100, 4600, "wolf"),
            Mob(3900, 290, self, "images/skeleton_sheet.png", 3900, 4600),
        ]

        # Go through the array above and add platforms
        for platform in level_plat:
            block = platforms.Platform(platform[0])
            block.rect.x = platform[1]
            block.rect.y = platform[2]
            block.player = self.player
            self.platform_list.add(block)
        
        # Add all the Ladders
        for ladder in level_lad:
            block = platforms.Ladder(ladder[0])
            block.rect.x = ladder[1]
            block.rect.y = ladder[2]
            block.player = self.player
            self.ladder_list.add(block)

        # Add all the tokens
        for coin in level_coins: self.token_list.add(coin)

        # Add all enemies
        for enemy in level_enemies: self.enemy_list.add(enemy)
        self.coin_total = len(level_coins)

        # Only one gate to add per level
        gate = Gate(3870, 520)
        self.gate_list.add(gate)

        # Add a custom moving platform
        # Horizontal
        block = platforms.MovingPlatform(platforms.DUNG_PLATFORM_MIDDLE )
        block.rect.x = 1350
        block.rect.y = 280
        block.boundary_left = 1350
        block.boundary_right = 1900
        block.change_x = 1
        block.player = self.player
        block.level = self
        self.platform_list.add(block)

        # Vertical
        block = platforms.MovingPlatform(platforms.DUNG_DIRT)
        block.rect.x = 3570
        block.rect.y = 300
        block.boundary_top = 100
        block.boundary_bottom = 550
        block.change_y = -1
        block.player = self.player
        block.level = self
        self.platform_list.add(block)

        # Transparent boxes
        """ Boundary boxes to keep player from going off screen """
        box_boundary_left = platforms.Platform(None, False, (50,600))
        box_boundary_left.rect.x = -150
        box_boundary_left.rect.y = 0
        box_boundary_left.image.set_alpha(0)
        self.platform_list.add(box_boundary_left)

        # Top
        box_boundary_top = platforms.Platform(None, False, (4000,5), constants.RED)
        box_boundary_top.rect.x = 0
        box_boundary_top.rect.y = 0
        box_boundary_top.image.set_alpha(0)
        self.platform_list.add(box_boundary_top)

        # Right
        box_boundary_right = platforms.Platform(None, False, (5,600), constants.RED)
        box_boundary_right.rect.x = 5400
        box_boundary_right.rect.y = 0
        box_boundary_right.image.set_alpha(0)
        self.platform_list.add(box_boundary_right)
        
# Create platforms for the level
class Level_02(Level):
    """ Definition for level 2. """

    def __init__(self, player):
        """ Create level 1. """

        # Call the parent constructor
        Level.__init__(self, player)

        self.background = pygame.Surface((constants.SCREEN_WIDTH * 1.8, constants.SCREEN_HEIGHT))
        self.background.fill(constants.SGREEN)
        self.music = "music/backgroundmusic02.wav"
        self.intro_text = "Millow's Forest"
        self.color = constants.SGREEN
        self.text_color = constants.WHITE
        self.player = player
        self.start_pos_x = 120
        self.start_pos_y = 61

        # How far the shift_world can go
        self.level_limit = -1900

        # Array with type of platform, and x, y location of the platform.
        level_plat = [ 
                # Platforms
                [platforms.MG_ROCK_PLAT_LEFT, 0, 113],# platform 3-1h
                [platforms.MG_ROCK_PLAT_LEFT, 534, 303],# platform 3-1h
                [platforms.MG_ROCK_PLAT_LEFT, 1105, 96],# platform 3-1h
                [platforms.MG_ROCK_PLAT_LEFT, 1620, 275],# platform 3-1h
                [platforms.MG_ROCK_PLAT_LEFT, 1710, 275],# platform 3-1h

                # # Pillars
                [platforms.MG_PILLAR_MIDDLE, 800, 540],
                ]

        # The first pillar (left to right)
        for i in range(5):
            level_plat.append([platforms.MG_PILLAR_MIDDLE, 459, (i * 64)])
        
        # The second pillar (left to right)
        for i in range(5):
            level_plat.append([platforms.MG_PILLAR_MIDDLE, 879, (205 + i * 64)])

        # The third pillar (left to right)
        for i in range(5):
            level_plat.append([platforms.MG_PILLAR_MIDDLE, 1296, (i * 64)])
        
        # The ground
        for i in range(21):
            level_plat.append([platforms.MG_ROCK_PLAT_MIDDLE, (-400 + 130 * i), 524])
        
        # Array with all the ladders of the level
        level_lad = [
            [platforms.LADDER_SPRITE, 1573, 282]
        ]

        # Array with all the coins of the level
        level_coins = [
            Token(1110, 73),
            Token(1210, 73),
            Token(560, 280),
            Token(650, 280)
        ]

        # Adding a straight line of coins
        for i in range(6):
            level_coins.append(Token((30 + i * 120), 503))

        for i in range(6):
            level_coins.append(Token((1120 + i * 120), 503))

        for i in range(4):
            level_coins.append(Token(280, (80 + i * 120)))

        for i in range(5):
            level_coins.append(Token(760, (100 + i * 90)))
        
        for i in range(3):
            level_coins.append(Token(989, (100 + i * 140)))
        
        level_images = [
            platforms.BackImage(platforms.MG_FENCE, 400, 500),
            platforms.BackImage(platforms.MG_TREE, 0, 255, True, (149, 273)),
            platforms.BackImage(platforms.MG_BUSH_LEFT, 258, 0),
            platforms.BackImage(platforms.MG_BUSH_RIGHT, 1350, 0),

        ]
        
        # Array with all the enemies of the level
        level_enemies = [
            Mob(112, 464, self, "images/skeleton_sheet.png", 112, 824),
            Mob(1132, 488, self, "images/wolf_sheet.png", 1132, 1860, "wolf")
        ]

        # Go through the array above and add platforms
        for platform in level_plat:
            block = platforms.Platform(platform[0], True, None, constants.BLACK, True)
            block.rect.x = platform[1]
            block.rect.y = platform[2]
            block.player = self.player
            self.platform_list.add(block)
        
        """ The pillar bottoms/tops """
        block = platforms.Platform(platforms.MG_PILLAR_BOTTOM, True, None, constants.BLACK, True, True)
        block.rect.x = 460
        block.rect.y = 314
        block.player = self.player
        self.platform_list.add(block)

        block = platforms.Platform(platforms.MG_PILLAR_BOTTOM, True, None, constants.BLACK, True)
        block.rect.x = 879
        block.rect.y = 147
        block.player = self.player
        self.platform_list.add(block)

        block = platforms.Platform(platforms.MG_PILLAR_BOTTOM, True, None, constants.BLACK, True, True)
        block.rect.x = 1296
        block.rect.y = 314
        block.player = self.player
        self.platform_list.add(block)
        
        # Add all the Ladders
        for ladder in level_lad:
            block = platforms.Ladder(ladder[0])
            block.rect.x = ladder[1]
            block.rect.y = ladder[2]
            block.player = self.player
            self.ladder_list.add(block)

        # Add all the tokens
        for coin in level_coins: self.token_list.add(coin)

        # Add all enemies
        for enemy in level_enemies: self.enemy_list.add(enemy)
        self.coin_total = len(level_coins)

        # Add all the background assets
        for asset in level_images: self.background_assets.add(asset)

        # Only one gate to add per level
        gate = Gate(1800, 220, False, True)
        self.gate_list.add(gate)

        # Add a custom moving platform
        # Vertical 1
        block = platforms.MovingPlatform(platforms.MG_MOVING_GREEN, True, None, constants.BLACK, True)
        block.rect.x = 261
        block.rect.y = 150
        block.boundary_top = 150
        block.boundary_bottom = 475
        block.change_y = -1
        block.player = self.player
        block.level = self
        block.put_on_top = True
        self.platform_list.add(block)

        # Vertical 2
        block = platforms.MovingPlatform(platforms.MG_MOVING_GREEN, True, None, constants.BLACK, True)
        block.rect.x = 740
        block.rect.y = 182
        block.boundary_top = 182
        block.boundary_bottom = 475
        block.change_y = -1
        block.player = self.player
        block.level = self
        block.put_on_top = True
        self.platform_list.add(block)

        # Vertical 3
        block = platforms.MovingPlatform(platforms.MG_MOVING_GREEN, True, None, constants.BLACK, True)
        block.rect.x = 969
        block.rect.y = 400
        block.boundary_top = 182
        block.boundary_bottom = 475
        block.change_y = -1
        block.player = self.player
        block.level = self
        block.put_on_top = True
        self.platform_list.add(block)


        # Transparent boxes
        """ Boundary boxes to keep player from going off screen """
        box_boundary_left = platforms.Platform(None, False, (5,600))
        box_boundary_left.rect.x = 0
        box_boundary_left.rect.y = 0
        box_boundary_left.image.set_alpha(0)
        self.platform_list.add(box_boundary_left)

        # Top
        box_boundary_top = platforms.Platform(None, False, (4000,5), constants.RED)
        box_boundary_top.rect.x = 0
        box_boundary_top.rect.y = 0
        box_boundary_top.image.set_alpha(0)
        self.platform_list.add(box_boundary_top)

        # Right
        box_boundary_right = platforms.Platform(None, False, (5,600), constants.RED)
        box_boundary_right.rect.x = 1870
        box_boundary_right.rect.y = 0
        box_boundary_right.image.set_alpha(0)
        self.platform_list.add(box_boundary_right)
