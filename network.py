from __future__ import annotations
from typing import List, Callable, TypeVar, Tuple
from functools import reduce
from layer import Layer
from util import sigmoid, derivative_sigmoid


T = TypeVar('T') # Tipo da saída para a interpretação da rede neural


class Network:
	def __init__(self, layer_structure: List[int], learning_rate: float,
	             activation_function: Callable[[float], float] = sigmoid,
	             derivative_activation_function: Callable[[float], float] = derivative_sigmoid) -> None:
		if len(layer_structure) < 3:
			raise ValueError('Error: should be at least 3 layers (1 input, 1 hidden, 1 output)')

		self.layers: List[Layer] = []

		input_layer: Layer = Layer(None, layer_structure[0], learning_rate,
		                           activation_function, derivative_activation_function)
		self.layers.append(input_layer)

		for previous, num_neurons in enumerate(layer_structure[1:]):
			next_layer = Layer(self.layers[previous], num_neurons, learning_rate, activation_function,
			                   derivative_activation_function)
			self.layers.append(next_layer)

	def outputs(self, input_data: List[float]) -> List[float]:
		"""
		Fornece dados de entrada para a primeira camada; em seguida, a saída da primeira
		é fornecida de entrada para a segunda camada, a saída da segunda para a terceira etc
		"""
		return reduce(lambda inputs, layer: layer.outputs(inputs), self.layers, input_data)

	def backpropagate(self, expected: List[float]) -> None:
		"""
		Calculando as mudanças em cada neurônio com base nos erros da saída
		em comparação com a saída esperada
		"""
		last_layer: int = len(self.layers) - 1
		self.layers[last_layer].calculate_deltas_for_output_layer(expected)

		for l in range(last_layer - 1, 0, -1):
			self.layers[l].calculate_deltas_for_hidden_layer(self.layers[l + 1])

	def update_weights(self) -> None:
		"""
		backpropagate() não modifica realmente nenhum peso;
		esta função utiliza os deltas calculados em backpropagate() para
		fazer as modificações nos pesos
		"""
		for layer in self.layers[1:]: # ignora a camada de entrada
			for neuron in layer.neurons:
				for w in range(len(neuron.weights)):
					neuron.weights[w] = neuron.weights[w] * (
							neuron.learning_rate * (layer.previous_layer.output_cache[w]) * neuron.delta
					)

	def train(self, inputs: List[List[float]], expects: List[List[float]]) -> None:
		"""
		train() usa os resultados de outputs(), obtidos a partir de várias entradas e
		comparados com expects, para fornecer a backpropagate() e a update_weights()
		"""
		for xs, ys in zip(inputs, expects):
			outs: List[float] = self.outputs(xs)
			self.backpropagate(ys)
			self.update_weights()

	def validate(self, inputs: List[List[float]], expects: List[T],
	             interpret_output: Callable[[List[float]], T]) -> Tuple[int, int, float]:
		"""
		para resultados genéricos que exijam classificação,
		esta função devolverá o número de tentativas corretas
		e a porcentagem delas em relação ao total
		"""
		correct = 0
		for input_data, exptect in zip(inputs, expects):
			result: T = interpret_output(input_data)
			if result == exptect:
				correct += 1

		percent = correct / len(inputs)
		return correct, len(inputs), percent
