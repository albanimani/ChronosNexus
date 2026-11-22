from algorithms.mission_scheduling import calculate_mission_route


def find_unavailable_routes(galaxy):
    unavailable_routes = []

    for routes in galaxy.routes.values():
        for route in routes:
            if not route.is_available:
                unavailable_routes.append(route)

    return unavailable_routes


def replan_mission_route(galaxy, mission):
    return calculate_mission_route(galaxy, mission)
def is_plan_affected(path, unavailable_routes):
    for i in range(len(path) - 1):
        for route in unavailable_routes:
            if (
                route.origin == path[i]
                and route.destination == path[i + 1]
            ):
                return True

    return False