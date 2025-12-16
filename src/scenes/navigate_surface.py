from src.utils.definition import Monster, Item
from src.interface.components import Button
import pygame as pg

from functools import partial

from src.scenes.scene import Scene
from src.core import GameManager, OnlineManager
from src.utils import Logger, PositionCamera, GameSettings, Position, TextDrawer
from src.core.services import scene_manager, sound_manager
from src.sprites import Sprite
from typing import override

button_data = [
    {
        "name": "spawn",
        "dest_x": "16",
        "dest_y": "31"
    },
    {
        "name": "gym",
        "dest_x": "24",
        "dest_y": "24"
    },
    {
        "name": "tl-corner",
        "dest_x": "56",
        "dest_y": "7"
    }
]
offset = 20
class NavigateSurface:
    def __init__(self):
        self.surface_width, self.surface_height = GameSettings.SCREEN_WIDTH//2, GameSettings.SCREEN_HEIGHT//2
        self.surface_x = GameSettings.SCREEN_WIDTH//2 - self.surface_width//2
        self.surface_y = GameSettings.SCREEN_HEIGHT//2 - self.surface_height//2
        self.navigation_surface = pg.Surface((self.surface_width, self.surface_height))
        self.text_drawer = TextDrawer("assets/fonts/Minecraft.ttf")
        self.navigation_buttons = []

        self.close_button = Button(
            "UI/button_x.png", "UI/button_x_hover.png",
            20, self.surface_height - 50, 40, 40,
            lambda: scene_manager.close_navigation(), self.surface_x, self.surface_y
        )

        for i in range(len(button_data)):
            button = Button(
                "UI/button_play.png", "UI/button_play_hover.png",
                20 + i*(50+offset), 30, 50, 50,
                partial(self.navigate, i), self.surface_x, self.surface_y
            )
            self.navigation_buttons.append(button)

    def navigate(self, i):
        scene_manager.navigation_dest = (int(button_data[i]["dest_x"]), int(button_data[i]["dest_y"]))
        scene_manager.close_navigation()

    def update(self, dt: float):
        if scene_manager.navigation_opened:
            for i in range(len(self.navigation_buttons)):
                self.navigation_buttons[i].update(dt)
            self.close_button.update(dt)

    def draw(self, screen: pg.Surface):
        if scene_manager.navigation_opened:
            self.navigation_surface.fill("orange")
            for i in range(len(self.navigation_buttons)):
                self.navigation_buttons[i].draw(self.navigation_surface)
                self.text_drawer.draw(self.navigation_surface, button_data[i]["name"].lower(), 15, (45 + i * (50+offset), 100), align="center")
                # print(i)
            self.close_button.draw(self.navigation_surface)
            screen.blit(self.navigation_surface, (self.surface_x, self.surface_y))


