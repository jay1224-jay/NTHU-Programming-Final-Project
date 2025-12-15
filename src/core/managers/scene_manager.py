import pygame as pg

from src.scenes.scene import Scene
from src.utils import Logger

class SceneManager:
    
    _scenes: dict[str, Scene]
    _current_scene: Scene | None = None
    _next_scene: str | None = None
    
    def __init__(self):
        Logger.info("Initializing SceneManager")
        self._scenes = {}
        self.bag_opened = False
        self.setting_opened = False
        self.shop_opened = False
        self.navigation_opened = False
        self.navigation_dest = None
        self._scene_transition_done = False
        self.alpha = 0

    def close_bag(self):
        self.bag_opened = False
    def open_bag(self):
        self.bag_opened = True

    def close_navigation(self):
        self.navigation_opened = False
    def open_navigation(self):
        self.navigation_opened = True

    def open_setting(self):
        self.setting_opened = True
    def close_setting(self):
        self.setting_opened = False

    def open_shop(self):
        self.shop_opened = True
    def close_shop(self):
        self.shop_opened = False
        
    def register_scene(self, name: str, scene: Scene) -> None:
        self._scenes[name] = scene
        
    def change_scene(self, scene_name: str) -> None:
        if scene_name in self._scenes:
            Logger.info(f"Changing scene to '{scene_name}'")
            self._next_scene = scene_name
        else:
            raise ValueError(f"Scene '{scene_name}' not found")
            
    def update(self, dt: float) -> None:
        # Handle scene transition
        if self._next_scene is not None:
            self._perform_scene_switch()
            
        # Update current scene
        if self._current_scene:
            self._current_scene.update(dt)
            
    def draw(self, screen: pg.Surface) -> None:
        if self._current_scene:
            self._current_scene.draw(screen)

    def _perform_fade_in(self) -> None:
        print(self.alpha)

            
    def _perform_scene_switch(self) -> None:
        if self._next_scene is None:
            return
            
        # Exit current scene
        if self._current_scene:
            self._current_scene.exit()

        self._current_scene = self._scenes[self._next_scene]


        # Enter new scene
        if self._current_scene:
            Logger.info(f"Entering {self._next_scene} scene")
            self._current_scene.enter()
            
        # Clear the transition request
        self._next_scene = None
        