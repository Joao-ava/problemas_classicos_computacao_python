from __future__ import annotations
from dataclasses import dataclass


@dataclass
class Edge:
    u: int # o vértice "de"
    v: int # o vértice "para"

    def reversed(self) -> Edge:
        return Edge(self.v, self.u)
    
    def __str__(self) -> bool:
        return f"{self.u} -> {self.v}"
