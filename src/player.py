"""
This module is used to hold the Player class. The Player represents the user-
controlled sprite on the screen.
"""
import pygame

import constants

from platforms import MovingPlatform
from spritesheet_functions import SpriteSheet

class Player(pygame.sprite.Sprite):
    """ This class represents the bar at the bottom that the player
    controls. """

    # Player variables
    lives = 3
    score = 0
    next_level = False
    win = False

    # Keeps track of player's position in the world
    distance_traveled = 0

    # -- Attributes
    # Set speed vector of player
    change_x = 0
    change_y = 0

    # This holds all the images for the animated walk left/right
    # of our player
    walking_frames_l = []
    walking_frames_r = []
    walking_frames_climb = []

    # What direction is the player facing?
    direction = "R"

    # List of sprites we can bump against
    level = None

    # Under a ladder?
    is_under = False
    ladder_hit_list = None

    # -- Methods
    def __init__(self):
        """ Constructor function """

        # Call the parent's constructor
        pygame.sprite.Sprite.__init__(self)

        sprite_sheet = SpriteSheet("images/player_walk.png")
        sprite_sheet_02 = SpriteSheet("images/player_climb.png", True)
        # Load all the right facing images into a list
        image = sprite_sheet.get_image(6, 0, 41, 52)
        self.walking_frames_r.append(image)
        image = sprite_sheet.get_image(57, 0, 41, 52)
        self.walking_frames_r.append(image)
        image = sprite_sheet.get_image(107, 0, 41, 52)
        self.walking_frames_r.append(image)
        image = sprite_sheet.get_image(155, 0, 41, 52)
        self.walking_frames_r.append(image)

        # Load all the right facing images, then flip them
        # to face left.
        image = pygame.transform.flip(self.walking_frames_r[0], True, False)
        self.walking_frames_l.append(image)
        image = pygame.transform.flip(self.walking_frames_r[1], True, False)
        self.walking_frames_l.append(image)
        image = pygame.transform.flip(self.walking_frames_r[2], True, False)
        self.walking_frames_l.append(image)
        image = pygame.transform.flip(self.walking_frames_r[3], True, False)
        self.walking_frames_l.append(image)

        # Load the images for climbing
        image = sprite_sheet_02.get_image(0, 0, 44, 57)
        self.walking_frames_climb.append(image)
        image = sprite_sheet_02.get_image(72, 0, 44, 57)
        self.walking_frames_climb.append(image)
        image = sprite_sheet_02.get_image(138, 0, 44, 57)
        self.walking_frames_climb.append(image)
        image = sprite_sheet_02.get_image(206, 0, 44, 57)
        self.walking_frames_climb.append(image)
        image = sprite_sheet_02.get_image(270, 0, 44, 57)
        self.walking_frames_climb.append(image)

        # Resize the images
        for index, image in enumerate(self.walking_frames_r):
                self.walking_frames_r[index] =  pygame.transform.scale(image, (41, 52))

        # Set the image the player starts with
        self.image = self.walking_frames_r[0]

        # Set a referance to the image rect.
        self.rect = self.image.get_rect()

    def update(self):
        """ Move the player. """
        # Gravity
        self.calc_grav()

        # Move left/right
        self.rect.x += self.change_x

        pos = self.rect.x + self.level.world_shift
        pos_y = self.rect.y + self.level.world_shift
        if self.direction == "R" and self.change_x > 0:
            frame = (pos // 20) % len(self.walking_frames_r)
            self.image = self.walking_frames_r[frame]
        elif self.is_under:
            frame = (pos_y // 20) % len(self.walking_frames_climb)
            self.image = self.walking_frames_climb[frame]
        elif self.change_x < 0:
            frame = (pos // 20) % len(self.walking_frames_l)
            self.image = self.walking_frames_l[frame]

        # See if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            # If we are moving right,
            # set our right side to the left side of the item we hit
            if self.change_x > 0:
                self.rect.right = block.rect.left
            elif self.change_x < 0:
                # Otherwise if we are moving left, do the opposite.
                self.rect.left = block.rect.right

        # Move up/down
        self.rect.y += self.change_y

        # Check and see if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:

            # Reset our position based on the top/bottom of the object.
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            elif self.change_y < 0:
                self.rect.top = block.rect.bottom

            # Stop our vertical movement
            self.change_y = 0

            if isinstance(block, MovingPlatform):
                self.rect.x += block.change_x
        
        # See if we any tokens
        token_hit_list = pygame.sprite.spritecollide(self, self.level.token_list, False)
        for token in token_hit_list:
            """ See if we hit any tokens, increase score and remove the token if we do """
            if len(token_hit_list) > 0:
                self.level.token_list.remove(token)
                self.score += 1
        
        # See if we hit any mobs
        mob_hit_list = pygame.sprite.spritecollide(self, self.level.enemy_list, False)
        if len(mob_hit_list) > 0:
            self.lives -= 1
            # Reset player position to begining of the level
            self.reset_pos(self.level.start_pos_x, self.level.start_pos_y)

        # See if we hit the gate (End of the level)
        gate_hit_list = pygame.sprite.spritecollide(self, self.level.gate_list, False)
        if len(gate_hit_list) > 0: 
            self.next_level = True

    def calc_grav(self):
        """ Calculate effect of gravity. """
        self.ladder_hit_list = pygame.sprite.spritecollide(self, self.level.ladder_list, False)
        if len(self.ladder_hit_list) > 0: self.is_under = True
        else: self.is_under = False

        if not self.is_under:
            if self.change_y == 0:
                self.change_y = 1
            else:
                self.change_y += .35

        # See if we are on the ground
        if self.rect.y >= constants.SCREEN_HEIGHT - self.rect.height and self.change_y >= 0:
            self.change_y = 0
            self.rect.y = constants.SCREEN_HEIGHT - self.rect.height

    def jump(self):
        """ Called when user hits 'jump' button. """

        self.rect.y += 2
        platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        self.ladder_hit_list = pygame.sprite.spritecollide(self, self.level.ladder_list, False)
        self.rect.y -= 2

        # If it is ok to jump, set our speed upwards
        if len(platform_hit_list) > 0 or self.rect.bottom >= constants.SCREEN_HEIGHT:
            self.change_y = -5 if self.is_under else -10
        
        # If player is under a ladder, set up speed upwards
        if self.is_under: self.change_y = -5


    # Player-controlled movement:
    def go_left(self):
        """ Called when the user hits the left arrow. """
        self.change_x = -6
        self.direction = "L"

    def go_right(self):
        """ Called when the user hits the right arrow. """
        self.change_x = 6
        self.direction = "R"

    def stop(self):
        """ Called when the user lets off the keyboard. """
        self.change_x = 0
    
    def reset_pos(self, start_pos_x, start_pos_y):
        """ Resets player to starting position """
        self.level.shift_world(self.level.world_shift * -1)
        self.rect.x = start_pos_x
        self.rect.y = start_pos_y

    def reset_player(self):
        """ Resets the player values after each level """
        self.next_level = False
        self.score = 0
        self.rect.x = self.level.start_pos_x
        self.rect.y = self.level.start_pos_y
