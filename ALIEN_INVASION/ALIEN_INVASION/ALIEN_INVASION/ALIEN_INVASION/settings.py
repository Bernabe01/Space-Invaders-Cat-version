from colors import DARK_GREY, RED

class Settings:
    def __init__(self):
        """Initialize the game's settings."""
        self.scr_width = 1200  # Screen width
        self.scr_height = 800  # Screen height
        self.w_h = (self.scr_width, self.scr_height)  # Add this line to define w_h as a tuple (width, height)
        
        # Initial Alien Speed
        self.initial_alien_speed_factor = 1.0
        self.alien_speed_factor = self.initial_alien_speed_factor
        self.total_aliens = 52
        
        # Background color
        self.bg_color = DARK_GREY

        # Laser settings
        self.laser_speed = 17.0
        self.laser_width = 8
        self.laser_height = 15
        self.laser_color = RED
        self.lasers_allowed = 3  # Add this line to set the max number of lasers that can be on screen at once

        # Ship settings
        self.ship_limit = 3

        # Alien settings
        self.fleet_drop_speed = 10
        self.alien_spacing = 1.2  # You can adjust this value to control the spacing of the alien fleet

        # to enable AI
        self.ai_enabled = True

        # UFO settings
        self.ufo_speed = 5.0  # Speed of the UFO

        # Speed up settings
        self.speedup_scale = 1.1
        self.score_scale = 1.5

        # Ship laser settings
        self.laser_speed = 5.0

        # Alien laser settings
        self.alien_laser_speed = 3.0  # Slower than ship lasers
        


        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Initialize settings that change throughout the game."""
        self.ship_speed = 10.0
        self.laser_speed = 17.0
        self.alien_speed = 1.0
        self.alien_points = 50

    def increase_speed(self):
        """Increase speed settings and alien point values."""
        self.ship_speed *= self.speedup_scale
        self.laser_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)


def main():
    print('\n*** message from settings.py --- run from alien_invasions.py\n')

if __name__ == "__main__":
    main()
