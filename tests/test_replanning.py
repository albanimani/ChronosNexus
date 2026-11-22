import unittest

from models.galaxy import Galaxy
from models.route import Route
from simulation.replanning import find_unavailable_routes


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


if __name__ == "__main__":
    unittest.main()