import pygame
import pygame_gui

APP_WIDTH = 1280
APP_HEIGHT = 720
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
FONT_SIZE = 16
PADDING = 8

class Grid:
    def __init__(self, size_x : int, size_y: int, tile_size: int) -> None:
        self.size_x = size_x
        self.size_y = size_y
        self.tile_size = tile_size
        self.offset_x = 0
        self.offset_y = 0
        self.width = self.size_x * self.tile_size
        self.height = self.size_y * self.tile_size

    def draw(self, surface: pygame.Surface):
        for row in range(self.size_x + 1):
            start_pos = (self.offset_x + row * self.tile_size, self.offset_y)
            end_pos = (start_pos[0], start_pos[1] + self.height)
            pygame.draw.line(surface, WHITE, start_pos, end_pos, 1)
    
        for col in range(self.size_y + 1):
            start_pos = (self.offset_x, self.offset_y + col * self.tile_size)
            end_pos = (start_pos[0] + self.width, start_pos[1])
            pygame.draw.line(surface, WHITE, start_pos, end_pos, 1)

    def set_offset(self, x, y):
        self.offset_x = x
        self.offset_y = y

    def get_cell(self, x, y):
        assert x >= 0 and x < self.size_x
        assert y >= 0 and y < self.size_y
        return pygame.Rect(1 + x * self.tile_size + self.offset_x, 1 + y * self.tile_size + self.offset_y, self.tile_size - 1, self.tile_size - 1)
    
    def iter_cell(self):
        for x in range(self.size_x):
            for y in range (self.size_y):
                return self.get_cell(x, y)

    def hit_test(self, x, y):
        if self.offset_x <= x and x < self.offset_x + self.width and self.offset_y <= y and y < self.offset_y + self.height:
            return self.get_cell(int((x - self.offset_x) * self.size_x / self.width), int((y - self.offset_y) * self.size_y / self.height))
        else:
            return None

pygame.init()
pygame.display.set_caption('Miam')

window_surface = pygame.display.set_mode((1280, 720), vsync=1)
manager = pygame_gui.UIManager((1280,720))
font = pygame.font.SysFont(None, FONT_SIZE)

close_button_rect = pygame.Rect(0, 0, 64, 32)
close_button_rect.right = APP_WIDTH - 8
close_button_rect.top = 8
close_button = pygame_gui.elements.UIButton(relative_rect=close_button_rect, text='Close', manager=manager)

clock = pygame.time.Clock()
is_running = True

grid = Grid(16, 16, 32)
grid.set_offset(PADDING, PADDING)

while is_running:
    time_delta = clock.tick() / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

        manager.process_events(event)

    if close_button.pressed:
        is_running = False

    manager.update(time_delta)
    mouse_x, mouse_y = pygame.mouse.get_pos()    
    mouse_cell = grid.hit_test(mouse_x, mouse_y)

    window_surface.fill(BLACK)
    grid.draw(window_surface)
    if mouse_cell is not None:
        mouse_cell.width += 4
        mouse_cell.height += 4
        mouse_cell.top -= 2
        mouse_cell.left -= 2
        pygame.draw.rect(window_surface, RED, mouse_cell, width=3)


    if pygame.mouse.get_focused():
        text_surface = font.render("Mouse: x = {}, y = {}".format(mouse_x, mouse_y), True, WHITE)
        text_rect = text_surface.get_rect(left=PADDING, bottom=APP_HEIGHT - PADDING)
        window_surface.blit(text_surface, text_rect)

    manager.draw_ui(window_surface)

    pygame.display.flip()