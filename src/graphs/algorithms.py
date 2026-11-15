"""Structural checks on graphs: connectivity, cycles, trees and forests.

The public functions ``is_connected``, ``has_cycles``, ``is_tree`` and
``is_forest`` both **return** the result and **print** it as
``<function_name>: <result>``.

They work with ``UndirectedGraph`` and ``DirectedGraph``:

* ``is_connected`` / ``is_tree`` / ``is_forest`` ignore edge direction
  (weak connectivity, i.e. they look at the underlying undirected graph).
* ``has_cycles`` respects direction on directed graphs (directed cycles).

Conventions for the empty graph (0 vertices): not connected, not a tree,
it *is* a forest (zero trees), and it has no cycles.
"""

from __future__ import annotations

from .graph import DirectedGraph, UndirectedGraph

Graph = UndirectedGraph | DirectedGraph


# --------------------------------------------------------------------------
# Internal helpers (no printing)
# --------------------------------------------------------------------------
def _count_components(graph: Graph) -> int:
    """Number of connected components, ignoring edge direction (iterative DFS)."""
    visited: set = set()
    components = 0
    for start in graph.vertices():
        if start in visited:
            continue
        components += 1
        stack = [start]
        visited.add(start)
        while stack:
            vertex = stack.pop()
            for neighbor in graph.underlying_neighbors(vertex):
                if neighbor not in visited:
                    visited.add(neighbor)
                    stack.append(neighbor)
    return components


def _connected(graph: Graph) -> bool:
    return graph.num_vertices() > 0 and _count_components(graph) == 1


def _undirected_has_cycle(graph: UndirectedGraph) -> bool:
    """DFS: a cycle exists if we reach a visited vertex that is not our parent."""
    visited: set = set()
    for start in graph.vertices():
        if start in visited:
            continue
        visited.add(start)
        stack = [(start, None)]  # (vertex, parent)
        while stack:
            vertex, parent = stack.pop()
            for neighbor in graph.neighbors(vertex):
                if neighbor == vertex:
                    return True  # self-loop
                if neighbor not in visited:
                    visited.add(neighbor)
                    stack.append((neighbor, vertex))
                elif neighbor != parent:
                    return True
    return False


def _directed_has_cycle(graph: DirectedGraph) -> bool:
    """Iterative DFS with three colors; an edge to a GRAY vertex is a cycle."""
    white, gray, black = 0, 1, 2
    color = {vertex: white for vertex in graph.vertices()}

    for start in graph.vertices():
        if color[start] != white:
            continue
        color[start] = gray
        stack = [(start, iter(graph.neighbors(start)))]
        while stack:
            vertex, children = stack[-1]
            advanced = False
            for child in children:
                if color[child] == gray:
                    return True
                if color[child] == white:
                    color[child] = gray
                    stack.append((child, iter(graph.neighbors(child))))
                    advanced = True
                    break
            if not advanced:
                color[vertex] = black
                stack.pop()
    return False


def _has_cycles(graph: Graph) -> bool:
    if isinstance(graph, DirectedGraph):
        return _directed_has_cycle(graph)
    return _undirected_has_cycle(graph)


def _forest(graph: Graph) -> bool:
    """A graph is a forest iff |E| = |V| - (number of components)."""
    return graph.num_edges() == graph.num_vertices() - _count_components(graph)


# --------------------------------------------------------------------------
# Public API (return AND print)
# --------------------------------------------------------------------------
def is_connected(graph: Graph) -> bool:
    result = _connected(graph)
    print(f"is_connected: {result}")
    return result


def has_cycles(graph: Graph) -> bool:
    result = _has_cycles(graph)
    print(f"has_cycles: {result}")
    return result


def is_tree(graph: Graph) -> bool:
    """A tree is a connected graph with no cycles (|E| = |V| - 1)."""
    result = _connected(graph) and _forest(graph)
    print(f"is_tree: {result}")
    return result


def is_forest(graph: Graph) -> bool:
    """A forest is a graph whose connected components are all trees."""
    result = _forest(graph)
    print(f"is_forest: {result}")
    return result
