from __future__ import annotations

import pygame as pg


from src.sprites import Sprite
from src.core.services import input_manager
from src.utils import Logger
from typing import Callable, override
from .component import UIComponent

class Button(UIComponent):
    img_button: Sprite
    img_button_default: Sprite
    img_button_hover: Sprite
    hitbox: pg.Rect
    on_click: Callable[[], None] | None

    def __init__(
        self,
        img_path: str, img_hovered_path:str,
        x: int, y: int, width: int, height: int,
        on_click: Callable[[], None] | None = None, surface_x=0, surface_y=0,
    ):
        self.img_button_default = Sprite(img_path, (width, height))
        self.hitbox = pg.Rect(x, y, width, height)
        '''
        [TODO HACKATHON 1]
        Initialize the properties
        '''
        self.img_button_hover = Sprite(img_hovered_path, (width, height))
        self.img_button = Sprite(img_path, (width, height))      # --> This is a reference for which image to render
        self.on_click = on_click
        self.surface_x = surface_x
        self.surface_y = surface_y

    @override
    def update(self, dt: float) -> None:
        '''
        [TODO HACKATHON 1]
        Check if the mouse cursor is colliding with the button, 
        1. If collide, draw the hover image
        2. If collide & clicked, call the on_click function
        
        if self.hitbox.collidepoint(input_manager.mouse_pos):
            ...
            if input_manager.mouse_pressed(1) and self.on_click is not None:
                ...
        else:
            ...
        '''
        if self.hitbox.collidepoint((input_manager.mouse_pos[0]-self.surface_x, input_manager.mouse_pos[1]-self.surface_y)):
            self.img_button_default.image = self.img_button_hover.image
            if input_manager.mouse_pressed(1) and self.on_click is not None:
                self.on_click()
        else:
            self.img_button_default.image = self.img_button.image
    
    @override
    def draw(self, screen: pg.Surface) -> None:
        '''
        [TODO HACKATHON 1]
        You might want to change this too
        '''
        _ = screen.blit(self.img_button_default.image, self.hitbox)

def main():
    import sys
    import os

    
    pg.init()

    WIDTH, HEIGHT = 800, 800
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    pg.display.set_caption("Button Test")
    clock = pg.time.Clock()
    
    bg_color = (0, 0, 0)
    def on_button_click():
        nonlocal bg_color
        if bg_color == (0, 0, 0):
            bg_color = (255, 255, 255)
        else:
            bg_color = (0, 0, 0)
        
    button = Button(
        img_path="UI/button_play.png",
        img_hovered_path="UI/button_play_hover.png",
        x=WIDTH // 2 - 50,
        y=HEIGHT // 2 - 50,
        width=100,
        height=100,
        on_click=on_button_click
    )
    
    running = True
    dt = 0
    
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            input_manager.handle_events(event)
        
        dt = clock.tick(60) / 1000.0
        button.update(dt)
        
        input_manager.reset()
        
        _ = screen.fill(bg_color)
        
        button.draw(screen)
        
        pg.display.flip()
    
    pg.quit()


if __name__ == "__main__":
    main()
