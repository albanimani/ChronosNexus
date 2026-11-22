import unittest

from models.infrastructure import Infrastructure
from algorithms.infrastructure_selection import (
    calculate_infrastructure_value,
    can_build_infrastructure,
    filter_affordable_infrastructures,
    select_infrastructure
)


class TestInfrastructureSelection(unittest.TestCase):

    def test_calculate_infrastructure_value(self):
        infrastructure = Infrastructure(
            "Solar Plant",
            "energy",
            "Mars",
            100,
            {"energy": 50},
            10,
            20,
            8,
            7,
            5
        )

        result = calculate_infrastructure_value(infrastructure)

        self.assertEqual(result, 15)
    def test_can_build_infrastructure_with_enough_budget(self):
        infrastructure = Infrastructure(
            "Solar Plant",
            "energy",
            "Mars",
            100,
            {"energy": 50},
            10,
            20,
            8,
            7,
            5
        )

        result = can_build_infrastructure(infrastructure, 150)

        self.assertTrue(result)
    def test_filter_affordable_infrastructures(self):
        solar_plant = Infrastructure(
            "Solar Plant",
            "energy",
            "Mars",
            100,
            {"energy": 50},
            10,
            20,
            8,
            7,
            5
        )

        hospital = Infrastructure(
            "Hospital",
            "health",
            "Earth",
            200,
            {"medicine": 30},
            20,
            15,
            9,
            8,
            10
        )

        result = filter_affordable_infrastructures(
            [solar_plant, hospital],
            150
        )

        self.assertEqual(result, [solar_plant])
    def test_select_infrastructure(self):
        solar_plant = Infrastructure(
            "Solar Plant",
            "energy",
            "Mars",
            100,
            {"energy": 50},
            10,
            20,
            8,
            7,
            5
        )

        hospital = Infrastructure(
            "Hospital",
            "health",
            "Earth",
            200,
            {"medicine": 30},
            20,
            15,
            9,
            8,
            10
        )

        result = select_infrastructure(
            [solar_plant, hospital],
            200
        )

        self.assertEqual(result["selected"], [hospital])
        self.assertEqual(result["total_value"], 17)
        self.assertEqual(result["total_cost"], 200)
    def test_select_infrastructure_without_enough_budget(self):
        solar_plant = Infrastructure(
            "Solar Plant",
            "energy",
            "Mars",
            100,
            {"energy": 50},
            10,
            20,
            8,
            7,
            5
        )

        result = select_infrastructure(
            [solar_plant],
            50
        )

        self.assertEqual(result["selected"], [])
        self.assertEqual(result["total_value"], 0)
        self.assertEqual(result["total_cost"], 0)

    


if __name__ == "__main__":
    unittest.main()