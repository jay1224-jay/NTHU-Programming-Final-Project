from __future__ import annotations

import pygame as pg

from src.sprites import Sprite
from src.core.services import input_manager
from src.utils import Logger
from typing import Callable, override
from .component import UIComponent


class Slider(UIComponent):
    img_button: Sprite
    img_button_default: Sprite
    img_button_hover: Sprite
    hitbox: pg.Rect
    on_click: Callable[[], None] | None

    def __init__(
            self,
            x: int, y: int, width: int, height: int, initial_value = 0,
            on_click: Callable[[], None] | None = None, surface_x=0, surface_y=0,
    ):
        img_path = "UI/raw/UI_Flat_Button02a_4.png"

        self.slider_background = pg.Rect(x, y, width, height)
        self.slider_background_start_x = x
        self.initial_value = initial_value
        self.value = self.initial_value

        self.img_button_default = Sprite(img_path, (height, height))
        self.hitbox = pg.Rect(x + (width * self.initial_value / 100), y, height, height)

        self.img_button = Sprite(img_path, (height, height))  # --> This is a reference for which image to render
        self.on_click = on_click
        self.surface_x = surface_x
        self.surface_y = surface_y

    def get_value(self):
        return int(self.value)

    @override
    def update(self, dt: float) -> None:
        if self.hitbox.collidepoint(
                (input_manager.mouse_pos[0] - self.surface_x, input_manager.mouse_pos[1] - self.surface_y)):
            if input_manager.mouse_down(1) and self.on_click is not None:
                # print(self.hitbox.x, input_manager.mouse_pos[0])
                self.hitbox.x = max(self.slider_background.x, input_manager.mouse_pos[0] - self.surface_x - self.hitbox.width//2) # centered to the mouse
                self.hitbox.x = min(self.slider_background.x + self.slider_background.width - self.hitbox.width, self.hitbox.x)
                self.value = (self.hitbox.x - self.slider_background_start_x)/(self.slider_background.width - self.hitbox.width) * 100

        # print(round(self.value, 1))

    @override
    def draw(self, screen: pg.Surface) -> None:
        pg.draw.rect(screen, (100, 100, 100), self.slider_background)
        _ = screen.blit(self.img_button_default.image, self.hitbox)


