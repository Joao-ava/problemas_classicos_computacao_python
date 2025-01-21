from __future__ import annotations
from typing import TypeVar, Optional
from dataclasses import dataclass
from mst import WeightedPath, print_weight_path
from weighted_graph import WeightedGraph
from weighted_graph import WeightedEdge
from generic_search import PriorityQueue


V = TypeVar('V')


@dataclass
class DijkstraNode:
	vertex: int
	distance: float
	def __lt__(self, other: DijkstraNode) -> bool:
		return self.distance < other.distance
	def __eq__(self, other: DijkstraNode) -> bool:
		return self.distance == other.distance


def dijkstra(wg: WeightedGraph[V], root: V) -> tuple[list[Optional[float]], dict[int, WeightedEdge]]:
	first: int = wg.index_of(root) # encontra o índice inicial
	# inicialmente, as distâncias são desconhecidas
	distances: list[Optional[float]] = [None] * wg.vertex_count
	distances[first] = 0 # a raiz está a uma distância 0 da raiz
	path_dict: dict[int, WeightedEdge] = {} # como chegamos até cada vértice
	pq: PriorityQueue[DijkstraNode] = PriorityQueue()
	pq.push(DijkstraNode(first, 0))
	while not pq.empty:
		u: int = pq.pop().vertex # explora o vértice mais próximo a seguir
		dist_u: float = distances[u] # caso já tenha sido visto
		# analisa todas as arestas/vértices a partir deste vértice
		for we in wg.edges_for_index(u):
			# a distância anterior até este vértice
			dist_v: float = distances[we.v]
			# não há distância anterior ou um caminho mais curto foi encontrado
			if dist_v is None or dist_v > we.weight + dist_u:
				# atualiza a distância até este vértice
				distances[we.v] = we.weight + dist_u
				# atualiza a aresta no caminho mínimo até este vértice
				path_dict[we.v] = we
				# será explorado em breve
				pq.push(DijkstraNode(we.v, we.weight + dist_u))
	return distances, path_dict


# Função auxiliar para ter um acesso mais fácil aos resultados de dijkstra
def distance_array_to_vertex_dict(wg: WeightedGraph[V], distances: list[Optional[float]]) -> dict[V, Optional[float]]:
	distance_dict: dict[int, Optional[float]] = {}
	for i in range(len(distances)):
		distance_dict[wg.vertex_at(i)] = distances[i]
	return distance_dict


# Recebe um ducionário de arestas para alcançar cada nó e devolve
# uma lista de arestas que vão de `start` até `end`
def path_dict_to_path(start: int, end: int, path_dict: dict[int, WeightedEdge]) -> WeightedPath:
	if len(path_dict) == 0:
		return []
	edge_path: WeightedPath = []
	e: WeightedEdge = path_dict[end]
	edge_path.append(e)
	while e.u != start:
		e = path_dict[e.u]
		edge_path.append(e)
	return list(reversed(edge_path))


if __name__ == '__main__':
	city_graph2: WeightedGraph[str] = WeightedGraph([
		"Seattle", "San Francisco", "Los Angeles", "Riverside", "Phoenix",
		"Chicago", "Boston", "New York", "Atlanta", "Miami", "Dallas",
		"Houston", "Detroit", "Philadelphia", "Washington"
	])
	city_graph2.add_edge_by_vertices("Seattle", "Chicago", 1737)
	city_graph2.add_edge_by_vertices("Seattle", "San Francisco", 678)
	city_graph2.add_edge_by_vertices("San Francisco", "Riverside", 386)
	city_graph2.add_edge_by_vertices("San Francisco", "Los Angeles", 348)
	city_graph2.add_edge_by_vertices("Los Angeles", "Riverside", 50)
	city_graph2.add_edge_by_vertices("Los Angeles", "Phoenix", 357)
	city_graph2.add_edge_by_vertices("Riverside", "Phoenix", 307)
	city_graph2.add_edge_by_vertices("Riverside", "Chicago", 1704)
	city_graph2.add_edge_by_vertices("Phoenix", "Dallas", 887)
	city_graph2.add_edge_by_vertices("Phoenix", "Houston", 1015)
	city_graph2.add_edge_by_vertices("Dallas", "Chicago", 805)
	city_graph2.add_edge_by_vertices("Dallas", "Atlanta", 721)
	city_graph2.add_edge_by_vertices("Dallas", "Houston", 225)
	city_graph2.add_edge_by_vertices("Houston", "Atlanta", 702)
	city_graph2.add_edge_by_vertices("Houston", "Miami", 968)
	city_graph2.add_edge_by_vertices("Atlanta", "Chicago", 588)
	city_graph2.add_edge_by_vertices("Atlanta", "Washington", 543)
	city_graph2.add_edge_by_vertices("Atlanta", "Miami", 604)
	city_graph2.add_edge_by_vertices("Miami", "Washington", 923)
	city_graph2.add_edge_by_vertices("Chicago", "Detroit", 238)
	city_graph2.add_edge_by_vertices("Detroit", "Boston", 613)
	city_graph2.add_edge_by_vertices("Detroit", "Washington", 396)
	city_graph2.add_edge_by_vertices("Detroit", "New York", 482)
	city_graph2.add_edge_by_vertices("Boston", "New York", 190)
	city_graph2.add_edge_by_vertices("New York", "Philadelphia", 81)
	city_graph2.add_edge_by_vertices("Philadelphia", "Washington", 123)

	distances, path_dict = dijkstra(city_graph2, "Los Angeles")
	name_distance: dict[str, Optional[float]] = distance_array_to_vertex_dict(city_graph2, distances)
	print("Distances from Los Angeles:")
	for key, value in name_distance.items():
		print(f"{key}: {value}")
	print("") # linha em branco
	print("Shortest path from Los Angeles to Boston:")
	path: WeightedPath = path_dict_to_path(city_graph2.index_of("Los Angeles"), city_graph2.index_of("Boston"), path_dict)
	print_weight_path(city_graph2, path)
