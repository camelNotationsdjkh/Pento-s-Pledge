"""
Module for managing platforms.
"""
import pygame

import constants
from spritesheet_functions import SpriteSheet

# These constants define our platform types:
#   Name of file
#   X location of sprite
#   Y location of sprite
#   Width of sprite
#   Height of sprite

""" Put these constants here instead of
    constants.py because it's easier to
    manage that way """

# Level 1 assets
DUNG_PLATFORM_MIDDLE   = (0, 0, 300, 80)
DUNG_PLATFORM_PILLAR   = (0, 140, 50, 60)
LADDER_SPRITE          = (422, 238, 40, 172)
DUNG_SLIVER            = (195, 147, 107, 55)
DUNG_DIRT              = (60, 84, 125, 53)

# Level two assets
MG_ROCK_PLAT_LEFT      = (608, 0, 159, 80)
MG_ROCK_PLAT_MIDDLE    = (608, 0, 136, 80)
MG_GREEN_PLAT          = (414, 0, 173, 36)
MG_FLOWER_01           = (837, 333, 38, 24)
MG_FLOWER_02           = (837, 386, 38, 24)
MG_FENCE               = (844, 146, 141, 34)
MG_PILLAR_MIDDLE       = (766, 54, 61, 66)
MG_PILLAR_BOTTOM       = (766, 0, 61, 66)
MG_MOVING_GREEN        = (472, 59, 114, 60)
MG_TREE                = (130, 0, 268, 471)
MG_BUSH_LEFT           = (995, 189, 205, 128)
MG_BUSH_RIGHT          = (998, 342, 199, 124)

# King
MG_KING                = (1006, 8, 41, 54)


class Platform(pygame.sprite.Sprite):
    """ Platform the user can jump on """

    def __init__(self, sprite_sheet_data, is_image=True, surface_box=None, color=constants.BLACK, mg_sheet=False, flip=False):
        """ Platform constructor. Assumes constructed with user passing in
            an array of 5 numbers like what's defined at the top of this
            code. """
        pygame.sprite.Sprite.__init__(self)

        # Load the sprite sheet for the platforms (level 1 has a different one)
        sprite_sheet = SpriteSheet("images/special_sprites.png") if not mg_sheet else SpriteSheet("images/sheet.png", True) 

        # Grab the image for this platform
        if is_image: self.image = sprite_sheet.get_image(
                                            sprite_sheet_data[0],
                                            sprite_sheet_data[1],
                                            sprite_sheet_data[2],
                                            sprite_sheet_data[3])
        else:
            self.image = pygame.Surface(surface_box)
            self.image.fill(color)
        
        if flip:
            self.image = pygame.transform.flip(self.image, False, True)

        self.rect = self.image.get_rect()

class MovingPlatform(Platform):
    """ This is a fancier platform that can actually move. """

    change_x = 0
    change_y = 0

    boundary_top = 0
    boundary_bottom = 0
    boundary_left = 0
    boundary_right = 0
    put_on_top = False

    level = None
    player = None

    def update(self):
        """ Move the platform.
            If the player is in the way, it will shove the player
            out of the way. This does NOT handle what happens if a
            platform shoves a player into another object. Make sure
            moving platforms have clearance to push the player around
            or add code to handle what happens if they don't. """

        # Move left/right
        self.rect.x += self.change_x

        # See if we hit the player
        hit = pygame.sprite.collide_rect(self, self.player)
        if hit:
            # We did hit the player. Shove the player around and
            # assume he/she won't hit anything else.

            # If we are moving right, set our right side
            # to the left side of the item we hit
            if self.change_x < 0:
                self.player.rect.right = self.rect.left
            else:
                # Otherwise if we are moving left, do the opposite.
                self.player.rect.left = self.rect.right

        # Move up/down
        self.rect.y += self.change_y

        # Check and see if we hit the player
        hit = pygame.sprite.collide_rect(self, self.player)
        if hit:
            # We did hit the player. Shove the player around and
            # assume he/she won't hit anything else.
            
            # Reset our position based on the top/bottom of the object.
            if self.change_y < 0:
                self.player.rect.bottom = self.rect.top
            else:
                if self.put_on_top: self.player.rect.bottom = self.rect.top
                else: self.player.rect.top = self.rect.bottom

        # Check the boundaries and see if we need to reverse
        # direction.
        if self.rect.bottom > self.boundary_bottom or self.rect.top < self.boundary_top:
            self.change_y *= -1

        cur_pos = self.rect.x - self.level.world_shift
        if cur_pos < self.boundary_left or cur_pos > self.boundary_right:
            self.change_x *= -1

class Ladder(pygame.sprite.Sprite):
    """ A ladder for the user to climb """

    def __init__(self, sprite_sheet_data, player=None):
        super().__init__()

        # Get the ladder sprite image
        ladder = SpriteSheet("images/sheet.png", True)
        self.player = player
        self.image = ladder.get_image(
            sprite_sheet_data[0],
            sprite_sheet_data[1],
            sprite_sheet_data[2],
            sprite_sheet_data[3]
        )
        self.rect = self.image.get_rect()

class BackImage(pygame.sprite.Sprite):
    """ A simple image object used just for decoration
        Written by entirely by me """

    def __init__(self, sprite_sheet_data, x, y, scale=False, scale_size=None):
        super().__init__()

        # The images from the sprite sheet
        only_images = SpriteSheet("images/sheet.png", True)
        self.image = only_images.get_image(
            sprite_sheet_data[0],
            sprite_sheet_data[1],
            sprite_sheet_data[2],
            sprite_sheet_data[3]
        )

        # Scale the image if needed
        if scale:
            self.image = pygame.transform.scale(self.image, scale_size)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    
