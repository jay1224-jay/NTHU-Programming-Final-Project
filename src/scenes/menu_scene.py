import pygame as pg

from src.utils import GameSettings
from src.sprites import BackgroundSprite
from src.scenes.scene import Scene
from src.interface.components import Button
from src.core.services import scene_manager, sound_manager, input_manager
from typing import override
import json

class MenuScene(Scene):
    # Background Image
    background: BackgroundSprite
    # Buttons
    play_button: Button
    setting_button: Button
    
    def __init__(self):
        super().__init__()
        self.background = BackgroundSprite("backgrounds/background1.png")

        px, py = GameSettings.SCREEN_WIDTH // 2, GameSettings.SCREEN_HEIGHT * 3 // 4
        self.play_button = Button(
            "UI/button_play.png", "UI/button_play_hover.png",
            px + 50, py, 100, 100,
            lambda: scene_manager.change_scene("game")
        )

        self.setting_button = Button(
            "UI/button_setting.png", "UI/button_setting_hover.png",
            px - 150 , py, 100, 100,
            lambda: scene_manager.change_scene("setting")
        )
        
    @override
    def enter(self) -> None:
        sound_manager.play_bgm("RBY 101 Opening (Part 1).ogg")
        val = None
        mute = None
        with open('saves/game0.json') as f:
            d = json.load(f)
            val = d["volume"]["value"]
            mute = d["volume"]["mute"]
        if mute:
            sound_manager.set_bgm_volume(0)
        else:
            sound_manager.set_bgm_volume(val)

    @override
    def exit(self) -> None:
        pass

    @override
    def update(self, dt: float) -> None:
        if input_manager.key_pressed(pg.K_SPACE):
            scene_manager.change_scene("game")
            return
        self.play_button.update(dt)
        self.setting_button.update(dt)

    @override
    def draw(self, screen: pg.Surface) -> None:
        self.background.draw(screen)
        self.play_button.draw(screen)
        self.setting_button.draw(screen)
