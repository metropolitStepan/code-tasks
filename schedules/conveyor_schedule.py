from schedules.abstract_schedule import AbstractSchedule
from schedules.errors import (
    ScheduleArgumentError,
    ErrorMessages,
    ErrorTemplates,
)
from schedules.staged_task import StagedTask
from schedules.schedule_item import ScheduleItem


class ConveyorSchedule(AbstractSchedule):
    """Класс представляет оптимальное расписание для списка задач, состоящих
     из двух этапов и двух исполнителей. Для построения расписания используется
     алгоритм Джонсона.

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

    def __init__(self, tasks: list[StagedTask]):
        """Конструктор для инициализации объекта расписания.

        :param tasks: Список задач для составления расписания.
        :raise ScheduleArgumentError: Если список задач предоставлен в
        некорректном формате или количество этапов для какой-либо задачи не
        равно двум.
        """
        ConveyorSchedule.__validate_params(tasks)
        super().__init__(tasks, 2)

        # Процедура заполняет пустую заготовку расписания для каждого
        # исполнителя объектами ScheduleItem.
        self.__fill_schedule(ConveyorSchedule.__sort_tasks(tasks))

    def reset_tasks(self, tasks: list[StagedTask]) -> None:
        """Изменяет состав задач расписания и полностью пересчитывает его"""
        ConveyorSchedule.__validate_params(tasks)
        self._tasks = tasks
        self.__rebuild_schedule()

    def __rebuild_schedule(self) -> None:
        """Переинициализирует внутреннее расписание на основе текущих задач"""
        self._executor_schedule = [[] for _ in range(self.executor_count)]
        sorted_tasks = ConveyorSchedule.__sort_tasks(self._tasks)
        self.__fill_schedule(sorted_tasks)

    @property
    def duration(self) -> float:
        """Возвращает общую продолжительность расписания."""
        return self._executor_schedule[0][-1].end

    def __fill_schedule(self, tasks: list[StagedTask]) -> None:
        """Процедура составляет расписание из элементов ScheduleItem для каждого
        исполнителя, согласно алгоритму Джонсона."""
        exec1 = self._executor_schedule[0]
        exec2 = self._executor_schedule[1]

        finish1 = 0
        finish2 = 0

        for task in tasks:
            first_duration = task.stage_duration(0)
            second_duration = task.stage_duration(1)
            # первый исполнитель без дыр
            start1 = finish1
            exec1.append(ScheduleItem(task, start1, first_duration))
            finish1 = start1 + first_duration
            ready_time = finish1

            # 2 исполнитель, только после окончания 1 и закончил прошлую задачу
            if ready_time >= finish2:
                start2 = ready_time
            else:
                start2 = finish2

            # простой 2
            idle_time = start2 - finish2
            if idle_time > 0:
                exec2.append(ScheduleItem(None, finish2, idle_time))

            exec2.append(ScheduleItem(task, start2, second_duration))
            finish2 = start2 + second_duration

        total_time = finish2

        if finish1 < total_time:
            exec1.append(ScheduleItem(None, finish1, total_time - finish1))

    @staticmethod
    def __sort_tasks(tasks: list[StagedTask]) -> list[StagedTask]:
        """Возвращает отсортированный список задач для применения
        алгоритма Джонсона."""
        first_tasks: list[StagedTask] = []
        last_tasks: list[StagedTask] = []

        for job in tasks:
            a_i = job.stage_duration(0)
            b_i = job.stage_duration(1)
            if a_i <= b_i:
                first_tasks.append(job)
            else:
                last_tasks.append(job)

        first_tasks.sort(key=lambda work: work.stage_duration(0))
        last_tasks.sort(key=lambda work: work.stage_duration(1), reverse=True)

        return first_tasks + last_tasks

    @staticmethod
    def __validate_params(tasks: list[StagedTask]) -> None:
        """Проводит валидацию входящих параметров для инициализации объекта
        класса ConveyorSchedule."""
        if not isinstance(tasks, list):
            raise ScheduleArgumentError(ErrorMessages.TASKS_NOT_LIST)
        if len(tasks) < 1:
            raise ScheduleArgumentError(ErrorMessages.TASKS_EMPTY_LIST)
        for idx, value in enumerate(tasks):
            if not isinstance(value, StagedTask):
                raise ScheduleArgumentError(ErrorTemplates.INVALID_TASK.format(idx))
            if value.stage_count != 2:
                raise ScheduleArgumentError(
                    ErrorTemplates.INVALID_STAGE_CNT.format(idx)
                )


if __name__ == "__main__":
    print("Пример использования класса ConveyorSchedule")

    # Инициализируем входные данные для составления расписания
    tasks = [
        StagedTask("a", [7, 2]),
        StagedTask("b", [3, 4]),
        StagedTask("c", [2, 5]),
        StagedTask("d", [4, 1]),
        StagedTask("e", [6, 6]),
        StagedTask("f", [5, 3]),
        StagedTask("g", [4, 5]),
    ]

    # Инициализируем экземпляр класса Schedule
    # при этом будет рассчитано расписание для каждого исполнителя
    schedule = ConveyorSchedule(tasks)

    # Выведем в консоль полученное расписание
    print(schedule)
    for i in range(schedule.executor_count):
        print(f"\nРасписание для исполнителя # {i + 1}:")
        for schedule_item in schedule.get_schedule_for_executor(i):
            print(schedule_item)
