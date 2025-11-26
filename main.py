import networkx as nx

from graphs import GraphGenerator, GraphValidator
from schedules import LexicSchedule


def main():
    print("Пример использования класса GraphGenerator")

    graph = GraphGenerator.generate_random_graph(3, 18)
    GraphGenerator.show_plot(graph)

    print("Пример использования класса GraphValidator")
    matrix = nx.adjacency_matrix(graph).toarray()
    print("Матрица смежности для графа:")
    print(matrix)
    print(
        "Список транзитивных ребер:",
        GraphValidator.get_transitive_edges(graph),
    )
    print("Количество компонентов в графе:", GraphValidator.get_component_count(graph))
    print("Граф содержит петли:", GraphValidator.has_loop(graph))

    print("Пример использования класса Schedule")

    # Инициализируем экземпляр класса Schedule
    # при этом будет рассчитано расписание для каждого исполнителя
    schedule = LexicSchedule(graph)

    # Выведем в консоль полученное расписание
    print(schedule)
    for i in range(schedule.executor_count):
        print(f"\nРасписание для исполнителя # {i + 1}:")
        for schedule_item in schedule.get_schedule_for_executor(i):
            print(schedule_item)


if __name__ == "__main__":
    main()
