import pygame as pg
from vector import Vector
from point import Point
from laser import Laser
from pygame.sprite import Sprite
from timer import Timer
from random import randint

class Alien(Sprite):
    # Load images for the different alien types
    # We will now load only the three cat alien types
    # Load first cat alien type
    alien_images0 = [pg.image.load(f"images/space_invader_cat.png").subsurface(pg.Rect(n * 80, 0, 80, 80)) for n in range(7)]
    
    # Load second cat alien type
    alien_images1 = [pg.image.load(f"images/space_invader_cat_1.png").subsurface(pg.Rect(n * 80, 0, 80, 80)) for n in range(7)]
    
    # Load third cat alien type
    alien_images2 = [pg.image.load(f"images/space_invader_cat_2.png").subsurface(pg.Rect(n * 80, 0, 80, 80)) for n in range(7)]
    
    # Combine all three cat alien image sets
    alien_images = [alien_images0, alien_images1, alien_images2]

    def __init__(self, ai_game, v, alien_type=0):
        super().__init__()
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.v = v
        self.type = alien_type

        # Ensure we don't use an invalid alien_type
        if self.type >= len(Alien.alien_images):
            self.type = 0  # Default to the first cat alien

        # Load explosion frames from the explosion sprite sheet
        sprite_sheet = pg.image.load("images/explosion_frames.png").convert_alpha()
        frame_width = 64
        frame_height = 64
        self.explosion_frames = [sprite_sheet.subsurface(pg.Rect(n * frame_width, 0, frame_width, frame_height)) for n in range(8)]

        # Set the initial animation to the alien's normal frames
        self.alive = True
        self.timer = Timer(images=Alien.alien_images[self.type], delta=200, loop_continuously=True)
        self.image = self.timer.current_image()
        self.rect = self.image.get_rect()

        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        # Laser cooldown timer attributes
        self.laser_cooldown = 2000  # Cooldown of 2 seconds
        self.last_shot_time = pg.time.get_ticks()

    def hit(self):
        """Handle being hit by a laser or bullet."""
        self.alive = False
        self.timer = Timer(images=self.explosion_frames, delta=100, loop_continuously=False)
        self.ai_game.sound.play_killedSpaceInvader()
        self.ai_game.calculate_alien_speed()

    def check_edges(self):
        """Return True if alien is at edge of screen."""
        sr = self.screen.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        return self.x + self.rect.width >= sr.right or self.x <= 0

    def fire_laser(self):
        """Fire a laser downwards from the alien if cooldown has passed."""
        current_time = pg.time.get_ticks()
        if current_time - self.last_shot_time > self.laser_cooldown:
            print(f"Alien at position {self.rect.midbottom} is firing!")  # Debugging output
            new_laser = Laser(self.ai_game, self.rect.midbottom, direction="down", laser_type="alien")
            self.ai_game.alien_lasers.add(new_laser)
            self.last_shot_time = current_time  # Reset the cooldown timer

    def is_eligible_to_fire(self):
        """Return True if this alien is allowed to fire."""
        # Only allow aliens in the bottom 25% of the screen or randomly selected ones to fire
        return self.rect.y > self.screen.get_rect().height * 0.75 or randint(1, 5000) == 1

    def update(self):
        """Move the alien and update its animation."""
        if self.alive:
            self.x += self.v.x
            self.y += self.v.y

            # Only fire if this alien is eligible
            if self.is_eligible_to_fire():
                self.fire_laser()

        self.image = self.timer.current_image()

        if not self.alive and self.timer.finished():
            self.kill()

        self.draw()

    def draw(self):
        """Draw the alien on the screen."""
        self.rect.x = self.x
        self.rect.y = self.y
        self.screen.blit(self.image, self.rect)


def main():
    print('\n run from alien_invasions.py\n')

if __name__ == "__main__":
    main()
