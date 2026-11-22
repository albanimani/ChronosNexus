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

def needs_replanning(galaxy, path):
    unavailable_routes = find_unavailable_routes(galaxy)
    return is_plan_affected(path, unavailable_routes)
def update_mission_plan(galaxy, mission, current_path):
    if not needs_replanning(galaxy, current_path):
        return {
            "path": current_path,
            "replanned": False
        }

    new_route = replan_mission_route(galaxy, mission)

    if new_route is None:
        return {
            "path": None,
            "replanned": True
        }

    return {
        "path": new_route["path"],
        "replanned": True
    }
def replan_affected_missions(galaxy, mission_plans):
    updated_plans = {}

    for mission_name, current_path in mission_plans.items():
        mission = galaxy.missions.get(mission_name)

        if mission is None:
            updated_plans[mission_name] = {
                "path": current_path,
                "replanned": False
            }
            continue

        updated_plans[mission_name] = update_mission_plan(
            galaxy,
            mission,
            current_path
        )

    return updated_plans