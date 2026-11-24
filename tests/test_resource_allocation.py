
import unittest

from models.galaxy import Galaxy
from models.planet import Planet
from models.route import Route
from algorithms.resource_allocation import (
    identify_resource_needs,
    allocate_resources,
    plan_proactive_resource_supply
)


class TestResourceAllocation(unittest.TestCase):

    def setUp(self):
        self.galaxy = Galaxy()

        self.earth = Planet(
            "Earth", 100, {"food": 100}, {"food": 70},
            {}, 500, 5, 3, 8, 0, 0
        )

        self.mars = Planet(
            "Mars", 80, {"food": 40}, {"food": 60},
            {}, 400, 4, 2, 6, 10, 0
        )

        self.galaxy.add_planet(self.earth)
        self.galaxy.add_planet(self.mars)

    def test_identify_surplus_and_deficit(self):
        surplus, deficit = identify_resource_needs(
            self.galaxy, "food"
        )

        self.assertEqual(surplus[0], (self.earth, 30))
        self.assertEqual(deficit[0], (self.mars, 20))

    def test_allocate_resources(self):
        route = Route(
            "Earth", "Mars", 10, 2, 5, 0.1, 100, 0.9, True
        )

        self.galaxy.add_route(route)

        result = allocate_resources(self.galaxy, "food")

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["from"], "Earth")
        self.assertEqual(result[0]["to"], "Mars")
        self.assertEqual(result[0]["amount"], 20)

    def test_choose_shortest_route(self):
        self.galaxy.add_route(
            Route("Earth", "Mars", 20, 4, 10, 0.2, 100, 0.9, True)
        )

        self.galaxy.add_route(
            Route("Earth", "Mars", 10, 2, 5, 0.1, 100, 0.9, True)
        )

        result = allocate_resources(self.galaxy, "food")

        self.assertEqual(result[0]["amount"], 20)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["distance"], 10)

    def test_respect_route_capacity(self):
        route = Route(
            "Earth", "Mars", 10, 2, 5, 0.1, 10, 0.9, True
        )

        self.galaxy.add_route(route)

        result = allocate_resources(self.galaxy, "food")

        self.assertEqual(result[0]["amount"], 10)

    def test_ignore_unavailable_route(self):
        route = Route(
            "Earth", "Mars", 10, 2, 5, 0.1, 100, 0.9, False
        )

        self.galaxy.add_route(route)

        result = allocate_resources(self.galaxy, "food")

        self.assertEqual(len(result), 0)
    
    def test_allocate_surplus_to_multiple_planets(self):
        jupiter = Planet(
            "Jupiter", 90, {"food": 20}, {"food": 40},
            {}, 600, 6, 4, 9, 20, 10
        )

        self.galaxy.add_planet(jupiter)

        self.galaxy.add_route(
            Route("Earth", "Jupiter", 15, 3, 8, 0.1, 100, 0.9, True)
        )

        self.galaxy.add_route(
            Route("Earth", "Mars", 10, 2, 5, 0.1, 100, 0.9, True)
        )

        result = allocate_resources(self.galaxy, "food")

        total_allocated = sum(
            allocation["amount"] for allocation in result
        )

        self.assertEqual(total_allocated, 30)
        self.assertEqual(result[0]["amount"], 20)
        self.assertEqual(result[1]["amount"], 10)
    def test_plan_proactive_resource_supply(self):
        route = Route(
            "Earth", "Mars", 10, 2, 5, 0.1, 100, 0.9, True
        )

        self.galaxy.add_route(route)

        result = plan_proactive_resource_supply(
            self.galaxy,
            "food",
            2
        )

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["from"], "Earth")
        self.assertEqual(result[0]["to"], "Mars")
        self.assertEqual(result[0]["resource"], "food")
        self.assertEqual(result[0]["amount"], 40)
    def test_proactive_supply_without_available_route(self):
        route = Route(
            "Earth", "Mars", 10, 2, 5, 0.1, 100, 0.9, False
        )

        self.galaxy.add_route(route)

        result = plan_proactive_resource_supply(
            self.galaxy,
            "food",
            2
        )

        self.assertEqual(result, [])
    def test_proactive_supply_respects_route_capacity(self):
        route = Route(
            "Earth", "Mars", 10, 2, 5, 0.1, 15, 0.9, True
        )

        self.galaxy.add_route(route)

        result = plan_proactive_resource_supply(
            self.galaxy,
            "food",
            2
        )

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["amount"], 15)



if __name__ == "__main__":
    unittest.main()
