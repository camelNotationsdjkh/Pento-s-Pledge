#! python3
# carrot.py

""" The classes for the coins and goal elements in game """
""" Written entirely by me """

import pygame
from spritesheet_functions import SpriteSheet
import platforms

class Token(pygame.sprite.Sprite):
    def __init__(self, x, y):
        """ Generic class for tokens """
        super().__init__()
        self.animation_frames = []
        self.frame_num = 0
        self.total = 0 # Keeps track of total number of frames
        sprite_sheet = SpriteSheet("images/coin_sheet.png", True)

        # Load the coin images
        image = sprite_sheet.get_image(0, 0, 22, 22)
        self.animation_frames.append(image)
        image = sprite_sheet.get_image(0, 22, 22, 22)
        self.animation_frames.append(image)
        image = sprite_sheet.get_image(0, 44, 22, 22)
        self.animation_frames.append(image)
        image = sprite_sheet.get_image(0, 66, 22, 22)
        self.animation_frames.append(image)

        self.image = pygame.image.load("images/coin_sheet.png") # Starting image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    
    def update(self):
        """ Simple animation that goes through the coin sheet """
        if self.frame_num < len(self.animation_frames) - 1:
            self.image = self.animation_frames[self.frame_num]
            self.total += 1
            # Changes the token image if the total frames (60) is divisible by 15, since 60 / 15 = 4
            if self.total < 61 and self.total % 15 == 0: self.frame_num = self.total // 15
        else: 
            self.frame_num = 0
            self.total = 0

class Gate(pygame.sprite.Sprite):
    def __init__(self, x, y, sign=False, king=False):
        """ Class for the gate of the game """
        super().__init__()

        # Load sprite sheet
        sprite_sheet = SpriteSheet("images/sheet.png", True)

        """ Get the image of the gate for the level """
        if sign: self.image = sprite_sheet.get_image(platforms.MG_SIGN[0], platforms.MG_SIGN[1], platforms.MG_SIGN[2], platforms.MG_SIGN[3])
        elif king:
            self.image = sprite_sheet.get_image(platforms.MG_KING[0], platforms.MG_KING[1], platforms.MG_KING[2], platforms.MG_KING[3])
            self.image = pygame.transform.flip(self.image, True, False)
        else: self.image = pygame.transform.scale(pygame.image.load("images/gate.png"), (80, 80))

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    




