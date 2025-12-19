# ai_player.py
# --------------------------------------------------------------------------------------------
# AI player module:
# Automatically controls ship movement and firing logic based on alien alignment.
# Prevents firing when barriers, explosions, or UFO are blocking.
# --------------------------------------------------------------------------------------------

import pygame as pg
import random

class AIPlayer:
    def __init__(self, ship, fleet, alien_lasers, barriers):
        self.ship = ship
        self.fleet = fleet
        self.alien_lasers = alien_lasers
        self.barriers = barriers

        self.last_fire_time = 0
        self.fire_delay = 400  # ms between shots
        self.move_target = None  # NEW: goal position to move toward

        # NEW: dodge system
        self.last_dodge_time = 0
        self.dodge_cooldown = 900  # ms prevent jitter spam

    def update(self):
        # -------------------------------------------
        # DODGE FIRST if danger is close
        # -------------------------------------------
        if self._dodge():
            self.ship.bound()
            return

        # -------------------------------------------
        # CONTINUOUS MOVEMENT IMPROVEMENT
        # -------------------------------------------
        target = self.find_best_target()
        if target:
            self.move_target = target.rect.centerx
            self._move_towards_target()
        else:
            self.ship.v.x = 0  # nothing to chase

        # Keep ship in bounds
        self.ship.bound()

        aligned = self.find_aligned_alien()
        if aligned and self.can_fire_at(aligned):
            self.ship.open_fire()
        else:
            self.ship.cease_fire()

    # --------------------------------------------------------------------
    # NEW: continuous pursuit movement (no tiny nudges)
    # --------------------------------------------------------------------
    def _move_towards_target(self):
        if self.move_target is None:
            self.ship.v.x = 0
            return

        dx = self.move_target - self.ship.rect.centerx

        if abs(dx) > 6:
            direction = 1 if dx > 0 else -1
            self.ship.v.x = direction * self.ship.settings.ship_speed
        else:
            self.ship.v.x = 0
            self.move_target = None

    # --------------------------------------------------------------------
    # Pick closest alien horizontally (not exact align)
    # --------------------------------------------------------------------
    def find_best_target(self):
        visible = [a for a in self.fleet.aliens.sprites() if a.alive]
        if not visible:
            return None

        return min(visible, key=lambda alien: abs(alien.rect.centerx - self.ship.rect.centerx))

    def find_aligned_alien(self):
        # Alien directly above ship, alive only
        for alien in self.fleet.aliens.sprites():
            if alien.alive and abs(alien.rect.centerx - self.ship.rect.centerx) < 15:
                return alien
        return None

    def can_fire_at(self, target):
        # -------------------------------------------
        # Strict vertical collision check
        # -------------------------------------------
        if not target.alive:
            return False  # << NEW: don't shoot explosions or dead sprites

        line = pg.Rect(
            self.ship.rect.centerx - 2,
            target.rect.bottom,
            4,
            self.ship.rect.top - target.rect.bottom
        )

        # barriers block shots properly now
        for barrier in self.barriers.barriers:
            for b in barrier.barrier_pieces:
                if line.colliderect(b.rect):
                    return False

        # NEW: STOP FIRING IF explosion sprite is sitting on that column
        for alien in self.fleet.aliens.sprites():
            if not alien.alive:  # explosion frame
                if line.colliderect(alien.rect):
                    return False

        now = pg.time.get_ticks()
        return now - self.last_fire_time > self.fire_delay

    # --------------------------------------------------------------------
    # NEW: Laser dodging logic
    # --------------------------------------------------------------------
    def _dodge(self):
        now = pg.time.get_ticks()

        # prevent panic dancing
        if now - self.last_dodge_time < self.dodge_cooldown:
            return False

        ship_x = self.ship.rect.centerx
        ship_y = self.ship.rect.top

        for laser in self.alien_lasers.sprites():
            dx = abs(laser.rect.centerx - ship_x)
            dy = ship_y - laser.rect.bottom

            # only dodge if laser is directly above and close
            if dx < 18 and 0 < dy < 110:
                # check barrier density left vs right
                left_count = sum(
                    1 for barrier in self.barriers.barriers
                    for b in barrier.barrier_pieces
                    if b.rect.centerx < ship_x
                )
                right_count = sum(
                    1 for barrier in self.barriers.barriers
                    for b in barrier.barrier_pieces
                    if b.rect.centerx > ship_x
                )

                if left_count < right_count:
                    self.ship.v.x = -self.ship.settings.ship_speed
                else:
                    self.ship.v.x = self.ship.settings.ship_speed

                self.last_dodge_time = now
                return True  # dodge overrides shooting & alignment

        return False
