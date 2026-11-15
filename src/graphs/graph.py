"""Graph representations (adjacency lists) for undirected and directed graphs.

Both classes store the graph as a dictionary of dictionaries:

    adjacency[u][v] = weight

No graph libraries are used.
"""

from __future__ import annotations

from typing import Hashable, Iterator

Vertex = Hashable
Weight = float | int


class UndirectedGraph:
    """Weighted undirected graph stored as an adjacency list.

    Each edge {u, v} is stored twice (``adjacency[u][v]`` and
    ``adjacency[v][u]``) so neighbor lookups are O(1) on average.
    Adding an edge that already exists overwrites its weight.
    """

    def __init__(self) -> None:
        self._adjacency: dict[Vertex, dict[Vertex, Weight]] = {}

    # -- construction ------------------------------------------------------
    def add_vertex(self, vertex: Vertex) -> None:
        self._adjacency.setdefault(vertex, {})

    def add_edge(self, source: Vertex, target: Vertex, weight: Weight = 1) -> None:
        self.add_vertex(source)
        self.add_vertex(target)
        self._adjacency[source][target] = weight
        self._adjacency[target][source] = weight

    # -- queries -----------------------------------------------------------
    def vertices(self) -> list[Vertex]:
        return list(self._adjacency)

    def neighbors(self, vertex: Vertex) -> list[Vertex]:
        return list(self._adjacency[vertex])

    def underlying_neighbors(self, vertex: Vertex) -> list[Vertex]:
        """Neighbors ignoring direction (same as ``neighbors`` here)."""
        return self.neighbors(vertex)

    def has_edge(self, source: Vertex, target: Vertex) -> bool:
        return source in self._adjacency and target in self._adjacency[source]

    def get_weight(self, source: Vertex, target: Vertex) -> Weight:
        return self._adjacency[source][target]

    def edges(self) -> list[tuple[Vertex, Vertex, Weight]]:
        """Every edge exactly once (a self-loop counts as one edge)."""
        seen: set[frozenset] = set()
        result = []
        for u, neighbors in self._adjacency.items():
            for v, w in neighbors.items():
                key = frozenset((u, v))
                if key not in seen:
                    seen.add(key)
                    result.append((u, v, w))
        return result

    def num_vertices(self) -> int:
        return len(self._adjacency)

    def num_edges(self) -> int:
        return len(self.edges())

    def __contains__(self, vertex: Vertex) -> bool:
        return vertex in self._adjacency

    def __iter__(self) -> Iterator[Vertex]:
        return iter(self._adjacency)

    def __repr__(self) -> str:
        return (
            f"UndirectedGraph(vertices={self.num_vertices()}, "
            f"edges={self.num_edges()})"
        )


class DirectedGraph:
    """Weighted directed graph stored as an adjacency list of successors.

    ``adjacency[u][v] = w`` means there is an edge u -> v with weight w.
    A map of predecessors is also kept so the underlying undirected
    structure can be traversed without rebuilding the graph.
    """

    def __init__(self) -> None:
        self._adjacency: dict[Vertex, dict[Vertex, Weight]] = {}
        self._predecessors: dict[Vertex, set[Vertex]] = {}

    # -- construction ------------------------------------------------------
    def add_vertex(self, vertex: Vertex) -> None:
        self._adjacency.setdefault(vertex, {})
        self._predecessors.setdefault(vertex, set())

    def add_edge(self, source: Vertex, target: Vertex, weight: Weight = 1) -> None:
        self.add_vertex(source)
        self.add_vertex(target)
        self._adjacency[source][target] = weight
        self._predecessors[target].add(source)

    # -- queries -----------------------------------------------------------
    def vertices(self) -> list[Vertex]:
        return list(self._adjacency)

    def neighbors(self, vertex: Vertex) -> list[Vertex]:
        """Successors of ``vertex`` (edges leaving it)."""
        return list(self._adjacency[vertex])

    def underlying_neighbors(self, vertex: Vertex) -> list[Vertex]:
        """Successors and predecessors, ignoring edge direction."""
        return list(set(self._adjacency[vertex]) | self._predecessors[vertex])

    def has_edge(self, source: Vertex, target: Vertex) -> bool:
        return source in self._adjacency and target in self._adjacency[source]

    def get_weight(self, source: Vertex, target: Vertex) -> Weight:
        return self._adjacency[source][target]

    def edges(self) -> list[tuple[Vertex, Vertex, Weight]]:
        return [
            (u, v, w) for u, out in self._adjacency.items() for v, w in out.items()
        ]

    def num_vertices(self) -> int:
        return len(self._adjacency)

    def num_edges(self) -> int:
        return sum(len(out) for out in self._adjacency.values())

    def __contains__(self, vertex: Vertex) -> bool:
        return vertex in self._adjacency

    def __iter__(self) -> Iterator[Vertex]:
        return iter(self._adjacency)

    def __repr__(self) -> str:
        return (
            f"DirectedGraph(vertices={self.num_vertices()}, "
            f"edges={self.num_edges()})"
        )
