from enum import Enum
from typing import List, NamedTuple, Callable, Optional
from math import sqrt
import random
# dfs, bfs, node_to_path, astar, Node
from generic_search import dfs, bfs, node_to_path, astar, Node


class Cell(str, Enum):
    """Enumerador com as possiveis celulas no labirito"""
    EMPTY = " "
    BLOCKED = "X"
    START = "S"
    GOAL = "G"
    PATH = "*"


class MazeLocation(NamedTuple):
    """Representa um lugar no labirito"""
    row: int
    column: int


class Maze:
    def __init__(self, rows: int = 10, columns: int = 10, sparseness: float = 0.2,
                 start: MazeLocation = MazeLocation(0, 0),
                 goal: MazeLocation = MazeLocation(9, 9)) -> None:
        self._rows: int = rows
        self._columns: int = columns
        self.start: MazeLocation = start
        self.goal: MazeLocation = goal

        # prencher o labirito com items vazios
        self._grid = [[Cell.EMPTY for x in range(
            columns)] for i in range(rows)]

        self._ramdomly_fill(rows, columns, sparseness)

        self._grid[start.row][start.column] = Cell.START
        self._grid[goal.row][goal.column] = Cell.GOAL

    def _ramdomly_fill(self, rows: int, columns: int, sparseness: float) -> None:
        """Gera os obstaculos"""
        for row in range(rows):
            for column in range(columns):
                if random.uniform(0, 1.0) < sparseness:
                    self._grid[row][column] = Cell.BLOCKED

    def goal_test(self, ml: MazeLocation) -> bool:
        """Testa se esta no objetivo"""
        return ml == self.goal

    def sucessors(self, ml: MazeLocation) -> List[MazeLocation]:
        """Retorna a lista de posições posíveis a se mover"""
        locations: List[MazeLocation] = []

        # checa a posição a direita
        if ml.row + 1 < self._rows and self._grid[ml.row + 1][ml.column] != Cell.BLOCKED:
            locations.append(MazeLocation(ml.row + 1, ml.column))

        # checa a posição a esquerda
        if ml.row - 1 >= 0 and self._grid[ml.row - 1][ml.column] != Cell.BLOCKED:
            locations.append(MazeLocation(ml.row - 1, ml.column))

        # checa a posição a cima
        if ml.column - 1 >= 0 and self._grid[ml.row][ml.column - 1] != Cell.BLOCKED:
            locations.append(MazeLocation(ml.row, ml.column - 1))

        # checa a posição a baixo
        if ml.column + 1 < self._columns and self._grid[ml.row][ml.column + 1] != Cell.BLOCKED:
            locations.append(MazeLocation(ml.row, ml.column + 1))

        return locations

    def mark(self, path: List[MazeLocation]):
        for maze_location in path:
            self._grid[maze_location.row][maze_location.column] = Cell.PATH

        self._grid[self.start.row][self.start.column] = Cell.START
        self._grid[self.goal.row][self.goal.column] = Cell.GOAL

    def clear(self, path: List[MazeLocation]):
        for maze_location in path:
            self._grid[maze_location.row][maze_location.column] = Cell.EMPTY

        self._grid[self.start.row][self.start.column] = Cell.START
        self._grid[self.goal.row][self.goal.column] = Cell.GOAL

    def __str__(self) -> str:
        output: str = ""

        output += "=" * self._columns + "==\n"

        for row in self._grid:
            output += "=" + "".join([column.value for column in row]) + "=\n"

        output += "=" * self._columns + "==\n"

        return output


def euclidean_distance(goal: MazeLocation) -> Callable[[MazeLocation], float]:
    def distance(ml: MazeLocation) -> float:
        xdist: int = ml.column - goal.column
        ydist: int = ml.row - goal.row

        return sqrt((xdist ** 2) + (ydist ** 2))

    return distance


def manhattan_distance(goal: MazeLocation) -> Callable[[MazeLocation], float]:
    def distance(ml: MazeLocation) -> float:
        xdist: int = abs(ml.column - goal.column)
        ydist: int = abs(ml.row - goal.row)

        return (xdist + ydist)

    return distance


if __name__ == "__main__":
    maze: Maze = Maze()
    print(maze)
    solution1: Optional[Node[MazeLocation]] = dfs(
        maze.start, maze.goal_test, maze.sucessors)

    if solution1 is None:
        print("Depth-first search não achou uma solução")

    else:
        print("Depth-first")
        path1: List[MazeLocation] = node_to_path(solution1)
        maze.mark(path1)

        print(maze)

        maze.clear(path1)

    solution2: Optional[Node[MazeLocation]] = bfs(
        maze.start, maze.goal_test, maze.sucessors)

    if solution2 is None:
        print("Bread-first search não achou uma solução")

    else:
        print("Bread-first")
        path2: List[MazeLocation] = node_to_path(solution2)
        maze.mark(path2)

        print(maze)

        maze.clear(path2)

    distance: Callable[[MazeLocation], float] = manhattan_distance(maze.goal)
    solution3: Optional[Node[MazeLocation]] = astar(
        maze.start, maze.goal_test, maze.sucessors, distance
    )

    if solution3 is None:
        print("A star não achou uma solução")

    else:
        print("A star")
        path3: List[MazeLocation] = node_to_path(solution3)
        maze.mark(path3)

        print(maze)

        maze.clear(path3)
