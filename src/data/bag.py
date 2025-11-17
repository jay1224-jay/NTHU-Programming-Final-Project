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
        print(self._monsters_data)

        self.surface_width, self.surface_height = GameSettings.SCREEN_WIDTH//2, GameSettings.SCREEN_HEIGHT//2
        self.surface_x = GameSettings.SCREEN_WIDTH//2 - self.surface_width//2
        self.surface_y = GameSettings.SCREEN_HEIGHT//2 - self.surface_height//2
        self.bag_surface = pg.Surface((self.surface_width, self.surface_height))
        self.close_button = Button(
            "UI/button_x.png", "UI/button_x_hover.png",
            self.surface_width - 20 - 30, 20, 40, 40,
            lambda: scene_manager.close_bag(), self.surface_x, self.surface_y
        )

        self.game_fonts = {} # 18, 22, 26
        for _size in range(18, 27, 4):
            self.game_fonts[_size] = pg.font.Font(GameSettings.GAME_FONT, _size)

        # self.back_button.screen_pos = Position(self.surface_x, self.surface_y)

    def draw_text(self, screen, text, text_col, x, y, size, align="left"):
        game_font = self.game_fonts[size]
        img = game_font.render(text, True, text_col)
        if align == "left":
            rect = img.get_rect(topleft=(x, y))
        elif align == "right":
            rect = img.get_rect(topright=(x, y))
        else:
            rect = img.get_rect(topleft=(x, y))
        screen.blit(img, rect)

    def update(self, dt: float):
        self.close_button.update(dt)

    def draw(self, screen: pg.Surface):
        if scene_manager.bag_opened:
            self.bag_surface.fill("ORANGE")
            self.close_button.draw(self.bag_surface)
            self.draw_text(self.bag_surface, "BAG", "black", 10, 10, 26)
            # Draw items
            i = 0
            for item in self._items_data:
                item_sprite = Sprite(item["sprite_path"], (30, 30))
                self.bag_surface.blit(item_sprite.image, (400, self.close_button.hitbox.y + self.close_button.hitbox.height + 15 + i*40))
                self.draw_text(self.bag_surface, item["name"], "black", 400 + 30 + 30, self.close_button.hitbox.y + self.close_button.hitbox.height + 15 + i*40+7, 18)
                self.draw_text(self.bag_surface, f"x{item["count"]}", "black", 400 + 30 + 150,
                               self.close_button.hitbox.y + self.close_button.hitbox.height + 15 + i*40+7, 18, "right")
                i += 1

            # Draw monster, name, hp, max_hp, level
            i = 0
            start_x = 100
            start_y = self.close_button.hitbox.y
            sprite_size = 50
            for monster in self._monsters_data:
                monster_sprite = Sprite(monster["sprite_path"], (sprite_size, sprite_size))
                self.bag_surface.blit(monster_sprite.image,
                                      (start_x, start_y + i * (sprite_size+5)))
                self.draw_text(self.bag_surface, monster["name"], "black", start_x + 30 + 30,
                               start_y + i * (sprite_size+5) + 7 , 18)
                # self.draw_text(self.bag_surface, monster["level"], "black", start_x + 30 + 150, )
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