import unittest

import networkx as nx

from schedules import ScheduleItem, Task
from schedules.abs_schedule import AbstractSchedule
from schedules.constants import SCHEDULE_STR_TEMPL
from schedules.errors import ScheduleArgumentError
from schedules.errors.error_messages import ErrorMessages
from schedules.lexic_schedule import LexicSchedule

not_implemented = False
try:
    LexicSchedule(None)
except Exception as e:
    if isinstance(e, NotImplementedError):
        not_implemented = True


@unittest.skipIf(
    not_implemented, "Пропущено, так как класс LexicSchedule не реализован"
)
class TestLexicSchedule(unittest.TestCase):
    graph = nx.DiGraph()

    def setUp(self):
        self.graph = nx.DiGraph()

    def __check_schedule(self, schedule: LexicSchedule, graph: nx.Graph):
        """Проверяет корректность составленного расписания"""
        task_names = list(graph.nodes.keys())
        task_start_dict = {}
        for idx in range(schedule.executor_count):
            ex_schedule = schedule.get_schedule_for_executor(idx)
            # расписания для всех исполнителей должны быть одинаковой длины
            if ex_schedule[-1].end != schedule.duration:
                return False
            prev_end = 0
            for row in ex_schedule:
                # Текущее задание должно начинаться в момент окончания
                # предыдущего
                if row.start != prev_end:
                    return False
                prev_end = row.end
                if row.is_downtime:
                    continue
                # Задание должно быть включено в список
                if row.task_name not in task_names:
                    return False
                # Задание должно встречаться в расписании только один раз
                if row.task_name in task_start_dict:
                    return False
                task_start_dict[row.task_name] = row.start
        for src, trg in graph.edges:
            # Дочернее задание должно начинаться после окончания родительского
            if task_start_dict[src] >= task_start_dict[trg]:
                return False
        return True

    def test_class_inheritance(self):
        """Проверяет наследование от класса AbstractSchedule"""
        self.graph.add_nodes_from(["a"])
        schedule = LexicSchedule(self.graph)
        self.assertIsInstance(schedule, AbstractSchedule)

    def test_not_int_executor_idx(self):
        """Проверяет выброс исключения при передаче не корректного индекса
        исполнителя."""
        self.graph.add_nodes_from(["a"])
        schedule = LexicSchedule(self.graph)
        incorrect_idx = [-1, 1.1, None, "str", []]
        for idx in incorrect_idx:
            with self.subTest(idx=idx):
                with self.assertRaises(ScheduleArgumentError) as error:
                    schedule.get_schedule_for_executor(idx)
                self.assertEqual(ErrorMessages.EXECUTOR_NOT_INT, str(error.exception))

    def test_out_of_range_executor_idx(self):
        """Проверяет выброс исключения при передаче не корректного индекса
        исполнителя."""
        self.graph.add_nodes_from(["a"])
        schedule = LexicSchedule(self.graph)
        with self.assertRaises(ScheduleArgumentError) as error:
            schedule.get_schedule_for_executor(2)
        self.assertEqual(ErrorMessages.EXECUTOR_OUT_OF_RANGE, str(error.exception))

    def test_str(self):
        """Проверяет корректность приведения расписания к строковому типу."""
        self.graph.add_nodes_from(["a"])
        schedule = LexicSchedule(self.graph)
        str_schedule = SCHEDULE_STR_TEMPL.format(1, 1, 2)
        self.assertEqual(str_schedule, str(schedule))

    def test_1comp_1task(self):
        """Проверяет расписание для 1 компоненты, 1 задачи."""
        self.graph.add_nodes_from(["a"])
        schedule = LexicSchedule(self.graph)
        task_a = Task("a", 1)
        ex1_schedule = (ScheduleItem(task_a, 0, 1),)
        self.assertEqual(tuple([task_a]), schedule.tasks)
        self.assertEqual(1, schedule.task_count)
        self.assertEqual(1, schedule.duration)
        self.assertEqual(ex1_schedule, schedule.get_schedule_for_executor(0))
        self.assertTrue(self.__check_schedule(schedule, self.graph))

    def test_1comp_2task(self):
        """Проверяет расписание для 1 компоненты, 2 задач."""
        self.graph.add_nodes_from(["a", "b"])
        self.graph.add_edges_from([("b", "a")])
        schedule = LexicSchedule(self.graph)
        task_a = Task("a", 1)
        task_b = Task("b", 1)
        ex1_schedule = (
            ScheduleItem(task_b, 0, 1),
            ScheduleItem(task_a, 1, 1),
        )
        ex2_schedule = (
            ScheduleItem(None, 0, 1),
            ScheduleItem(None, 1, 1),
        )
        self.assertEqual(tuple([task_a, task_b]), schedule.tasks)
        self.assertEqual(2, schedule.task_count)
        self.assertEqual(2, schedule.duration)
        self.assertEqual(ex1_schedule, schedule.get_schedule_for_executor(0))
        self.assertEqual(ex2_schedule, schedule.get_schedule_for_executor(1))
        self.assertTrue(self.__check_schedule(schedule, self.graph))

    def test_1comp_3task(self):
        """Проверяет расписание для 1 компоненты, 3 задач."""
        self.graph.add_nodes_from(["a", "b", "c"])
        self.graph.add_edges_from([("c", "a"), ("b", "a")])
        schedule = LexicSchedule(self.graph)
        task_a = Task("a", 1)
        task_b = Task("b", 1)
        task_c = Task("c", 1)
        self.assertEqual(tuple([task_a, task_b, task_c]), schedule.tasks)
        self.assertEqual(3, schedule.task_count)
        self.assertEqual(2, schedule.duration)
        self.assertTrue(self.__check_schedule(schedule, self.graph))

    def test_1comp_5task(self):
        """Проверяет расписание для 1 компоненты, 5 задач."""
        self.graph.add_nodes_from(["a", "b", "c", "d", "e"])
        self.graph.add_edges_from([("c", "b"), ("b", "a"), ("e", "a"), ("d", "e")])
        schedule = LexicSchedule(self.graph)
        task_a = Task("a", 1)
        task_b = Task("b", 1)
        task_c = Task("c", 1)
        task_d = Task("d", 1)
        task_e = Task("e", 1)
        self.assertEqual(
            tuple([task_a, task_b, task_c, task_d, task_e]), schedule.tasks
        )
        self.assertEqual(5, schedule.task_count)
        self.assertEqual(3, schedule.duration)
        self.assertTrue(self.__check_schedule(schedule, self.graph))

    def test_2comp_2task(self):
        """Проверяет расписание для 2 компонент, 2 задач."""
        self.graph.add_nodes_from(["a", "b"])
        schedule = LexicSchedule(self.graph)
        task_a = Task("a", 1)
        task_b = Task("b", 1)
        self.assertEqual(tuple([task_a, task_b]), schedule.tasks)
        self.assertEqual(2, schedule.task_count)
        self.assertEqual(1, schedule.duration)
        self.assertTrue(self.__check_schedule(schedule, self.graph))

    def test_2comp_5task(self):
        """Проверяет расписание для 2 компонент, 5 задач."""
        self.graph.add_nodes_from(["a", "b", "c", "d", "e"])
        self.graph.add_edges_from([("c", "a"), ("b", "a"), ("e", "d")])
        schedule = LexicSchedule(self.graph)
        task_a = Task("a", 1)
        task_b = Task("b", 1)
        task_c = Task("c", 1)
        task_d = Task("d", 1)
        task_e = Task("e", 1)
        self.assertEqual(
            tuple([task_a, task_b, task_c, task_d, task_e]), schedule.tasks
        )
        self.assertEqual(5, schedule.task_count)
        self.assertEqual(3, schedule.duration)
        self.assertTrue(self.__check_schedule(schedule, self.graph))

    def test_2comp_6task(self):
        """Проверяет расписание для 2 компонент, 6 задач."""
        self.graph.add_nodes_from(["a", "b", "c", "d", "e", "f"])
        self.graph.add_edges_from([("c", "a"), ("b", "a"), ("e", "d"), ("f", "e")])
        schedule = LexicSchedule(self.graph)
        task_a = Task("a", 1)
        task_b = Task("b", 1)
        task_c = Task("c", 1)
        task_d = Task("d", 1)
        task_e = Task("e", 1)
        task_f = Task("f", 1)
        self.assertEqual(
            tuple([task_a, task_b, task_c, task_d, task_e, task_f]), schedule.tasks
        )
        self.assertEqual(6, schedule.task_count)
        self.assertEqual(3, schedule.duration)
        self.assertTrue(self.__check_schedule(schedule, self.graph))

    def test_1comp_12task(self):
        """Проверяет расписание для 1 компоненты, 12 задач."""
        self.graph.add_nodes_from(
            ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l"]
        )
        self.graph.add_edges_from(
            [
                ("d", "e"),
                ("c", "e"),
                ("c", "f"),
                ("e", "h"),
                ("f", "h"),
                ("i", "h"),
                ("i", "l"),
                ("h", "a"),
                ("h", "g"),
                ("l", "g"),
                ("a", "b"),
                ("a", "j"),
                ("g", "j"),
                ("g", "k"),
            ]
        )
        schedule = LexicSchedule(self.graph)
        self.assertEqual(12, schedule.task_count)
        self.assertEqual(7, schedule.duration)
        self.assertTrue(self.__check_schedule(schedule, self.graph))

    def test_3comp_13task(self):
        """Проверяет расписание для 3 компонент, 13 задач."""
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
        schedule = LexicSchedule(self.graph)
        self.assertEqual(13, schedule.task_count)
        self.assertEqual(7, schedule.duration)
        self.assertTrue(self.__check_schedule(schedule, self.graph))

    def test_1comp_13task(self):
        """Проверяет расписание для 1 компоненты, 13 задач."""
        self.graph.add_nodes_from(
            ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m"]
        )
        self.graph.add_edges_from(
            [
                ("b", "e"),
                ("c", "b"),
                ("d", "a"),
                ("e", "a"),
                ("f", "b"),
                ("g", "l"),
                ("h", "l"),
                ("i", "c"),
                ("j", "c"),
                ("k", "d"),
                ("l", "d"),
                ("m", "l"),
            ]
        )
        schedule = LexicSchedule(self.graph)
        self.assertEqual(13, schedule.task_count)
        self.assertEqual(7, schedule.duration)
        self.assertTrue(self.__check_schedule(schedule, self.graph))


if __name__ == "__main__":
    unittest.main()
