from typing import Optional, Iterator, Tuple

class Entity:
    def __init__(self) -> None:
        pass

class _EntityStack:
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
        self._stacks : list[list[_EntityStack]] = [[_EntityStack() for _ in range(self.size_y)] for _ in range(self.size_x)]

    def _get_stack(self, x: int, y: int) -> _EntityStack:
        assert 0 <= x and x < self.size_x
        assert 0 <= y and y < self.size_y

        return self._stacks[x][y]     

    def is_valid_cell(self, x: int, y: int) -> bool:
        return 0 <= x and x < self.size_x and 0 <= y and y < self.size_y

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

class Game:
    @staticmethod
    def do_action(world: World, x: int, y: int) -> bool:
        raise NotImplementedError("Implement 'do_action' method")

    @staticmethod
    def select(world: World, x: int, y: int) -> bool:
        raise NotImplementedError("Implement 'select' method")
    
    
    @staticmethod
    def unselect(world: World) -> bool:
        raise NotImplementedError("Implement 'unselect' method")
    
    @staticmethod
    def do_pass(world: World) -> bool:
        raise NotImplementedError("Implement 'do_pass' method")
    
    @staticmethod
    def get_world_size() -> Tuple[int, int]:
        raise NotImplementedError("Implement 'get_world_size' method")