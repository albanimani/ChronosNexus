import unittest
from models.infrastructure import Infrastructure


class TestInfrastructure(unittest.TestCase):

    def setUp(self):
        self.infrastructure = Infrastructure(
            "Solar Plant",
            "Energy Plant",
            "Mars",
            500,
            {"energy": 100, "water": 20},
            50,
            -30,
            80,
            150,
            10
        )

    def test_infrastructure_name(self):
        self.assertEqual(self.infrastructure.name, "Solar Plant")

    def test_infrastructure_type(self):
        self.assertEqual(self.infrastructure.facility_type, "Energy Plant")

    def test_infrastructure_location(self):
        self.assertEqual(self.infrastructure.location, "Mars")

    def test_construction_cost(self):
        self.assertEqual(self.infrastructure.construction_cost, 500)

    def test_resource_impact(self):
        self.assertEqual(self.infrastructure.resource_impact["energy"], 100)

    def test_fits_budget(self):
        self.assertTrue(self.infrastructure.fits_budget(600))

    def test_does_not_fit_budget(self):
        self.assertFalse(self.infrastructure.fits_budget(400))


if __name__ == "__main__":
    unittest.main()