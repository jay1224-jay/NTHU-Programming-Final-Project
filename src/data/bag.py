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
        # print(self._monsters_data)

        self.surface_width, self.surface_height = GameSettings.SCREEN_WIDTH//2, GameSettings.SCREEN_HEIGHT//2
        self.surface_x = GameSettings.SCREEN_WIDTH//2 - self.surface_width//2
        self.surface_y = GameSettings.SCREEN_HEIGHT//2 - self.surface_height//2
        self.bag_surface = pg.Surface((self.surface_width, self.surface_height))
        self.close_button = Button(
            "UI/button_x.png", "UI/button_x_hover.png",
            self.surface_width - 20 - 30, 20, 40, 40,
            lambda: scene_manager.close_bag(), self.surface_x, self.surface_y
        )

        self.game_fonts = {}
        for _size in range(10, 27, 2):
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
                self.draw_text(self.bag_surface, item["name"], "black", 400 + 30 + 30, self.close_button.hitbox.y + self.close_button.hitbox.height + 15 + i*40+7, 16)
                self.draw_text(self.bag_surface, f"x{item["count"]}", "black", 400 + 30 + 150,
                               self.close_button.hitbox.y + self.close_button.hitbox.height + 15 + i*40+7, 16, "right")
                i += 1

            # Draw monster, name, hp, max_hp, level
            i = 0
            start_x = 90
            start_y = self.close_button.hitbox.y - 30
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
                self.draw_text(monster_surface, monster["name"], "black", 30 + 25,10 , 14)
                self.draw_text(monster_surface, "Lv" + str(monster["level"]), "black", 15 + 115, 25, 12)

                # hp
                background_rect = pg.Rect(30 + 25,  25, background_rect_width, background_rect_height)
                pg.draw.rect(monster_surface, (50, 50, 50), background_rect)
                hp_rect = pg.Rect(30 + 25, 25,
                                          int(background_rect_width * monster["hp"] / monster["max_hp"]), background_rect_height)
                pg.draw.rect(monster_surface, (50, 200, 50), hp_rect)
                self.draw_text(monster_surface, f"{monster["hp"]}/{monster["max_hp"]}", "black",  30 + 25,40, 10)
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