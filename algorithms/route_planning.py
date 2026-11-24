import heapq
import math


def calculate_max_speed(galaxy):
    max_speed = 0

    for routes in galaxy.routes.values():
        for route in routes:
            if route.travel_time > 0:
                speed = route.distance / route.travel_time
                max_speed = max(max_speed, speed)

    return max_speed


def heuristic(galaxy, planet1, planet2, weights, max_speed=None):
    return 0


def calculate_route_cost(route, weights):
    cost = (
        route.distance * weights["distance"]
        + route.fuel_consumption * weights["fuel"]
        + route.calculate_expected_travel_time() * weights["time"]
        + route.risk * weights["risk"]
    )

    return cost


def a_star_search(galaxy, start_name, goal_name, weights):
    if start_name not in galaxy.planets or goal_name not in galaxy.planets:
        return None

    if start_name == goal_name:
        return [start_name], 0

    start_planet = galaxy.planets[start_name]
    goal_planet = galaxy.planets[goal_name]

    max_speed = calculate_max_speed(galaxy)

    open_list = []
    heapq.heappush(open_list, (0, start_name))

    came_from = {}
    g_score = {start_name: 0}

    f_score = {
        start_name: heuristic(
            galaxy, start_planet, goal_planet, weights, max_speed
        )
    }

    while open_list:
        current_priority, current_name = heapq.heappop(open_list)

        if current_priority > f_score.get(current_name, float("inf")):
            continue

        if current_name == goal_name:
            path = [goal_name]

            while path[-1] != start_name:
                path.append(came_from[path[-1]])

            path.reverse()

            return path, g_score[goal_name]

        for route in galaxy.get_routes_from(current_name):
            if not route.is_available:
                continue

            neighbor_name = route.destination

            if neighbor_name not in galaxy.planets:
                continue

            tentative_g = (
                g_score[current_name]
                + calculate_route_cost(route, weights)
            )

            if tentative_g < g_score.get(neighbor_name, float("inf")):
                came_from[neighbor_name] = current_name
                g_score[neighbor_name] = tentative_g

                neighbor_planet = galaxy.planets[neighbor_name]

                h_score = heuristic(
                    galaxy,
                    neighbor_planet,
                    goal_planet,
                    weights,
                    max_speed
                )

                f_score[neighbor_name] = tentative_g + h_score

                heapq.heappush(
                    open_list,
                    (f_score[neighbor_name], neighbor_name)
                )

    return None
