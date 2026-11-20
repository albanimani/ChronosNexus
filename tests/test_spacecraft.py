
import unittest

from models.spacecraft import Spacecraft


class TestSpacecraft(unittest.TestCase):

    def setUp(self):
        self.spacecraft = Spacecraft(
            "Explorer-01",
            "Earth",
            500,
            1000,
            800,
            25,
            0.95,
            150,
            ["cargo", "research", "exploration"],
            10
        )

    def test_enough_fuel(self):
        self.assertTrue(self.spacecraft.has_enough_fuel(500))

    def test_not_enough_fuel(self):
        self.assertFalse(self.spacecraft.has_enough_fuel(900))

    def test_enough_capacity(self):
        self.assertTrue(self.spacecraft.has_enough_capacity(400))

    def test_not_enough_capacity(self):
        self.assertFalse(self.spacecraft.has_enough_capacity(600))

    def test_required_capabilities(self):
        self.assertTrue(
            self.spacecraft.has_capability(["cargo", "research"])
        )

    def test_missing_capability(self):
        self.assertFalse(
            self.spacecraft.has_capability(["military"])
        )

    def test_available_spacecraft(self):
        self.assertTrue(self.spacecraft.is_available(15))

    def test_unavailable_spacecraft(self):
        self.assertFalse(self.spacecraft.is_available(5))


if __name__ == "__main__":
    unittest.main()
