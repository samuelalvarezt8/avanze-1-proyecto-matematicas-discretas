"""Command line entry point: ``uv run python -m graphs data/ejemplo_1.csv``."""

from __future__ import annotations

import argparse

from . import has_cycles, is_connected, is_forest, is_tree, load_graph


def main() -> None:
    parser = argparse.ArgumentParser(description="Analyze a graph stored in a CSV file.")
    parser.add_argument("path", help="CSV file with header source,target,weight")
    parser.add_argument(
        "--directed", action="store_true", help="treat the edges as directed"
    )
    args = parser.parse_args()

    graph = load_graph(args.path, directed=args.directed)
    print(graph)
    is_connected(graph)
    has_cycles(graph)
    is_tree(graph)
    is_forest(graph)


if __name__ == "__main__":
    main()
