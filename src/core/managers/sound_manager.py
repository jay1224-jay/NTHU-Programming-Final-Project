import pygame as pg
from src.utils import load_sound, GameSettings

class SoundManager:
    def __init__(self):
        pg.mixer.init()
        pg.mixer.set_num_channels(GameSettings.MAX_CHANNELS)
        self.current_bgm = None
        self.previous_bgm = None
        
    def play_bgm(self, filepath: str):
        if self.current_bgm:
            self.current_bgm.stop()
        audio = load_sound(filepath)
        audio.set_volume(GameSettings.AUDIO_VOLUME)
        audio.play(-1)
        self.current_bgm = audio
        self.previous_bgm = audio

    def set_bgm_volume(self, volume: float):
        if self.current_bgm:
            self.current_bgm.stop()
        audio = self.current_bgm
        audio.set_volume(volume)
        audio.play(-1)
        
    def pause_all(self):
        pg.mixer.pause()

    def resume_all(self):
        pg.mixer.unpause()
        
    def play_sound(self, filepath, volume=0.7):
        sound = load_sound(filepath)
        sound.set_volume(volume)
        sound.play()

    def stop_all_sounds(self):
        pg.mixer.stop()
        self.current_bgm = None