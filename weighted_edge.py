from __future__ import annotations
from dataclasses import dataclass
from edge import Edge


@dataclass
class WeightedEdge(Edge):
    weight: float

    def reversed(self) -> WeightedEdge:
        return WeightedEdge(self.v, self.u, self.weight)
    
    # para que possamos ordenar as arestas por peso a fim de encontrar
    # a aresta de menor peso
    def __lt__(self, other: WeightedEdge) -> bool:
        return self.weight < other.weight
    
    def __str__(self):
        return f"{self.u} {self.weight}> {self.v}"
