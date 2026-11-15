"""Load graphs from a CSV file with the header ``source,target,weight``."""

from __future__ import annotations

import csv
from pathlib import Path

from .graph import DirectedGraph, UndirectedGraph

EXPECTED_HEADER = ["source", "target", "weight"]


def _parse_vertex(raw: str):
    """Vertices are ints when possible (``"3"`` -> ``3``), strings otherwise."""
    raw = raw.strip()
    try:
        return int(raw)
    except ValueError:
        return raw


def _parse_weight(raw: str):
    raw = raw.strip()
    try:
        return int(raw)
    except ValueError:
        return float(raw)  # raises ValueError if not numeric


def load_graph(path: str | Path, directed: bool = False):
    """Read ``path`` and return a graph initialized from its rows.

    Args:
        path: path to a text file whose lines are ``source,target,weight``
            (the first line must be the header ``source,target,weight``).
        directed: build a ``DirectedGraph`` when True, otherwise an
            ``UndirectedGraph``.

    Raises:
        FileNotFoundError: if the file does not exist.
        ValueError: if the header or any row is malformed.
    """
    graph = DirectedGraph() if directed else UndirectedGraph()

    with open(path, newline="", encoding="utf-8") as file:
        reader = csv.reader(file, delimiter=",")
        header = next(reader, None)
        if header is None or [h.strip().lower() for h in header] != EXPECTED_HEADER:
            raise ValueError(
                f"Invalid header in {path}: expected 'source,target,weight'"
            )

        for row in reader:
            if not row or all(not cell.strip() for cell in row):
                continue  # skip blank lines
            line = reader.line_num
            if len(row) != 3:
                raise ValueError(f"Line {line}: expected 3 columns, got {len(row)}")
            try:
                source, target = _parse_vertex(row[0]), _parse_vertex(row[1])
                weight = _parse_weight(row[2])
            except ValueError as error:
                raise ValueError(f"Line {line}: invalid value ({error})") from error
            graph.add_edge(source, target, weight)

    return graph
