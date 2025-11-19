# UI_Flat_ButtonCheck01a.png

from __future__ import annotations

import pygame as pg

from src.sprites import Sprite
from src.core.services import input_manager
from src.utils import Logger
from typing import Callable, override
from .component import UIComponent


class Checkbox(UIComponent):
    img_button: Sprite
    img_button_default: Sprite
    img_button_hover: Sprite
    hitbox: pg.Rect
    on_click: Callable[[], None] | None

    def __init__(
            self,
            x: int, y: int, width: int, height: int, initial_value: bool,
            on_click: Callable[[], None] | None = None, surface_x=0, surface_y=0,
    ):
        self.img_on_path = "UI/raw/UI_Flat_ToggleOn03a.png"
        self.img_off_path = "UI/raw/UI_Flat_ToggleOff03a.png"

        self.initial_value = initial_value
        self.value = self.initial_value

        self.img_button_default = Sprite((self.img_on_path if self.initial_value else self.img_off_path), (width, height))
        self.hitbox = pg.Rect(x + (width * self.initial_value / 100), y, width, height)

        self.box_on = Sprite(self.img_on_path, (width, height))
        self.box_off = Sprite(self.img_off_path, (width, height))

        self.on_click = on_click
        self.surface_x = surface_x
        self.surface_y = surface_y

    def get_value(self):
        return bool(self.value)

    @override
    def update(self, dt: float) -> None:
        if self.hitbox.collidepoint(
                (input_manager.mouse_pos[0] - self.surface_x, input_manager.mouse_pos[1] - self.surface_y)):
            if input_manager.mouse_pressed(1):
                self.value = not self.value

                if self.value:
                    # Mute
                    self.img_button_default = self.box_on
                else:
                    self.img_button_default = self.box_off
                self.on_click()

    @override
    def draw(self, screen: pg.Surface) -> None:
        _ = screen.blit(self.img_button_default.image, self.hitbox)


