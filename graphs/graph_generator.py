import random as rnd

import matplotlib

from graphs.errors.error_messages import ErrorMessages

matplotlib.use("QtAgg")

import matplotlib.pyplot as plt
import networkx as nx

from graphs.constants import CHARS


class GraphGenerator:
    """Класс для генерации графа.

    Methods
    -------
    generate_random_forest(tree_count: int = 3, vertex_count: int = 15)\
            -> nx.Graph:
        Возвращает случайно сгенерированный граф, представляющий собой
        лес из обратно ориентированных деревьев.

    show_plot(graph: nx.Graph) -> None:
        Выводит изображение графа.
    """

    @staticmethod
    def generate_random_graph(
        conn_component_count: int = 3, vertex_count: int = 15
    ) -> nx.Graph:
        """Возвращает случайно сгенерированный граф, представляющий собой
        лес из обратно ориентированных деревьев. Названия вершин уникальны
        и состоят из латинских букв. Вершины, относящиеся к одному дереву,
        имеют одинаковый цвет.

        :param tree_count: Количество деревьев в графе.
        :param vertex_count:Количество вершин в графе.
        :raises TypeError: Если количество вершин или количество деревьев
        не являются целыми числами.
        :raises ValueError: Если количество вершин или количество деревьев
        меньше единицы, если количество вершин меньше чем количество деревьев.
        :return: Граф.
        """
        GraphGenerator.__validate_params(conn_component_count, vertex_count)
        graph = nx.DiGraph()
        names = GraphGenerator.__generate_names(vertex_count)
        colors = GraphGenerator.__generate_colors(conn_component_count)
        vertices_by_components = GraphGenerator.__get_distributed_vertices(
            names, conn_component_count
        )
        GraphGenerator.__add_nodes_to_graph(graph, vertices_by_components, colors)
        GraphGenerator.__add_edges_to_graph(graph, vertices_by_components)
        return graph

    @staticmethod
    def show_plot(graph: nx.Graph) -> None:
        """Выводит изображение графа."""
        color_map = [graph.nodes[name]["color"] for name in graph.nodes]
        nx.draw_planar(graph, with_labels=True, node_color=color_map)
        plt.show()

    @staticmethod
    def __add_nodes_to_graph(
        graph: nx.DiGraph, vertices_by_trees: list[list[str]], colors: list[str]
    ) -> None:
        raise NotImplementedError()  # Удалить при реализации метода

    @staticmethod
    def __add_edges_to_graph(
        graph: nx.DiGraph, vertices_by_trees: list[list[str]]
    ) -> None:
        raise NotImplementedError()  # Удалить при реализации метода

    @staticmethod
    def __get_distributed_vertices(names: list[str], conn_component_count: int):
        raise NotImplementedError()  # Удалить при реализации метода

    @staticmethod
    def __generate_names(count: int) -> list[str]:
        base = len(CHARS)
        names = []
        for number in range(count):
            name = []
            if number == 0:
                name = [CHARS[0]]
            while number > 0:
                name.append(CHARS[number % base])
                number //= base
            names.append("".join(name[::-1]))
        rnd.shuffle(names)
        return names

    @staticmethod
    def __generate_colors(count: int) -> list[str]:
        chars = "ABCDEF0123456789"
        chars_in_color = 6
        colors = []
        for _ in range(count):
            color = "#" + "".join([rnd.choice(chars) for _ in range(chars_in_color)])
            colors.append(color)
        return colors

    @staticmethod
    def __validate_params(conn_component_count: int, vertex_count: int) -> None:
        """Проводит валидацию входящих параметров для генерации графа."""
        if not isinstance(conn_component_count, int):
            raise TypeError(ErrorMessages.NOT_INT_COMP_CNT)
        if conn_component_count < 1:
            raise ValueError(ErrorMessages.LESS_THAN_1_COMP_CNT)
        if not isinstance(vertex_count, int):
            raise TypeError(ErrorMessages.NOT_INT_VERTEX_CNT)
        if vertex_count < 1:
            raise ValueError(ErrorMessages.LESS_THAN_1_VERTEX_CNT)
        if conn_component_count > vertex_count:
            raise ValueError(ErrorMessages.VERTEX_CNT_LESS_THAN_COMP_CNT)


if __name__ == "__main__":
    graph = GraphGenerator.generate_random_graph(3, 20)
    GraphGenerator.show_plot(graph)
