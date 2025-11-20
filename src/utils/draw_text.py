
import pygame as pg

class TextDrawer:
    def __init__(self, font):
        self.font = font
        self._font_sizes = {}
        for _size in range(8, 27, 2):
            self._font_sizes[_size] = pg.font.Font(font, _size)

    def draw(self, screen, text, size, position, align="left", color="black"):
        if size not in self._font_sizes.keys():
            self._font_sizes[size] = pg.font.Font(self.font, size)
        _font = self._font_sizes[size]
        img = _font.render(text, True, color)
        x = position[0]
        y = position[1]
        if align == "left":
            rect = img.get_rect(topleft=(x, y))
        elif align == "right":
            rect = img.get_rect(topright=(x, y))
        elif align == "center":
            rect = img.get_rect(center=(x, y))
        else:
            rect = img.get_rect(topleft=(x, y))
        screen.blit(img, rect)