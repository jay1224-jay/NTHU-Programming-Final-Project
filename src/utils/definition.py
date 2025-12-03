from pygame import Rect
from .settings import GameSettings
from dataclasses import dataclass
from enum import Enum
from typing import overload, TypedDict, Protocol

MouseBtn = int
Key = int

Direction = Enum('Direction', ['UP', 'DOWN', 'LEFT', 'RIGHT', 'NONE'])

@dataclass
class Position:
    x: float
    y: float
    
    def copy(self):
        return Position(self.x, self.y)
        
    def distance_to(self, other: "Position") -> float:
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5

    def __add__(self, other: "Position") -> "Position":
        return Position(self.x + other.x, self.y + other.y)
        
@dataclass
class PositionCamera:
    x: int
    y: int
    
    def copy(self):
        return PositionCamera(self.x, self.y)
        
    def to_tuple(self) -> tuple[int, int]:
        return (self.x, self.y)
        
    def transform_position(self, position: Position) -> tuple[int, int]:
        return (int(position.x) - self.x, int(position.y) - self.y)
        
    def transform_position_as_position(self, position: Position) -> Position:
        return Position(int(position.x) - self.x, int(position.y) - self.y)
        
    def transform_rect(self, rect: Rect) -> Rect:
        return Rect(rect.x - self.x, rect.y - self.y, rect.width, rect.height)

@dataclass
class Teleport:
    pos: Position
    destination: str
    target_pos: Position
    
    @overload
    def __init__(self, x: int, y: int, destination: str, target_pos = None) -> None: ...
    @overload
    def __init__(self, pos: Position, destination: str, target_pos = None) -> None: ...

    def __init__(self, *args, **kwargs):
        self.target_pos = kwargs.get('target_pos', None)
        if isinstance(args[0], Position):
            self.pos = args[0]
            self.destination = args[1]
        else:
            x, y, dest = args
            self.pos = Position(x, y)
            self.destination = dest
    
    def to_dict(self):
        data = {
            "x": self.pos.x // GameSettings.TILE_SIZE,
            "y": self.pos.y // GameSettings.TILE_SIZE,
            "destination": self.destination,
            "target_pos": {"destination_x": 0, "destination_y": 0},
        }
        if self.target_pos:
            data["target_pos"]["destination_x"] = self.target_pos.x // GameSettings.TILE_SIZE
            data["target_pos"]["destination_y"] = self.target_pos.y // GameSettings.TILE_SIZE
        return data
    
    @classmethod
    def from_dict(cls, data: dict):
        target = None
        if "target_pos" in data:
            target = Position(
                data["target_pos"]["destination_x"] * GameSettings.TILE_SIZE,
                data["target_pos"]["destination_y"] * GameSettings.TILE_SIZE
            )
        return cls(
            data["x"] * GameSettings.TILE_SIZE,
            data["y"] * GameSettings.TILE_SIZE,
            data["destination"],
            target_pos=target  # Pass the new target
        )
    
class Monster(TypedDict):
    name: str
    hp: int
    max_hp: int
    level: int
    sprite_path: str

class Item(TypedDict):
    name: str
    count: int
    sprite_path: str