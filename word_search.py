from typing import NamedTuple, Optional
from random import choice
from string import ascii_uppercase
from csp import CSP, Constraint


Grid = list[list[str]]


class GridLocation(NamedTuple):
    row: int
    column: int


def generete_grid(rows: int, columns: int) -> Grid:
    return [
        [choice(ascii_uppercase) for _ in range(columns)]
        for _ in range(rows)
    ]


def display_grid(grid: Grid) -> None:
    for row in grid:
        print("".join(row))


def generete_domain(word: str, grid: Grid) -> list[list[GridLocation]]:
    domain: list[list[GridLocation]] = []
    height: int = len(grid)
    width: int = len(grid[0])
    length: int = len(word)

    for row in range(height):
        for col in range(width):
            columns: range = range(col, col + length + 1)
            rows: range = range(row, row + length + 1)
            if col + length <= width:
                # da esquerda para direita
                domain.append([GridLocation(row, c) for c in columns])
                # diagonal em direção ao canto inferior direito
                if row + length <= height:
                    domain.append([GridLocation(r, col + (r - row)) for r in rows])

            if row + length <= height:
                # de cima para baixo
                domain.append([GridLocation(r, col) for r in rows])
                # diagonal em direção ao canto inferior esquerdo
                if col - length >= 0:
                    domain.append([GridLocation(r, col - (r - row)) for r in rows])

    return domain


class WordSearchConstraint(Constraint[str, list[GridLocation]]):
    def __init__(self, words: list[str]) -> None:
        super().__init__(words)
        self.words: list[str] = words

    def satisfied(self, assignment: dict[str, list[GridLocation]]):
        # se houver alguma posição duplicada na grade, é sinal que há uma sobreposição
        all_locations = [locs for values in assignment.values() for locs in values]
        return len(set(all_locations)) == len(all_locations)


if __name__ == '__main__':
    grid: Grid = generete_grid(9, 9)
    words: list[str] = ["MATTHEN", "JOE", "MARRY", "SARAH", "SALLY"]
    locations: dict[str, list[list[GridLocation]]] = {}
    for word in words:
        locations[word] = generete_domain(word, grid)
    csp: CSP = CSP(words, locations)
    csp.add_constraint(WordSearchConstraint(words))
    solution: Optional[dict[str, list[GridLocation]]] = csp.backtracking_search()
    if solution is None:
        print("No solution found!")
    else:
        for word, grid_locations in solution.items():
            # inversão aleatória na metade das vezes
            if choice([True, False]):
                grid_locations.reverse()
            for index, letter in enumerate(word):
                row, column = grid_locations[index].row, grid_locations[index].column
                grid[row][column] = letter
        display_grid(grid)
