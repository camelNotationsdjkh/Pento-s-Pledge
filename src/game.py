#! python3
# game.py
# The place where most of the things of the game happens

import pygame

import constants, levels, animate
from player import Player

pygame.init()

class Game(object):
    def __init__(self):
        """ The game object where most events of the game takes
            place. This includes the menu screen, instructions and
            the actual game. Borrows a lot of the structure that I made
            in my previous game, CamelsVsVultures.
        """
        self.size = pygame.display.set_mode(constants.SCREEN_SIZE)
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(constants.SCREEN_SIZE)
        self.highscore = 0
    
    def play(self):
        player = Player()
        done = False

        # Array to hold the hearts for player health
        lives_image = [
            pygame.image.load("images/heart.png").convert_alpha(),
            pygame.image.load("images/heart.png").convert_alpha(),
            pygame.image.load("images/heart.png").convert_alpha()
        ]

        font_write = pygame.font.SysFont('Arial', 30, True)
        coin = pygame.image.load("images/coin.png")

        # Create all the levels
        level_list = []
        level_list.append(levels.Level_01(player))
        level_list.append(levels.Level_02(player))

        # Set the current level
        current_level_no = 0
        current_level = level_list[current_level_no]
        active_sprite_list = pygame.sprite.Group()
        player.level = current_level

        player.rect.x = current_level.start_pos_x
        player.rect.y = current_level.start_pos_y
        player.rect.y = constants.SCREEN_HEIGHT - player.rect.height
        active_sprite_list.add(player)
        intro = animate.Transition(current_level.intro_text)
        active_sprite_list.add(intro)
        pygame.display.set_caption(constants.WINDOW_TITLE)

        # Make the music
        pygame.mixer.init() # might be unnessary
        pygame.mixer.music.load("music/backgroundmusic01.wav")
        pygame.mixer.music.play(-1)

        # -------- Main Program Loop -----------
        while not done:
            """ Game event handler """
            for event in pygame.event.get(): # User did something
                if event.type == pygame.QUIT: # If user clicked close
                    return True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        player.go_left()
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        player.go_right()
                    elif event.key == pygame.K_UP or event.key == pygame.K_w:
                        player.jump()

                elif event.type == pygame.KEYUP:
                    if (event.key == pygame.K_LEFT or event.key == pygame.K_a) and player.change_x < 0:
                        player.stop()
                    elif (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and player.change_x > 0:
                        player.stop()

            # Update the player.
            active_sprite_list.update()

            # Update items in the level
            current_level.update()

            # Update the intro
            intro.update()

            # If the player gets near the right side, shift the world left (-x)
            if player.rect.x >= 500:
                diff = player.rect.x - 500
                player.rect.x = 500
                current_level.shift_world(-diff)

            # If the player gets near the left side, shift the world right (+x)
            if player.rect.x <= 120:
                diff = 120 - player.rect.x
                player.rect.x = 120
                current_level.shift_world(diff)
            
            # Did the player lose a life and game over if they have no lives left
            if player.lives < len(lives_image): lives_image.pop(0)
            if player.lives == 0: 
                # Game Over screen
                pygame.mixer.music.stop()
                if self.game_over(False): return True
                else: return False

            # If the player hits the gate or the goal of the level
            # Go to next level
            if player.next_level and not player.win:
                current_level_no += 1
                # Checks if player won
                if current_level_no == 2:
                    player.win = True
                    current_level_no -= 1 # To allow the wi screen to show
                player.distance_traveled = 0
                current_level = level_list[current_level_no]
                player.level = current_level
                pygame.mixer.music.stop()

                # Show progress screen
                if self.progress(player.score, current_level.coin_total):
                    # Reset for the new level
                    intro = animate.Transition(current_level.intro_text, current_level.color, current_level.text_color)
                    active_sprite_list.add(intro)
                    player.reset_player()
                    pygame.mixer.music.load(current_level.music)
                    pygame.mixer.music.play(-1)
                else: return True
            
            # If the player wins, go to win screen
            if player.win: 
                pygame.mixer.music.stop()
                if self.game_over(True): return True
                else: return False

            # Deletes the intro after it's over
            if intro.transparency < 0: active_sprite_list.remove(intro)

            # ALL CODE TO DRAW SHOULD GO BELOW THIS COMMENT
            current_level.draw(self.screen)
            active_sprite_list.draw(self.screen)

            if intro.transparency > 180: self.screen.blit(
                intro.text, 
                [(constants.SCREEN_WIDTH // 2) - len(current_level.intro_text) * 10, (constants.SCREEN_HEIGHT // 2) - 30]
                )
            
            # Draws the hearts
            for index, image in enumerate(lives_image): self.screen.blit(image, ((int(index) * 35), 12))

            # Blit the score
            score_text = font_write.render(f"{player.score} / {current_level.coin_total}", True, constants.CONCERET)
            spacing = 850 if player.score < 10 else 840
            self.screen.blit(score_text, (spacing, 12))
            self.screen.blit(coin, (940, 12))
            
            
            # Limit to 60 frames per second
            self.clock.tick(constants.REFRESH_RATE)

            # Go ahead and update the screen with what we've drawn.
            pygame.display.flip()

        pygame.quit()
   
    def instructions(self):
        """ The instruction pages of the game
            Includes the story and movement controls """
        
        done = False
        instruction_page = 0

        # The instruction pages
        background_image = [
            pygame.image.load("images/instructions01.png").convert(),
            pygame.image.load("images/instructions02.png").convert(),
            pygame.image.load("images/instructions03.png").convert(),
            pygame.image.load("images/instructions04.png").convert(),
        ]

        pygame.display.set_caption(constants.WINDOW_TITLE)

        while not done:
            # Event handler
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_KP_ENTER or event.key == pygame.K_RETURN: return False
                    # Change the instruction page
                    elif event.key == pygame.K_n and instruction_page < len(background_image) - 1: instruction_page += 1
                    elif event.key == pygame.K_b and instruction_page != 0: instruction_page -= 1
                    elif event.key == pygame.K_KP_ENTER or event.key == pygame.K_RETURN: return False
                

            # Drawing --------
            self.screen.blit(background_image[instruction_page], [0, 0])

            pygame.display.flip() 

            # Clock Tick ------
            self.clock.tick(constants.REFRESH_RATE)

        pygame.quit()
    
    def progress(self, score, coin_total):
        """ The progress screen to show
            player how well they are doing """

        # The instruction pages
        background_image = pygame.image.load("images/progress_screen.png").convert()
        player_big = pygame.image.load("images/player_big.png").convert_alpha()

        # Keeps track of player position
        player_pos_x = 0

        # Text position
        text_pos = 0

        # Load the font
        font_display = pygame.font.SysFont('Arial', 35, True)

        # Calculate the scores
        self.highscore += score * 125
        level_score = font_display.render(str(score), True, constants.CONCERET)
        score_percent =  font_display.render(f"{((score / coin_total) * 100) // 1}%", True, constants.BLACK)
        highscore = font_display.render(str(self.highscore), True, constants.BLACK)

        pygame.display.set_caption(constants.WINDOW_TITLE)

        while True:
            # Event handler
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_KP_ENTER or event.key == pygame.K_RETURN: return True
            
            # A very simple animation
            if player_pos_x < 650:
                player_pos_x += 10
            
            if text_pos > -10:
                text_pos -= 0.5

            # Drawing --------
            self.screen.blit(background_image, [0, 0])
            self.screen.blit(player_big, [player_pos_x, 200])

            # Draw the scores
            self.screen.blit(level_score, (427, (187 + text_pos)))
            self.screen.blit(score_percent, (276, (246 + text_pos)))
            self.screen.blit(highscore, (270, (332 + text_pos)))


            pygame.display.flip() 

            # Clock Tick ------
            self.clock.tick(constants.REFRESH_RATE)

        pygame.quit()
    
    def reset_game(self):
        """ Resets the game and writes
            player's highscore on a txt
            file """
        
        # Add the score to a new file
        text = f"Highscore: {self.highscore}\n"
        with open("scoresheet/score.txt", "a") as score_file:
            score_file.write(text)

        self.highscore = 0

    def game_over(self, win):
        """ The game over screen if the 
            player runs out of lives """

        # The game over images
        if not win: background_image = pygame.image.load("images/game_over.png").convert()
        else: background_image = pygame.image.load("images/win.png").convert()

        self.reset_game()
        pygame.display.set_caption(constants.WINDOW_TITLE)

        while True:
            # Event handler
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_KP_ENTER or event.key == pygame.K_RETURN: return False

            # Drawing --------
            self.screen.blit(background_image, [0, 0])

            pygame.display.flip() 

            # Clock Tick ------
            self.clock.tick(constants.REFRESH_RATE)

        pygame.quit()

    def menu(self):
        """ The main handler window of the game
            Returns - None, ends program """

        background_image = pygame.image.load("images/menu.png").convert()
        done = False
        pygame.display.set_caption(constants.WINDOW_TITLE)

        while not done:
            # Event handler
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "Thanks for playing!"
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1: done = self.instructions() # Instructions
                    elif event.key == pygame.K_2: done = self.play() # Game
                    elif event.key == pygame.K_3: done = True # Exit

            # Drawing --------
            self.screen.blit(background_image, [0, 0])

            pygame.display.flip() 

            # Clock Tick ------
            self.clock.tick(constants.REFRESH_RATE)
        
        pygame.quit()
