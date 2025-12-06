import pygame as pg
import threading
import time

from src.scenes.scene import Scene
from src.core import GameManager, OnlineManager
from src.utils import Logger, PositionCamera, GameSettings, Position, TextDrawer
from src.core.services import scene_manager, sound_manager
from src.sprites import Sprite, Animation
from typing import override
from src.data import bag
from .setting_surface import GameSettingSurface
from .shop_surface import GameShopSurface

from src.interface.components import Button


class GameScene(Scene):
    game_manager: GameManager
    online_manager: OnlineManager | None
    sprite_online: Sprite
    
    def __init__(self):
        super().__init__()
        # Game Manager
        manager = GameManager.load("saves/game0.json")
        self.game_manager = manager
        if manager is None:
            Logger.error("Failed to load game manager")
            exit(1)
        self.game_manager = manager
        
        # Online Manager
        if GameSettings.IS_ONLINE:
            self.online_manager = OnlineManager()
        else:
            self.online_manager = None
        self.sprite_online = Animation(
            "character/ow5.png", ["down", "left", "right", "up"], 4,
            (GameSettings.TILE_SIZE, GameSettings.TILE_SIZE)
        )
        self.online_player_pre_position = []

        self.bag_opened = False
        self.setting_button = Button(
            "UI/button_setting.png", "UI/button_setting_hover.png",
            GameSettings.SCREEN_WIDTH - 75, 50, 50, 50,
            lambda: scene_manager.open_setting()
        )

        self.backpack_button = Button(
            "UI/button_backpack.png", "UI/button_backpack_hover.png",
            GameSettings.SCREEN_WIDTH - 75 - 50 - 10, 50, 50, 50,
            lambda: scene_manager.open_bag()
        )
        self.setting_surface = None
        self.shop_surface = None
        self.text_drawer = TextDrawer("assets/fonts/Minecraft.ttf")

    def save_settings(self):
        """
        : Save Volume Settings
        """
        data = self.game_manager.to_dict()
        data["volume"] = {"value": self.setting_surface.volume_slider.get_value(), "mute": self.setting_surface.mute_checkbox.get_value()}
        self.game_manager = self.game_manager.from_dict(data)
        sound_manager.set_bgm_volume(self.setting_surface.volume_slider.get_value())
        self.game_manager.save("saves/game0.json")
        self.setting_surface.save_settings = False

    def load_settings(self):
        self.game_manager = self.game_manager.load("saves/game0.json")
        self.setting_surface.load_settings = False

    @override
    def enter(self) -> None:
        sound_manager.play_bgm("RBY 103 Pallet Town.ogg")
        if self.online_manager:
            self.online_manager.enter()

        data = GameManager.load(
            "saves/game0.json").to_dict()
        self.setting_surface = GameSettingSurface(data["volume"])
        self.shop_surface = GameShopSurface()
        val = data["volume"]["value"]
        mute = data["volume"]["mute"]
        if mute:
            sound_manager.set_bgm_volume(0)
        else:
            sound_manager.set_bgm_volume(val)
    @override
    def exit(self) -> None:
        if self.online_manager:
            self.online_manager.exit()
        
    @override
    def update(self, dt: float):
        # Check if there is assigned next scene
        self.game_manager.try_switch_map()
        # print(self.game_manager.player.position)
        
        # Update player and other data
        if self.game_manager.player:
            self.game_manager.player.update(dt)
        for enemy in self.game_manager.current_enemy_trainers:
            enemy.update(dt)
        for merchant in self.game_manager.current_merchants:
            merchant.update(dt)
            
        # Update others
        self.game_manager.bag.update(dt)
        self.setting_surface.update(dt)
        self.shop_surface.update(dt)
        self.setting_button.update(dt)
        self.backpack_button.update(dt)
        
        if self.game_manager.player is not None and self.online_manager is not None:
            _ = self.online_manager.update(
                self.game_manager.player.position.x, 
                self.game_manager.player.position.y,
                self.game_manager.player.direction,
                self.game_manager.current_map.path_name,
                dt
            )
        if self.setting_surface.save_settings:
            self.save_settings()
        if self.setting_surface.load_settings:
            self.load_settings()

    @override
    def draw(self, screen: pg.Surface):

        if self.game_manager.player:
            '''
            [TODO HACKATHON 3]
            Implement the camera    algorithm logic here
            Right now it's hard coded, you need to follow the player's positions
            you may use the below example, but the function still incorrect, you may trace the entity.py
            
            camera = self.game_manager.player.camera
            '''
            camera = self.game_manager.player.camera
            # camera = PositionCamera(16 * GameSettings.TILE_SIZE, 30 * GameSettings.TILE_SIZE)
            self.game_manager.current_map.draw(screen, camera, scene_manager.bag_opened)
            self.game_manager.player.draw(screen, camera)
        else:
            camera = PositionCamera(0, 0)
            self.game_manager.current_map.draw(screen, camera)
        for enemy in self.game_manager.current_enemy_trainers:
            enemy.draw(screen, camera)

        for merchant in self.game_manager.current_merchants:
            merchant.draw(screen, camera)

        if self.online_manager and self.game_manager.player:
            list_online = self.online_manager.get_list_players()
            if len(self.online_player_pre_position) != len(list_online):
                self.online_player_pre_position = list_online
            # print(self.online_player_pre_position)
            for i in range(len(list_online)):
                player = list_online[i]
                if player["map"] == self.game_manager.current_map.path_name:

                    if self.online_player_pre_position[i] == (player["x"], player["y"]):
                        self.sprite_online.stationary = True
                        self.sprite_online.stationary_time += player["dt"]
                    else:
                        self.sprite_online.stationary_time = 0
                        self.sprite_online.stationary = False
                    cam = self.game_manager.player.camera
                    pos = cam.transform_position_as_position(Position(player["x"], player["y"]))
                    self.sprite_online.update_pos(pos)
                    self.sprite_online.switch(player["dir"])
                    if player["inactive"]:
                        self.text_drawer.draw(screen, "AFK", 14, [pos.x+15, pos.y-15])
                    self.sprite_online.draw(screen, None, player["inactive"])
                    self.sprite_online.update(player["dt"])

            self.online_player_pre_position = [(player["x"], player["y"]) for player in list_online]
            # print(self.online_player_pre_position)



        self.setting_button.draw(screen)
        if scene_manager.bag_opened or scene_manager.setting_opened or scene_manager.shop_opened:
            dark_overlay = pg.Surface(screen.get_size(), pg.SRCALPHA)
            dark_overlay.fill((0, 0, 0, 128))
            screen.blit(dark_overlay, (0, 0))


        self.game_manager.bag.draw(screen)
        self.setting_surface.draw(screen)
        self.shop_surface.draw(screen)
        self.backpack_button.draw(screen)

        self.text_drawer.draw(screen,
        f"Tile Pos: ({int(self.game_manager.player.position.x//GameSettings.TILE_SIZE)},{int(self.game_manager.player.position.y//GameSettings.TILE_SIZE)})",
        20, (0, GameSettings.SCREEN_HEIGHT - 20), color=(255, 255, 255))
