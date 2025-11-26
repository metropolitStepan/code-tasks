from unittest import TestLoader, TestSuite, TextTestRunner

from graphs.tests.test_graph_generator import TestGraphGenerator
from graphs.tests.test_graph_validator import TestGraphValidator
from schedules.tests.test_schedule import TestLevelSchedule
from schedules.tests.test_schedule_item import TestScheduleItem
from schedules.tests.test_task import TestTask


def suite():
    """Создает набор тест-кейсов для тестирования модуля Расписания."""
    test_suite = TestSuite()
    test_suite.addTest(TestLoader().loadTestsFromTestCase(TestTask))
    test_suite.addTest(TestLoader().loadTestsFromTestCase(TestScheduleItem))
    test_suite.addTest(TestLoader().loadTestsFromTestCase(TestLevelSchedule))
    test_suite.addTest(TestLoader().loadTestsFromTestCase(TestGraphValidator))
    test_suite.addTest(TestLoader().loadTestsFromTestCase(TestGraphGenerator))
    return test_suite


if __name__ == "__main__":
    runner = TextTestRunner(verbosity=2)
    runner.run(suite())
