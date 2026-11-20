
import unittest

from models.planet import Planet


class TestPlanet(unittest.TestCase):

    def setUp(self):
        self.planet = Planet(
            "Earth",
            8000000000,
            {"food": 100, "water": 80},
            {"food": 70, "water": 90},
            {"food": 200, "water": 100},
            500,
            8,
            7,
            10,
            0,
            0
        )

    def test_resource_surplus(self):
        self.assertEqual(
            self.planet.get_resource_balance("food"), 30
        )

    def test_resource_deficit(self):
        self.assertEqual(
            self.planet.get_resource_balance("water"), -10
        )

    def test_missing_resource(self):
        self.assertEqual(
            self.planet.get_resource_balance("medicine"), 0
        )

    def test_available_storage(self):
        self.assertEqual(
            self.planet.get_available_storage(), 200
        )


if __name__ == "__main__":
    unittest.main()
