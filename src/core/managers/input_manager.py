import pygame as pg
from src.utils import Logger, MouseBtn, Key


class InputManager:
    def __init__(self) -> None:
        # Keyboard
        self._down_keys: set[Key] = set()
        self._pressed_keys: set[Key] = set()
        self._released_keys: set[Key] = set()

        # Mouse
        self._down_mouse: set[MouseBtn] = set()
        self._pressed_mouse: set[MouseBtn] = set()
        self._released_mouse: set[MouseBtn] = set()
        self.mouse_pos: tuple[int, int] = (0, 0)
        self.mouse_wheel: int = 0  # +1 / -1

    def reset(self) -> None:
        self._pressed_keys.clear()
        self._released_keys.clear()
        self._pressed_mouse.clear()
        self._released_mouse.clear()
        self.mouse_wheel = 0
        
    def handle_events(self, e: pg.event.Event) -> None:
        if e.type == pg.MOUSEMOTION:
            self.mouse_pos = e.pos

        elif e.type == pg.MOUSEBUTTONDOWN:
            if e.button in (1, 2, 3):
                self._down_mouse.add(e.button)
                self._pressed_mouse.add(e.button)
                Logger.debug(f"MOUSEMOTION event: {e}")
            elif e.button in (4, 5):
                self.mouse_wheel += 1 if e.button == 4 else -1
        elif e.type == pg.MOUSEBUTTONUP:
            if e.button in (1, 2, 3):
                self._down_mouse.discard(e.button)
                self._released_mouse.add(e.button)
        elif e.type == pg.KEYDOWN:
            # Logger.debug(f"Key {e.key} pressed")
            self._down_keys.add(e.key)
            self._pressed_keys.add(e.key)
        elif e.type == pg.KEYUP:
            # Logger.debug(f"Key {e.key} released")
            self._down_keys.discard(e.key)
            self._released_keys.add(e.key)

    def key_down(self, k: Key) -> bool:
        return k in self._down_keys
        
    def key_pressed(self, k: Key) -> bool:  
        return k in self._pressed_keys
        
    def key_released(self, k: Key) -> bool:  
        return k in self._released_keys
        
    def mouse_down(self, b: MouseBtn) -> bool:     
        return b in self._down_mouse
        
    def mouse_pressed(self, b: MouseBtn) -> bool:     
        return b in self._pressed_mouse
        
    def mouse_released(self, b: MouseBtn) -> bool:     
        return b in self._released_mouse
