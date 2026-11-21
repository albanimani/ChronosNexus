import unittest
from models.dynamic_event import DynamicEvent


class TestDynamicEvent(unittest.TestCase):

    def setUp(self):
        self.event = DynamicEvent(
            "Food Shortage",
            "resource_decrease",
            "Mars",
            "Food production has decreased",
            -60,
            10,
            5
        )

    def test_initial_status(self):
        self.assertEqual(self.event.status, "pending")

    def test_activate_event(self):
        self.event.activate_event()
        self.assertEqual(self.event.status, "active")

    def test_complete_event(self):
        self.event.activate_event()
        self.event.complete_event()
        self.assertEqual(self.event.status, "completed")

    def test_event_is_active(self):
        self.event.activate_event()
        self.assertTrue(self.event.is_active(12))

    def test_event_is_not_active_before_start(self):
        self.event.activate_event()
        self.assertFalse(self.event.is_active(8))

    def test_event_is_not_active_after_duration(self):
        self.event.activate_event()
        self.assertFalse(self.event.is_active(16))

    def test_completed_event_is_not_active(self):
        self.event.activate_event()
        self.event.complete_event()
        self.assertFalse(self.event.is_active(12))


if __name__ == "__main__":
    unittest.main()