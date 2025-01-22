from __future__ import annotations
from typing import TypeVar, Generic, Callable
from enum import Enum
from random import choices, random
from heapq import nlargest
from statistics import mean
from chromosome import Chromosome


C = TypeVar('C', bound=Chromosome) # tipos dos cromossomos


class GenericAlgorithm(Generic[C]):
	SelectionType = Enum("SelectionType", "ROULETTE TOURNAMENT")

	def __init__(
		self, initial_population: list[C], threshold: float, max_generations: int = 100, mutation_chance: float = 0.1,
			crossover_chance: float = 0.7, selection_type: SelectionType = SelectionType.TOURNAMENT
	) -> None:
		self._population = initial_population
		self._threshold: float = threshold
		self._max_generations: int = max_generations
		self._mutation_chance: float = mutation_chance
		self._crossover_chance: float = crossover_chance
		self._selection_type: GenericAlgorithm.SelectionType = selection_type
		self._fitness_key: Callable = type(self._population[0]).fitness

	# Usa a roleta de distribuição de probabilidades para escolher dois pais
	# Nota: não trabalhamos com resultados negativos de aptidão
	def _pick_roulette(self, wheel: list[float]) -> tuple[C, C]:
		first, second = choices(self._population, weights=wheel, k=2)
		return first, second

	# Escolhe num_participants aleatoriamente e seleciona os 2 melhores
	def _pick_tournament(self, num_participants: int) -> tuple[C, C]:
		participants: list[C] = choices(self._population, k=num_participants)
		first, second = nlargest(2, participants, key=self._fitness_key)
		return first, second

	# Substitui a população por uma nova geração de indivíduos
	def _reproduce_and_replace(self) -> None:
		new_population: list[C] = []
		# continua até ter completado a nova geração
		while len(new_population) < len(self._population):
			# escolhe os 2 pais
			if self._selection_type == GenericAlgorithm.SelectionType.ROULETTE:
				parents: tuple[C, C] = self._pick_roulette(self._population)
			else:
				parents: tuple[C, C] = self._pick_tournament(len(self._population) // 2)
			# faz um possível crossover dos dois pais
			if random() < self._crossover_chance:
				new_population.extend(parents[0].crossover(parents[1]))
			else:
				new_population.extend(parents)

		# se tivemos um número ímpar, teremos 1 extra, portanto ele será removido
		if len(new_population) > len(self._population):
			new_population.pop()

		self._population = new_population # substitui a referência

	# Com uma probabilidade de _mutation_chance faz uma mutação em cada indivíduo
	def _mutate(self) -> None:
		for individual in self._population:
			if random() < self._mutation_chance:
				individual.mutate()

	# Executa o algoritmo genético para max_generations iterações
	# e devolve o melhor indivíduo encontrado
	def run(self) -> C:
		best: C = max(self._population, key=self._fitness_key)
		for generation in range(self._max_generations):
			# sai antes, se o limiar for atingido
			if best.fitness() >= self._threshold:
				return best

			print(f"Generation {generation} Best {best.fitness()} Avg {mean(map(self._fitness_key, self._population))}")
			self._reproduce_and_replace()
			self._mutate()
			highest: C = max(self._population, key=self._fitness_key)
			if highest.fitness() > best.fitness():
				best = highest # encontrado um novo cromossomo melhor
		return best # o melhor encontrado em _max_generations
		
