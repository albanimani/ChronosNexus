import unittest

from models.infrastructure import Infrastructure
from algorithms.infrastructure_selection import (
    calculate_infrastructure_value
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


if __name__ == "__main__":
    unittest.main()