import pygame as pg

from .sprite import Sprite
from src.utils import GameSettings, Logger, PositionCamera, Position
from typing import Optional

class Animation(Sprite):
    # Animations
    animations: dict[str, list[pg.Surface]]
    cur_row: str
    # Time information for selections
    accumulator: float  # time elapsed
    loop: float         # maximum time 
    n_keyframes: int    # number of keyframes
    
    def __init__(
        self, image_path: str,
        rows: list[str], n_keyframes: int,  # Row x Column for grids
        size: tuple[int, int],              # Size of the animation in rendering
        loop: float = 1                     # loop in second
    ):
        super().__init__(image_path)
        sheet_w, sheet_h = self.image.get_size()
        frame_w = sheet_w // n_keyframes
        frame_h = sheet_h // len(rows)
        
        if (len(rows) <= 0 or n_keyframes <= 0):
            Logger.error("Invalid number of rows")
        
        self.animations = {}
        for r, name in enumerate(rows):
            anim : list[pg.Surface] = []
            for c in range(n_keyframes):
                frame = self.image.subsurface(pg.Rect(
                    c * frame_w, r * frame_h,
                    frame_w, frame_h
                ))
                anim.append(pg.transform.smoothscale(frame, size))
            self.animations[name] = anim
            
        self.accumulator = 0
        self.cur_row = rows[0]
        self.loop = loop
        self.n_keyframes = n_keyframes
        self.rect = pg.Rect(0, 0, GameSettings.TILE_SIZE, GameSettings.TILE_SIZE)
            
    def switch(self, name: str):
        if name not in self.animations:
            Logger.error(f"name {name} not in animations list!")
        self.cur_row = name

    def update_pos(self, pos: Position):
        self.rect.topleft = (int(pos.x), int(pos.y))
        
    def update(self, dt: float):
         self.accumulator = (self.accumulator + dt) % self.loop
        
    def draw(self, screen: pg.Surface, camera: Optional[PositionCamera] = None):
        frames = self.animations[self.cur_row]
        idx = int((self.accumulator / self.loop) * self.n_keyframes)
        if camera:
            screen.blit(frames[idx], camera.transform_rect(self.rect))
        else:
            screen.blit(frames[idx], self.rect)
    