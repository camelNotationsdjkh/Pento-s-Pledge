#! python3
# enemy.py

""" The class for the enemies of the game """

import pygame, constants, random
from spritesheet_functions import SpriteSheet

class Mob(pygame.sprite.Sprite):
    def __init__(self, x, y, level, mob_sheet, bounds_left, bounds_right, type="skeleton"):
        """ Generic class for mobs """
        super().__init__()

        """ Using the animation code from the Player and MovingPlatform classes """
        self.walking_frames_l = []
        self.walking_frames_r = []
        self.direction = "R" # direction to start off in
        self.boundary_left = bounds_left
        self.boundary_right = bounds_right
        self.change_x = random.randint(2, 5) # Random Speed

        sprite_sheet = SpriteSheet(mob_sheet, True)
        # Load images based on type of the monster
        if type == "skeleton":
            """ Skeleton images, 9 frames """ 
            image = sprite_sheet.get_image(16, 0, 37, 46)
            self.walking_frames_r.append(image)
            image = sprite_sheet.get_image(81, 0, 34, 46)
            self.walking_frames_r.append(image)
            image = sprite_sheet.get_image(146, 0, 34, 46)
            self.walking_frames_r.append(image)
            image = sprite_sheet.get_image(211, 0, 34, 46)
            self.walking_frames_r.append(image)
            image = sprite_sheet.get_image(274, 0, 34, 46)
            self.walking_frames_r.append(image)
            image = sprite_sheet.get_image(335, 0, 34, 46)
            self.walking_frames_r.append(image)
            image = sprite_sheet.get_image(401, 0, 34, 46)
            self.walking_frames_r.append(image)
            image = sprite_sheet.get_image(465, 0, 34, 46)
            self.walking_frames_r.append(image)
            image = sprite_sheet.get_image(528, 0, 34, 46)
            self.walking_frames_r.append(image)

            # Make the images bigger
            for index, image in enumerate(self.walking_frames_r):
                self.walking_frames_r[index] =  pygame.transform.scale(image, (45, 60))

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
            image = pygame.transform.flip(self.walking_frames_r[4], True, False)
            self.walking_frames_l.append(image)
            image = pygame.transform.flip(self.walking_frames_r[5], True, False)
            self.walking_frames_l.append(image)
            image = pygame.transform.flip(self.walking_frames_r[6], True, False)
            self.walking_frames_l.append(image)
            image = pygame.transform.flip(self.walking_frames_r[7], True, False)
            self.walking_frames_l.append(image)
            image = pygame.transform.flip(self.walking_frames_r[8], True, False)
            self.walking_frames_l.append(image)

        elif type == "wolf":
            """ Wolf images, 5 frames """
            image = sprite_sheet.get_image(0, 0, 62, 32)
            self.walking_frames_r.append(image)
            image = sprite_sheet.get_image(64, 0, 62, 32)
            self.walking_frames_r.append(image)
            image = sprite_sheet.get_image(128, 0, 62, 32)
            self.walking_frames_r.append(image)
            image = sprite_sheet.get_image(192, 0, 62, 32)
            self.walking_frames_r.append(image)
            image = sprite_sheet.get_image(256, 0, 62, 32)
            self.walking_frames_r.append(image)

            # Make the images bigger
            for index, image in enumerate(self.walking_frames_r):
                self.walking_frames_r[index] =  pygame.transform.scale(image, (80, 40))

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
            image = pygame.transform.flip(self.walking_frames_r[4], True, False)
            self.walking_frames_l.append(image)

        else:
            """ Goblin images, 6 frames """
            image = sprite_sheet.get_image(0, 0, 40, 53)
            self.walking_frames_r.append(image)
            image = sprite_sheet.get_image(63, 0, 40, 53)
            self.walking_frames_r.append(image)
            image = sprite_sheet.get_image(128, 0, 40, 53)
            self.walking_frames_r.append(image)
            image = sprite_sheet.get_image(192, 0, 40, 53)
            self.walking_frames_r.append(image)
            image = sprite_sheet.get_image(253, 0, 40, 53)
            self.walking_frames_r.append(image)

            # Make the images bigger
            for index, image in enumerate(self.walking_frames_r):
                self.walking_frames_r[index] =  pygame.transform.scale(image, (50, 60))

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
            image = pygame.transform.flip(self.walking_frames_r[4], True, False)
            self.walking_frames_l.append(image)
       
        self.image = pygame.image.load("images/coin_sheet.png") # Starting image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.level = level
    
    def update(self):
        """ Updates enemies to move left or right """

        self.rect.x += self.change_x
        pos = self.rect.x - self.level.world_shift
        if pos < self.boundary_left or pos > self.boundary_right:
            self.change_x *= -1
            # Changes direction based on change_x value
            if self.change_x < 0: self.direction = "L"
            else: self.direction = "R"
        
        # Animates the mob
        if self.direction == "R":
            frame = (pos // 20) % len(self.walking_frames_r)
            self.image = self.walking_frames_r[frame]
        else:
            frame = (pos // 20) % len(self.walking_frames_l)
            self.image = self.walking_frames_l[frame]
        


