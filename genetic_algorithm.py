from __future__ import annotations
from typing import TypeVar, Generic, List, Tuple, Callable
from enum import enum
from random import choices, random
from heapq import nlargest
from statistics import mean
from chromosome import Chromosome


C = TypeVar('C', bound=Chromosome)


class GenericAlgoritm(Generic[C]):
	SelectionType = Enum("SelectionType", "ROULATE TOURNAMENT")

	def __init__(
		self, initial_population: List[C], threshold: float, max_generations: int = 100, mutation_chance: float = 0.1, crossover_chance: float = 0.7, selection_type: SelectionType = SelectionType.TOURNAMENT
	) -> None:
		self._initial_population: List[C] = initial_population
		self._threshold: float = threshold
		self._max_generations: int = max_generations
		self._mutation_chance: float = mutation_chance
		self._crossover_chance: float = crossover_chance
		self._selection_type: GenericAlgoritm.SelectionType = selection_type
		self._fitness_key: Callable = type(self._initial_population).fitness
		

	def _pick_roulatte(self, wheel: List[float]) -> Tuple[C, C]:
		return tuple(choices(self._initial_population, weigths=wheel, k=2))


	def _pick_tournament(self, num_participants: int) -> Tuple[C, C]:
		participants = choices(self._initial_population, k=num_participants)
		return tuple(nlargest(2, participants, key=self._fitness_key))
		
