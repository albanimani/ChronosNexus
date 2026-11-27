
import unittest

from models.galaxy import Galaxy
from models.route import Route
from models.planet import Planet
from models.mission import Mission
from simulation.replanning import find_unavailable_routes
from simulation.replanning import replan_mission_route
from simulation.replanning import is_plan_affected
from simulation.replanning import needs_replanning
from simulation.replanning import update_mission_plan
from simulation.replanning import replan_affected_missions
from simulation.event_handler import apply_dynamic_event


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

    def test_replan_mission_with_alternative_route(self):
        earth = Planet(
            "Earth", 100, {}, {}, {}, 500, 5, 3, 8, 0, 0
        )
        mars = Planet(
            "Mars", 80, {}, {}, {}, 400, 4, 3, 7, 20, 0
        )
        jupiter = Planet(
            "Jupiter", 50, {}, {}, {}, 300, 6, 5, 9, 10, 10
        )

        self.galaxy.add_planet(earth)
        self.galaxy.add_planet(mars)
        self.galaxy.add_planet(jupiter)

        alternative_route_1 = Route(
            "Earth", "Jupiter", 15, 5, 10, 0.1, 50, 0.9, True
        )
        alternative_route_2 = Route(
            "Jupiter", "Mars", 15, 5, 10, 0.1, 50, 0.9, True
        )

        self.galaxy.add_route(alternative_route_1)
        self.galaxy.add_route(alternative_route_2)

        self.route.is_available = False

        mission = Mission(
            "Mission 1", "Earth", "Mars",
            "food", 10, 100, 5, 8, []
        )

        result = replan_mission_route(self.galaxy, mission)

        self.assertEqual(
            result["path"],
            ["Earth", "Jupiter", "Mars"]
        )

    def test_replan_mission_without_alternative_route(self):
        earth = Planet(
            "Earth", 100, {}, {}, {}, 500, 5, 3, 8, 0, 0
        )
        mars = Planet(
            "Mars", 80, {}, {}, {}, 400, 4, 3, 7, 20, 0
        )

        self.galaxy.add_planet(earth)
        self.galaxy.add_planet(mars)

        self.route.is_available = False

        mission = Mission(
            "Mission 2", "Earth", "Mars",
            "food", 10, 100, 5, 8, []
        )

        result = replan_mission_route(self.galaxy, mission)

        self.assertIsNone(result)

    def test_is_plan_affected(self):
        self.route.is_available = False

        result = is_plan_affected(
            ["Earth", "Mars"],
            [self.route]
        )

        self.assertTrue(result)

    def test_is_plan_not_affected(self):
        self.route.is_available = False

        result = is_plan_affected(
            ["Earth", "Jupiter", "Mars"],
            [self.route]
        )

        self.assertFalse(result)

    def test_needs_replanning_when_route_is_blocked(self):
        self.route.is_available = False

        result = needs_replanning(
            self.galaxy,
            ["Earth", "Mars"]
        )

        self.assertTrue(result)

    def test_does_not_need_replanning_when_route_is_available(self):
        result = needs_replanning(
            self.galaxy,
            ["Earth", "Mars"]
        )

        self.assertFalse(result)

    def test_keep_existing_plan_when_route_is_available(self):
        earth = Planet(
            "Earth", 100, {}, {}, {}, 500, 5, 3, 8, 0, 0
        )
        mars = Planet(
            "Mars", 80, {}, {}, {}, 400, 4, 3, 7, 20, 0
        )

        self.galaxy.add_planet(earth)
        self.galaxy.add_planet(mars)

        mission = Mission(
            "Mission 3", "Earth", "Mars",
            "food", 10, 100, 5, 8, []
        )

        result = update_mission_plan(
            self.galaxy,
            mission,
            ["Earth", "Mars"]
        )

        self.assertEqual(result["path"], ["Earth", "Mars"])
        self.assertFalse(result["replanned"])

    def test_update_mission_plan_after_route_blockage(self):
        earth = Planet(
            "Earth", 100, {}, {}, {}, 500, 5, 3, 8, 0, 0
        )
        mars = Planet(
            "Mars", 80, {}, {}, {}, 400, 4, 3, 7, 20, 0
        )
        jupiter = Planet(
            "Jupiter", 50, {}, {}, {}, 300, 6, 5, 9, 10, 10
        )

        self.galaxy.add_planet(earth)
        self.galaxy.add_planet(mars)
        self.galaxy.add_planet(jupiter)

        self.galaxy.add_route(
            Route("Earth", "Jupiter", 15, 5, 10, 0.1, 50, 0.9, True)
        )
        self.galaxy.add_route(
            Route("Jupiter", "Mars", 15, 5, 10, 0.1, 50, 0.9, True)
        )

        self.route.is_available = False

        mission = Mission(
            "Mission 4", "Earth", "Mars",
            "food", 10, 100, 5, 8, []
        )

        result = update_mission_plan(
            self.galaxy,
            mission,
            ["Earth", "Mars"]
        )

        self.assertEqual(
            result["path"],
            ["Earth", "Jupiter", "Mars"]
        )
        self.assertTrue(result["replanned"])

    def test_update_mission_plan_without_alternative_route(self):
        earth = Planet(
            "Earth", 100, {}, {}, {}, 500, 5, 3, 8, 0, 0
        )
        mars = Planet(
            "Mars", 80, {}, {}, {}, 400, 4, 3, 7, 20, 0
        )

        self.galaxy.add_planet(earth)
        self.galaxy.add_planet(mars)

        self.route.is_available = False

        mission = Mission(
            "Mission 5", "Earth", "Mars",
            "food", 10, 100, 5, 8, []
        )

        result = update_mission_plan(
            self.galaxy,
            mission,
            ["Earth", "Mars"]
        )

        self.assertIsNone(result["path"])
        self.assertTrue(result["replanned"])

    def test_replan_only_affected_missions(self):
        earth = Planet(
            "Earth", 100, {}, {}, {}, 500, 5, 3, 8, 0, 0
        )
        mars = Planet(
            "Mars", 80, {}, {}, {}, 400, 4, 3, 7, 20, 0
        )
        venus = Planet(
            "Venus", 60, {}, {}, {}, 300, 4, 2, 6, 10, 10
        )

        self.galaxy.add_planet(earth)
        self.galaxy.add_planet(mars)
        self.galaxy.add_planet(venus)

        alternative_route = Route(
            "Earth", "Venus", 50, 5, 10, 0.1, 50, 0.9, True
        )
        destination_route = Route(
            "Venus", "Mars", 60, 6, 10, 0.1, 50, 0.9, True
        )

        self.galaxy.add_route(alternative_route)
        self.galaxy.add_route(destination_route)

        mission_plans = {
            "Mission 1": ["Earth", "Mars"],
            "Mission 2": ["Earth", "Venus"]
        }

        mission1 = Mission(
            "Mission 1", "Earth", "Mars",
            "food", 10, 100, 5, 8, []
        )

        mission2 = Mission(
            "Mission 2", "Earth", "Venus",
            "food", 10, 100, 5, 8, []
        )

        self.galaxy.add_mission(mission1)
        self.galaxy.add_mission(mission2)

        self.route.is_available = False

        updated_plans = replan_affected_missions(
            self.galaxy,
            mission_plans
        )

        self.assertEqual(
            updated_plans["Mission 1"]["path"],
            ["Earth", "Venus", "Mars"]
        )
        self.assertTrue(updated_plans["Mission 1"]["replanned"])

        self.assertEqual(
            updated_plans["Mission 2"]["path"],
            ["Earth", "Venus"]
        )
        self.assertFalse(updated_plans["Mission 2"]["replanned"])

    def test_block_route_with_dynamic_event(self):
        from models.dynamic_event import DynamicEvent

        event = DynamicEvent(
            "Wormhole Collapse",
            "route_blockage",
            "Earth-Mars",
            "Route blocked",
            1,
            10,
            5
        )

        apply_dynamic_event(self.galaxy, event)

        self.assertFalse(self.route.is_available)
        self.assertEqual(event.status, "active")

    def test_dynamic_event_for_nonexistent_route(self):
        from models.dynamic_event import DynamicEvent

        event = DynamicEvent(
            "Unknown Route",
            "route_blockage",
            "Earth-Jupiter",
            "Route does not exist",
            1,
            10,
            5
        )

        result = apply_dynamic_event(self.galaxy, event)

        self.assertFalse(result)
        self.assertEqual(event.status, "pending")

    def test_increase_route_risk_with_dynamic_event(self):
        from models.dynamic_event import DynamicEvent

        event = DynamicEvent(
            "Pirate Attack",
            "route_risk_increase",
            "Earth-Mars",
            "Route risk increased",
            0.3,
            10,
            5
        )

        result = apply_dynamic_event(self.galaxy, event)

        self.assertTrue(result)
        self.assertEqual(self.route.risk, 0.4)
        self.assertEqual(event.status, "active")

    def test_reduce_resource_production_with_dynamic_event(self):
        from models.dynamic_event import DynamicEvent

        planet = Planet(
            "Earth", 100, {"food": 100}, {"food": 70},
            {"food": 50}, 500, 5, 3, 8, 0, 0
        )

        self.galaxy.add_planet(planet)

        event = DynamicEvent(
            "Crop Failure",
            "production_decrease",
            "Earth",
            "Food production decreased",
            0.6,
            10,
            5
        )

        result = apply_dynamic_event(self.galaxy, event)

        self.assertTrue(result)
        self.assertEqual(planet.resource_production["food"], 40)
        self.assertEqual(event.status, "active")

    def test_destroy_spacecraft_with_dynamic_event(self):
        from models.spacecraft import Spacecraft
        from models.dynamic_event import DynamicEvent

        spacecraft = Spacecraft(
            "Explorer",
            "Earth",
            100,
            200,
            150,
            10,
            0.9,
            50,
            ["transport"],
            0
        )

        self.galaxy.add_spacecraft(spacecraft)

        event = DynamicEvent(
            "Spacecraft Destruction",
            "spacecraft_destroyed",
            "Explorer",
            "Spacecraft destroyed",
            1,
            10,
            5
        )

        result = apply_dynamic_event(self.galaxy, event)

        self.assertTrue(result)
        self.assertFalse(spacecraft.is_operational)
        self.assertEqual(event.status, "active")

    def test_dynamic_event_cannot_be_applied_twice(self):
        from models.dynamic_event import DynamicEvent

        planet = Planet(
            "Earth", 100, {"food": 100}, {"food": 70},
            {"food": 50}, 500, 5, 3, 8, 0, 0
        )

        self.galaxy.add_planet(planet)

        event = DynamicEvent(
            "Crop Failure",
            "production_decrease",
            "Earth",
            "Food production decreased",
            0.6,
            10,
            5
        )

        first_result = apply_dynamic_event(self.galaxy, event)
        second_result = apply_dynamic_event(self.galaxy, event)

        self.assertTrue(first_result)
        self.assertFalse(second_result)
        self.assertEqual(planet.resource_production["food"], 40)
    
    def test_replan_when_route_risk_increases(self):
        earth = Planet(
            "Earth", 100, {}, {}, {}, 500, 5, 3, 8, 0, 0
        )
        mars = Planet(
            "Mars", 80, {}, {}, {}, 400, 4, 3, 7, 20, 0
        )
        jupiter = Planet(
            "Jupiter", 50, {}, {}, {}, 300, 6, 5, 9, 10, 10
        )

        self.galaxy.add_planet(earth)
        self.galaxy.add_planet(mars)
        self.galaxy.add_planet(jupiter)

        direct_route = self.route

        self.galaxy.add_route(
            Route("Earth", "Jupiter", 15, 5, 10, 0.1, 50, 0.9, True)
        )
        self.galaxy.add_route(
            Route("Jupiter", "Mars", 15, 5, 10, 0.1, 50, 0.9, True)
        )

        direct_route.risk = 0.8

        mission = Mission(
            "Risky Mission", "Earth", "Mars",
            "food", 10, 100, 5, 8, []
        )

        result = update_mission_plan(
            self.galaxy,
            mission,
            ["Earth", "Mars"]
        )

        self.assertEqual(
            result["path"],
            ["Earth", "Jupiter", "Mars"]
        )
        self.assertTrue(result["replanned"])

    
    def test_replan_when_assigned_spacecraft_is_destroyed(self):
        from models.spacecraft import Spacecraft

        earth = Planet(
            "Earth", 100, {}, {}, {}, 500, 5, 3, 8, 0, 0
        )
        mars = Planet(
            "Mars", 80, {}, {}, {}, 400, 4, 3, 7, 20, 0
        )

        self.galaxy.add_planet(earth)
        self.galaxy.add_planet(mars)

        destroyed_spacecraft = Spacecraft(
            "Explorer",
            "Earth",
            100,
            200,
            150,
            10,
            0.9,
            50,
            ["transport"],
            0
        )

        replacement_spacecraft = Spacecraft(
            "Voyager",
            "Earth",
            100,
            200,
            150,
            10,
            0.9,
            40,
            ["transport"],
            0
        )

        destroyed_spacecraft.is_operational = False

        self.galaxy.add_spacecraft(destroyed_spacecraft)
        self.galaxy.add_spacecraft(replacement_spacecraft)

        mission = Mission(
            "Mission 1", "Earth", "Mars",
            "food", 10, 100, 5, 8, []
        )

        mission.assign_spacecraft(destroyed_spacecraft, 0)
        self.galaxy.add_mission(mission)

        mission_plans = {
            "Mission 1": ["Earth", "Mars"]
        }

        updated_plans = replan_affected_missions(
            self.galaxy,
            mission_plans
        )

        self.assertEqual(
            mission.assigned_spacecraft,
            replacement_spacecraft
        )
        self.assertEqual(
            updated_plans["Mission 1"]["path"],
            ["Earth", "Mars"]
        )
        self.assertTrue(
            updated_plans["Mission 1"]["replanned"]
        )

    def test_completed_mission_is_not_replanned_when_spacecraft_is_destroyed(self):
        from models.spacecraft import Spacecraft

        earth = Planet(
            "Earth", 100, {}, {}, {}, 500, 5, 3, 8, 0, 0
        )
        mars = Planet(
            "Mars", 80, {}, {}, {}, 400, 4, 3, 7, 20, 0
        )

        self.galaxy.add_planet(earth)
        self.galaxy.add_planet(mars)

        spacecraft = Spacecraft(
            "Explorer",
            "Earth",
            100,
            200,
            150,
            10,
            0.9,
            50,
            ["transport"],
            0
        )

        self.galaxy.add_spacecraft(spacecraft)

        mission = Mission(
            "Mission 1", "Earth", "Mars",
            "food", 10, 100, 5, 8, []
        )

        mission.assign_spacecraft(spacecraft, 0)
        mission.complete_mission()

        spacecraft.is_operational = False

        self.galaxy.add_mission(mission)

        mission_plans = {
            "Mission 1": ["Earth", "Mars"]
        }

        updated_plans = replan_affected_missions(
            self.galaxy,
            mission_plans
        )

        self.assertEqual(
            mission.assigned_spacecraft,
            spacecraft
        )
        self.assertEqual(
            updated_plans["Mission 1"]["path"],
            ["Earth", "Mars"]
        )
        self.assertFalse(
            updated_plans["Mission 1"]["replanned"]
        )




if __name__ == "__main__":
    unittest.main()
