import re
import unittest

import networkx as nx

from graphs.errors.error_messages import ErrorMessages
from graphs.graph_generator import CHARS, GraphGenerator

COLOR = "color"

not_implemented = False
try:
    GraphGenerator.generate_random_graph()
except Exception as e:
    if isinstance(e, NotImplementedError):
        not_implemented = True


@unittest.skipIf(
    not_implemented, "Пропущено, так как класс GraphGenerator не реализован"
)
class TestGraphGenerator(unittest.TestCase):
    def __check_color_cnt(self, graph: nx.DiGraph, comp_cnt):
        """Проверяет соответствие количества цветов вершин количеству
        компонентов в графе."""
        color_set = set()
        for node_name in list(graph.nodes.keys()):
            if COLOR not in graph.nodes[node_name]:
                return False
            color_set.add(graph.nodes[node_name][COLOR])
        return len(color_set) == comp_cnt

    def __check_vertex_names(self, graph: nx.DiGraph):
        """Проверяет корректность наименования вершин графа."""
        pattern = f"^[{CHARS}]+$"
        for node_name in list(graph.nodes.keys()):
            if not re.match(pattern, node_name):
                return False
        return True

    def test_not_int_comp_cnt(self):
        """Проверяет выброс исключения при передаче нечислового значения
        количества компонентов."""
        incorrect_val = [1.1, None, "str", []]
        for val in incorrect_val:
            with self.assertRaises(TypeError) as error:
                GraphGenerator.generate_random_graph(val, 1)
            self.assertEqual(ErrorMessages.NOT_INT_COMP_CNT, str(error.exception))

    def test_less_than_1_comp_cnt(self):
        """Проверяет выброс исключения при передаче некорректного значения
        количества компонентов."""
        incorrect_val = [-1, 0]
        for val in incorrect_val:
            with self.assertRaises(ValueError) as error:
                GraphGenerator.generate_random_graph(val, 1)
            self.assertEqual(ErrorMessages.LESS_THAN_1_COMP_CNT, str(error.exception))

    def test_not_int_vertex_cnt(self):
        """Проверяет выброс исключения при передаче нечислового значения
        количества вершин."""
        incorrect_val = [1.1, None, "str", []]
        for val in incorrect_val:
            with self.assertRaises(TypeError) as error:
                GraphGenerator.generate_random_graph(1, val)
            self.assertEqual(ErrorMessages.NOT_INT_VERTEX_CNT, str(error.exception))

    def test_less_than_1_vertex_cnt(self):
        """Проверяет выброс исключения при передаче некорректного значения
        количества вершин."""
        incorrect_val = [-1, 0]
        for val in incorrect_val:
            with self.assertRaises(ValueError) as error:
                GraphGenerator.generate_random_graph(1, val)
            self.assertEqual(ErrorMessages.LESS_THAN_1_VERTEX_CNT, str(error.exception))

    def test_vertex_cnt_less_than_comp_cnt(self):
        """Проверяет выброс исключения при передаче некорректного значения
        количества вершин меньшего чем значение количества компонентов."""
        with self.assertRaises(ValueError) as error:
            GraphGenerator.generate_random_graph(2, 1)
        self.assertEqual(
            ErrorMessages.VERTEX_CNT_LESS_THAN_COMP_CNT, str(error.exception)
        )

    def test_comp1_vertex1(self):
        """Проверяет генерацию графа с одной вершиной."""
        graph = GraphGenerator.generate_random_graph(1, 1)
        self.assertEqual(1, graph.order())

    def test_comp1_vertex2(self):
        """Проверяет генерацию графа с одним компонентом и двумя вершинами."""
        graph = GraphGenerator.generate_random_graph(1, 2)
        self.assertEqual(2, graph.order())
        self.assertEqual(1, len(graph.edges))
        self.assertTrue(self.__check_color_cnt(graph, 1))
        self.assertTrue(self.__check_vertex_names(graph))

    def test_comp1_vertex3(self):
        """Проверяет генерацию графа с одним компонентом и тремя вершинами."""
        graph = GraphGenerator.generate_random_graph(1, 3)
        self.assertEqual(3, graph.order())
        self.assertLessEqual(2, len(graph.edges))
        self.assertTrue(self.__check_color_cnt(graph, 1))
        self.assertTrue(self.__check_vertex_names(graph))

    def test_comp2_vertex2(self):
        """Проверяет генерацию графа с двумя компонентами и двумя вершинами."""
        graph = GraphGenerator.generate_random_graph(2, 2)
        self.assertEqual(2, graph.order())
        self.assertEqual(0, len(graph.edges))
        self.assertTrue(self.__check_color_cnt(graph, 2))
        self.assertTrue(self.__check_vertex_names(graph))

    def test_comp2_vertex3(self):
        """Проверяет генерацию графа с двумя компонентами и тремя вершинами."""
        graph = GraphGenerator.generate_random_graph(2, 3)
        self.assertEqual(3, graph.order())
        self.assertEqual(1, len(graph.edges))
        self.assertTrue(self.__check_color_cnt(graph, 2))
        self.assertTrue(self.__check_vertex_names(graph))

    def test_comp3_vertex3(self):
        """Проверяет генерацию графа с тремя компонентами и тремя вершинами."""
        graph = GraphGenerator.generate_random_graph(3, 3)
        self.assertEqual(3, graph.order())
        self.assertEqual(0, len(graph.edges))
        self.assertTrue(self.__check_color_cnt(graph, 3))
        self.assertTrue(self.__check_vertex_names(graph))

    def test_comp3_vertex4(self):
        """Проверяет генерацию графа с тремя компонентами и четырьмя вершинами."""
        graph = GraphGenerator.generate_random_graph(3, 4)
        self.assertEqual(4, graph.order())
        self.assertLessEqual(1, len(graph.edges))
        self.assertTrue(self.__check_color_cnt(graph, 3))
        self.assertTrue(self.__check_vertex_names(graph))

    def test_comp3_vertex5(self):
        """Проверяет генерацию графа с тремя компонентами и пятью вершинами."""
        graph = GraphGenerator.generate_random_graph(3, 5)
        self.assertEqual(5, graph.order())
        self.assertLessEqual(2, len(graph.edges))
        self.assertTrue(self.__check_color_cnt(graph, 3))
        self.assertTrue(self.__check_vertex_names(graph))

    def test_comp3_vertex6(self):
        """Проверяет генерацию графа с тремя компонентами и шестью вершинами."""
        graph = GraphGenerator.generate_random_graph(3, 6)
        self.assertEqual(6, graph.order())
        self.assertLessEqual(3, len(graph.edges))
        self.assertTrue(self.__check_color_cnt(graph, 3))
        self.assertTrue(self.__check_vertex_names(graph))


if __name__ == "__main__":
    unittest.main()
