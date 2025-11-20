from schedules.abstract_schedule import AbstractSchedule
from schedules.errors import (
    ScheduleArgumentError,
    ErrorMessages,
    ErrorTemplates,
)
from schedules.staged_task import StagedTask
from schedules.schedule_item import ScheduleItem
from datetime import datetime, timedelta

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

    @property
    def duration(self) -> float:
        """Возвращает общую продолжительность расписания."""
        return self._executor_schedule[1][-1].end

    def __str__(self) -> str:
        return (
        "Расписание продолжительностью {0}, количество задач {1} "
        "количество исполнителей {2}".format(
            int(self.duration),  
            self.task_count,
            self.executor_count
        )
    )


    def to_mermaid_gantt(self) -> str:
        """Возвращает строку с диаграммой Ганта в формате Mermaid."""
        base_date = datetime(2025, 1, 1)
        lines = [
            "gantt",
            "    title Расписание по алгоритму Джонсона",
            "    dateFormat  YYYY-MM-DD",
            "    excludes weekdays"
        ]

        lines.append("    section Исполнитель 1")
        for item in self._executor_schedule[0]:
            if item.is_downtime:
                continue
            start_date = base_date + timedelta(days=int(round(item.start)))
            duration_days = int(round(item.duration))
            task_name = item.task_name
            safe_id = task_name.replace(" ", "_") + "_A"
            lines.append(f"    {task_name} :{safe_id}, {start_date.strftime('%Y-%m-%d')}, {duration_days}d")

        lines.append("    section Исполнитель 2")
        for item in self._executor_schedule[1]:
            if item.is_downtime:
                continue
            start_date = base_date + timedelta(days=int(round(item.start)))
            duration_days = int(round(item.duration))
            task_name = item.task_name
            safe_id = task_name.replace(" ", "_") + "_B"
            lines.append(f"    {task_name} :{safe_id}, {start_date.strftime('%Y-%m-%d')}, {duration_days}d")

        return "\n".join(lines)

    def __fill_schedule(self, tasks: list[StagedTask]) -> None:
        """Процедура составляет расписание из элементов ScheduleItem для каждого
        исполнителя, согласно алгоритму Джонсона."""
        without_downtime_A = []
        without_downtime_B = []

        time_A = 0.0
        time_B = 0.0

        for task in tasks:
            start_A = time_A
            end_A = time_A + task.stage_durations[0]
            time_A = end_A
            without_downtime_A.append((task, start_A, end_A))
            
            start_B = max(time_B, end_A)
            end_B = start_B + task.stage_durations[1]
            time_B = end_B
            without_downtime_B.append((task, start_B, end_B))

        schedule_A = []
        current = 0.0
        for task, start, end in without_downtime_A:
            if current < start:
                schedule_A.append(ScheduleItem(None, current, start - current))
            schedule_A.append(ScheduleItem(task, start, end - start))
            current = end
        if current < time_B:
            schedule_A.append(ScheduleItem(None, current, time_B - current))

        schedule_B = []
        current = 0.0
        for task, start, end in without_downtime_B:
            if current < start:
                schedule_B.append(ScheduleItem(None, current, start - current))
            schedule_B.append(ScheduleItem(task, start, end - start))
            current = end
        if current < time_B:
            schedule_B.append(ScheduleItem(None, current, time_B - current))

        self._executor_schedule = [tuple(schedule_A), tuple(schedule_B)]
        

    @staticmethod
    def __sort_tasks(tasks: list[StagedTask]) -> list[StagedTask]:
        """Возвращает отсортированный список задач для применения
        алгоритма Джонсона."""
        group1 = []
        group2 = []

        for task in tasks:
            if task.stage_durations[0] <= task.stage_durations[1]:
                group1.append(task)
            else:
                group2.append(task)
        
        group1.sort(key=lambda task: task.stage_durations[0])
        group2.sort(key=lambda task: task.stage_durations[1],reverse=True)

        return group1 + group2
        

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
            
    print("\nДиаграмма Ганта (Mermaid):")
    print(schedule.to_mermaid_gantt())