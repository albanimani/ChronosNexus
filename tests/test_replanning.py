import unittest

from models.galaxy import Galaxy
from models.route import Route
from simulation.replanning import find_unavailable_routes
from models.planet import Planet
from models.mission import Mission
from simulation.replanning import replan_mission_route
from simulation.replanning import is_plan_affected


class TestReplanning(unittest.TestCase):

    def setUp(self):
        self.galaxy = Galaxy()

        self.route = Route(
            "Earth",
            "Mars",
            100,
            10,
            20,
            0.1,
            50,
            0.9,
            True
        )

        self.galaxy.add_route(self.route)

    def test_detect_unavailable_route(self):
        self.route.is_available = False

        self.assertFalse(self.route.is_available)
    def test_find_unavailable_routes(self):
        self.route.is_available = False

        result = find_unavailable_routes(self.galaxy)

        self.assertEqual(result, [self.route])
    def test_replan_mission_with_alternative_route(self):
        earth = Planet(
            "Earth", 100, {}, {}, {}, 500, 5, 3, 8, 0, 0
        )
        mars = Planet(
            "Mars", 80, {}, {}, {}, 400, 4, 3, 7, 20, 0
        )
        jupiter = Planet(
            "Jupiter", 50, {}, {}, {}, 300, 6, 5, 9, 10, 10
        )

        self.galaxy.add_planet(earth)
        self.galaxy.add_planet(mars)
        self.galaxy.add_planet(jupiter)

        alternative_route_1 = Route(
            "Earth", "Jupiter", 15, 5, 10, 0.1, 50, 0.9, True
        )
        alternative_route_2 = Route(
            "Jupiter", "Mars", 15, 5, 10, 0.1, 50, 0.9, True
        )

        self.galaxy.add_route(alternative_route_1)
        self.galaxy.add_route(alternative_route_2)

        self.route.is_available = False

        mission = Mission(
            "Mission 1", "Earth", "Mars",
            "food", 10, 100, 5, 8, []
        )

        result = replan_mission_route(self.galaxy, mission)

        self.assertEqual(
            result["path"],
            ["Earth", "Jupiter", "Mars"]
        )
    def test_replan_mission_without_alternative_route(self):
        earth = Planet(
            "Earth", 100, {}, {}, {}, 500, 5, 3, 8, 0, 0
        )
        mars = Planet(
            "Mars", 80, {}, {}, {}, 400, 4, 3, 7, 20, 0
        )

        self.galaxy.add_planet(earth)
        self.galaxy.add_planet(mars)

        self.route.is_available = False

        mission = Mission(
            "Mission 2", "Earth", "Mars",
            "food", 10, 100, 5, 8, []
        )

        result = replan_mission_route(self.galaxy, mission)

        self.assertIsNone(result)
    def test_is_plan_affected(self):
        self.route.is_available = False

        result = is_plan_affected(
            ["Earth", "Mars"],
            [self.route]
        )

        self.assertTrue(result)

    def test_is_plan_not_affected(self):
        self.route.is_available = False

        result = is_plan_affected(
            ["Earth", "Jupiter", "Mars"],
            [self.route]
        )

        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()