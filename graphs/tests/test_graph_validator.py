import unittest

import networkx as nx

from graphs.graph_validator import GraphValidator

not_implemented = False
try:
    GraphValidator.get_component_count(None)
except Exception as e:
    if isinstance(e, NotImplementedError):
        not_implemented = True


@unittest.skipIf(
    not_implemented, "Пропущено, так как класс GraphValidator не реализован"
)
class TestGraphValidator(unittest.TestCase):
    graph = nx.DiGraph()

    def setUp(self):
        self.graph = nx.DiGraph()

    def test_get_transitive_edges_1comp_1node(self):
        """Проверка наличия транзитивных ребер в графе из одной вершины."""
        self.graph.add_nodes_from(["a"])
        self.assertEqual([], GraphValidator.get_transitive_edges(self.graph))

    def test_get_comp_count_1comp(self):
        """Проверка подсчета компонент связности для одной компоненты."""
        self.graph.add_nodes_from(["a"])
        self.assertEqual(1, GraphValidator.get_component_count(self.graph))

    def test_graph_has_loop_1comp_1node(self):
        """Проверка отсутствия цикла для графа из одной вершины."""
        self.graph.add_nodes_from(["a"])
        self.assertFalse(GraphValidator.has_loop(self.graph))

    def test_get_transitive_edges_1comp_2node(self):
        """Проверка наличия транзитивных ребер для графа из двух вершин."""
        self.graph.add_nodes_from(["a", "b"])
        self.graph.add_edges_from([("b", "a")])
        self.assertEqual([], GraphValidator.get_transitive_edges(self.graph))

    def test_get_transitive_edges_1comp_3node(self):
        """Проверка наличия транзитивных ребер для графа из трех вершин."""
        self.graph.add_nodes_from(["a", "b", "c"])
        self.graph.add_edges_from([("c", "b"), ("b", "a"), ("c", "a")])
        self.assertEqual([("c", "a")], GraphValidator.get_transitive_edges(self.graph))

    def test_get_transitive_edges_2comp_2node(self):
        """Проверка наличия транзитивных ребер в графе из двух компонент и двух вершин."""
        self.graph.add_nodes_from(["a", "b"])
        self.assertEqual([], GraphValidator.get_transitive_edges(self.graph))

    def test_get_comp_count_2comp(self):
        """Проверка подсчета компонент связности для двух компонент."""
        self.graph.add_nodes_from(["a", "b"])
        self.assertEqual(2, GraphValidator.get_component_count(self.graph))

    def test_get_transitive_edges_2comp_5node(self):
        """Проверка наличия транзитивных ребер в графе с двумя компонентами и пятью вершинами."""
        self.graph.add_nodes_from(["a", "b", "c", "d", "e"])
        self.graph.add_edges_from([("c", "a"), ("c", "b"), ("b", "a"), ("e", "d")])
        self.assertEqual([("c", "a")], GraphValidator.get_transitive_edges(self.graph))

    def test_graph_has_loop_2comp_5node(self):
        """Проверка отсутствия цикла в графе с двумя компонентами и пятью вершинами."""
        self.graph.add_nodes_from(["a", "b", "c", "d", "e"])
        self.graph.add_edges_from([("c", "a"), ("b", "a"), ("e", "d")])
        self.assertFalse(GraphValidator.has_loop(self.graph))

    def test_get_transitive_edges_3comp_13node_true(self):
        """Проверка наличия транзитивных ребер (есть) в графе из трех компонент и тринадцати вершин."""
        self.graph.add_nodes_from(
            ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m"]
        )
        self.graph.add_edges_from(
            [
                ("d", "a"),
                ("j", "d"),
                ("e", "b"),
                ("k", "b"),
                ("f", "b"),
                ("k", "e"),
                ("g", "c"),
                ("h", "c"),
                ("i", "c"),
                ("l", "g"),
                ("m", "l"),
                ("m", "c"),
            ]
        )
        self.assertEqual(
            set([("k", "b"), ("m", "c")]),
            set(GraphValidator.get_transitive_edges(self.graph)),
        )

    def test_get_transitive_edges_3comp_13node_false(self):
        """Проверка наличия транзитивных ребер (нет) в графе из трех компонент и тринадцати вершин."""
        self.graph.add_nodes_from(
            ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m"]
        )
        self.graph.add_edges_from(
            [
                ("d", "a"),
                ("j", "d"),
                ("e", "b"),
                ("f", "b"),
                ("k", "e"),
                ("g", "c"),
                ("h", "c"),
                ("i", "c"),
                ("l", "g"),
                ("m", "l"),
            ]
        )
        self.assertEqual([], GraphValidator.get_transitive_edges(self.graph))

    def test_get_comp_count_3comp(self):
        """Проверка подсчета компонент связности для графа из трех компонент."""
        self.graph.add_nodes_from(
            ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m"]
        )
        self.graph.add_edges_from(
            [
                ("d", "a"),
                ("j", "d"),
                ("e", "b"),
                ("f", "b"),
                ("k", "e"),
                ("g", "c"),
                ("h", "c"),
                ("i", "c"),
                ("l", "g"),
                ("m", "g"),
            ]
        )
        self.assertEqual(3, GraphValidator.get_component_count(self.graph))

    def test_graph_has_loop_3comp_13node(self):
        """Проверка отсутствия цикла для графа из трех компонент и тринадцати вершин."""
        self.graph.add_nodes_from(
            ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m"]
        )
        self.graph.add_edges_from(
            [
                ("d", "a"),
                ("j", "d"),
                ("e", "b"),
                ("f", "b"),
                ("k", "e"),
                ("g", "c"),
                ("h", "c"),
                ("i", "c"),
                ("l", "g"),
                ("m", "g"),
            ]
        )
        self.assertFalse(GraphValidator.has_loop(self.graph))

    def test_graph_has_loop_3comp_13node_true(self):
        """Наличие цикла в графе из трех компонент и тринадцати вершин."""
        self.graph.add_nodes_from(
            ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m"]
        )
        self.graph.add_edges_from(
            [
                ("d", "a"),
                ("j", "d"),
                ("e", "b"),
                ("f", "b"),
                ("k", "e"),
                ("g", "c"),
                ("h", "c"),
                ("i", "c"),
                ("l", "g"),
                ("m", "g"),
                ("l", "n"),
                ("c", "l"),
            ]
        )
        self.assertTrue(GraphValidator.has_loop(self.graph))

    def test_graph_has_loop_1comp_3node_true(self):
        """Наличие цикла в связном графе из трех вершин"""
        self.graph.add_nodes_from(["a", "b", "c"])
        self.graph.add_edges_from([("a", "b"), ("b", "c"), ("c", "a")])
        self.assertTrue(GraphValidator.has_loop(self.graph))

    def test_graph_has_loop_2comp_5node_true(self):
        """Наличие цикла в графе из пяти вершин и двух компонент связности."""
        self.graph.add_nodes_from(["a", "b", "c", "d", "e"])
        self.graph.add_edges_from([("c", "b"), ("b", "a"), ("a", "c"), ("e", "d")])
        self.assertTrue(GraphValidator.has_loop(self.graph))


if __name__ == "__main__":
    unittest.main()
