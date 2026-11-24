import unittest

from models.galaxy import Galaxy
from models.planet import Planet
from models.route import Route
from models.mission import Mission
from models.spacecraft import Spacecraft

from algorithms.mission_scheduling import (
    calculate_mission_route,
    is_spacecraft_suitable,
    schedule_mission,
    schedule_missions
)

class TestMissionScheduling(unittest.TestCase):

    def setUp(self):
        self.galaxy = Galaxy()

        self.earth = Planet(
            "Earth", 100, {"food": 100}, {"food": 70},
            {}, 500, 5, 3, 8, 0, 0
        )

        self.mars = Planet(
            "Mars", 80, {"food": 40}, {"food": 60},
            {}, 400, 4, 2, 6, 10, 0
        )

        self.galaxy.add_planet(self.earth)
        self.galaxy.add_planet(self.mars)

        self.mission = Mission(
            "Food Delivery",
            "Earth",
            "Mars",
            "food",
            20,
            100,
            1,
            8,
            []
        )

    def test_calculate_mission_route(self):
        route = Route(
            "Earth", "Mars", 10, 2, 5, 0.1, 100, 0.9, True
        )

        self.galaxy.add_route(route)

        result = calculate_mission_route(
            self.galaxy, self.mission
        )

        self.assertEqual(result["path"], ["Earth", "Mars"])
        self.assertEqual(result["total_fuel"], 5)
        self.assertAlmostEqual(result["total_time"], 2.2222222222)

    def test_no_available_route(self):
        result = calculate_mission_route(
            self.galaxy, self.mission
        )

        self.assertIsNone(result)
    def test_spacecraft_suitable(self):
        spacecraft = Spacecraft(
            "Explorer",
            "Earth",
            100,
            200,
            150,
            10,
            0.95,
            50,
            [],
            0
        )

        route_info = {
            "path": ["Earth", "Mars"],
            "total_cost": 20,
            "total_fuel": 50,
            "total_time": 5
        }

        result = is_spacecraft_suitable(
            spacecraft,
            self.mission,
            route_info,
            10
        )

        self.assertTrue(result)
    def test_schedule_mission(self):
        route = Route(
            "Earth", "Mars", 10, 2, 5, 0.1, 100, 0.9, True
        )

        spacecraft = Spacecraft(
            "Explorer",
            "Earth",
            100,
            200,
            150,
            10,
            0.95,
            50,
            [],
            0
        )

        self.galaxy.add_route(route)
        self.galaxy.add_spacecraft(spacecraft)

        result = schedule_mission(
            self.galaxy,
            self.mission,
            10
        )

        self.assertEqual(result["spacecraft"], "Explorer")
        self.assertEqual(result["route"], ["Earth", "Mars"])
        self.assertEqual(result["departure_time"], 10)
        self.assertAlmostEqual(result["arrival_time"], 12.2222222222)
        self.assertEqual(self.mission.status, "assigned")
    def test_schedule_multiple_missions_by_priority(self):
        second_mission = Mission(
            "Medicine Delivery",
            "Mars",
            "Earth",
            "medicine",
            10,
            50,
            3,
            9,
            []
        )

        earth_to_mars = Route(
            "Earth", "Mars", 10, 2, 5, 0.1, 100, 0.9, True
        )

        mars_to_earth = Route(
            "Mars", "Earth", 10, 2, 5, 0.1, 100, 0.9, True
        )

        explorer = Spacecraft(
            "Explorer", "Earth", 100, 200, 150,
            10, 0.95, 50, [], 0
        )

        voyager = Spacecraft(
            "Voyager", "Mars", 100, 200, 150,
            10, 0.95, 40, [], 0
        )

        self.galaxy.add_route(earth_to_mars)
        self.galaxy.add_route(mars_to_earth)
        self.galaxy.add_spacecraft(explorer)
        self.galaxy.add_spacecraft(voyager)

        results = schedule_missions(
            self.galaxy,
            [self.mission, second_mission],
            10
        )

        self.assertEqual(
            [result["mission"] for result in results],
            ["Medicine Delivery", "Food Delivery"]
        )
    def test_schedule_mission_without_enough_fuel(self):
        route = Route(
            "Earth", "Mars", 10, 2, 100, 0.1, 100, 0.9, True
        )

        spacecraft = Spacecraft(
            "Explorer",
            "Earth",
            100,
            200,
            20,
            10,
            0.95,
            50,
            [],
            0
        )

        self.galaxy.add_route(route)
        self.galaxy.add_spacecraft(spacecraft)

        result = schedule_mission(
            self.galaxy,
            self.mission,
            10
        )

        self.assertIsNone(result)
    def test_schedule_mission_without_enough_capacity(self):
        route = Route(
            "Earth", "Mars", 10, 2, 5, 0.1, 100, 0.9, True
        )

        spacecraft = Spacecraft(
            "Explorer",
            "Earth",
            10,
            200,
            150,
            10,
            0.95,
            50,
            [],
            0
        )

        self.galaxy.add_route(route)
        self.galaxy.add_spacecraft(spacecraft)

        result = schedule_mission(
            self.galaxy,
            self.mission,
            10
        )

        self.assertIsNone(result)
    def test_schedule_mission_without_required_capabilities(self):
        route = Route(
            "Earth", "Mars", 10, 2, 5, 0.1, 100, 0.9, True
        )

        spacecraft = Spacecraft(
            "Explorer",
            "Earth",
            100,
            200,
            150,
            10,
            0.95,
            50,
            [],
            0
        )

        self.mission.required_capabilities = ["medical"]

        self.galaxy.add_route(route)
        self.galaxy.add_spacecraft(spacecraft)

        result = schedule_mission(
            self.galaxy,
            self.mission,
            10
        )

        self.assertIsNone(result)
    def test_schedule_mission_after_deadline(self):
        route = Route(
            "Earth", "Mars", 10, 200, 5, 0.1, 100, 0.9, True
        )

        spacecraft = Spacecraft(
            "Explorer",
            "Earth",
            100,
            200,
            150,
            10,
            0.95,
            50,
            [],
            0
        )

        self.galaxy.add_route(route)
        self.galaxy.add_spacecraft(spacecraft)

        result = schedule_mission(
            self.galaxy,
            self.mission,
            10
        )

        self.assertIsNone(result)
    def test_schedule_mission_rejected_due_to_low_reliability(self):
        route = Route(
            "Earth", "Mars", 10, 2, 5, 0.1, 100, 0.5, True
        )

        spacecraft = Spacecraft(
            "Explorer",
            "Earth",
            100,
            200,
            150,
            10,
            0.95,
            50,
            [],
            0
        )

        self.mission.deadline = 13

        self.galaxy.add_route(route)
        self.galaxy.add_spacecraft(spacecraft)

        result = schedule_mission(
            self.galaxy,
            self.mission,
            10
        )

        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()

