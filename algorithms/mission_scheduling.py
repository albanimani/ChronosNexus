
from algorithms.route_planning import (
    a_star_search,
    calculate_route_cost
)


def calculate_mission_route(galaxy, mission):
    weights = {
        "distance": 1,
        "fuel": 1,
        "time": 1,
        "risk": 1
    }

    result = a_star_search(
        galaxy,
        mission.origin,
        mission.destination,
        weights
    )

    if result is None:
        return None

    path, total_cost = result

    total_fuel = 0
    total_time = 0

    for i in range(len(path) - 1):
        available_routes = [
            route
            for route in galaxy.get_routes_from(path[i])
            if route.destination == path[i + 1]
            and route.is_available
        ]

        if not available_routes:
            return None

        route = min(
            available_routes,
            key=lambda route: calculate_route_cost(route, weights)
        )

        total_fuel += route.fuel_consumption
        total_time += route.calculate_expected_travel_time()

    return {
        "path": path,
        "total_cost": total_cost,
        "total_fuel": total_fuel,
        "total_time": total_time
    }


def is_spacecraft_suitable(spacecraft, mission, route_info, departure_time):
    if spacecraft.current_location != mission.origin:
        return False

    if not spacecraft.has_enough_capacity(mission.cargo_amount):
        return False

    if not spacecraft.has_enough_fuel(route_info["total_fuel"]):
        return False

    if not spacecraft.has_capability(mission.required_capabilities):
        return False

    if not spacecraft.is_available(departure_time):
        return False

    arrival_time = departure_time + route_info["total_time"]

    if arrival_time > mission.deadline:
        return False

    return True


def schedule_mission(galaxy, mission, departure_time):
    route_info = calculate_mission_route(galaxy, mission)

    if route_info is None:
        return None

    suitable_spacecraft = []

    for spacecraft in galaxy.spacecraft.values():
        if is_spacecraft_suitable(
            spacecraft,
            mission,
            route_info,
            departure_time
        ):
            suitable_spacecraft.append(spacecraft)

    if not suitable_spacecraft:
        return None

    selected_spacecraft = min(
        suitable_spacecraft,
        key=lambda spacecraft: spacecraft.operating_cost
    )

    mission.assign_spacecraft(
        selected_spacecraft,
        departure_time
    )

    selected_spacecraft.current_location = mission.destination
    selected_spacecraft.available_at = (
        departure_time + route_info["total_time"]
    )

    return {
        "mission": mission.name,
        "spacecraft": selected_spacecraft.name,
        "route": route_info["path"],
        "departure_time": departure_time,
        "arrival_time": departure_time + route_info["total_time"],
        "total_fuel": route_info["total_fuel"],
        "total_cost": route_info["total_cost"]
    }


def schedule_missions(galaxy, missions, departure_time):
    sorted_missions = sorted(
        missions,
        key=lambda mission: (-mission.priority, mission.deadline)
    )

    scheduled_missions = []

    for mission in sorted_missions:
        result = schedule_mission(
            galaxy,
            mission,
            departure_time
        )

        if result is not None:
            scheduled_missions.append(result)
            departure_time = result["arrival_time"]

    return scheduled_missions
