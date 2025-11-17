from src.utils.definition import Monster, Item
from src.interface.components import Button
from src.interface.components import Slider
from src.interface.components import Checkbox
import pygame as pg
import threading
import time

from src.scenes.scene import Scene
from src.core import GameManager, OnlineManager
from src.utils import Logger, PositionCamera, GameSettings, Position
from src.core.services import scene_manager, sound_manager
from src.sprites import Sprite
from typing import override

class GameSettingSurface:
    _monsters_data: list[Monster]
    _items_data: list[Item]

    def __init__(self):

        self.surface_width, self.surface_height = GameSettings.SCREEN_WIDTH//2, GameSettings.SCREEN_HEIGHT//2
        self.surface_x = GameSettings.SCREEN_WIDTH//2 - self.surface_width//2
        self.surface_y = GameSettings.SCREEN_HEIGHT//2 - self.surface_height//2
        self.setting_surface = pg.Surface((self.surface_width, self.surface_height))

        self.save_button = Button(
            "UI/button_save.png", "UI/button_save_hover.png",
            20, self.surface_height - 50 - 20, 50, 50,
            lambda: self.save(), self.surface_x, self.surface_y
        )
        self.load_button = Button(
            "UI/button_load.png", "UI/button_load_hover.png",
            20 + 10 + 50, self.surface_height - 50 - 20, 50, 50,
            lambda: scene_manager.close_setting(), self.surface_x, self.surface_y
        )
        self.back_button = Button(
            "UI/button_back.png", "UI/button_back_hover.png",
            20 + 10 + 50 + 10 + 50, self.surface_height - 50 - 20, 50, 50,
            lambda: scene_manager.close_setting(), self.surface_x, self.surface_y
        )
        self.close_button = Button(
            "UI/button_x.png", "UI/button_x_hover.png",
            self.surface_width - 20 - 30, 20, 40, 40,
            lambda: scene_manager.close_setting(), self.surface_x, self.surface_y
        )

        self.volume_slider = Slider(
            35, self.surface_height//2 - 20, self.surface_width - 70, 20, 50, self.surface_x, self.surface_y
        )
        self.game_font = pg.font.Font(GameSettings.GAME_FONT, 24)

        self.mute_checkbox = Checkbox(
            155, self.surface_height//2 + 20 + 30 - 5, 25, 25,
            lambda: self.mute(), self.surface_x, self.surface_y
        )


    def save(self):
        Logger.debug(f"Set volume to {int(self.volume_slider.get_value())}%")
        sound_manager.set_bgm_volume(self.volume_slider.get_value()/100)
        scene_manager.close_setting()

    def mute(self):
        if self.mute_checkbox.get_value():
            Logger.debug(f"Mute checkbox muted")
            sound_manager.set_bgm_volume(0)

    def update(self, dt: float):
        self.close_button.update(dt)
        self.save_button.update(dt)
        self.load_button.update(dt)
        self.back_button.update(dt)
        self.volume_slider.update(dt)
        self.mute_checkbox.update(dt)

    def draw(self, screen: pg.Surface):
        if scene_manager.setting_opened:
            self.setting_surface.fill("ORANGE")
            self.back_button.draw(self.setting_surface)
            self.load_button.draw(self.setting_surface)
            self.save_button.draw(self.setting_surface)
            self.close_button.draw(self.setting_surface)
            self.volume_slider.draw(self.setting_surface)
            self.mute_checkbox.draw(self.setting_surface)

            volume_text_surface = self.game_font.render(f"VOLUME: {self.volume_slider.get_value()}%", True, (255, 255, 255))
            self.setting_surface.blit(volume_text_surface, (20, self.surface_height//2 - 50))

            mute_text_surface = self.game_font.render("MUTE: " + ("ON" if self.mute_checkbox.get_value() else "OFF"), True,
                                                             (255, 255, 255))
            self.setting_surface.blit(mute_text_surface, (20, self.surface_height//2 + 20 + 30))

            screen.blit(self.setting_surface, (self.surface_x, self.surface_y))

