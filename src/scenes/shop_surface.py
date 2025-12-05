from src.utils.definition import Monster, Item
from src.interface.components import Button
from src.interface.components import Slider
from src.interface.components import Checkbox
import pygame as pg
import threading
import time

from enum import Enum

from src.scenes.scene import Scene
from src.core import GameManager, OnlineManager
from src.utils import Logger, PositionCamera, GameSettings, Position
from src.core.services import scene_manager, sound_manager
from src.sprites import Sprite
from typing import override

BUY = 1
SELL = 2

_d = {
    "monsters": [
        {
            "name": "Pickachu",
            "hp": 20,
            "max_hp": 20,
            "level": 1,
            "sprite_path": "menu_sprites/menusprite1.png"
        }
    ],
    "items": [
        {
            "name": "Potion",
            "count": 5,
            "sprite_path": "ingame_ui/potion.png"
        },
        {
            "name": "Pokeball",
            "count": 87,
            "sprite_path": "ingame_ui/ball.png"
        }
    ]
}

class GameShopSurface:
    def __init__(self):
        self.surface_width, self.surface_height = 400, 500
        self.surface_x = GameSettings.SCREEN_WIDTH//2 - self.surface_width//2
        self.surface_y = GameSettings.SCREEN_HEIGHT//2 - self.surface_height//2
        self.shop_surface = pg.Surface((self.surface_width, self.surface_height))

        self.close_button = Button(
            "UI/button_x.png", "UI/button_x_hover.png",
            self.surface_width - 20 - 30, 20, 40, 40,
            lambda: scene_manager.close_shop(), self.surface_x, self.surface_y
        )
        self.buy_button = Button(
            "UI/raw/UI_Flat_Button02a_4.png", "UI/raw/UI_Flat_Button02a_2.png",
            10, 20,  70, 40,
            lambda: print(), self.surface_x, self.surface_y, label="BUY"
        )
        self.sell_button = Button(
            "UI/raw/UI_Flat_Button02a_4.png", "UI/raw/UI_Flat_Button02a_2.png",
            90, 20, 70, 40,
            lambda: print(), self.surface_x, self.surface_y, label="SELL"
        )
        self.game_font = pg.font.Font(GameSettings.GAME_FONT, 24)

        self.save_settings = False
        self.load_settings = False

        self._status = BUY

        self._shop_data = _d.copy()

    def save(self):
        self.save_settings = True
        scene_manager.close_setting()

    def load(self):
        self.load_settings = True
        scene_manager.close_setting()


    def update(self, dt: float):
        self.close_button.update(dt)
        self.buy_button.update(dt)
        self.sell_button.update(dt)

    def draw(self, screen: pg.Surface):
        if scene_manager.shop_opened:
            self.shop_surface.fill("ORANGE")
            self.close_button.draw(self.shop_surface)
            self.buy_button.draw(self.shop_surface)
            self.sell_button.draw(self.shop_surface)

            start_x = 0
            if self._status == BUY:
                # only 
                pass
            elif self._status == SELL:
                # only monsters
                pass
            else:
                Logger.debug("Unknown shop status")

            screen.blit(self.shop_surface, (self.surface_x, self.surface_y))

