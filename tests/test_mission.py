
import unittest

from models.mission import Mission
from models.spacecraft import Spacecraft


class TestMission(unittest.TestCase):

    def setUp(self):
        self.mission = Mission(
            "Food Delivery",
            "Earth",
            "Mars",
            "food",
            200,
            50,
            8,
            9,
            ["cargo"]
        )

        self.spacecraft = Spacecraft(
            "Explorer-01",
            "Earth",
            500,
            1000,
            800,
            25,
            0.95,
            150,
            ["cargo"],
            10
        )

    def test_initial_status(self):
        self.assertEqual(self.mission.status, "pending")

    def test_initial_assignment(self):
        self.assertIsNone(self.mission.assigned_spacecraft)

    def test_assign_spacecraft(self):
        self.mission.assign_spacecraft(self.spacecraft, 15)

        self.assertEqual(self.mission.assigned_spacecraft, self.spacecraft)
        self.assertEqual(self.mission.departure_time, 15)
        self.assertEqual(self.mission.status, "assigned")

    def test_complete_mission(self):
        self.mission.complete_mission()

        self.assertEqual(self.mission.status, "completed")

    def test_overdue_mission(self):
        self.assertTrue(self.mission.is_overdue(60))

    def test_mission_not_overdue(self):
        self.assertFalse(self.mission.is_overdue(40))

    def test_completed_mission_not_overdue(self):
        self.mission.complete_mission()

        self.assertFalse(self.mission.is_overdue(60))


if __name__ == "__main__":
    unittest.main()
