import unittest

from models.galaxy import Galaxy
from models.planet import Planet
from models.route import Route
from algorithms.route_planning import a_star_search
from algorithms.route_planning import calculate_route_cost
from algorithms.route_planning import calculate_max_speed

class TestRoutePlanning(unittest.TestCase):

    def setUp(self):
        self.galaxy = Galaxy()

        self.earth = Planet(
            "Earth", 100, {}, {}, {}, 500, 5, 3, 8, 0, 0
        )

        self.mars = Planet(
            "Mars", 80, {}, {}, {}, 400, 4, 2, 6, 10, 0
        )

        self.jupiter = Planet(
            "Jupiter", 200, {}, {}, {}, 800, 7, 5, 9, 20, 0
        )

        self.galaxy.add_planet(self.earth)
        self.galaxy.add_planet(self.mars)
        self.galaxy.add_planet(self.jupiter)

        self.galaxy.add_route(
            Route("Earth", "Mars", 10, 2, 5, 0.1, 100, 0.9, True)
        )

        self.galaxy.add_route(
            Route("Mars", "Jupiter", 10, 2, 5, 0.1, 100, 0.9, True)
        )

        self.weights = {
            "distance": 0.3,
            "fuel": 0.3,
            "time": 0.2,
            "risk": 0.2
        }

    def test_find_route(self):
        result = a_star_search(
            self.galaxy, "Earth", "Jupiter", self.weights
        )

        self.assertEqual(result[0], ["Earth", "Mars", "Jupiter"])
    def test_find_lowest_cost_route(self):
        self.galaxy.add_route(
            Route("Earth", "Jupiter", 30, 10, 20, 0.5, 100, 0.8, True)
        )

        result = a_star_search(
            self.galaxy, "Earth", "Jupiter", self.weights
        )

        self.assertEqual(result[0], ["Earth", "Mars", "Jupiter"])
    def test_ignore_unavailable_route(self):
        self.galaxy.add_route(
            Route("Earth", "Jupiter", 5, 1, 2, 0.1, 100, 0.9, False)
        )

        result = a_star_search(
            self.galaxy, "Earth", "Jupiter", self.weights
        )

        self.assertEqual(result[0], ["Earth", "Mars", "Jupiter"])
    def test_no_route_available(self):
        self.galaxy.routes["Earth"] = []

        result = a_star_search(
            self.galaxy, "Earth", "Jupiter", self.weights
        )

        self.assertIsNone(result)
    def test_same_start_and_goal(self):
        result = a_star_search(
            self.galaxy, "Earth", "Earth", self.weights
        )

        self.assertEqual(result, (["Earth"], 0))
    def test_route_reliability_affects_cost(self):
        reliable_route = Route(
            "Earth", "Mars", 10, 5, 5, 0.1, 100, 0.9, True
        )

        unreliable_route = Route(
            "Earth", "Mars", 10, 5, 5, 0.1, 100, 0.5, True
        )

        reliable_cost = calculate_route_cost(
            reliable_route, self.weights
        )

        unreliable_cost = calculate_route_cost(
            unreliable_route, self.weights
        )

        self.assertGreater(unreliable_cost, reliable_cost)
    def test_calculate_max_speed_ignores_zero_travel_time(self):
        self.galaxy.add_route(
        Route("Earth", "Jupiter", 5, 0, 2, 0.1, 100, 0.9, True)
    )

        self.assertEqual(calculate_max_speed(self.galaxy), 5)


if __name__ == "__main__":
    unittest.main()