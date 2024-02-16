import pygame
import pygame_gui
from typing import Optional, Iterator, Tuple

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
BUTTON_WIDTH = 64
BUTTON_HEIGHT = 32

class Entity:
    def __init__(self) -> None:
        pass

class EntityStack:
    def __init__(self) -> None:
        self._stack : list[Entity] = []

    def push(self, entity: Entity) -> None:
        self._stack.append(entity)

    def is_empty(self) -> bool:
        return len(self._stack) == 0

    def head(self) -> Entity:
        assert not self.is_empty()
        return self._stack[-1]
    
    def pop(self) -> Entity:
        assert not self.is_empty()
        return self._stack.pop()
    
    def iter(self) -> Iterator[Entity]:
        iter(self._stack)

class World:
    def __init__(self, size_x: int, size_y: int) -> None:
        self.size_x = size_x
        self.size_y = size_y
        self.selected = None
        self._stacks : list[list[EntityStack]] = [[EntityStack() for _ in range(self.size_y)] for _ in range(self.size_x)]

    def _get_stack(self, x: int, y: int) -> EntityStack:
        assert 0 <= x and x < self.size_x
        assert 0 <= y and y < self.size_y

        return self._stacks[x][y]
    

    def select(self, x: int, y: int) -> None:
        self.selected = (x, y)

    def unselect(self) -> None:
        self.selected = None

    def get_selection(self) -> Optional[Tuple[int, int]]:
        return self.selected

    def get_size(self) -> Tuple[int, int]:
        return (self.size_x, self.size_y)

    def push(self, x: int, y: int, entity: Entity) -> None:
        self._get_stack(x, y).push(entity)

    def is_empty(self, x: int, y: int) -> bool:
        return self._get_stack(x, y).is_empty()

    def head(self, x: int, y: int) -> Entity:
        return self._get_stack(x, y).head()
    
    def pop(self, x: int, y: int) -> Entity:
        return self._get_stack(x, y).pop()
    
    def iter_cell(self, x: int, y: int) -> Iterator[Entity]:
        return self._get_stack(x, y).iter()
    
    def iter(self) -> Iterator[Tuple[int, int]]:
        for x in range(self.size_x):
            for y in range (self.size_y):
                yield (x, y)

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

class Game:
    @staticmethod
    def do_action(world: World, x: int, y: int) -> bool:
        raise NotImplementedError("Implement 'do_action' method")

    @staticmethod
    def select(world: World, x: int, y: int) -> bool:
        raise NotImplementedError("Implement 'do_action' method")
    
    
    @staticmethod
    def unselect(world: World) -> bool:
        raise NotImplementedError("Implement 'do_action' method")
    
    @staticmethod
    def do_pass(world: World) -> bool:
        raise NotImplementedError("Implement 'do_action' method")

class GameOfLife(Game):
    @staticmethod
    def do_action(world: World, x: int, y: int) -> bool:
        if world.is_empty(x, y):
            entity = Entity()
            entity.color = (139, 99, 49)
            world.push(x, y, entity)
        else:
            world.pop(x, y)
            if world.get_selection() == (x, y):
                world.unselect()

        return True
    
    @staticmethod
    def select(world: World, x: int, y: int) -> bool:
        if not world.is_empty(x, y):
            world.select(x, y)
            return True
        else:
            world.unselect()
            return False

    @staticmethod
    def unselect(world: World) -> bool:
        world.unselect()
        return True
    
    @staticmethod
    def do_pass(world: World) -> bool:
        return True
    
pygame.init()
pygame.display.set_caption('Miam')

window_surface = pygame.display.set_mode((1280, 720), vsync=1)
manager = pygame_gui.UIManager((1280,720))
font = pygame.font.SysFont(None, FONT_SIZE)

close_button_rect = pygame.Rect(0, 0, BUTTON_WIDTH, BUTTON_HEIGHT)
close_button_rect.right = APP_WIDTH - PADDING
close_button_rect.top = PADDING
close_button = pygame_gui.elements.UIButton(relative_rect=close_button_rect, text='Close', manager=manager)

step_button_rect = pygame.Rect(0, 0, BUTTON_WIDTH, BUTTON_HEIGHT)
step_button_rect.left = PADDING
step_button_rect.top = PADDING
step_button = pygame_gui.elements.UIButton(relative_rect=step_button_rect, text='Step', manager=manager)

play_button_rect = pygame.Rect(0, 0, BUTTON_WIDTH, BUTTON_HEIGHT)
play_button_rect.left = PADDING + 64 + PADDING
play_button_rect.top = PADDING
play_button = pygame_gui.elements.UIButton(relative_rect=play_button_rect, text='Play', manager=manager)

clock = pygame.time.Clock()
is_running = True

world : World = World(16, 16)
game : Game = GameOfLife()
is_playing = False

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

    grid = Grid(world.get_size(), 32)
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
        game.do_pass(world)

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

    manager.draw_ui(window_surface)

    pygame.display.flip()