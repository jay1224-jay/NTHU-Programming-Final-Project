from src.utils.definition import Monster, Item
from src.interface.components import Button
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
            lambda: scene_manager.close_setting(), self.surface_x, self.surface_y
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

    def update(self, dt: float):
        self.close_button.update(dt)
        self.save_button.update(dt)
        self.load_button.update(dt)
        self.back_button.update(dt)

    def draw(self, screen: pg.Surface):
        if scene_manager.setting_opened:
            self.setting_surface.fill("ORANGE")
            self.back_button.draw(self.setting_surface)
            self.load_button.draw(self.setting_surface)
            self.save_button.draw(self.setting_surface)
            self.close_button.draw(self.setting_surface)
            screen.blit(self.setting_surface, (self.surface_x, self.surface_y))

