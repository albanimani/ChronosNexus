import unittest
from models.galaxy import Galaxy
from models.planet import Planet
from models.route import Route
from models.spacecraft import Spacecraft
from models.mission import Mission
from models.infrastructure import Infrastructure
from models.dynamic_event import DynamicEvent


class TestGalaxy(unittest.TestCase):

    def setUp(self):
        self.galaxy = Galaxy()

        self.planet = Planet(
            "Earth", 8000,
            {"food": 100},
            {"food": 70},
            {"food": 200},
            1000, 5, 8, 9, 0, 0
        )

        self.route = Route(
            "Earth", "Mars", 150, 5, 80,
            0.2, 100, 0.9, True
        )

        self.spacecraft = Spacecraft(
            "Explorer", "Earth", 500, 300,
            250, 50, 0.9, 100, ["cargo"], 0
        )

        self.mission = Mission(
            "Food Delivery", "Earth", "Mars",
            "food", 50, 20, 8, 9, ["cargo"]
        )

        self.infrastructure = Infrastructure(
            "Solar Plant", "Energy Plant", "Mars",
            500, {"energy": 100}, 50, -30,
            80, 150, 10
        )

        self.event = DynamicEvent(
            "Food Shortage", "resource_decrease",
            "Mars", "Food production decreased",
            -60, 10, 5
        )

    def test_add_planet(self):
        self.galaxy.add_planet(self.planet)
        self.assertIn("Earth", self.galaxy.planets)

    def test_add_route(self):
        self.galaxy.add_route(self.route)
        self.assertEqual(len(self.galaxy.routes["Earth"]), 1)

    def test_add_spacecraft(self):
        self.galaxy.add_spacecraft(self.spacecraft)
        self.assertIn("Explorer", self.galaxy.spacecraft)

    def test_add_mission(self):
        self.galaxy.add_mission(self.mission)
        self.assertIn("Food Delivery", self.galaxy.missions)

    def test_add_infrastructure(self):
        self.galaxy.add_infrastructure(self.infrastructure)
        self.assertIn("Solar Plant", self.galaxy.infrastructure)

    def test_add_event(self):
        self.galaxy.add_event(self.event)
        self.assertIn("Food Shortage", self.galaxy.events)

    def test_get_routes_from(self):
        self.galaxy.add_route(self.route)
        routes = self.galaxy.get_routes_from("Earth")
        self.assertEqual(len(routes), 1)


if __name__ == "__main__":
    unittest.main()