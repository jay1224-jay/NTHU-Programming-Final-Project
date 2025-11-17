import pygame as pg
import threading
import time

from src.scenes.scene import Scene
from src.core import GameManager, OnlineManager
from src.utils import Logger, PositionCamera, GameSettings, Position
from src.core.services import scene_manager, sound_manager
from src.sprites import Sprite
from typing import override
from src.data import bag
from .setting_surface import GameSettingSurface

from src.interface.components import Button

class GameScene(Scene):
    game_manager: GameManager
    online_manager: OnlineManager | None
    sprite_online: Sprite
    
    def __init__(self):
        super().__init__()
        # Game Manager
        manager = GameManager.load("saves/game0.json")
        if manager is None:
            Logger.error("Failed to load game manager")
            exit(1)
        self.game_manager = manager
        
        # Online Manager
        if GameSettings.IS_ONLINE:
            self.online_manager = OnlineManager()
        else:
            self.online_manager = None
        self.sprite_online = Sprite("ingame_ui/options1.png", (GameSettings.TILE_SIZE, GameSettings.TILE_SIZE))

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

        self.setting_surface = GameSettingSurface()


    @override
    def enter(self) -> None:
        sound_manager.play_bgm("RBY 103 Pallet Town.ogg")
        if self.online_manager:
            self.online_manager.enter()
        
    @override
    def exit(self) -> None:
        if self.online_manager:
            self.online_manager.exit()
        
    @override
    def update(self, dt: float):
        # Check if there is assigned next scene
        self.game_manager.try_switch_map()
        
        # Update player and other data
        if self.game_manager.player:
            self.game_manager.player.update(dt)
        for enemy in self.game_manager.current_enemy_trainers:
            enemy.update(dt)
            
        # Update others
        self.game_manager.bag.update(dt)
        self.setting_surface.update(dt)
        self.setting_button.update(dt)
        self.backpack_button.update(dt)
        
        if self.game_manager.player is not None and self.online_manager is not None:
            _ = self.online_manager.update(
                self.game_manager.player.position.x, 
                self.game_manager.player.position.y,
                self.game_manager.current_map.path_name
            )
        
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



        
        if self.online_manager and self.game_manager.player:
            list_online = self.online_manager.get_list_players()
            for player in list_online:
                if player["map"] == self.game_manager.current_map.path_name:
                    cam = self.game_manager.player.camera
                    pos = cam.transform_position_as_position(Position(player["x"], player["y"]))
                    self.sprite_online.update_pos(pos)
                    self.sprite_online.draw(screen)

        self.setting_button.draw(screen)
        if scene_manager.bag_opened or scene_manager.setting_opened:
            dark_overlay = pg.Surface(screen.get_size(), pg.SRCALPHA)
            dark_overlay.fill((0, 0, 0, 128))
            screen.blit(dark_overlay, (0, 0))


        self.game_manager.bag.draw(screen)
        self.setting_surface.draw(screen)

        self.backpack_button.draw(screen)
