# Space Invaders Project 
# Date October 13, 2024
#--------------------------------------------------------------------------------------------
# Worked together in the project for Space Invaders
# Bernabe Amaya
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
from ai_player import AIPlayer
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

        # Ship & Fleet MUST be created before AIPlayer
        self.ship = Ship(self)  
        self.fleet = Fleet(self)
        self.ship.set_fleet(self.fleet)
        self.ship.set_sb(self.sb)

        # Laser + Barriers
        self.barriers = Barriers(self)
        self.alien_lasers = pg.sprite.Group()

        # SIMPLE AI VERSION – ONLY 4 ARGUMENTS MATCHING YOUR ai_player.py
        self.ai_player = AIPlayer(self.ship, self.fleet, self.alien_lasers, self.barriers)

        self.high_scores = HighScores()
        self.show_high_scores = False

        # UFO setup
        self.ufo = None
        self.ufo_timer = pg.time.get_ticks()

        # Explosion frames
        sprite_sheet = pg.image.load("images/explosion_frames.png").convert_alpha()
        frame_width = 64
        frame_height = 64
        self.explosion_frames = [
            sprite_sheet.subsurface(pg.Rect(n * frame_width, 0, frame_width, frame_height)) 
            for n in range(8)
        ]

        pg.display.set_caption("Alien Invasion")
        self.bg_color = self.settings.bg_color
        self.game_active = False
        self.first = True
        self.play_button = Button(self, "Play")
        self.high_scores_button = Button(self, "High Scores")
        self.event = Event(self)

        # Alien images
        self.alien_images0 = [pg.image.load("images/space_invader_cat.png").subsurface(pg.Rect(0, 0, 80, 80))]
        self.alien_images1 = [pg.image.load("images/space_invader_cat_1.png").subsurface(pg.Rect(0, 0, 80, 80))]
        self.alien_images2 = [pg.image.load("images/space_invader_cat_2.png").subsurface(pg.Rect(0, 0, 80, 80))]
        self.alien_images = [self.alien_images0, self.alien_images1, self.alien_images2]

    # ---------------------------- GAME LOGIC BELOW ------------------------------

    def game_over(self):
        print("Game Over!")
        self.sound.play_gameover()
        sys.exit()

    def ship_hit(self):
        if self.stats.ships_left > 0:
            self.stats.ships_left -= 1
            self.sb.prep_score_level_ships()
            explosion_timer = Timer(images=self.explosion_frames, delta=100, loop_continuously=False)

            while not explosion_timer.finished():
                self.screen.fill(self.bg_color)
                self.screen.blit(explosion_timer.current_image(), self.ship.rect)
                pg.display.flip()

            self.ship.reset_ship()
            self.fleet.reset_fleet()
            self.alien_lasers.empty()
            pg.time.delay(600)
        else:
            if self.stats.score > min(self.high_scores.scores):
                self.high_scores.update_high_scores(self.stats.score)
            self.high_scores.save_high_scores()
            self.game_over()

    def reset_game(self):
        self.stats.reset_stats()
        self.sb.prep_score_level_ships()
        self.game_active = True
        self.sound.play_background()
        self.ship.reset_ship()
        self.fleet.reset_fleet()
        pg.mouse.set_visible(False)
        self.ufo_timer = pg.time.get_ticks()
        self.ufo = None
    
    def fire_random_alien(self):
        if len(self.fleet.aliens) > 0:
            alien = randint(0, len(self.fleet.aliens.sprites()) - 1)
            self.fleet.aliens.sprites()[alien].fire_laser()

    def check_ufo_spawn(self):
        if not self.ufo and pg.time.get_ticks() - self.ufo_timer > 2500 and randint(0, 100) < 10:
            self.ufo = UFO(self)
            self.ufo_timer = pg.time.get_ticks()

    def check_ufo_collision(self):
        if self.ufo and pg.sprite.spritecollideany(self.ufo, self.ship.lasers):
            self.ufo.hit()
            self.stats.score += self.ufo.points
            self.sb.prep_score()

    def check_alien_laser_collision(self):
        if pg.sprite.spritecollideany(self.ship, self.alien_lasers):
            self.ship_hit()

    def check_alien_laser_barrier_collision(self):
        for barrier in self.barriers.barriers:
            collisions = pg.sprite.groupcollide(self.alien_lasers, barrier.barrier_pieces, True, False)
            for piece_list in collisions.values():
                for part in piece_list:
                    part.hit()

    # ---------------------------- RENDERING SCREENS ------------------------------

    def title_screen(self):
        self.screen.fill(self.bg_color)
        font = pg.font.SysFont(None, 100)
        title = font.render("Kitty Invasion!", True, (0, 135, 0))
        rect = title.get_rect(center=self.screen.get_rect().center)
        rect.y -= 200
        self.screen.blit(title, rect)

        self.play_button.rect.y = rect.bottom + 30
        self.high_scores_button.rect.y = self.play_button.rect.bottom + 20

        self.play_button.reset_message("Play")
        self.high_scores_button.reset_message("High Scores")
        self.play_button.draw_button()
        self.high_scores_button.draw_button()

    # ---------------------------- MAIN GAME LOOP ------------------------------

    def run_game(self):
        self.finished = False
        self.first = True
        self.game_active = False

        while not self.finished:
            self.finished = self.event.check_events()

            if not self.game_active:
                self.title_screen()
            else:
                self.screen.fill(self.bg_color)
                self.ship.update()
                self.fleet.update()
                self.barriers.update()
                self.alien_lasers.update()
                self.sb.show_score()

                # AI movement + firing (ONLY if ai_enabled flag)
                if self.settings.ai_enabled:
                    self.ai_player.update()

                self.check_ufo_spawn()
                if self.ufo:
                    self.ufo.update()

                self.check_ufo_collision()
                self.check_alien_laser_collision()
                self.check_alien_laser_barrier_collision()

                self.barriers.draw()

                for laser in self.alien_lasers:
                    laser.draw()

            pg.display.flip()
            self.clock.tick(60)

        sys.exit()


if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()
