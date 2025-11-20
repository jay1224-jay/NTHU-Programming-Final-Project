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
from src.sprites import BackgroundSprite

class SettingScene(Scene):
    def __init__(self):
        super().__init__()
        self.background = BackgroundSprite("backgrounds/background1.png")

        self.surface_width, self.surface_height = GameSettings.SCREEN_WIDTH//2, GameSettings.SCREEN_HEIGHT//2
        self.surface_x = GameSettings.SCREEN_WIDTH//2 - self.surface_width//2
        self.surface_y = GameSettings.SCREEN_HEIGHT//2 - self.surface_height//2
        self.setting_surface = pg.Surface((self.surface_width, self.surface_height))

        self.data = GameManager.load("saves/game0.json").to_dict()["volume"]

        self.back_button = Button(
            "UI/button_back.png", "UI/button_back_hover.png",
            20 + 10 + 50 + 10 + 50, self.surface_height - 50 - 20, 50, 50,
            lambda: scene_manager.change_scene("menu"), self.surface_x, self.surface_y
        )
        self.close_button = Button(
            "UI/button_x.png", "UI/button_x_hover.png",
            self.surface_width - 20 - 30, 20, 40, 40,
            lambda: scene_manager.change_scene("menu"), self.surface_x, self.surface_y
        )

        self.volume_slider = Slider(
            35, self.surface_height//2 - 20, self.surface_width - 70, 20, self.data.get("value"), self.surface_x, self.surface_y
        )
        self.game_font = pg.font.Font(GameSettings.GAME_FONT, 24)

        self.mute_checkbox = Checkbox(
            155, self.surface_height//2 + 20 + 30 - 5, 35, 25, self.data.get("mute"),
            lambda: self.mute(), self.surface_x, self.surface_y
        )

    @override
    def enter(self) -> None:
        sound_manager.play_bgm("RBY 102 Opening (Part 2).ogg")
        self.data = GameManager.load("saves/game0.json").to_dict()["volume"]

    @override
    def exit(self) -> None:
        pass

    def mute(self):
        if self.mute_checkbox.get_value():
            Logger.debug(f"Mute checkbox muted")
            sound_manager.set_bgm_volume(0)

    def update(self, dt: float):
        self.close_button.update(dt)
        self.back_button.update(dt)
        self.volume_slider.update(dt)
        self.mute_checkbox.update(dt)

    def draw(self, screen: pg.Surface):

        self.background.draw(screen)

        self.setting_surface.fill((50, 50, 100))
        self.back_button.draw(self.setting_surface)
        self.close_button.draw(self.setting_surface)
        self.volume_slider.draw(self.setting_surface)
        self.mute_checkbox.draw(self.setting_surface)

        volume_text_surface = self.game_font.render(f"VOLUME: {self.volume_slider.get_value()}%", True, (255, 255, 255))
        self.setting_surface.blit(volume_text_surface, (20, self.surface_height//2 - 50))

        mute_text_surface = self.game_font.render("MUTE: " + ("ON" if self.mute_checkbox.get_value() else "OFF"), True,
                                                         (255, 255, 255))
        self.setting_surface.blit(mute_text_surface, (20, self.surface_height//2 + 20 + 30))

        screen.blit(self.setting_surface, (self.surface_x, self.surface_y))

