from copy import deepcopy

import networkx as nx

UNDISCOVERED = 1
DISCOVERED = 2
PROCESSED = 3


class GraphValidator:
    """Класс для проверки графа на соответствие различным условиям.

    Methods
    -------
    is_inverted_trees(graph: nx.Graph) -> bool:
        Проверяет является ли граф обратно ориентированным деревом или
        лесом из обратно ориентированных деревьев.

    has_loop(graph: nx.Graph) -> bool:
        Проверяет наличие цикла в графе.

    get_component_count(graph: nx.Graph) -> int:
        Возвращает количество компонентов связности в графе.
    """

    @staticmethod
    def is_inverted_trees(graph: nx.Graph) -> bool:
        """Проверяет является ли граф обратно ориентированным деревом или
        лесом из обратно ориентированных деревьев."""
        return True  # Удалить при реализации метода

    @staticmethod
    def has_loop(graph: nx.Graph) -> bool:
        """Проверяет наличие цикла в графе."""
        return False  # Удалить при реализации метода

    @staticmethod
    def get_component_count(graph: nx.Graph) -> int:
        """Возвращает количество компонентов связности в графе."""
        raise NotImplementedError()  # Удалить при реализации метода


if __name__ == "__main__":
    graph = nx.DiGraph()
    graph.add_nodes_from(["a", "b", "c", "d"])
    graph.add_edges_from([("c", "b"), ("b", "a")])
    matrix = nx.adjacency_matrix(graph).toarray()
    print("Матрица смежности для графа:")
    print(matrix)
    print(
        "Граф является обратно ориентированным деревом/лесом:",
        GraphValidator.is_inverted_trees(graph),
    )
    print("Количество деревьев в графе:", GraphValidator.get_component_count(graph))
    print("Граф содержит петли:", GraphValidator.has_loop(graph))

    graph_with_loop = nx.DiGraph()
    graph_with_loop.add_nodes_from(["a", "b", "c", "d"])
    graph_with_loop.add_edges_from([("a", "b"), ("b", "c"), ("c", "d"), ("d", "a")])
    matrix = nx.adjacency_matrix(graph_with_loop).toarray()
    print("\nМатрица смежности для графа:")
    print(matrix)
    print("Граф содержит петли:", GraphValidator.has_loop(graph_with_loop))
