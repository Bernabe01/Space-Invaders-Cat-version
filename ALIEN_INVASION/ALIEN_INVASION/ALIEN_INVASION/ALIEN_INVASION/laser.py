import pygame as pg
from pygame.sprite import Sprite

class Laser(Sprite):
    def __init__(self, ai_game, position, direction="up", laser_type="ship"):
        """Initialize the laser at the ship or alien's position."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.laser_type = laser_type  # Either "ship" or "alien"
        self.direction = direction  # Direction of laser: "up" for ship, "down" for alien

        # Set laser properties based on who fired it
        if self.laser_type == "ship":
            self.color = self.settings.laser_color  # Ship's laser color
            self.speed = -self.settings.laser_speed  # Ship's laser moves upward
            self.rect = pg.Rect(0, 0, self.settings.laser_width, self.settings.laser_height)
            self.rect.midtop = position  # Position the laser at the ship's top

        elif self.laser_type == "alien":
            self.color = (255, 0, 0)  # Alien laser is red
            self.speed = self.settings.alien_laser_speed  # Alien laser moves downward
            self.rect = pg.Rect(0, 0, self.settings.laser_width, self.settings.laser_height)
            self.rect.midbottom = position  # Position the laser at the alien's bottom

        self.y = float(self.rect.y)  # Track the laser's y-position

    def update(self):
        """Move the laser on the screen."""
        self.y += self.speed  # Move laser depending on speed
        self.rect.y = self.y  # Update rect position

        # Remove the laser if it moves off the screen
        if self.rect.bottom <= 0 or self.rect.top >= self.screen.get_rect().bottom:
            self.kill()  # Remove the laser if it goes off the screen

    def draw(self):
        """Draw the laser to the screen."""
        pg.draw.rect(self.screen, self.color, self.rect)

def main():
    print("\nYou have to run from alien_invasion.py\n")

if __name__ == "__main__":
    main()
