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
from src.utils import Logger, PositionCamera, GameSettings, Position, TextDrawer
from src.core.services import scene_manager, sound_manager, input_manager
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
            "price": 200,
            "sprite_path": "menu_sprites/menusprite1.png"
        },
        {
            "name": "Blastoise",
            "hp": 192,
            "max_hp": 192,
            "level": 4,
            "price": 499,
            "sprite_path": "menu_sprites/menusprite3.png"
        },
        { "name": "Dragonite", "hp": 180, "max_hp": 220, "level": 40, "sprite_path": "menu_sprites/menusprite6.png", "price": 799}
    ],
    "items": [
        {
            "name": "Potion",
            "price": 100,
            "sprite_path": "ingame_ui/potion.png"
        },
        {
            "name": "Pokeball",
            "price": 10,
            "sprite_path": "ingame_ui/ball.png"
        }
    ]
}

class GameShopSurface:
    def __init__(self, text_drawer):
        self.text_drawer = TextDrawer("assets/fonts/Minecraft.ttf")
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
            lambda: self.change_surface(0), self.surface_x, self.surface_y, label="BUY"
        )
        self.sell_button = Button(
            "UI/raw/UI_Flat_Button02a_4.png", "UI/raw/UI_Flat_Button02a_2.png",
            90, 20, 70, 40,
            lambda: self.change_surface(1), self.surface_x, self.surface_y, label="SELL"
        )
        self.game_font = pg.font.Font(GameSettings.GAME_FONT, 24)

        self.start_y_buy = 40
        self.start_y_sell = 40

        self.save_settings = False
        self.load_settings = False

        self._status = BUY

        self._shop_data = _d.copy()
        self.player_monster_data = None

    def buy(self, purchase_type, item_index):
        # Buy and Save
        product = self._shop_data[purchase_type][item_index].copy()
        print("Buy:", product)
        data = GameManager.load("saves/game0.json").to_dict()
        player_bag = data["bag"]
        coin_ind = -1.5
        for i in range(len(player_bag["items"])):
            if player_bag["items"][i]["name"].lower() == "coins":
                coin_ind = i
        player_coins = player_bag["items"][coin_ind]["count"]
        product_price = product["price"]
        if player_coins >= product_price:
            player_coins -= product_price
            data["bag"]["items"][coin_ind]["count"] = player_coins

            if purchase_type == "monsters":
                del product["price"]
                data["bag"]["monsters"].append(product)
            else:
                # if duplicate
                d_ind = -1
                for i in range(len(data["bag"]["items"])):
                    if data["bag"]["items"][i]["name"].lower() == product["name"].lower():
                        d_ind = i
                        break
                if d_ind >= 0:
                    data["bag"]["items"][d_ind]["count"] += 1
                else:
                    del product["price"]
                    product["count"] = 1
                    data["bag"]["items"].append(product)

            gm = GameManager.from_dict(data)
            gm.save("saves/game0.json")
        else:
            print("Error: Not enough coins...")

    def sell(self, item_index, sold_price):

        data = GameManager.load("saves/game0.json").to_dict()
        player_bag = data["bag"]
        coin_ind = -1.5
        for i in range(len(player_bag["items"])):
            if player_bag["items"][i]["name"].lower() == "coins":
                coin_ind = i
        player_coins = player_bag["items"][coin_ind]["count"]
        player_coins += sold_price
        del player_bag["monsters"][item_index]
        data["bag"] = player_bag
        gm = GameManager.from_dict(data)
        gm.save("saves/game0.json")
        self.player_monster_data = data["bag"]["monsters"]

    def change_surface(self, n):
        if n == 1:
            self.start_y_sell = 40
            self._status = SELL
            data = GameManager.load("saves/game0.json").to_dict()
            self.player_monster_data = data.copy()["bag"]["monsters"]
        else:
            self.start_y_buy = 40
            self._status = BUY

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
        mouse_speed = 0
        # print(input_manager.mouse_pos)
        if 440 <= input_manager.mouse_pos[0] <= 800 and 190 <= input_manager.mouse_pos[1] <= 600 and scene_manager.shop_opened:
            mouse_speed = input_manager.mouse_wheel
        if self._status == BUY:
            self.start_y_buy += (dt * mouse_speed * 400)
        else:
            self.start_y_sell += (dt * mouse_speed * 400)

    def draw(self, screen: pg.Surface):
        if scene_manager.shop_opened:
            self.shop_surface.fill("ORANGE")
            self.close_button.draw(self.shop_surface)
            self.buy_button.draw(self.shop_surface)
            self.sell_button.draw(self.shop_surface)



            if self._status == BUY:
                start_x = 20
                start_y = self.start_y_buy - 80
                sprite_size = 50
                background_rect_width = 70
                background_rect_height = 10
                monster_surface_width = 250
                monster_surface_height = 50
                offset = 10

                # monsters and items
                # 2 Pokemons and 3 items
                buy_surface = pg.Surface((360, 350))
                buy_surface.fill("ORANGE")
                i = 0
                for monster in self._shop_data["monsters"]:
                    monster_surface = pg.Surface((monster_surface_width, monster_surface_height))
                    monster_surface.fill("WHITE")

                    monster_sprite = Sprite(monster["sprite_path"], (sprite_size, sprite_size))
                    monster_surface.blit(monster_sprite.image, (0, -5))
                    self.text_drawer.draw(monster_surface, monster["name"], 14, (30 + 25, 10))
                    self.text_drawer.draw(monster_surface, "Lv" + str(monster["level"]), 12, (15 + 115, 25))

                    # hp
                    background_rect = pg.Rect(30 + 25, 25, background_rect_width, background_rect_height)
                    pg.draw.rect(monster_surface, (50, 50, 50), background_rect)
                    hp_rect = pg.Rect(30 + 25, 25,
                                      int(background_rect_width * monster["hp"] / monster["max_hp"]),
                                      background_rect_height)
                    pg.draw.rect(monster_surface, (50, 200, 50), hp_rect)
                    self.text_drawer.draw(monster_surface, f"{monster["hp"]}/{monster["max_hp"]}", 10,
                                          (30 + 25, 40))
                    self.text_drawer.draw(monster_surface, f"${monster["price"]}", 20, (240, 20),
                                          "right")
                    buy_surface.blit(monster_surface,
                                          (start_x, start_y + i * (monster_surface_height + offset) + 40))


                    button = Button(
                        "UI/button_shop.png", "UI/button_shop_hover.png",
                        start_x + monster_surface_width + 20, start_y + i * (monster_surface_height + offset) + 40, 40, 40,
                    lambda: self.buy("monsters", i), self.surface_x + 20, self.surface_y + 90)
                    button.update(0)
                    button.draw(buy_surface)

                    i += 1

                pg.draw.rect(buy_surface, "BLACK",
                (start_x - 15, start_y + len(self._shop_data["monsters"]) * (monster_surface_height + offset) + 50, self.surface_width - start_x + 5, 5))
                i = 0
                padding = 40
                start_y = start_y + len(self._shop_data["monsters"]) * (monster_surface_height + offset)
                start_y = start_y + padding
                for item in self._shop_data["items"]:
                    item_surface = pg.Surface((monster_surface_width, monster_surface_height))
                    item_surface.fill("WHITE")
                    item_sprite = Sprite(item["sprite_path"], (30, 30))
                    item_surface.blit(item_sprite.image, (5, 10))
                    self.text_drawer.draw(item_surface, item["name"], 20,
                                          (50, 20))
                    self.text_drawer.draw(item_surface, f"${item["price"]}", 20, (240, 20),
                                          "right")

                    buy_surface.blit(item_surface,
                        (start_x, start_y + i * (monster_surface_height + offset) + 40))
                    button = Button(
                        "UI/button_shop.png", "UI/button_shop_hover.png",
                        start_x + monster_surface_width + 20, start_y + i * (monster_surface_height + offset) + 40, 40, 40,
                    lambda: self.buy("items", i), self.surface_x + 20, self.surface_y+90)
                    button.update(0)
                    button.draw(buy_surface)
                    i += 1

                self.shop_surface.blit(buy_surface, (start_x, 90))
            elif self._status == SELL:
                start_x = 20
                start_y = self.start_y_sell - 80
                sprite_size = 50
                background_rect_width = 70
                background_rect_height = 10
                monster_surface_width = 250
                monster_surface_height = 50
                offset = 10
                # only monsters
                buy_surface = pg.Surface((360, 350))
                buy_surface.fill("ORANGE")
                i = 0
                for monster in self.player_monster_data:
                    monster_surface = pg.Surface((monster_surface_width, monster_surface_height))
                    monster_surface.fill("WHITE")

                    monster_sprite = Sprite(monster["sprite_path"], (sprite_size, sprite_size))
                    monster_surface.blit(monster_sprite.image, (0, -5))
                    self.text_drawer.draw(monster_surface, monster["name"], 14, (30 + 25, 10))
                    self.text_drawer.draw(monster_surface, "Lv" + str(monster["level"]), 12, (15 + 115, 25))

                    # hp
                    background_rect = pg.Rect(30 + 25, 25, background_rect_width, background_rect_height)
                    pg.draw.rect(monster_surface, (50, 50, 50), background_rect)
                    hp_rect = pg.Rect(30 + 25, 25,
                                      int(background_rect_width * monster["hp"] / monster["max_hp"]),
                                      background_rect_height)
                    pg.draw.rect(monster_surface, (50, 200, 50), hp_rect)
                    self.text_drawer.draw(monster_surface, f"{monster["hp"]}/{monster["max_hp"]}", 10,
                                          (30 + 25, 40))

                    # Price
                    monster_price = monster["level"]
                    self.text_drawer.draw(monster_surface, f"${monster_price}", 20, (240, 20),
                                          "right")
                    # Price

                    buy_surface.blit(monster_surface,
                                     (start_x, start_y + i * (monster_surface_height + offset) + 40))

                    button = Button(
                        "UI/button_shop.png", "UI/button_shop_hover.png",
                        start_x + monster_surface_width + 20, start_y + i * (monster_surface_height + offset) + 40, 40,
                        40,
                        lambda: self.sell(i, monster_price), self.surface_x + 20, self.surface_y + 90)
                    button.update(0)
                    button.draw(buy_surface)

                    i += 1

                self.shop_surface.blit(buy_surface, (start_x, 90))
            else:
                Logger.debug("Unknown shop status")


            screen.blit(self.shop_surface, (self.surface_x, self.surface_y))

