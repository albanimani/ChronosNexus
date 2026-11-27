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
    def test_expected_travel_time(self):
        self.assertAlmostEqual(
            self.route.calculate_expected_travel_time(),
            5.5555555556
        )

    def test_expected_travel_time_with_zero_reliability(self):
        route = Route(
            "Earth",
            "Mars",
            150,
            5,
            80,
            0.2,
            100,
            0,
            True
        )

        self.assertEqual(
            route.calculate_expected_travel_time(),
            float("inf")
        )
    
    def test_invalid_risk(self):
        for risk in [-0.1, 1.1]:
            with self.subTest(risk=risk):
                with self.assertRaises(ValueError):
                    Route("Earth", "Mars", 10, 5, 80, risk, 100, 0.9, True)    

    def test_negative_travel_time(self):
        with self.assertRaises(ValueError):
            Route("Earth", "Mars", 10, -5, 80, 0.2, 100, 0.9, True)

    def test_negative_fuel_consumption(self):
        with self.assertRaises(ValueError):
            Route("Earth", "Mars", 10, 5, -80, 0.2, 100, 0.9, True)

    
    def test_negative_capacity(self):
        with self.assertRaises(ValueError):
            Route("Earth", "Mars", 10, 5, 80, 0.2, -100, 0.9, True)

    def test_invalid_reliability(self):
        for reliability in [-0.1, 1.1]:
            with self.subTest(reliability=reliability):
                with self.assertRaises(ValueError):
                    Route("Earth", "Mars", 10, 5, 80, 0.2, 100, reliability, True)



if __name__ == "__main__":
    unittest.main()