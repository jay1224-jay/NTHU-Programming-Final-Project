import pygame as pg
import pytmx

from src.utils import load_tmx, Position, GameSettings, PositionCamera, Teleport
from src.utils import Logger

class Map:
    # Map Properties
    path_name: str
    tmxdata: pytmx.TiledMap
    # Position Argument
    spawn: Position
    teleporters: list[Teleport]
    # Rendering Properties
    _surface: pg.Surface
    _collision_map: list[pg.Rect]
    _bush_map: list[pg.Rect]

    def __init__(self, path: str, tp: list[Teleport], spawn: Position):
        self.path_name = path
        self.tmxdata = load_tmx(path)
        self.spawn = spawn
        self.teleporters = tp

        pixel_w = self.tmxdata.width * GameSettings.TILE_SIZE
        pixel_h = self.tmxdata.height * GameSettings.TILE_SIZE

        # Prebake the map
        self._surface = pg.Surface((pixel_w, pixel_h), pg.SRCALPHA)
        self._render_all_layers(self._surface)
        # Prebake the collision map
        self._collision_map = self._create_collision_map()
        self._bush_map = self._create_bush_map()

    def update(self, dt: float):
        return

    def draw(self, screen: pg.Surface, camera: PositionCamera, darken=False):

        if darken:
            dark_overlay = pg.Surface(screen.get_size(), pg.SRCALPHA)
            dark_overlay.fill((0, 0, 0, 128))
            screen.blit(dark_overlay, (0, 0))

        screen.blit(self._surface, camera.transform_position(Position(0, 0)))
        # Draw the hitboxes collision map
        if GameSettings.DRAW_HITBOXES:
            for rect in self._collision_map:
                pg.draw.rect(screen, (255, 0, 0), camera.transform_rect(rect), 1)
        '''
        if darken:
            self._surface.set_alpha(128)
        else:
            self._surface.set_alpha(255)
        '''
    def check_collision(self, rect: pg.Rect) -> bool:
        return any(rect.colliderect(r) for r in self._collision_map)

    def check_bush(self, rect: pg.Rect) -> bool:
        return any(rect.colliderect(x) for x in self._bush_map)
        
    def check_teleport(self, pos: Position) -> Teleport | None:
        error_range = GameSettings.TILE_SIZE
        # print(self.teleporters)
        for i in self.teleporters:
            if (i.pos.x - error_range <= pos.x <= i.pos.x + error_range  and \
                i.pos.y - error_range <= pos.y <= i.pos.y + error_range):
                return i
        return None

    def _render_all_layers(self, target: pg.Surface) -> None:
        for layer in self.tmxdata.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                self._render_tile_layer(target, layer)
            # elif isinstance(layer, pytmx.TiledImageLayer) and layer.image:
            #     target.blit(layer.image, (layer.x or 0, layer.y or 0))
 
    def _render_tile_layer(self, target: pg.Surface, layer: pytmx.TiledTileLayer) -> None:
        for x, y, gid in layer:
            if gid == 0:
                continue
            image = self.tmxdata.get_tile_image_by_gid(gid)
            if image is None:
                continue

            image = pg.transform.scale(image, (GameSettings.TILE_SIZE, GameSettings.TILE_SIZE))
            target.blit(image, (x * GameSettings.TILE_SIZE, y * GameSettings.TILE_SIZE))
    
    def _create_collision_map(self) -> list[pg.Rect]:
        rects = []
        for layer in self.tmxdata.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer) and ("collision" in layer.name.lower() or "house" in layer.name.lower()):
                for x, y, gid in layer:
                    if gid != 0:
                        '''
                        [TODO HACKATHON 4]
                        rects.append(pg.Rect(...))
                        Append the collision rectangle to the rects[] array
                        Remember scale the rectangle with the TILE_SIZE from settings
                        '''
                        rects.append(pg.Rect(x * GameSettings.TILE_SIZE, y * GameSettings.TILE_SIZE, GameSettings.TILE_SIZE, GameSettings.TILE_SIZE))
        return rects

    def _create_bush_map(self):
        rects = []
        for layer in self.tmxdata.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer) and ("PokemonBush" == layer.name):
                for x, y, gid in layer:
                    if gid != 0 and gid > 30:
                        rects.append(pg.Rect(x * GameSettings.TILE_SIZE, y * GameSettings.TILE_SIZE, GameSettings.TILE_SIZE, GameSettings.TILE_SIZE))
        return rects

    @classmethod
    def from_dict(cls, data: dict) -> "Map":
        tp = [Teleport.from_dict(t) for t in data["teleport"]]
        pos = Position(data["player"]["x"] * GameSettings.TILE_SIZE, data["player"]["y"] * GameSettings.TILE_SIZE)
        return cls(data["path"], tp, pos)

    def to_dict(self):
        return {
            "path": self.path_name,
            "teleport": [t.to_dict() for t in self.teleporters],
            "player": {
                "x": self.spawn.x // GameSettings.TILE_SIZE,
                "y": self.spawn.y // GameSettings.TILE_SIZE,
            }
        }
