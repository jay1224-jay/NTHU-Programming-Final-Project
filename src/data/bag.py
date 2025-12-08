from src.utils.definition import Monster, Item
from src.interface.components import Button
import pygame as pg
import threading
import time

from src.scenes.scene import Scene
from src.core import GameManager, OnlineManager
from src.utils import Logger, PositionCamera, GameSettings, Position, TextDrawer
from src.core.services import scene_manager, sound_manager, input_manager
from src.sprites import Sprite
from typing import override

class Bag:
    _monsters_data: list[Monster]
    _items_data: list[Item]

    def __init__(self, monsters_data: list[Monster] | None = None, items_data: list[Item] | None = None):
        self._monsters_data = monsters_data if monsters_data else []
        self._items_data = items_data if items_data else []
        # print(self._monsters_data)

        self.surface_width, self.surface_height = GameSettings.SCREEN_WIDTH//2, GameSettings.SCREEN_HEIGHT//2
        self.surface_x = GameSettings.SCREEN_WIDTH//2 - self.surface_width//2
        self.surface_y = GameSettings.SCREEN_HEIGHT//2 - self.surface_height//2
        self.bag_surface = pg.Surface((self.surface_width, self.surface_height))
        self.close_button = Button(
            "UI/button_x.png", "UI/button_x_hover.png",
            self.surface_width - 20 - 30, 20, 40, 40,
            lambda: self.close_bag(), self.surface_x, self.surface_y
        )
        self.not_updating_bag = True
        self.text_drawer = TextDrawer("assets/fonts/Minecraft.ttf")
        self.start_y = self.close_button.hitbox.y - 30
        self.mouse_speed = 0

    def close_bag(self):
        self.not_updating_bag = True
        scene_manager.close_bag()

    def update(self, dt: float):
        self.close_button.update(dt)
        n = len(self._monsters_data)
        if 90 <= (input_manager.mouse_pos[0] - self.surface_x) <= 90 + 170:
            self.mouse_speed = input_manager.mouse_wheel
        if n > 5:
            self.start_y += (dt * self.mouse_speed * 400)

            """
            end_y = self.start_y + (n-1) * (50 + 5) + 40 + 50
            if self.surface_height <= end_y:
                self.start_y = self.surface_height - ((n-1) * (50 + 5) + 40 + 50) - 2

            if self.start_y < -35:
                self.start_y = -34
            """

        """        # slow down
        print(self.mouse_speed)
        if abs(self.mouse_speed) < 0.01:
            self.mouse_speed = 0
        elif self.mouse_speed > 0:
            self.mouse_speed -= 0.01
        elif self.mouse_speed < 0:
            print("in")
            self.mouse_speed += 0.01"""

    def draw(self, screen: pg.Surface):
        if scene_manager.bag_opened:
            if self.not_updating_bag:
                _data = GameManager.load("saves/game0.json").to_dict()["bag"]
                self._monsters_data = _data["monsters"]
                self._items_data = _data["items"]
                self.not_updating_bag = False
            self.bag_surface.fill("ORANGE")
            self.close_button.draw(self.bag_surface)
            self.text_drawer.draw(self.bag_surface, "BAG", 26, (10, 10))

            # Draw items
            i = 0
            for item in self._items_data:
                item_sprite = Sprite(item["sprite_path"], (30, 30))
                self.bag_surface.blit(item_sprite.image, (400, self.close_button.hitbox.y + self.close_button.hitbox.height + 15 + i*40))
                self.text_drawer.draw(self.bag_surface, item["name"], 16,
                                      (400 + 30 + 30, self.close_button.hitbox.y + self.close_button.hitbox.height + 15 + i*40+7))
                self.text_drawer.draw(self.bag_surface, f"x{item["count"]}", 16, (400 + 30 + 150,
                               self.close_button.hitbox.y + self.close_button.hitbox.height + 15 + i*40+7), "right")
                i += 1

            # Draw monster, name, hp, max_hp, level
            i = 0
            start_x = 90
            # start_y = self.close_button.hitbox.y - 30

            start_y = self.start_y
            sprite_size = 50
            background_rect_width = 70
            background_rect_height = 10
            monster_surface_width = 170
            monster_surface_height = 50
            for monster in self._monsters_data:

                monster_surface = pg.Surface((monster_surface_width, monster_surface_height))
                monster_surface.fill("WHITE")

                monster_sprite = Sprite(monster["sprite_path"], (sprite_size, sprite_size))
                monster_surface.blit(monster_sprite.image,(0,  -5))
                self.text_drawer.draw(monster_surface, monster["name"], 14, (30 + 25,10))
                self.text_drawer.draw(monster_surface, "Lv" + str(monster["level"]), 12, (15 + 115, 25))

                # hp
                background_rect = pg.Rect(30 + 25,  25, background_rect_width, background_rect_height)
                pg.draw.rect(monster_surface, (50, 50, 50), background_rect)
                hp_rect = pg.Rect(30 + 25, 25,
                                          int(background_rect_width * monster["hp"] / monster["max_hp"]), background_rect_height)
                pg.draw.rect(monster_surface, (50, 200, 50), hp_rect)
                self.text_drawer.draw(monster_surface, f"{monster["hp"]}/{monster["max_hp"]}", 10,  (30 + 25,40))
                self.bag_surface.blit(monster_surface, (start_x + 15, start_y + i * (monster_surface_height + 5) + 40))
                i += 1

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