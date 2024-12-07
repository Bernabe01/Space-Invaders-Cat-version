import pygame as pg
from pygame.sprite import Sprite
from timer import Timer

class UFO(Sprite):
    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.images = [pg.image.load('images/ufo01.png'), pg.image.load('images/ufo02.png')]

        # Load explosion frames from the sprite sheet (explosion_frames.png)
        sprite_sheet = pg.image.load("images/explosion_frames.png").convert_alpha()
        frame_width = 64  # Adjust to match the width of your explosion frames
        frame_height = 64  # Adjust to match the height of your explosion frames
        self.explosion_frames = [sprite_sheet.subsurface(pg.Rect(n * frame_width, 0, frame_width, frame_height)) for n in range(8)]

        self.rect = self.images[0].get_rect()
        self.rect.x = -self.rect.width  # Start off-screen
        self.rect.y = 20  # Position the UFO near the top
        self.x = float(self.rect.x)
        self.speed = self.settings.ufo_speed

        # UFO animation using the Timer class
        self.timer = Timer(self.images, delta=500)  # Animation timer for UFO
        self.explosion_timer = Timer(self.explosion_frames, delta=100, loop_continuously=False)  # Timer for explosion

        self.alive = True
        self.exploding = False  # Track if the UFO is currently exploding
        self.points = 500  # Assign point value for destroying the UFO

    def hit(self):
        """Handle the UFO being hit."""
        print("UFO hit!")  # Debugging output
        self.alive = False
        self.exploding = True  # Set exploding state
        self.timer = self.explosion_timer  # Switch to explosion animation

    def update(self):
        """Move the UFO and handle explosion animation."""
        if self.alive:
            # Move the UFO across the screen if it's still alive
            self.x += self.speed
            self.rect.x = self.x
            print("UFO moving: ", self.rect.x)  # Debugging output
            self.screen.blit(self.timer.current_image(), self.rect)
        else:
            # Handle explosion animation
            if self.exploding:
                current_image = self.timer.current_image()
                if self.timer.finished():
                    #print("UFO explosion finished!")  # Debugging output
                    self.kill()  # Remove the UFO from the game once the explosion finishes
                else:
                    self.screen.blit(current_image, self.rect)

        # Remove UFO once it moves off the screen (if still alive)
        if self.alive and self.rect.left > self.settings.scr_width:
            print("UFO off screen, removing...")  # Debugging output
            self.kill()  # Remove the UFO from the game


    def draw(self):
        """Draw the animated UFO or explosion."""
        current_image = self.timer.current_image()  # Get the current frame
        self.screen.blit(current_image, self.rect)  # Draw the UFO or explosion


def main():
    print('\n run from alien_invasions.py\n')

if __name__ == "__main__":
    main()
