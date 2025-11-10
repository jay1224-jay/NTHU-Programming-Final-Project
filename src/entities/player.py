from __future__ import annotations

import dis

import pygame as pg
from .entity import Entity
from src.core.services import input_manager, scene_manager
from src.utils import Position, PositionCamera, GameSettings, Logger
from src.core import GameManager
import math
from typing import override

class Player(Entity):
    speed: float = 4.0 * GameSettings.TILE_SIZE
    game_manager: GameManager

    def __init__(self, x: float, y: float, game_manager: GameManager) -> None:
        super().__init__(x, y, game_manager)

    @override
    def update(self, dt: float) -> None:
        dis = Position(0, 0)
        '''
        [TODO HACKATHON 2]
        Calculate the distance change, and then normalize the distance
  
        [TODO HACKATHON 4]
        Check if there is collision, if so try to make the movement smooth
        Hint #1 : use entity.py _snap_to_grid function or create a similar function
        Hint #2 : Beware of glitchy teleportation, you must do
                    1. Update X
                    2. If collide, snap to grid
                    3. Update Y
                    4. If collide, snap to grid
                  instead of update both x, y, then snap to grid
        '''


        d = self.speed * dt
        if input_manager.key_down(pg.K_LSHIFT):
            d *= 1.5
            # print("Accelarate")

        if input_manager.key_down(pg.K_LEFT) or input_manager.key_down(pg.K_a):
            dis.x -= d
            self.animation.switch("left")
        if input_manager.key_down(pg.K_RIGHT) or input_manager.key_down(pg.K_d):
            dis.x += d
            self.animation.switch("right")

        if input_manager.key_down(pg.K_UP) or input_manager.key_down(pg.K_w):
            dis.y -= d
            self.animation.switch("up")
        if input_manager.key_down(pg.K_DOWN) or input_manager.key_down(pg.K_s):
            dis.y += d
            self.animation.switch("down")

        if dis.x and dis.y:
            # Normalize distance
            # Use 1+1=sqrt(2)^2 (in triangle)
            dis.x /= math.sqrt(2)
            dis.y /= math.sqrt(2)

        x, y, width, height = self.game_manager.player.animation.rect
        # print(x, y, width, height)
        x = self.position.x + dis.x

        if self.game_manager.check_collision(pg.Rect(x, y, width, height)):
            x = self._snap_to_grid(x)


        y = self.position.y + dis.y
        if self.game_manager.check_collision(pg.Rect(x, y, width, height)):
            y = self._snap_to_grid(y)

        if not scene_manager.bag_opened:
            self.position = Position(x, y)
        # self.position = Position(self.position

        # Check teleportation
        tp = self.game_manager.current_map.check_teleport(self.position)
        if tp:
            dest = tp.destination
            self.game_manager.switch_map(dest)
                
        super().update(dt)

    @override
    def draw(self, screen: pg.Surface, camera: PositionCamera) -> None:
        super().draw(screen, camera)
        
    @override
    def to_dict(self) -> dict[str, object]:
        return super().to_dict()
    
    @property
    @override
    def camera(self) -> PositionCamera:
        player_width = self.game_manager.player.animation.rect.width
        player_height = self.game_manager.player.animation.rect.height
        return PositionCamera(int(self.position.x) - GameSettings.SCREEN_WIDTH // 2 + player_width//2, int(self.position.y) - GameSettings.SCREEN_HEIGHT // 2 + player_height//2)
            
    @classmethod
    @override
    def from_dict(cls, data: dict[str, object], game_manager: GameManager) -> Player:
        return cls(data["x"] * GameSettings.TILE_SIZE, data["y"] * GameSettings.TILE_SIZE, game_manager)

