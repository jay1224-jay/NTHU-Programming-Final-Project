import pygame


class MiniMap:
    def __init__(self, world_surface, max_width=200, position=(10, 10), border_color=(255, 255, 255)):
        self.position = position
        self.border_color = border_color

        world_width = world_surface.get_width()
        world_height = world_surface.get_height()
        # print(world_width)
        self.scale = max_width / (world_width)

        self.mm_w = int(world_width * self.scale)
        self.mm_h = int(world_height * self.scale)

        self.image = pygame.transform.smoothscale(world_surface, (self.mm_w, self.mm_h))

        self.rect = self.image.get_rect(topleft=position)

    def draw(self, display_surface, player_x, player_y):

        display_surface.blit(self.image, self.position)

        pygame.draw.rect(display_surface, self.border_color, self.rect, 2)

        mm_player_x = self.position[0] + (player_x * self.scale / 4)
        mm_player_y = self.position[1] + (player_y * self.scale / 4)

        pygame.draw.circle(display_surface, 'black', (int(mm_player_x + 8 * self.scale), int(mm_player_y + 8 * self.scale)), 3)