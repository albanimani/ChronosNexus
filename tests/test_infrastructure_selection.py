import unittest

from models.infrastructure import Infrastructure
from algorithms.infrastructure_selection import (
    calculate_infrastructure_value,
    can_build_infrastructure
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


if __name__ == "__main__":
    unittest.main()