import unittest
from models.route import Route


class TestRoute(unittest.TestCase):

    def setUp(self):
        self.route = Route(
            "Earth",
            "Mars",
            150,
            5,
            80,
            0.2,
            100,
            0.9,
            True
        )

    def test_route_origin(self):
        self.assertEqual(self.route.origin, "Earth")

    def test_route_destination(self):
        self.assertEqual(self.route.destination, "Mars")

    def test_route_capacity(self):
        self.assertEqual(self.route.capacity, 100)

    def test_route_is_available(self):
        self.assertTrue(self.route.is_available)

    def test_route_is_suitable(self):
        self.assertTrue(self.route.is_suitable(70))

    def test_route_is_not_suitable(self):
        self.assertFalse(self.route.is_suitable(120))

    def test_failure_probability(self):
        self.assertAlmostEqual(
            self.route.calculate_failure_probability(),
            0.1
        )


if __name__ == "__main__":
    unittest.main()