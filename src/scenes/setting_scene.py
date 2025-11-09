'''
[TODO HACKATHON 5]
Try to mimic the menu_scene.py or game_scene.py to create this new scene
'''

import pygame as pg

from src.utils import GameSettings
from src.sprites import BackgroundSprite
from src.scenes.scene import Scene
from src.interface.components import Button
from src.core.services import scene_manager, sound_manager, input_manager
from typing import override


class SettingScene(Scene):
    # Background Image
    background: BackgroundSprite
    # Buttons
    back_button: Button

    def __init__(self):
        super().__init__()
        self.background = BackgroundSprite("backgrounds/background1.png")

        px, py = GameSettings.SCREEN_WIDTH // 2, GameSettings.SCREEN_HEIGHT * 3 // 4
        self.back_button = Button(
            "UI/button_back.png", "UI/button_back_hover.png",
            px - 150, py, 75, 75,
            lambda: scene_manager.change_scene("menu")
        )

    @override
    def enter(self) -> None:
        sound_manager.play_bgm("RBY 102 Opening (Part 2).ogg")
        pass

    @override
    def exit(self) -> None:
        pass

    @override
    def update(self, dt: float) -> None:
        if input_manager.key_pressed(pg.K_SPACE):
            scene_manager.change_scene("game")
            return
        self.back_button.update(dt)

    @override
    def draw(self, screen: pg.Surface) -> None:
        self.background.draw(screen)
        self.back_button.draw(screen)
