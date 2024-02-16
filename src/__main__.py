import pygame
import pygame_gui

APP_WIDTH = 1280
APP_HEIGHT = 720
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

class Grid:
    def __init__(self, nx : int, ny: int, tile_size: int) -> None:
        self.nx = nx
        self.ny = ny
        self.tile_size = tile_size
        self.offset_x = 0
        self.offset_y = 0
        self.width = self.nx * self.tile_size
        self.height = self.ny * self.tile_size

    def draw(self, surface: pygame.Surface):
        for row in range(self.nx + 1):
            start_pos = (self.offset_x + row * self.tile_size, self.offset_y)
            end_pos = (start_pos[0], start_pos[1] + self.height)
            pygame.draw.line(surface, WHITE, start_pos, end_pos, 1)
    
        for col in range(self.ny + 1):
            start_pos = (self.offset_x, self.offset_y + col * self.tile_size)
            end_pos = (start_pos[0] + self.width, start_pos[1])
            pygame.draw.line(surface, WHITE, start_pos, end_pos, 1)

    def set_offset(self, x, y):
        self.offset_x = x
        self.offset_y = y

pygame.init()

pygame.display.set_caption('Quick Start')
window_surface = pygame.display.set_mode((1280, 720), vsync=1)

manager = pygame_gui.UIManager((1280,720))

hello_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((350, 275), (100, 50)),
                                            text='Say Hello',
                                            manager=manager)

clock = pygame.time.Clock()
is_running = True

grid = Grid(16, 16, 32)
grid.set_offset(100, 100)

while is_running:
    time_delta = clock.tick() / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == hello_button:
                print('Hello World')

        manager.process_events(event)

    manager.update(time_delta)

    window_surface.fill(BLACK)

    grid.draw(window_surface)

    manager.draw_ui(window_surface)

    pygame.display.flip()