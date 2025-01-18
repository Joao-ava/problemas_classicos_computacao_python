from typing import TypeVar, Generic, Optional
from edge import Edge


V = TypeVar('V') # tipo dos vértices no grafo


class Graph(Generic[V]):
    def __init__(self, vertices: list[V] = []) -> None:
        self._vertices: list[V] = vertices
        self._edges: list[list[Edge]] = [[] for _ in vertices]

    @property
    def vertex_count(self) -> int:
        return len(self._vertices) # Número de vértices
    
    @property
    def edge_count(self) -> int:
        return sum(map(len, self._edges)) # Número de arestas
    
    # Adicione um vértice no grafo e devolve o seu index
    def add_vertex(self, vertex: V) -> int:
        self._vertices.append(vertex)
        self._edges.append([]) # Adicione uma lista vazia para conter as arestas
        return self.vertex_count - 1 # Devolve o indice do vértice adicionado
    
    # Este grafo não é direcionado,
    # portanto, smpre adicionamos arestas nas duas direções
    def add_edge(self, edge: Edge) -> None:
        self._edges[edge.u].append(edge)
        self._edges[edge.v].append(edge.reversed())

    # Adiciona uma aresta usando indices dos vértices (método auxiliar)
    def add_edge_by_indices(self, u: int, v: int) -> None:
        edge: Edge = Edge(u, v)
        self.add_edge(edge)

    # Adicionando uma aresta consultando os indices dos vértices (método auxiliar)
    def add_edge_by_vertices(self, first: V, second: V) -> None:
        u: int = self._vertices.index(first)
        v: int = self._vertices.index(second)
        self.add_edge_by_indices(u, v)

    # Encontra o vértice em um índice especifico
    def vertex_at(self, index: int) -> V:
        return self._vertices[index]

    # Ecnontra o índice de um vértices no grafo
    def index_of(self, vertex: V) -> int:
        return self._vertices.index(vertex)

    # Encontra os vértices aos quais um vértice com determinado índice está conectado
    def neighbors_for_index(self, index: int) -> list[V]:
        return list(map(self.vertex_at, [e.v for e in self._edges[index]]))

    # Devolve todas as arestas associadas a um vértice em um índice
    def edges_for_index(self, index: int) -> list[Edge]:
        return self._edges[index]

    # Consulta o índice de um vértice e devolve suas arestas (métpodo auxiliar)
    def edges_for_vertex(self, vertex: V) -> list[Edge]:
        return self.edges_for_index(self.index_of(vertex))

    # Facilita a exibição elegante de um Graph
    def __str__(self) -> str:
        desc: str = ""
        for i in range(self.vertex_count):
            desc += f"{self.vertex_at(i)} -> {self.neighbors_for_index(i)}\n"
        return desc


if __name__ == '__main__':
    city_graph: Graph[str] = Graph([
        "Seattle", "San Francisco", "Los Angeles", "Riverside", "Phoenix",
        "Chicago", "Boston", "New York", "Atlanta", "Miami", "Dallas",
        "Houston", "Detroit", "Philadelphia", "Washington"
    ])
    city_graph.add_edge_by_vertices("Seattle", "Chicago")
    city_graph.add_edge_by_vertices("Seattle", "San Francisco")
    city_graph.add_edge_by_vertices("San Francisco", "Riverside")
    city_graph.add_edge_by_vertices("San Francisco", "Los Angeles")
    city_graph.add_edge_by_vertices("Los Angeles", "Riverside")
    city_graph.add_edge_by_vertices("Los Angeles", "Phoenix")
    city_graph.add_edge_by_vertices("Riverside", "Phoenix")
    city_graph.add_edge_by_vertices("Riverside", "Chicago")
    city_graph.add_edge_by_vertices("Phoenix", "Dallas")
    city_graph.add_edge_by_vertices("Phoenix", "Houston")
    city_graph.add_edge_by_vertices("Dallas", "Chicago")
    city_graph.add_edge_by_vertices("Dallas", "Atlanta")
    city_graph.add_edge_by_vertices("Dallas", "Houston")
    city_graph.add_edge_by_vertices("Houston", "Atlanta")
    city_graph.add_edge_by_vertices("Houston", "Miami")
    city_graph.add_edge_by_vertices("Atlanta", "Chicago")
    city_graph.add_edge_by_vertices("Atlanta", "Washington")
    city_graph.add_edge_by_vertices("Atlanta", "Miami")
    city_graph.add_edge_by_vertices("Miami", "Washington")
    city_graph.add_edge_by_vertices("Chicago", "Detroit")
    city_graph.add_edge_by_vertices("Detroit", "Boston")
    city_graph.add_edge_by_vertices("Detroit", "Washington")
    city_graph.add_edge_by_vertices("Detroit", "New York")
    city_graph.add_edge_by_vertices("Boston", "New York")
    city_graph.add_edge_by_vertices("New York", "Philadelphia")
    city_graph.add_edge_by_vertices("Philadelphia", "Washington")
    print(city_graph)
