def find_unavailable_routes(galaxy):
    unavailable_routes = []

    for routes in galaxy.routes.values():
        for route in routes:
            if not route.is_available:
                unavailable_routes.append(route)

    return unavailable_routes
