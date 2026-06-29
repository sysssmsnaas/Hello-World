from dataclasses import dataclass, field
from typing import List, Tuple, Dict, Optional
import heapq

Position = Tuple[int, int]

@dataclass(order=True)
class PriorityNode:
    priority: int
    position: Position = field(compare=False)
    cost: int = field(compare=False)

class Grid:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.walls = set()

    def in_bounds(self, pos: Position) -> bool:
        x, y = pos
        return 0 <= x < self.width and 0 <= y < self.height

    def passable(self, pos: Position) -> bool:
        return pos not in self.walls

    def neighbors(self, pos: Position):
        x, y = pos
        candidates = [
            (x+1, y),
            (x-1, y),
            (x, y+1),
            (x, y-1),
        ]

        return [
            p for p in candidates
            if self.in_bounds(p) and self.passable(p)
        ]

def heuristic(a: Position, b: Position):
    return abs(a[0]-b[0]) + abs(a[1]-b[1])

def astar(grid: Grid, start: Position, goal: Position):

    frontier = []
    heapq.heappush(frontier, PriorityNode(0, start, 0))

    came_from: Dict[Position, Optional[Position]] = {}
    cost_so_far: Dict[Position, int] = {}

    came_from[start] = None
    cost_so_far[start] = 0

    while frontier:

        current = heapq.heappop(frontier).position

        if current == goal:
            break

        for nxt in grid.neighbors(current):

            new_cost = cost_so_far[current] + 1

            if nxt not in cost_so_far or new_cost < cost_so_far[nxt]:

                cost_so_far[nxt] = new_cost
                priority = new_cost + heuristic(goal, nxt)

                heapq.heappush(
                    frontier,
                    PriorityNode(priority, nxt, new_cost)
                )

                came_from[nxt] = current

    if goal not in came_from:
        return None

    path = []

    current = goal

    while current is not None:
        path.append(current)
        current = came_from[current]

    path.reverse()

    return path

def draw(grid: Grid, path, start, goal):

    path = set(path or [])

    for y in range(grid.height):

        row = ""

        for x in range(grid.width):

            p = (x, y)

            if p == start:
                row += "S "
            elif p == goal:
                row += "G "
            elif p in grid.walls:
                row += "■ "
            elif p in path:
                row += "* "
            else:
                row += ". "

        print(row)

grid = Grid(20, 12)

walls = [
    (5,0),(5,1),(5,2),(5,3),(5,4),(5,5),
    (5,6),(5,7),(5,8),
    (10,3),(11,3),(12,3),(13,3),(14,3),
    (10,8),(11,8),(12,8),(13,8),(14,8),
    (15,4),(15,5),(15,6),(15,7)
]

grid.walls.update(walls)

start = (1, 1)
goal = (18, 10)

path = astar(grid, start, goal)

if path:
    print(f"Camino encontrado con {len(path)} pasos.\n")
else:
    print("No existe camino.\n")

draw(grid, path, start, goal)
