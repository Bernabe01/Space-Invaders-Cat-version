import pygame as pg
import sys
from vector import Vector

class Event:
    # Dictionary for movement vectors corresponding to key presses
    di = {
        pg.K_RIGHT: Vector(1, 0), pg.K_LEFT: Vector(-1, 0),
        pg.K_UP: Vector(0, -1), pg.K_DOWN: Vector(0, 1),
        pg.K_d: Vector(1, 0), pg.K_a: Vector(-1, 0),
        pg.K_w: Vector(0, -1), pg.K_s: Vector(0, 1)
    }

    def __init__(self, ai_game):
        """Initialize event handling for the game."""
        self.ai_game = ai_game
        self.settings = ai_game.settings
        self.stats = ai_game.stats
        self.sb = ai_game.sb
        self.game_active = ai_game.game_active
        self.ship = ai_game.ship
        self.play_button = ai_game.play_button
        self.high_scores_button = ai_game.high_scores_button  # Add reference to high scores button

    def check_events(self):
        """Check for keypresses and mouse events."""
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_q):
                sys.exit()
                return True  # finished is True
            elif event.type == pg.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pg.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pg.MOUSEBUTTONDOWN:
                mouse_pos = pg.mouse.get_pos()
                if self.ai_game.show_high_scores:
                    self._check_return_to_title(mouse_pos)  # Check if "Return to Title" is clicked
                else:
                    self._check_play_button(mouse_pos)
                    self._check_high_scores_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        """Start a new game when the Play button is clicked."""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.game_active and not self.ai_game.show_high_scores:
            self.settings.initialize_dynamic_settings()
            self.ai_game.reset_game()

    def _check_high_scores_button(self, mouse_pos):
        """Display high scores screen when the High Scores button is clicked."""
        button_clicked = self.high_scores_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.game_active and not self.ai_game.show_high_scores:
            self.ai_game.show_high_scores = True  # Show the high scores screen

    def _check_keydown_events(self, event):
        """Respond to key presses."""
        key = event.key
        if key in Event.di.keys():
            self.ship.v += self.settings.ship_speed * Event.di[key]
        elif event.key == pg.K_SPACE:
            self.ship.open_fire()

    def _check_keyup_events(self, event):
        """Respond to key releases."""
        if event.key in Event.di.keys():
            self.ship.v = Vector()  # Reset velocity when key is released
        elif event.key == pg.K_SPACE:
            self.ship.cease_fire()

    def _check_return_to_title(self, mouse_pos):
        """Return to title screen when 'Return to Title' button is clicked."""
        button_clicked = self.ai_game.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and self.ai_game.show_high_scores:
            self.ai_game.show_high_scores = False  # Switch back to title screen
