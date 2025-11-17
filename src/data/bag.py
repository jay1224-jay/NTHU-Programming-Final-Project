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

class Bag:
    _monsters_data: list[Monster]
    _items_data: list[Item]

    def __init__(self, monsters_data: list[Monster] | None = None, items_data: list[Item] | None = None):
        self._monsters_data = monsters_data if monsters_data else []
        self._items_data = items_data if items_data else []

        self.surface_width, self.surface_height = GameSettings.SCREEN_WIDTH//2, GameSettings.SCREEN_HEIGHT//2
        self.surface_x = GameSettings.SCREEN_WIDTH//2 - self.surface_width//2
        self.surface_y = GameSettings.SCREEN_HEIGHT//2 - self.surface_height//2
        self.bag_surface = pg.Surface((self.surface_width, self.surface_height))
        self.close_button = Button(
            "UI/button_x.png", "UI/button_x_hover.png",
            self.surface_width - 20 - 30, 20, 40, 40,
            lambda: scene_manager.close_bag(), self.surface_x, self.surface_y
        )
        # self.back_button.screen_pos = Position(self.surface_x, self.surface_y)

    def update(self, dt: float):
        self.close_button.update(dt)

    def draw(self, screen: pg.Surface):
        if scene_manager.bag_opened:

            self.bag_surface.fill("ORANGE")
            self.close_button.draw(self.bag_surface)
            screen.blit(self.bag_surface, (self.surface_x, self.surface_y))

    def to_dict(self) -> dict[str, object]:
        return {
            "monsters": list(self._monsters_data),
            "items": list(self._items_data)
        }

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> "Bag":
        monsters = data.get("monsters") or []
        items = data.get("items") or []
        bag = cls(monsters, items)
        return bag