'''
Problema das oito rainhas
Mais informações em https://pt.wikipedia.org/wiki/Problema_das_oito_damas
'''
from csp import Constraint, CSP
from typing import List, Dict, Optional


class QueensConstraint(Constraint[int, int]):
	def __init__(self, columns: List[int]) -> None:
		super().__init__(columns)
		self.columns: List[int] = columns

	def satisfied(self, assigment: Dict[int, int]) -> bool:
		for first_queen_column, first_queen_row in assigment.items():
			for second_queen_column in range(first_queen_column + 1, len(self.columns) + 1):
				if second_queen_column not in assigment:
					continue

				second_queen_row: int = assigment[second_queen_column]
				# mesma linha
				if first_queen_row == second_queen_row:
					return False

				# mesma diagonal
				if abs(first_queen_row - second_queen_row) == abs(first_queen_column - second_queen_column):
					return False

		return True

if __name__ == '__main__':
	columns: List[int] = [1, 2, 3, 4, 5, 6, 7, 8]
	rows: Dict[int, List[int]] = {}
	for column in columns:
		rows[column] = columns

	csp: CSP[int, int] = CSP(columns, rows)
	csp.add_constraint(QueensConstraint(columns))
	solution: Optional[Dict[int, int]] = csp.backtracking_search()
	if solution is None:
		print("No solution found!")
	else:
		print(solution)
