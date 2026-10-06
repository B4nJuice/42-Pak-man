import heapq
from dataclasses import dataclass
from math import sqrt

from src.utils import Direction

from .level import Level
from .tile import Tile


def heuristic(a: Tile, b: Tile) -> float:
    return sqrt((a.get_x() - b.get_x())**2 + (a.get_y() - b.get_y())**2)


@dataclass
class Node:
    '''
    g: cost from start
    h: cost remaining estimate by heuristic
    f: total cost estimate
    '''

    tile: Tile
    g: float
    h: float
    f: float
    parent: 'Node | None'
    direction: Direction | None

    @classmethod
    def create(
                cls,
                tile: Tile,
                g: float = float('inf'),
                h: float = 0.0,
                parent: 'Node | None' = None,
                direction: Direction | None = None
            ) -> 'Node':
        return cls(
            tile=tile,
            g=g,
            h=h,
            f=g+h,
            parent=parent,
            direction=direction
        )


def reconstruct_path(goal_node: Node) -> list[tuple[Tile, Direction]]:
    path: list[tuple[Tile, Direction]] = []
    current: Node | None = goal_node

    while current is not None and current.direction is not None:
        path.append((current.tile, current.direction))
        current = current.parent

    return path[::-1]


class AStar:
    _level: Level

    def __init__(self, level: Level):
        self._level = level

    def find_path(self, start: Tile, end: Tile) -> list[tuple[Tile, Direction]]:
        start_node: Node = Node.create(start, 0.0, heuristic(start, end))

        open_list: list[tuple[float, Tile]] = [
            (start_node.f, start_node.tile)
        ]
        open_dict: dict[Tile, Node] = {
            start: start_node
        }
        visited_tile: set[Tile] = set()

        while open_list:
            _, current_tile = heapq.heappop(open_list)
            current_node = open_dict[current_tile]

            if current_tile == end:
                return reconstruct_path(current_node)

            visited_tile.add(current_tile)
            for next_tile, next_direction in self._level.get_possible_moves(current_tile):
                if next_tile in visited_tile:
                    continue

                new_g = current_node.g + heuristic(current_tile, next_tile)
                if next_tile not in open_dict:
                    next_node: Node = Node.create(
                        next_tile,
                        g=new_g,
                        h=heuristic(next_tile, end),
                        parent=current_node,
                        direction=next_direction
                    )
                    heapq.heappush(open_list, (new_g, next_tile))
                    open_dict[next_tile] = next_node
                elif new_g < open_dict[next_tile].g:
                    next_node = open_dict[next_tile]
                    next_node.g = new_g
                    next_node.f = new_g + next_node.h
                    next_node.parent = current_node
                    next_node.direction = next_direction

        return []
