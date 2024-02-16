from miam import Game, World, Entity
from typing import Optional, Iterator, Tuple

import copy

class GameOfLife(Game):
    @classmethod
    def _create_cell(cls, world: World, x: int, y: int) -> None:
        assert world.is_empty(x, y)
        entity = Entity()
        entity.color = (139, 99, 49)
        world.push(x, y, entity)

    @classmethod
    def _kill_cell(cls, world: World, x: int, y: int) -> bool:
        assert not world.is_empty(x, y)
        world.pop(x, y)
        if world.get_selection() == (x, y):
            world.unselect()

    @staticmethod
    def do_action(world: World, x: int, y: int) -> bool:
        if world.is_empty(x, y):
            GameOfLife._create_cell(world, x, y)
        else:
            GameOfLife._kill_cell(world, x, y)

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
        world_copy = copy.deepcopy(world)

        for x, y in world.iter():
            alive = not world_copy.is_empty(x, y)
            neighbor_count = 0
            for i in range(x-1,x+2):
                for j in range(y-1,y+2):
                    if world_copy.is_valid_cell(i, j) and (i != x or j != y) and not world_copy.is_empty(i, j):
                        neighbor_count += 1

            if alive and (neighbor_count < 2 or neighbor_count > 3):
                GameOfLife._kill_cell(world, x, y)
            if not alive and neighbor_count == 3:
                GameOfLife._create_cell(world, x, y)

        return True
    
    @staticmethod
    def get_world_size() -> Tuple[int, int]:
        return (16, 16)
    
def create_game() -> Game:
    return GameOfLife()