from __future__ import annotations
from typing import TypeVar, Type
from abc import ABC, abstractmethod


T = TypeVar('T', bound='Chromosome')


class Chromosome(ABC):
	@abstractmethod
	def fitness(self) -> float:
		...

	@classmethod
	@abstractmethod
	def random_instance(cls: Type[T]) -> T:
		...

	@abstractmethod
	def crossover(self: T, other: T) -> tuple[T, T]:
		...

	@abstractmethod
	def mutate(self) -> None:
		...
