# Space Invaders Project 
# Date October 13, 2024
#--------------------------------------------------------------------------------------------
# Worked together in the project for Space Invaders
# Bernabe Amaya CPSC 386-03 18330
#--------------------------------------------------------------------------------------------
# Description
# This project is a recreation of the classic Space Invaders game with a twist.
# Instead of the usual alien invaders, We designed and replaced them with cat-themed sprites.
# The player can shoot lasers to defeat waves of 'alien cats.'
# Additional features include destructible barriers, random UFO appearances,
# and a high score tracking system to keep track of the player's progress.
#--------------------------------------------------------------------------------------------


import sys
import pygame as pg
from settings import Settings
from ship import Ship
from vector import Vector
from fleet import Fleet
from game_stats import GameStats
from button import Button
from barrier import Barriers
from scoreboard import Scoreboard
from event import Event
from sounds import Sound
from ufo import UFO
from random import randint
from high_scores import HighScores
from timer import Timer  # Ensure you have the Timer class


class AlienInvasion:
    def __init__(self):
        pg.init()
        self.clock = pg.time.Clock()
        self.settings = Settings()
        self.screen = pg.display.set_mode(self.settings.w_h)
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)
        self.sound = Sound()
        self.ship = Ship(self)  # Create Ship object
        self.fleet = Fleet(self)
        self.ship.set_fleet(self.fleet)
        self.ship.set_sb(self.sb)
        self.barriers = Barriers(self)
        self.alien_lasers = pg.sprite.Group()  # Group to store alien lasers
        self.high_scores = HighScores()
        self.show_high_scores = False  # Flag to toggle high score screen

        # UFO setup
        self.ufo = None  # UFO starts inactive
        self.ufo_timer = pg.time.get_ticks()  # Initialize UFO timer

        # Load explosion frames for the ship
        sprite_sheet = pg.image.load("images/explosion_frames.png").convert_alpha()
        frame_width = 64  # Adjust based on your explosion frame size
        frame_height = 64
        self.explosion_frames = [sprite_sheet.subsurface(pg.Rect(n * frame_width, 0, frame_width, frame_height)) for n in range(8)]

        pg.display.set_caption("Alien Invasion")
        self.bg_color = self.settings.bg_color
        self.game_active = False
        self.first = True
        self.play_button = Button(self, "Play")
        self.high_scores_button = Button(self, "High Scores")
        self.event = Event(self)
        
        # Load alien images
        self.alien_images0 = [pg.image.load(f"images/space_invader_cat.png").subsurface(pg.Rect(n * 80, 0, 80, 80)) for n in range(1)]
        self.alien_images1 = [pg.image.load(f"images/space_invader_cat_1.png").subsurface(pg.Rect(n * 80, 0, 80, 80)) for n in range(1)]
        self.alien_images2 = [pg.image.load(f"images/space_invader_cat_2.png").subsurface(pg.Rect(n * 80, 0, 80, 80)) for n in range(1)]
        self.alien_images = [self.alien_images0, self.alien_images1, self.alien_images2]

    def game_over(self):
        print("Game Over!")
        self.sound.play_gameover()
        sys.exit()

    def ship_hit(self):
        """Handle what happens when the ship gets hit by an alien laser."""
        if self.stats.ships_left > 0:
            # Decrement ships left
            self.stats.ships_left -= 1

            # Update scoreboard with the new ship count
            self.sb.prep_score_level_ships()

            # Play explosion animation for the ship
            explosion_timer = Timer(images=self.explosion_frames, delta=100, loop_continuously=False)
            while not explosion_timer.finished():
                self.screen.fill(self.bg_color)
                self.screen.blit(explosion_timer.current_image(), self.ship.rect)
                pg.display.flip()

            # Reset the game state after explosion
            self.ship.reset_ship()
            self.fleet.reset_fleet()
            self.alien_lasers.empty()

            # Pause briefly
            pg.time.delay(1000)
        else:
            # Game over, check for new high score
            if self.stats.score > min(self.high_scores.scores):
                self.high_scores.update_high_scores(self.stats.score)
            self.high_scores.save_high_scores()  # Save the scores to the JSON file
            self.game_over()

    def reset_game(self):
        """Reset the game when the player hits play and start background music."""
        self.stats.reset_stats()
        self.sb.prep_score_level_ships()
        self.game_active = True
        self.sound.play_background()  # Play the normal-speed background music
        self.ship.reset_ship()
        self.fleet.reset_fleet()
        pg.mouse.set_visible(False)

        # Reset UFO spawn timer
        self.ufo_timer = pg.time.get_ticks()
        self.ufo = None  # Reset UFO at the beginning of the game
    
    def calculate_alien_speed(self):
        """Calculate new alien speed based on the number of remaining aliens."""
        remaining_aliens = len(self.fleet.aliens)
        if remaining_aliens > 0:
            threshold = int(self.settings.total_aliens * 0.3)  # Set the threshold to 30%
            if remaining_aliens <= threshold:
                # Speed up when below threshold
                self.settings.alien_speed_factor = self.settings.initial_alien_speed_factor * 2.0
                # Switch to fast music
                if not self.sound.fast_music_playing:
                    self.sound.play_music_fast()
            else:
                # Use default speed if above threshold
                self.settings.alien_speed_factor = self.settings.initial_alien_speed_factor
                # Switch back to normal music
                if self.sound.fast_music_playing:
                    self.sound.stop_music_fast()
                    self.sound.play_background()

    def fire_random_alien(self):
        """Randomly select one alien to fire a laser."""
        random_alien = randint(0, len(self.fleet.aliens.sprites()) - 1)  # Choose a random alien
        alien = self.fleet.aliens.sprites()[random_alien]  # Get the alien
        alien.fire_laser()  # Make the chosen alien fire a laser

    def start_new_level(self):
        """Start a new level by resetting aliens and UFO spawn timer."""
        self.stats.level += 1
        self.sb.prep_level()
        self.fleet.create_fleet()
        self.ship.reset_ship()
        self.ship.lasers.empty()

        # Reset UFO and speed
        self.ufo_timer = pg.time.get_ticks()
        self.ufo = None
        self.settings.alien_speed_factor = self.settings.initial_alien_speed_factor  # Reset speed

    def check_ufo_spawn(self):
        """Random chance to spawn the UFO at random intervals."""
        current_time = pg.time.get_ticks()

        # 5-second cooldown with a 0.5% chance of spawning the UFO
        if not self.ufo and current_time - self.ufo_timer > 2000 and randint(0, 100) < 20:
            print("UFO spawned!") #debugging output
            self.ufo = UFO(self)  # Spawn a new UFO
            self.ufo_timer = current_time  # Reset the UFO spawn timer

    def check_ufo_collision(self):
        """Check for collisions between lasers and the UFO."""
        if self.ufo and pg.sprite.spritecollideany(self.ufo, self.ship.lasers):
            self.ufo.hit()  # Trigger explosion for UFO
            self.stats.score += self.ufo.points  # Add points for destroying the UFO
            self.sb.prep_score()  # Update the score on the scoreboard
    
    def check_alien_laser_collision(self):
        """Check if any alien lasers hit the ship."""
        if pg.sprite.spritecollideany(self.ship, self.alien_lasers):
            self.ship_hit()  # Handle ship being hit by an alien laser

    def check_alien_laser_barrier_collision(self):
        """Check if alien lasers hit the barriers."""
        for barrier in self.barriers.barriers:  # Loop through all barriers in the Barriers group
            collisions = pg.sprite.groupcollide(self.alien_lasers, barrier.barrier_pieces, True, False)
            for barrier_piece in collisions.values():
                for b in barrier_piece:
                    b.hit()  # Reduce the barrier piece's health

    def title_screen(self):
        """Display the title screen with buttons and alien images."""
        self.screen.fill(self.bg_color)
        
        # Draw title
        font = pg.font.SysFont(None, 100)
        title_text = font.render("Kitty Invasion!", True, (0, 135, 0))
        title_rect = title_text.get_rect(center=self.screen.get_rect().center)
        title_rect.y -= 200  # Position the title higher
        self.screen.blit(title_text, title_rect)
        
        # Adjust button positions
        self.play_button.rect.y = self.screen.get_rect().center[1] - 100  # Move the Play button up
        self.high_scores_button.rect.y = self.play_button.rect.bottom + 20  # Place High Scores button below Play button

        # Reset button messages to ensure the text is correct
        self.play_button.reset_message("Play")
        self.high_scores_button.reset_message("High Scores")

        # Draw buttons
        self.play_button.draw_button()
        self.high_scores_button.draw_button()

        # Calculate total width of alien images
        alien_width = self.alien_images0[0].get_width()
        total_width = 3 * alien_width + 2 * 20  # 3 images with 20 pixels padding between them

        # Center the alien images on the screen
        x_offset = (self.screen.get_width() - total_width) // 2
        y_offset = self.high_scores_button.rect.bottom + 50  # Position below the buttons

        # Display alien images side by side
        for i, alien_set in enumerate([self.alien_images0, self.alien_images1, self.alien_images2]):
            self.screen.blit(alien_set[0], (x_offset + i * (alien_width + 20), y_offset))
    
    def high_scores_screen(self):
        """Display the high scores."""
        self.screen.fill(self.bg_color)

        # Move the "HIGH SCORES" title up more
        font = pg.font.SysFont(None, 100)
        high_scores_title = font.render("HIGH SCORES", True, (0, 135, 0))
        title_rect = high_scores_title.get_rect(center=self.screen.get_rect().center)
        title_rect.y -= 350  # Move title up more
        self.screen.blit(high_scores_title, title_rect)

        # Display the top 10 scores, center them better
        font = pg.font.SysFont(None, 48)
        for i, score in enumerate(self.high_scores.scores):
            score_str = f"{i + 1}. {score:,}"
            score_image = font.render(score_str, True, (255, 255, 255))
            score_rect = score_image.get_rect(center=self.screen.get_rect().center)
            
            # Adjust y-offset to better center the scores vertically
            score_rect.y += i * 50 - 225  # Adjust this value to fine-tune positioning
            self.screen.blit(score_image, score_rect)

        # Display return button
        self.play_button.rect.y = self.screen.get_rect().bottom - 100
        self.play_button.reset_message("Return to Title")
        self.play_button.draw_button()

    def run_game(self):
        self.finished = False
        self.first = True
        self.game_active = False
        self.show_high_scores = False  # Flag to indicate high score screen

        while not self.finished:
            self.finished = self.event.check_events()

            if self.show_high_scores:
                # Show high scores screen when the flag is set
                self.high_scores_screen()
            elif not self.game_active:
                # Display the title screen if the game is not active
                self.title_screen()
            else:
                # Normal game rendering
                self.screen.fill(self.bg_color)
                self.ship.update()
                self.fleet.update()
                self.sb.show_score()
                self.barriers.update()
                self.alien_lasers.update()

                # Check if UFO should appear
                self.check_ufo_spawn()

                if self.ufo:
                    self.ufo.update()

                self.check_ufo_collision()
                self.check_alien_laser_collision()
                self.check_alien_laser_barrier_collision()

                # Draw everything
                self.barriers.draw()
                for laser in self.alien_lasers:
                    laser.draw()

            # Draw the play and high scores button if the game is not active and high scores screen is not shown
            if not self.game_active and not self.show_high_scores:
                self.play_button.draw_button()
                self.high_scores_button.draw_button()

            pg.display.flip()
            self.clock.tick(60)

        sys.exit()


if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()
