import pygame as pg
from vector import Vector
from point import Point
from laser import Laser
from time import sleep
from pygame.sprite import Sprite
from sounds import Sound
from timer import Timer

class Ship(Sprite):
    def __init__(self, ai_game):
        """Initialize the ship and set its starting position."""
        super().__init__()
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.stats = ai_game.stats
        self.screen_rect = ai_game.screen.get_rect()
        self.sound = Sound()

        # Load the ship image and get its rect.
        self.image = pg.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()

        # Start each new ship at the bottom center of the screen.
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        # Explosion sprite sheet loading
        sprite_sheet = pg.image.load('images/explosion_frames.png').convert_alpha()
        frame_width = 64
        frame_height = 64
        self.explosion_frames = [sprite_sheet.subsurface(pg.Rect(n * frame_width, 0, frame_width, frame_height)) for n in range(8)]

        self.explosion_timer = None
        self.alive = True

        # Velocity vector
        self.v = Vector(0, 0)

        # Lasers
        self.lasers = pg.sprite.Group()
        self.firing = False
        self.fleet = None

    def set_fleet(self, fleet):
        self.fleet = fleet

    def set_sb(self, sb):
        self.sb = sb

    def reset_ship(self):
        self.lasers.empty()
        self.center_ship()
        self.alive = True
        self.image = pg.image.load('images/ship.bmp')
        self.explosion_timer = None

    def center_ship(self):
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def bound(self):
        self.x = max(0, min(self.x, self.screen_rect.width - self.rect.width))
        self.y = max(0, min(self.y, self.screen_rect.height - self.rect.height))

    def ship_hit(self):
        self.stats.ships_left -= 1
        print(f"Only {self.stats.ships_left} ships left now")
        self.sound.play_explosion()
        explosion_timer = Timer(images=self.ai_game.explosion_frames, delta=100, loop_continuously=False)

        while not explosion_timer.finished():
            self.screen.blit(explosion_timer.current_image(), self.rect)
            pg.display.flip()

        self.sb.prep_ships()

        if self.stats.ships_left <= 0:
            self.ai_game.game_over()
            return

        self.lasers.empty()
        self.fleet.aliens.empty()
        self.center_ship()
        self.fleet.create_fleet()
        sleep(0.5)

    def fire_laser(self):
        """Fire a laser if limit not reached."""
        if len(self.lasers) < self.settings.lasers_allowed:
            new_laser = Laser(self.ai_game, self.rect.midtop, direction="up", laser_type="ship")
            self.lasers.add(new_laser)

    def open_fire(self):
        self.firing = True 

    def cease_fire(self):
        self.firing = False

    def update(self):
        if self.alive:
            self.x += self.v.x
            self.y += self.v.y
            self.bound()

            if self.firing:
                self.fire_laser()

            self.lasers.update()

            for laser in self.lasers.copy():
                if laser.rect.bottom <= 0:
                    self.lasers.remove(laser)

            for laser in self.lasers.sprites():
                laser.draw()

            self.draw()

        else:
            if self.explosion_timer and not self.explosion_timer.finished():
                self.image = self.explosion_timer.current_image()
            elif self.explosion_timer and self.explosion_timer.finished():
                self.reset_ship()
                self.fleet.create_fleet()
                sleep(0.5)

    def draw(self):
        self.rect.x, self.rect.y = self.x, self.y
        self.screen.blit(self.image, self.rect)

    # Add these three AI methods
    def move_right(self):
        if self.rect.right < self.screen_rect.right:
            self.v.x = self.settings.ship_speed

    def move_left(self):
        if self.rect.left > 0:
            self.v.x = -self.settings.ship_speed

    #def fire_bullet(self):
    #    """Fire a bullet if limit not reached."""
     #   if len(self.lasers) < self.settings.bullets_allowed:
      #      self.sound.play_laser()
       #     new_laser = self.Laser(self)
        #    self.lasers.add(new_laser)
         #   self.sound.play_

    def stop(self):
        self.v.x = 0

def main():
    print('\n*** message from ship.py --- run from alien_invasions.py\n')

if __name__ == "__main__":
    main()
