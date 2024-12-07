import pygame as pg
from vector import Vector
from alien import Alien
from laser import Laser
from pygame.sprite import Sprite, Group
from random import randint

class Fleet(Sprite):
    def __init__(self, ai_game):
        super().__init__()
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.ship = ai_game.ship
        self.aliens = Group()
        self.fleet_lasers = Group()  # Group to track alien lasers
        self.settings = ai_game.settings
        self.stats = ai_game.stats
        self.sb = ai_game.sb
        self.v = Vector(self.settings.alien_speed, 0)
        self.spacing = max(1.0, self.settings.alien_spacing)  # Use alien_spacing from settings
        self.create_fleet()

    def reset_fleet(self):
        """Reset the fleet of aliens and clear lasers."""
        self.aliens.empty()
        self.fleet_lasers.empty()  # Clear alien lasers when resetting
        self.create_fleet()

    def create_fleet(self):
        """Create a full fleet of cat aliens only."""
        alien = Alien(ai_game=self.ai_game, v=self.v)
        alien_width = alien.rect.width
        alien_height = alien.rect.height

        # Calculate how many aliens fit in one row and how many rows fit on the screen
        num_cols = int((self.settings.scr_width - 2 * alien_width) // (self.spacing * alien_width))
        num_rows = int((self.settings.scr_height - 5 * alien_height) // (self.spacing * alien_height))

        # Create the fleet
        for row_number in range(min(num_rows, 6)):  # Limiting rows to 6 to avoid overlapping
            self.create_row(row_number, num_cols)

    def create_row(self, row_number, num_cols):
        """Create a row of aliens."""
        for col_number in range(num_cols):
            alien_type = randint(0, 2)  # Randomly pick one of the three types of cat aliens (0, 1, 2)
            alien = Alien(ai_game=self.ai_game, v=self.v, alien_type=alien_type)

            alien_width = alien.rect.width
            alien_height = alien.rect.height

            # Position the alien based on its row and column
            alien.x = alien_width + self.spacing * alien_width * col_number
            alien.rect.x = alien.x
            alien.rect.y = alien_height + self.spacing * alien_height * row_number
            alien.y = alien.rect.y
            
            self.aliens.add(alien)

    def fire_laser(self):
        """Randomly make an alien fire a laser."""
        if self.aliens:
            alien = randint(0, len(self.aliens.sprites()) - 1)
            shooter = list(self.aliens)[alien]  # Select random alien to fire
            new_laser = Laser(self.ai_game, shooter.rect.midbottom)  # Fire from bottom of alien
            self.fleet_lasers.add(new_laser)

    def check_edges(self):
        """Check if any aliens are at the edge of the screen."""
        for alien in self.aliens:
            if alien.check_edges():
                return True
        return False

    def check_bottom(self):
        """Check if any aliens have reached the bottom of the screen."""
        for alien in self.aliens:
            if alien.rect.bottom >= self.settings.scr_height:
                self.ship.ship_hit()  # Call ship_hit() when an alien reaches the bottom
                return True
        return False

    def update(self):
        """Update the fleet's position, lasers, and check for collisions."""
        # Apply the updated alien speed factor
        self.v.x = self.ai_game.settings.alien_speed_factor * (1 if self.v.x > 0 else -1)
        
        # Fire lasers randomly
        if randint(1, 120) == 1:  # Adjust this number to control how often aliens fire
            self.fire_laser()

        # Update alien lasers
        self.fleet_lasers.update()

        # Check for collisions between the ship's lasers and the aliens
        collisions = pg.sprite.groupcollide(self.ship.lasers, self.aliens, True, False)
        if collisions:
            for aliens in collisions.values():
                for alien in aliens:
                    alien.hit()  # Trigger explosion animation
                    self.stats.score += self.settings.alien_points
            self.sb.prep_score()
            self.sb.check_high_score()

        # If all aliens are gone, reset the fleet and level up
        if not self.aliens:
            self.ship.lasers.empty()  # Clear any remaining ship lasers
            self.create_fleet()  # Create a new fleet
            self.stats.level += 1
            self.sb.prep_level()
            return

        # Check for collisions between the aliens and the ship
        if pg.sprite.spritecollideany(self.ship, self.aliens):
            self.ship.ship_hit()  # Handle ship hit by alien
            return

        # Check if any aliens reached the bottom of the screen
        if self.check_bottom():
            return

        # Change direction if any alien hits an edge
        if self.check_edges():
            self.v.x *= -1  # Reverse direction
            for alien in self.aliens:
                alien.v.x = self.v.x
                alien.y += self.settings.fleet_drop_speed

        # Update each alien in the fleet
        for alien in self.aliens:
            alien.update()

    def draw(self):
        """Draw all the aliens and their lasers."""
        for alien in self.aliens:
            alien.draw()  # Draw the alien with its animation intact
        # Draw the alien lasers
        for laser in self.fleet_lasers:
            laser.draw()
