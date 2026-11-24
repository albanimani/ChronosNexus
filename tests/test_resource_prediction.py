
import unittest

from models.galaxy import Galaxy
from models.planet import Planet
from simulation.resource_prediction import predict_resource_shortages


class TestResourcePrediction(unittest.TestCase):

    def setUp(self):
        self.galaxy = Galaxy()

        self.earth = Planet(
            "Earth",
            100,
            {"food": 10},
            {"food": 20},
            {"food": 50},
            500,
            5,
            3,
            8,
            0,
            0
        )

        self.galaxy.add_planet(self.earth)

    def test_predict_resource_shortage(self):
        shortages = predict_resource_shortages(
            self.galaxy,
            6
        )

        self.assertEqual(len(shortages), 1)
        self.assertEqual(shortages[0]["planet"], "Earth")
        self.assertEqual(shortages[0]["resource"], "food")
        self.assertEqual(shortages[0]["shortage"], 10)

    def test_no_predicted_shortage(self):
        self.earth.inventory["food"] = 200

        shortages = predict_resource_shortages(
            self.galaxy,
            6
        )

        self.assertEqual(shortages, [])

    def test_shortage_without_production(self):
        self.earth.resource_production["food"] = 0
        self.earth.inventory["food"] = 30

        shortages = predict_resource_shortages(
            self.galaxy,
            2
        )

        self.assertEqual(len(shortages), 1)
        self.assertEqual(shortages[0]["shortage"], 10)

    def test_predict_multiple_resource_shortages(self):
        self.earth.inventory["water"] = 20
        self.earth.resource_production["water"] = 5
        self.earth.resource_consumption["water"] = 15

        shortages = predict_resource_shortages(
            self.galaxy,
            6
        )

        self.assertEqual(len(shortages), 2)

        resources = [
            shortage["resource"]
            for shortage in shortages
        ]

        self.assertIn("food", resources)
        self.assertIn("water", resources)

    def test_predict_shortages_for_multiple_planets(self):
        mars = Planet(
            "Mars",
            80,
            {"water": 5},
            {"water": 15},
            {"water": 20},
            300,
            3,
            2,
            7,
            10,
            10
        )

        self.galaxy.add_planet(mars)

        shortages = predict_resource_shortages(
            self.galaxy,
            6
        )

        planets = [
            shortage["planet"]
            for shortage in shortages
        ]

        self.assertIn("Earth", planets)
        self.assertIn("Mars", planets)

    def test_predict_shortage_for_resource_missing_from_inventory(self):
        self.earth.inventory = {}
        self.earth.resource_production = {"food": 0}
        self.earth.resource_consumption = {"food": 10}

        shortages = predict_resource_shortages(
            self.galaxy,
            2
        )

        self.assertEqual(len(shortages), 1)
        self.assertEqual(shortages[0]["resource"], "food")
        self.assertEqual(shortages[0]["shortage"], 20)
    def test_negative_periods(self):
        with self.assertRaises(ValueError):
            predict_resource_shortages(
                self.galaxy,
                -1
            )


if __name__ == "__main__":
    unittest.main()
