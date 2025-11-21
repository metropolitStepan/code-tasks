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
        :raise ScheduleArgumentError: Если список задач предоставлен в
        некорректном формате или количество исполнителей не является целым
        положительным числом.
        """
        super().__init__(tasks, executor_count)

        # Рассчитывается и сохраняется в приватном поле класса минимальная
        # продолжительность расписания
        self._duration = self.__calculate_duration()

        # Процедура заполняет пустую заготовку расписания для каждого
        # исполнителя объектами ScheduleItem.
        self.__fill_schedule_for_each_executor()

    @property
    def duration(self) -> float:
        """Возвращает общую продолжительность расписания."""
        return self._duration

    def __calculate_duration(self) -> float:
        """Вычисляет и возвращает минимальную продолжительность расписания"""
        longest_task = max(t.duration for t in self._tasks)
        sum_of_tasks = sum(t.duration for t in self._tasks)
        mean_duration = sum_of_tasks / self.executor_count

        return float(max(longest_task, mean_duration))

    def __fill_schedule_for_each_executor(self) -> None:
        """Процедура составляет расписание из элементов ScheduleItem для каждого
        исполнителя, на основе исходного списка задач и общей продолжительности
        расписания."""
        
        current_executor = 0
        executor_time = 0.0

        for task in self._tasks:
            task_remaining = task.duration

            while task_remaining > 0:
                time_left = self._duration - executor_time

                if time_left <= 0:
                    current_executor += 1
                    executor_time = 0.0
                    time_left = self._duration

                allocated_time = min(task_remaining, time_left)

                item = ScheduleItem(
                    task=task,
                    start=executor_time,
                    duration=allocated_time
                )
                self._executor_schedule[current_executor].append(item)

                task_remaining -= allocated_time
                executor_time += allocated_time

        self.__add_downtime_to_executors()

    def __add_downtime_to_executors(self) -> None:
        """Добавляет время простоя для всех исполнителей."""
        for executor_num in range(self.executor_count):
            schedule = self._executor_schedule[executor_num]

            if schedule:
                final_time = schedule[-1].end
            else:
                final_time = 0.0

            downtime = self._duration - final_time
            if downtime > 0:
                idle_item = ScheduleItem(
                    task=None,
                    start=final_time,
                    duration=downtime
                )
                self._executor_schedule[executor_num].append(idle_item)


if __name__ == "__main__":
    print("Пример использования класса Schedule")

    # Инициализируем входные данные для составления расписания
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

    # Инициализируем экземпляр класса Schedule
    # при этом будет рассчитано расписание для каждого исполнителя
    schedule = Schedule(tasks, 5)

    # Выведем в консоль полученное расписание
    print(schedule)
    for i in range(schedule.executor_count):
        print(f"\nРасписание для исполнителя # {i + 1}:")
        for schedule_item in schedule.get_schedule_for_executor(i):
            print(schedule_item)
