import pygame as pg

from src.core.managers import game_manager
from src.utils import GameSettings, TextDrawer, Logger
from src.sprites import BackgroundSprite
from src.scenes.scene import Scene
from src.interface.components import Button
from src.core.services import scene_manager, sound_manager, input_manager
from src.core import GameManager
from typing import override
from src.sprites import Sprite

from random import randint

MONSTERS = ["Pickachu", "Charizard", "Blastoise", "Venusaur", "Gengar", "Dragonite"]

class CatchScene(Scene):
    # Background Image
    background: BackgroundSprite
    # Buttons
    play_button: Button
    setting_button: Button

    def __init__(self):
        super().__init__()

        self.bag = None
        self.not_updating_bag = True
        self.current_item = 0
        self.item_data = GameManager.load("saves/game0.json").to_dict()["bag"]["items"]

        self.background = BackgroundSprite("backgrounds/background1.png")

        self.option_surface_width = GameSettings.SCREEN_WIDTH
        self.option_surface_height = int(GameSettings.SCREEN_HEIGHT * 0.2)
        self.option_surface_x = 0
        self.option_surface_y = GameSettings.SCREEN_HEIGHT - self.option_surface_height
        self.option_surface_color  = (50, 50, 50)
        self.option_surface = pg.Surface((self.option_surface_width, self.option_surface_height))

        self.opponent_monster = None

        self.run_button = Button(
            "UI/raw/UI_Flat_Button02a_4.png", "UI/raw/UI_Flat_Button02a_2.png",
            self.option_surface_width//2 + 100 + 30, 50, 100, 50,
            lambda: scene_manager.change_scene("game"), label="LEAVE",
            surface_x=self.option_surface_x, surface_y=self.option_surface_y,
        )

        self.catch_button = Button(
            "UI/raw/UI_Flat_Button02a_4.png", "UI/raw/UI_Flat_Button02a_2.png",
            self.option_surface_width//2, 50, 100, 50,
            lambda: self.start_catch(), label="CATCH",
            surface_x=self.option_surface_x, surface_y=self.option_surface_y,
        )

        self.next_button = Button(
            "UI/raw/UI_Flat_Button02a_4.png", "UI/raw/UI_Flat_Button02a_2.png",
            self.option_surface_width // 2 - 100 - 30, 50, 100, 50,
            lambda: self.next_item(), label="SWITCH",
            surface_x=self.option_surface_x, surface_y=self.option_surface_y,
        )

        self.opponent_sprite_size = 200

        self.text_drawer = TextDrawer("assets/fonts/Minecraft.ttf")
        self.battle_winner = None
        self.msg = None
        self.catch_time_lapse = 0
        self.catch_status = 0
        self.current_item = 0
        self.start_catching = False
        self.catch_probability = 0

    def start_catch(self):
        self.start_catching = True
        self.catch_time_lapse = 0

    def _perform_probability(self):
        return randint(0, 100) <= self.catch_probability

    def player_catch(self):
        if self.start_catching:
            if self.item_data[self.current_item]["count"] <= 0:
                return
            self.item_data[self.current_item]["count"] -= 1
            if self._perform_probability():
                print("Catch")
                self.catch_status = "catch"
                self.msg = f"NICE! YOU CATCH {self.opponent_monster["name"]}!"
            else:
                self.catch_probability += randint(1, max(1, int((100 - self.catch_probability)*0.5)))
                self.catch_probability = min(self.catch_probability, 100)
                self.msg = "Probability of next catch: {}%".format(self.catch_probability)
            self.start_catching = False

    def next_item(self):
        self.current_item += 1
        while "pokeball" not in self.item_data[self.current_item % len(self.item_data)]["name"].lower():
            self.current_item += 1
        self.current_item %= len(self.item_data)

    @override
    def enter(self) -> None:
        sound_manager.play_bgm("RBY 106 Rival Appears!.ogg")
        self.current_item = 0
        self.run_button.label = "RUN"
        self.battle_winner = None
        self.catch_time_lapse = 0
        self.catch_status = 0
        self.catch_status = "not catch"
        self.current_item = -1
        self.next_item()
        self.start_catching = False

        _max_hp = randint(100, 200)
        _chosen_monster = randint(0, len(MONSTERS) - 1)
        self.opponent_monster = {
            "name": MONSTERS[_chosen_monster],
            "hp": _max_hp - randint(5, 20),
            "max_hp": _max_hp,
            "level": randint(1, 20),
            "sprite_path": f"menu_sprites/menusprite{_chosen_monster+1}.png"
        }

        self.catch_probability = randint(20, 70)
        self.msg = f"Catch Probability: {self.catch_probability}%"

    @override
    def exit(self) -> None:
        """
        : Save Monster Data After Exiting The Battle Scene
        """
        if self.catch_status == "catch":
            self.opponent_monster["hp"] = self.opponent_monster["max_hp"]
            Logger.debug("Saving New Acquired Monster Data")
            _game_manager = GameManager.load("saves/game0.json")
            data = _game_manager.to_dict()
            data["bag"]["items"] = self.item_data
            data["bag"]["monsters"].append(self.opponent_monster)
            _game_manager = _game_manager.from_dict(data)
            _game_manager.save("saves/game0.json")
        print("Exiting Battle Scene...")

    @override
    def update(self, dt: float) -> None:
        self.run_button.update(dt)

        if self.item_data[self.current_item]["count"] > 0:
            self.catch_button.update(dt)
            self.next_button.update(dt)
        else:
            self.msg = f"OH NO! YOU DONT HAVE ENOUGH {self.item_data[self.current_item]["name"]}."
        self.catch_time_lapse = (self.catch_time_lapse + dt) % 5
        self.player_catch()

    @override
    def draw(self, screen: pg.Surface) -> None:

        if self.not_updating_bag:
            self.item_data = GameManager.load("saves/game0.json").to_dict()["bag"]["items"]
            self.not_updating_bag = False

        self.option_surface.fill(self.option_surface_color)

        self.background.draw(screen)

        background_rect_width = 70
        background_rect_height = 10

        item = self.item_data[self.current_item]
        item_size = 100
        item_sprite = Sprite(item["sprite_path"], (item_size, item_size))
        screen.blit(item_sprite.image, (150, 300))

        item_info_surface_width = 170
        item_info_surface_height = 30
        item_info_surface = pg.Surface((item_info_surface_width, item_info_surface_height))
        item_info_surface.fill("WHITE")
        offset = 10
        self.text_drawer.draw(item_info_surface, item["name"], 16, (25 - offset, 10))
        self.text_drawer.draw(item_info_surface, f"X{item["count"]}", 16, (25 - offset + 80, 10))
        screen.blit(item_info_surface, (140, 450))

        # opponent
        opponent_monster_sprite = Sprite(self.opponent_monster["sprite_path"], (self.opponent_sprite_size, self.opponent_sprite_size))
        opponent_monster_info_surface_width = 170
        opponent_monster_info_surface_height = 50
        opponent_monster_info_surface = pg.Surface((opponent_monster_info_surface_width, opponent_monster_info_surface_height))
        opponent_monster_info_surface.fill("WHITE")
        offset = 10
        self.text_drawer.draw(opponent_monster_info_surface, self.opponent_monster["name"], 14, (25 - offset, 10))
        # hp
        background_rect = pg.Rect(25-offset, 25, background_rect_width, background_rect_height)
        pg.draw.rect(opponent_monster_info_surface, (50, 50, 50), background_rect)
        hp_rect = pg.Rect(25 - offset, 25,
                          int(background_rect_width * self.opponent_monster["hp"] / self.opponent_monster["max_hp"]), background_rect_height)
        pg.draw.rect(opponent_monster_info_surface, (50, 200, 50), hp_rect)
        self.text_drawer.draw(opponent_monster_info_surface, f"{self.opponent_monster["hp"]}/{self.opponent_monster["max_hp"]}", 10, (25 - offset, 40))
        self.text_drawer.draw(opponent_monster_info_surface, "Lv" + str(self.opponent_monster["level"]), 12,
                              (25 - offset + 70, 40))
        screen.blit(opponent_monster_info_surface, (1000, 300))

        if self.catch_status != "catch" and self.item_data[self.current_item]["count"] > 0:
            self.catch_button.draw(self.option_surface)
            self.next_button.draw(self.option_surface)
        self.run_button.draw(self.option_surface)

        self.text_drawer.draw(self.option_surface, self.msg, 20, (10, 10), color="white", align="left")
        screen.blit(self.option_surface, (self.option_surface_x, self.option_surface_y))
        screen.blit(opponent_monster_sprite.image, (800, 200))