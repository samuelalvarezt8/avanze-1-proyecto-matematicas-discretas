from pathlib import Path

import pytest

from graphs import (
    DirectedGraph,
    UndirectedGraph,
    has_cycles,
    is_connected,
    is_forest,
    is_tree,
    load_graph,
)

DATA = Path(__file__).parent.parent / "data"

# file -> (connected, has_cycles, tree, forest)  [undirected]
EXPECTED_UNDIRECTED = {
    "ejemplo_1.csv": (True, False, True, True),
    "ejemplo_2.csv": (False, False, False, True),
    "ejemplo_3.csv": (True, True, False, False),
    "ejemplo_4.csv": (True, True, False, False),
    "ejemplo_5.csv": (False, True, False, False),
    "ejemplo_6.csv": (True, True, False, False),
}


@pytest.mark.parametrize("name,expected", EXPECTED_UNDIRECTED.items())
def test_undirected_examples(name, expected):
    graph = load_graph(DATA / name)
    assert isinstance(graph, UndirectedGraph)
    assert (
        is_connected(graph),
        has_cycles(graph),
        is_tree(graph),
        is_forest(graph),
    ) == expected


def test_directed_cycles():
    # ejemplo_4 is the directed ring 1->2->...->6->1
    assert has_cycles(load_graph(DATA / "ejemplo_4.csv", directed=True)) is True
    # ejemplo_1 is a directed tree (edges point away from the root)
    assert has_cycles(load_graph(DATA / "ejemplo_1.csv", directed=True)) is False


def test_directed_dag_with_undirected_cycle_is_not_a_forest():
    g = DirectedGraph()
    g.add_edge(1, 2)
    g.add_edge(1, 3)
    g.add_edge(2, 3)  # no directed cycle, but 1-2-3 is a cycle if direction is ignored
    assert has_cycles(g) is False
    assert is_connected(g) is True
    assert is_tree(g) is False
    assert is_forest(g) is False


def test_directed_two_cycle_is_not_a_tree():
    g = DirectedGraph()
    g.add_edge(1, 2)
    g.add_edge(2, 1)
    assert has_cycles(g) is True
    assert is_tree(g) is False


def test_self_loop_is_a_cycle():
    g = UndirectedGraph()
    g.add_edge(1, 1, 5)
    assert has_cycles(g) is True
    assert is_forest(g) is False


def test_empty_and_single_vertex():
    g = UndirectedGraph()
    assert (is_connected(g), has_cycles(g), is_tree(g), is_forest(g)) == (
        False, False, False, True,
    )
    g.add_vertex(1)
    assert (is_connected(g), has_cycles(g), is_tree(g), is_forest(g)) == (
        True, False, True, True,
    )


def test_print_format(capsys):
    g = load_graph(DATA / "ejemplo_1.csv")
    is_connected(g)
    has_cycles(g)
    is_tree(g)
    is_forest(g)
    assert capsys.readouterr().out.splitlines() == [
        "is_connected: True",
        "has_cycles: False",
        "is_tree: True",
        "is_forest: True",
    ]


def test_loader_reads_weights_and_edges():
    g = load_graph(DATA / "ejemplo_1.csv")
    assert g.num_vertices() == 7
    assert g.num_edges() == 6
    assert g.get_weight(1, 2) == 4
    assert g.get_weight(2, 1) == 4  # undirected


def test_loader_errors(tmp_path):
    bad_header = tmp_path / "bad_header.csv"
    bad_header.write_text("a,b,c\n1,2,3\n")
    with pytest.raises(ValueError):
        load_graph(bad_header)

    bad_row = tmp_path / "bad_row.csv"
    bad_row.write_text("source,target,weight\n1,2\n")
    with pytest.raises(ValueError):
        load_graph(bad_row)

    with pytest.raises(FileNotFoundError):
        load_graph(tmp_path / "missing.csv")
