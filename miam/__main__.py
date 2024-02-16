import pygame
import pygame_gui
from typing import Optional, Iterator, Tuple
import importlib
import pathlib
import sys

from miam import Game, World, Entity

APP_WIDTH = 1280
APP_HEIGHT = 720
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 190, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GRAY = (200, 200, 200)
FONT_SIZE = 16
PADDING = 8
BUTTON_WIDTH = 75
BUTTON_HEIGHT = 32

class DefaultGame(Game):
    @staticmethod
    def do_action(world: World, x: int, y: int) -> bool:
        return True
    
    @staticmethod
    def select(world: World, x: int, y: int) -> bool:
        world.select(x, y)
        return True
    
    @staticmethod
    def unselect(world: World) -> bool:
        world.unselect()
        return True
    
    @staticmethod
    def do_pass(world: World) -> bool:
        return True
    
    @staticmethod
    def get_world_size() -> Tuple[int, int]:
        return (24, 24)

class Grid:
    def __init__(self, size: Tuple[int, int], tile_size: int) -> None:
        self.size_x, self.size_y = size
        self.tile_size = tile_size
        self.offset_x = 0
        self.offset_y = 0
        self.width = self.size_x * self.tile_size
        self.height = self.size_y * self.tile_size

    def draw(self, surface: pygame.Surface) -> None:
        for row in range(self.size_x + 1):
            start_pos = (self.offset_x + row * self.tile_size, self.offset_y)
            end_pos = (start_pos[0], start_pos[1] + self.height)
            pygame.draw.line(surface, GRAY, start_pos, end_pos, 1)
    
        for col in range(self.size_y + 1):
            start_pos = (self.offset_x, self.offset_y + col * self.tile_size)
            end_pos = (start_pos[0] + self.width, start_pos[1])
            pygame.draw.line(surface, GRAY, start_pos, end_pos, 1)

    def draw_cell_highlight(self, cell: Tuple[int, int], color: Tuple[int, int, int], width=1):
        rect = self.get_cell_rect(cell)
        rect.width += width
        rect.height += width
        rect.top -= (width + 1) / 2
        rect.left -= (width + 1) / 2
        pygame.draw.rect(window_surface, color, rect, width=width)

    def set_offset(self, x, y) -> None:
        self.offset_x = x
        self.offset_y = y

    def get_cell_rect(self, cell: Tuple[int, int]) -> pygame.Rect:
        x, y = cell
        assert x >= 0 and x < self.size_x
        assert y >= 0 and y < self.size_y
        return pygame.Rect(1 + x * self.tile_size + self.offset_x, 1 + y * self.tile_size + self.offset_y, self.tile_size, self.tile_size)
    
    def hit_test(self, position: Tuple[int, int]) -> Tuple[int, int]:
        x, y = position
        if self.offset_x <= x and x < self.offset_x + self.width and self.offset_y <= y and y < self.offset_y + self.height:
            return (int((x - self.offset_x) * self.size_x / self.width), int((y - self.offset_y) * self.size_y / self.height))
        else:
            return None


    
pygame.init()
pygame.display.set_caption('Miam')

window_surface = pygame.display.set_mode((1280, 720), vsync=1)
manager = pygame_gui.UIManager((1280,720))
font = pygame.font.SysFont(None, FONT_SIZE)
font_menu = pygame.font.SysFont(None, 24)

close_button_rect = pygame.Rect(0, 0, BUTTON_WIDTH, BUTTON_HEIGHT)
close_button_rect.right = APP_WIDTH - PADDING
close_button_rect.top = PADDING
close_button = pygame_gui.elements.UIButton(relative_rect=close_button_rect, text='Close', manager=manager)

step_button_rect = pygame.Rect(0, 0, BUTTON_WIDTH, BUTTON_HEIGHT)
step_button_rect.left = PADDING
step_button_rect.top = PADDING
step_button = pygame_gui.elements.UIButton(relative_rect=step_button_rect, text='Step', manager=manager)

play_button_rect = pygame.Rect(0, 0, BUTTON_WIDTH, BUTTON_HEIGHT)
play_button_rect.left = PADDING + BUTTON_WIDTH + PADDING
play_button_rect.top = PADDING
play_button = pygame_gui.elements.UIButton(relative_rect=play_button_rect, text='Play', manager=manager)

step_rate_slider_rect = pygame.Rect(0, 0, 2 * BUTTON_WIDTH, BUTTON_HEIGHT)
step_rate_slider_rect.left = PADDING + BUTTON_WIDTH + PADDING + BUTTON_WIDTH + PADDING
step_rate_slider_rect.top = PADDING
step_rate_slider = pygame_gui.elements.UIHorizontalSlider(step_rate_slider_rect, 30, (1, 120), manager=manager)

clock = pygame.time.Clock()
is_running = True

if len(sys.argv) > 1:
    file_path = pathlib.Path(sys.argv[1])
    if not file_path.is_file():
        print("The file {} does not exist".format(file_path))
        sys.exit(-1)
    module_name = file_path.name
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    create_game = getattr(module, "create_game") 

    game : Game = create_game()
    print("Load {}".format(file_path))
else:
    game : Game = DefaultGame()
    print("Load default game")

world_x, world_y = game.get_world_size()
max_height = APP_HEIGHT - 2 *  (PADDING + BUTTON_HEIGHT + PADDING)
tile_size = int(max_height / world_y)
world : World = World(world_x, world_x)

is_playing = False
is_playing_count = 0

while is_running:
    time_delta = clock.tick() / 1000.0
    manager.update(time_delta)
    mouse_x, mouse_y = mouse_pos = pygame.mouse.get_pos()

    is_mouse_select = False
    is_mouse_action = False
    is_any_button_pressed = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_ESCAPE:
                game.unselect(world)
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                is_mouse_select = True
            
            if event.button == 3:
                is_mouse_action = True

        manager.process_events(event)

    if step_button_rect.collidepoint(mouse_pos) or play_button_rect.collidepoint(mouse_pos) or close_button_rect.collidepoint(mouse_pos):
        is_mouse_action = False
        is_mouse_select = False

    if close_button.pressed:
        is_running = False

    if play_button.pressed:
        if is_playing:
            is_playing = False
            play_button.set_text("Play")
        else:
            is_playing = True
            play_button.set_text("Stop")

    grid = Grid(world.get_size(), tile_size)
    grid.set_offset(PADDING, PADDING + BUTTON_HEIGHT + PADDING)
    
    hit_cell = grid.hit_test(mouse_pos)      

    if is_mouse_select:
        if hit_cell is not None:
            hit_x, hit_y = hit_cell
            game.select(world, hit_x, hit_y)
        else:
            game.unselect(world)

    if is_mouse_action:
        if hit_cell is not None:
            hit_x, hit_y = hit_cell
            game.do_action(world, hit_x, hit_y)

    if not is_playing and step_button.pressed:
        game.do_pass(world)

    if is_playing:
        rate = step_rate_slider.get_current_value()
        if is_playing_count == 0:
            game.do_pass(world)
        is_playing_count += 1
        is_playing_count %= rate

    window_surface.fill(BLACK)
    grid.draw(window_surface)

    for x, y in world.iter():
        if not world.is_empty(x, y):
            entity = world.head(x, y)
            assert hasattr(entity, 'color')
            rect = grid.get_cell_rect((x, y))
            rect.width -= 1
            rect.height -= 1
            pygame.draw.rect(window_surface, entity.color, rect)

    selected_cell = world.get_selection()
    if selected_cell is not None:
        grid.draw_cell_highlight(selected_cell, GREEN, width=3)

    if hit_cell is not None:
        grid.draw_cell_highlight(hit_cell, RED)

    if pygame.mouse.get_focused():
        text_surface = font.render("Mouse: x = {}, y = {}".format(mouse_x, mouse_y), True, WHITE)
        text_rect = text_surface.get_rect(left=PADDING, bottom=APP_HEIGHT - PADDING)
        window_surface.blit(text_surface, text_rect)

    text_surface = font_menu.render("1 step every {} frame.".format(step_rate_slider.get_current_value()), True, WHITE)
    text_rect = text_surface.get_rect(left=PADDING + BUTTON_WIDTH + PADDING + BUTTON_WIDTH + PADDING + 2 * BUTTON_WIDTH + PADDING, top=PADDING)
    window_surface.blit(text_surface, text_rect)

    manager.draw_ui(window_surface)

    pygame.display.flip()