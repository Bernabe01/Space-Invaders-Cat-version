import pygame as pg
import time

class Sound:
    def __init__(self): 
        # Load sounds
        self.pickup = pg.mixer.Sound('sounds/pickup.wav')
        self.gameover = pg.mixer.Sound('sounds/gameover.wav')
        self.invaderkilled = pg.mixer.Sound('sounds/invaderkilled.wav')
        self.fireBlaster = pg.mixer.Sound('sounds/blaster.mp3')
        self.explosion = pg.mixer.Sound('sounds/explosion.wav')
        
        # Load background music
        self.normal_music = 'sounds/ride_of_the_valkyries.mp3'
        self.fast_music = 'sounds/ride_of_the_valkyries_fast.mp3'
        pg.mixer.music.set_volume(0.2)
        
        # Initialize the state
        self.music_playing = False
        self.fast_music_playing = False  # Track if fast music is playing
        
    def play_background(self): 
        """Play normal-speed background music in a loop."""
        pg.mixer.music.stop()  # Stop any currently playing music
        pg.mixer.music.load(self.normal_music)  # Load the normal-speed music
        pg.mixer.music.play(-1, 0.0)  # Play in a loop
        self.music_playing = True
        self.fast_music_playing = False  # Ensure only normal music is playing

    def play_music_fast(self):
        """Play fast version of the background music."""
        if not self.fast_music_playing:
            pg.mixer.music.stop()  # Stop any currently playing music
            pg.mixer.music.load(self.fast_music)  # Load the fast-speed music
            pg.mixer.music.play(-1, 0.0)  # Play in a loop
            self.fast_music_playing = True
            self.music_playing = False  # Stop normal music flag

    def stop_background(self): 
        """Stop the normal background music."""
        if self.music_playing:
            pg.mixer.music.stop()
            self.music_playing = False

    def stop_music_fast(self):
        """Stop the fast background music."""
        if self.fast_music_playing:
            pg.mixer.music.stop()
            self.fast_music_playing = False

    def play_killedSpaceInvader(self):
        """Play when a space invader is killed."""
        self.invaderkilled.play()

    def play_pickup(self): 
        """Play pickup sound if background music is playing."""
        if self.music_playing or self.fast_music_playing:
            self.pickup.play()

    def play_gameover(self):
        """Play game over sound and stop the background music."""
        if self.music_playing or self.fast_music_playing:
            self.stop_background()  # Stop normal or fast music
            self.stop_music_fast()  # Stop fast music if playing
            self.gameover.play()
            time.sleep(5.0)

    def play_fireBlaster(self):
        """Play fire blaster sound."""
        self.fireBlaster.play()

    def play_explosion(self):
        """Play explosion sound."""
        self.explosion.play()
