from typing import List
from math import exp


def dot_product(xs: List[float], ys: List[float]) -> float:
	"""produto escalar de dois vetores"""
	return sum(x * y for x, y in zip(xs, ys))


# a clássica função de ativação sigmoide
def sigmoid(x: float) -> float:
	return 1.0 / (1.0 + exp(-x))


def derivative_sigmoid(x: float) -> float:
	sig: float = sigmoid(x)
	return sig * (1 - sig)


def normalize_by_feature_scaling(dataset: List[List[float]]) -> None:
	"""
	supõe que todas as linhas têm o mesmo tamanho
	e faz feature scaling de cada coluna para estar no intervalo de 0 a 1
	"""
	for col_num in range(len(dataset[0])):
		column: List[float] = [row[col_num] for row in dataset]
		maximum: float = max(column)
		minimum: float = min(column)
		for row_num in range(len(dataset)):
			dataset[row_num][col_num] = (dataset[row_num][col_num] - minimum) / (maximum - minimum)
