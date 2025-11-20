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
        max_duration = max(task.duration for task in self._tasks)
        total_duration = sum(task.duration for task in self._tasks)
        avg_duration = total_duration / self.executor_count

        return float(max(max_duration, avg_duration))

    def __fill_schedule_for_each_executor(self) -> None:
        """Процедура составляет расписание из элементов ScheduleItem для каждого
        исполнителя, на основе исходного списка задач и общей продолжительности
        расписания."""

        current_time = 0.0
        task_idx = 0
        executor_idx = 0

        while task_idx < len(self._tasks):
            task = self._tasks[task_idx]
            remaining_duration = task.duration

            while remaining_duration > 0 and executor_idx < self.executor_count:
                available_time = self._duration - current_time

                if available_time > 0:
                    time_to_assign = min(remaining_duration, available_time)

                    schedule_item = ScheduleItem(
                        task=task,
                        start=current_time,
                        duration=time_to_assign
                    )
                    self._executor_schedule[executor_idx].append(schedule_item)

                    remaining_duration -= time_to_assign
                    current_time += time_to_assign

                    if current_time >= self._duration:
                        executor_idx += 1
                        current_time = 0.0
                else:
                    executor_idx += 1
                    current_time = 0.0

            task_idx += 1

        for idx in range(self.executor_count):
            executor_schedule = self._executor_schedule[idx]
            total_work_time = sum(item.duration for item in executor_schedule if not item.is_downtime)

            if total_work_time < self._duration:
                if executor_schedule:
                    last_end_time = executor_schedule[-1].end
                else:
                    last_end_time = 0.0

                downtime_item = ScheduleItem(
                    task=None,
                    start=last_end_time,
                    duration=self._duration - last_end_time
                )
                self._executor_schedule[idx].append(downtime_item)

    def get_executor_downtime(self, executor_idx: int) -> float:
        total_downtime = 0.0
        for item in self._executor_schedule[executor_idx]:
            if item.is_downtime:
                total_downtime += item.duration
        return total_downtime

    def get_total_downtime(self) -> float:
        total_downtime = 0.0
        for executor_idx in range(self.executor_count):
            total_downtime += self.get_executor_downtime(executor_idx)
        return total_downtime

    def print_downtime_info(self) -> None:
        print("\nИнформация о времени простоя:")
        for executor_idx in range(self.executor_count):
            downtime = self.get_executor_downtime(executor_idx)
            print(f"Исполнитель #{executor_idx + 1}: время простоя = {downtime}")

        total_downtime = self.get_total_downtime()
        print(f"Общее время простоя всех исполнителей: {total_downtime}")


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

    # Информация о времени простоя
    schedule.print_downtime_info()