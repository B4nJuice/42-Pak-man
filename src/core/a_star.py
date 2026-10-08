import heapq
from dataclasses import dataclass
from itertools import count

from src.utils import Direction

from .level import Level
from .tile import Tile


def heuristic(a: Tile, b: Tile) -> float:
    return abs(a.get_x() - b.get_x()) + abs(a.get_y() - b.get_y())


@dataclass(slots=True)
class Node:
    tile: Tile
    g: float
    parent: 'Node | None' = None
    direction: Direction | None = None


def reconstruct_path(goal_node: Node) -> list[tuple[Tile, Direction]]:
    path: list[tuple[Tile, Direction]] = []
    current: Node | None = goal_node

    while current is not None and current.direction is not None:
        path.append((current.tile, current.direction))
        current = current.parent

    path.reverse()
    return path
    return path[::-1]


class AStar:
    _level: Level

    def __init__(self, level: Level):
        self._level = level

    def find_path(self, start: Tile, end: Tile) -> list[tuple[Tile, Direction]]:
        start_node: Node = Node(start, 0.0)
        nodes: dict[Tile, Node] = {start: start_node}
        closed: set[Tile] = set()

        tie = count()
        open_heap:  list[tuple[float, int, Tile]] = [
            (heuristic(start, end), next(tie), start)
        ]

        while open:
            _, _, current_tile = heapq.heappop(open_heap)

            if current_tile in closed:
                continue
            if current_tile == end:
                return reconstruct_path(nodes[current_tile])

            closed.add(current_tile)

            current_node: Node = nodes[current_tile]
            for next_tile, next_direction in self._level.get_possible_moves(current_tile):
                if next_tile in closed:
                    continue

                new_g = current_node.g + 1.0
                existing = nodes.get(next_tile)

                if existing is None:
                    nodes[next_tile] = Node(
                        next_tile,
                        new_g,
                        current_node,
                        next_direction
                    )
                elif new_g < existing.g:
                    existing.g = new_g
                    existing.parent = current_node
                    existing.direction = next_direction
                else:
                    continue

                heapq.heappush(
                    open_heap,
                    (new_g + heuristic(next_tile, end), next(tie), next_tile)
                )

        return []
