from collections import namedtuple
from copy import deepcopy

import networkx as nx

from graphs.graph_validator import GraphValidator
from schedules.abs_schedule import AbstractSchedule
from schedules.errors import ScheduleArgumentError
from schedules.schedule_item import ScheduleItem
from schedules.task import Task

Candidate = namedtuple("Candidate", ["idx", "child_priorities"])


class LexicSchedule(AbstractSchedule):
    """Класс представляет оптимальное расписание для списка задач. Все задачи
    единичной длительности и могут зависеть друг от друга. Для построения
    расписания используется лексикографическая стратегия.

    Properties
    ----------
    tasks(self) -> tuple[Task]:
        Возвращает исходный список задач для составления расписания.

    task_count(self) -> int:
        Возвращает количество задач для составления расписания.

    executor_count(self) -> int:
        Возвращает количество исполнителей.

    duration(self) -> float:
        Возвращает общую продолжительность расписания.

    Methods
    -------
    get_schedule_for_executor(self, executor_idx: int) -> tuple[ScheduleRow]:
        Возвращает расписание для указанного исполнителя.
    """

    def __init__(self, graph: nx.Graph):
        """Конструктор для инициализации объекта расписания.

        :param graph: Граф, представляющий зависимость между задачами.
        """
        # Удалить выброс исключения при разработке методов этого класса!!!
        raise NotImplementedError()

        if GraphValidator.has_loop(graph):
            raise ScheduleArgumentError("Граф содержит цикл")

        self.__graph = graph

        transitive_edges = GraphValidator.get_transitive_edges(graph)
        if transitive_edges:
            graph_without_transitive_edges = deepcopy(graph)
            for edge in transitive_edges:
                graph_without_transitive_edges.remove_edge(*edge)
            self.__matrix = (
                nx.adjacency_matrix(graph_without_transitive_edges)
            ).toarray()
        else:
            self.__matrix = (nx.adjacency_matrix(graph)).toarray()

        super().__init__(self.__get_tasks_from_graph(), 2)
        self.__fill_schedule()

    @property
    def duration(self) -> float:
        """Возвращает общую продолжительность расписания."""
        return self._executor_schedule[0][-1].end

    def __get_tasks_from_graph(self):
        """Возвращает список задач на основе вершин графа."""
        return [Task(node_name, 1) for node_name in list(self.__graph.nodes.keys())]

    def __fill_schedule(self) -> None:
        """Заполняет расписание для исполнителей согласно лексикографической стратегии"""
        pass

    def __get_sink_idxs(self):
        """Возвращает список индексов вершин, которые являются стоками графа."""
        pass

    def __get_src_idxs(self, trg_idx):
        """Возвращает список индексов вершин, которые соединены с заданными."""
        pass

    def __get_child_priorities(self, src_idx, vertex_priorities):
        """Возвращает список приоритетов вершин потомков заданной вершины."""
        pass


if __name__ == "__main__":
    print("Пример использования класса Schedule")

    # Инициализируем входные данные для составления расписания
    graph = nx.DiGraph()
    graph.add_nodes_from(["a", "b", "c", "d", "e", "f", "g"])
    graph.add_edges_from(
        [
            ("g", "e"),
            ("a", "e"),
            ("c", "g"),
            ("c", "a"),
            ("b", "c"),
            ("d", "c"),
            ("f", "c"),
        ]
    )

    # Пример с транзитивными ребрами
    # graph = nx.DiGraph()
    # graph.add_nodes_from(["a", "b", "c", "d", "e", "f"])
    # graph.add_edges_from(
    #     [
    #         ("c", "a"),
    #         ("d", "c"),
    #         ("d", "a"),
    #         ("d", "b"),
    #         ("e", "c"),
    #         ("e", "a"),
    #         ("e", "b"),
    #         ("f", "d"),
    #     ]
    # )

    # Инициализируем экземпляр класса Schedule
    # при этом будет рассчитано расписание для каждого исполнителя
    schedule = LexicSchedule(graph)

    # Выведем в консоль полученное расписание
    print(schedule)
    for i in range(schedule.executor_count):
        print(f"\nРасписание для исполнителя # {i + 1}:")
        for schedule_item in schedule.get_schedule_for_executor(i):
            print(schedule_item)
