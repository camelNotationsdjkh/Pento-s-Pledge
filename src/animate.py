#! python3
# animate.py
# A few classes for animation of background elements

import constants, pygame
from spritesheet_functions import SpriteSheet

class Transition(pygame.sprite.Sprite):
    def __init__(self, text, color=constants.BLACK, text_color=constants.WHITE):
        super().__init__()

        """ Intro for each level, reduces the transparentcy
            for the object per cycle to give a fade in effect
            - Written entirely by me
        """

        font = pygame.font.SysFont('Arial', 45, True)
        self.text = font.render(text, True, text_color)
        self.image = pygame.Surface((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
        self.image.fill(color)
        self.transparency = 256
        self.rect = self.image.get_rect()

    def update(self):
        # Slowly makes the image more transparent
        if self.transparency > 200: self.transparency -= 0.5
        elif self.transparency > 0: self.transparency -= 1
        self.image.set_alpha(self.transparency)
