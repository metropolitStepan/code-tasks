from schedules.abstract_schedule import AbstractSchedule
from schedules.constants import SCHEDULE_STR_TEMPL
from schedules.schedule_item import ScheduleItem
from schedules.task import Task


class Schedule(AbstractSchedule):
    """Класс представляет оптимальное расписание для списка задач и количества
    исполнителей. Для построения расписания используется Ленточная стратегия.

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

    def __init__(self, tasks: list[Task], executor_count: int):
        """Конструктор для инициализации объекта расписания.

        :param tasks: Список задач для составления расписания.
        :param executor_count: Количество исполнителей.
        """
        super().__init__(tasks, executor_count)

        # Рассчитывается и сохраняется минимальная продолжительность расписания
        self._duration = self.__calculate_duration()

        # Формируется расписание для каждого исполнителя
        self.__fill_schedule_for_each_executor()

    @property
    def duration(self) -> float:
        """Возвращает общую продолжительность расписания."""
        return self._duration

    def __calculate_duration(self) -> float:
        """Вычисляет и возвращает минимальную продолжительность расписания."""
        longest = 0
        total = 0

        for task in self._tasks:
            if task.duration > longest:
                longest = task.duration
            total += task.duration

        average = total / self.executor_count
        return float(longest if longest > average else average)

    def __fill_schedule_for_each_executor(self) -> None:
        """Процедура составляет расписание из элементов ScheduleItem для каждого
        исполнителя, на основе исходного списка задач и общей продолжительности
        расписания.
        """
        worker = 0
        offset = 0.0
        idx = 0

        while idx < len(self._tasks):
            task = self._tasks[idx]
            remaining = task.duration

            while remaining > 0 and worker < self.executor_count:
                free_time = self._duration - offset

                if free_time <= 0:
                    worker += 1
                    offset = 0.0
                    continue

                chunk = remaining if remaining < free_time else free_time

                self._executor_schedule[worker].append(
                    ScheduleItem(task=task, start=offset, duration=chunk)
                )

                offset += chunk
                remaining -= chunk

                if offset >= self._duration:
                    worker += 1
                    offset = 0.0

            idx += 1

        # Добавление пустых интервалов до полной длительности
        for w in range(self.executor_count):
            rows = self._executor_schedule[w]
            end_value = rows[-1].end if rows else 0.0

            if end_value < self._duration:
                rows.append(
                    ScheduleItem(task=None, start=end_value, duration=self._duration - end_value)
                )
    def update_tasks(self, new_tasks: list[Task]) -> None:
        """Обновляет список задач и выполняет перерасчёт расписания."""
        self._tasks = tuple(new_tasks)
        self._duration = self.__calculate_duration()

        for i in range(self.executor_count):
            self._executor_schedule[i].clear()

        self.__fill_schedule_for_each_executor()


if __name__ == "__main__":
    print("Пример использования класса Schedule")

    tasks = [
        Task("a", 3),
        Task("b", 4),
        Task("c", 6),
        Task("d", 7),
        Task("e", 7),
        Task("f", 9),
        Task("g", 10),
        Task("h", 12),
        Task("i", 17),
    ]

    schedule = Schedule(tasks, 5)

    print(schedule)
    for i in range(schedule.executor_count):
        print(f"\nРасписание для исполнителя # {i + 1}:")
        for schedule_item in schedule.get_schedule_for_executor(i):
            print(schedule_item)
