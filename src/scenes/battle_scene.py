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

class BattleScene(Scene):
    # Background Image
    background: BackgroundSprite
    # Buttons
    play_button: Button
    setting_button: Button

    def __init__(self):
        super().__init__()

        self.bag = None
        self.not_updating_bag = True
        self.current_monster = 0

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
            lambda: scene_manager.change_scene("game"), label="RUN",
            surface_x=self.option_surface_x, surface_y=self.option_surface_y,
        )

        self.attack_button = Button(
            "UI/raw/UI_Flat_Button02a_4.png", "UI/raw/UI_Flat_Button02a_2.png",
            self.option_surface_width//2, 50, 100, 50,
            lambda: self.player_attack(), label="ATTACK",
            surface_x=self.option_surface_x, surface_y=self.option_surface_y,
        )

        self.next_button = Button(
            "UI/raw/UI_Flat_Button02a_4.png", "UI/raw/UI_Flat_Button02a_2.png",
            self.option_surface_width // 2 - 100 - 30, 50, 100, 50,
            lambda: self.next_monster(), label="SWITCH",
            surface_x=self.option_surface_x, surface_y=self.option_surface_y,
        )

        self.fight_button = Button(
            "UI/raw/UI_Flat_Button02a_4.png", "UI/raw/UI_Flat_Button02a_2.png",
            self.option_surface_width // 2, 50, 100, 50,
            lambda: self.start_fight(), label="FIGHT",
            surface_x=self.option_surface_x, surface_y=self.option_surface_y,
        )

        self.text_drawer = TextDrawer("assets/fonts/Minecraft.ttf")
        self.battle_winner = None
        self.msg = None
        self.attack_turn = 0
        self.attack_time_lapse = 0
        self.start_fighting = 0

    def start_fight(self):
        self.start_fighting = 1

    def player_attack(self):
        if self.attack_turn % 2 == 0 and self.bag._monsters_data[self.current_monster]["hp"]:
            self.opponent_monster["hp"] -= self.bag._monsters_data[self.current_monster]["level"]
            self.attack_time_lapse = 0
            if self.opponent_monster["hp"] <= 0:
                self.opponent_monster["hp"] = 0
                self.battle_winner = "player"
                self.msg = "You win!"
                sound_manager.play_bgm("RBY 108 Victory! (Trainer).ogg")
            self.attack_turn += 1

    def enemy_attack(self):
        # print(self.attack_time_lapse)
        if self.attack_turn % 2 == 1 and self.opponent_monster["hp"]:
            if self.attack_time_lapse >= 0.5: # delay
                self.bag._monsters_data[self.current_monster]["hp"] -= self.opponent_monster["level"]
                if self.bag._monsters_data[self.current_monster]["hp"] <= 0:
                    self.bag._monsters_data[self.current_monster]["hp"] = 0
                    self.battle_winner = "enemy"
                    self.msg = "Your monster is dead!"
                self.attack_turn += 1


    def next_monster(self):
        self.current_monster += 1
        self.current_monster %= len(self.bag._monsters_data)

    @override
    def enter(self) -> None:
        sound_manager.play_bgm("RBY 107 Battle! (Trainer).ogg")
        self.current_monster = 0
        self.run_button.label = "RUN"
        self.battle_winner = None
        self.msg = None
        self.attack_turn = 0
        self.attack_time_lapse = 0
        self.start_fighting = 0


        _max_hp = randint(100, 200)
        _chosen_monster = randint(0, len(MONSTERS) - 1)
        self.opponent_monster = {
            "name": MONSTERS[_chosen_monster],
            "hp": _max_hp - randint(5, 20),
            "max_hp": _max_hp,
            "level": randint(1, 20),
            "sprite_path": f"menu_sprites/menusprite{_chosen_monster+1}.png"
          }


    @override
    def exit(self) -> None:
        """
        : Save Monster Data After Exiting The Battle Scene
        """
        self.start_fighting = 0
        if self.battle_winner == "player":
            self.opponent_monster["hp"] = self.opponent_monster["max_hp"]
            Logger.debug("Saving New Acquired Monster Data")
            _game_manager = GameManager.load("saves/game0.json")
            data = _game_manager.to_dict()
            data["bag"]["monsters"].append(self.opponent_monster)
            _game_manager = _game_manager.from_dict(data)
            _game_manager.save("saves/game0.json")
        print("Exiting Battle Scene...")

    @override
    def update(self, dt: float) -> None:
        if self.battle_winner:
            self.run_button.label = "LEAVE"
        self.run_button.update(dt)
        if self.bag is not None:
            if self.bag._monsters_data[self.current_monster]["hp"] > 0 and self.start_fighting:
                self.attack_button.update(dt)

        if not self.start_fighting:
            self.fight_button.update(dt)
            self.next_button.update(dt)
        self.attack_time_lapse = (self.attack_time_lapse + dt) % 5

        self.enemy_attack()

    @override
    def draw(self, screen: pg.Surface) -> None:

        if self.not_updating_bag:
            self.bag = GameManager.load("saves/game0.json").bag
            self.not_updating_bag = False

        self.option_surface.fill(self.option_surface_color)

        self.background.draw(screen)

        monster = self.bag._monsters_data[self.current_monster]
        sprite_size = 200
        monster_sprite = Sprite(monster["sprite_path"], (sprite_size, sprite_size))


        background_rect_width = 70
        background_rect_height = 10
        monster_info_surface_width = 170
        monster_info_surface_height = 50
        monster_info_surface = pg.Surface((monster_info_surface_width, monster_info_surface_height))
        monster_info_surface.fill("WHITE")
        offset = 10
        self.text_drawer.draw(monster_info_surface, monster["name"], 14, (25 - offset, 10))
        # hp
        background_rect = pg.Rect(25-offset, 25, background_rect_width, background_rect_height)
        pg.draw.rect(monster_info_surface, (50, 50, 50), background_rect)
        hp_rect = pg.Rect(25 - offset, 25,
                          int(background_rect_width * monster["hp"] / monster["max_hp"]), background_rect_height)
        pg.draw.rect(monster_info_surface, (50, 200, 50), hp_rect)
        self.text_drawer.draw(monster_info_surface, f"{monster["hp"]}/{monster["max_hp"]}", 10, (25 - offset, 40))
        self.text_drawer.draw(monster_info_surface, "Lv" + str(monster["level"]), 12,
                              (25 - offset + 70, 40))
        screen.blit(monster_info_surface, (25, 500))

        # opponent
        opponent_monster_sprite = Sprite(self.opponent_monster["sprite_path"], (sprite_size, sprite_size))
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

        self.run_button.draw(self.option_surface)
        if self.opponent_monster["hp"] > 0 and monster["hp"] > 0 and self.start_fighting:
            self.attack_button.draw(self.option_surface)

        if not self.start_fighting:
            self.fight_button.draw(self.option_surface)

            self.next_button.draw(self.option_surface)

        self.text_drawer.draw(self.option_surface, self.msg, 20, (10, 10), color="white", align="left")

        screen.blit(self.option_surface, (self.option_surface_x, self.option_surface_y))

        if monster["hp"] <= 0:
            screen.blit(pg.transform.grayscale(pg.transform.flip(monster_sprite.image, 1, 0)), (150, 300))
        else:
            screen.blit(pg.transform.flip(monster_sprite.image, 1, 0), (150, 300))

        if self.opponent_monster["hp"] <= 0:
            screen.blit(pg.transform.grayscale(opponent_monster_sprite.image), (800, 200))
        else:
            screen.blit(opponent_monster_sprite.image, (800, 200))