

def identify_resource_needs(galaxy, resource):
    surplus_planets = []
    deficit_planets = []

    for planet in galaxy.planets.values():
        balance = planet.get_resource_balance(resource)

        if balance > 0:
            surplus_planets.append((planet, balance))

        elif balance < 0:
            deficit_planets.append((planet, abs(balance)))

    return surplus_planets, deficit_planets


def allocate_resources(galaxy, resource):
    surplus_planets, deficit_planets = identify_resource_needs(
        galaxy, resource
    )

    remaining_surplus = {
        planet.name: amount
        for planet, amount in surplus_planets
    }

    surplus_order = {
        planet.name: index
        for index, (planet, amount) in enumerate(surplus_planets)
    }

    deficit_names = {
        planet.name
        for planet, amount in deficit_planets
    }

    routes_by_destination = {}

    for routes in galaxy.routes.values():
        for route in routes:
            if (
                route.is_available
                and route.origin in remaining_surplus
                and route.destination in deficit_names
            ):
                destination_routes = routes_by_destination.setdefault(
                    route.destination, {}
                )

                current_route = destination_routes.get(route.origin)

                if (
                    current_route is None
                    or route.distance < current_route.distance
                ):
                    destination_routes[route.origin] = route

    allocations = []

    for deficit_planet, deficit_amount in deficit_planets:
        available_routes = list(
            routes_by_destination.get(deficit_planet.name, {}).values()
        )

        available_routes.sort(
            key=lambda route: surplus_order[route.origin]
        )

        for route in available_routes:
            surplus_amount = remaining_surplus[route.origin]

            if surplus_amount <= 0:
                continue

            amount = min(
                surplus_amount,
                deficit_amount,
                route.capacity
            )

            if amount > 0:
                allocations.append({
                    "from": route.origin,
                    "to": deficit_planet.name,
                    "resource": resource,
                    "amount": amount,
                    "distance": route.distance
                })

                remaining_surplus[route.origin] -= amount
                deficit_amount -= amount

                if deficit_amount <= 0:
                    break

    return allocations

def plan_proactive_resource_supply(galaxy, resource, periods):
    if periods < 0:
        raise ValueError("Periods cannot be negative")

    surplus_planets = []
    deficit_planets = []

    for planet in galaxy.planets.values():
        inventory = planet.inventory.get(resource, 0)
        production = planet.resource_production.get(resource, 0)
        consumption = planet.resource_consumption.get(resource, 0)

        future_amount = inventory + (
            production - consumption
        ) * periods

        if future_amount > 0:
            surplus_planets.append((planet, future_amount))
        elif future_amount < 0:
            deficit_planets.append((planet, abs(future_amount)))

    remaining_surplus = {
        planet.name: amount
        for planet, amount in surplus_planets
    }

    surplus_order = {
        planet.name: index
        for index, (planet, amount) in enumerate(surplus_planets)
    }

    deficit_names = {
        planet.name
        for planet, amount in deficit_planets
    }

    routes_by_destination = {}

    for routes in galaxy.routes.values():
        for route in routes:
            if (
                route.is_available
                and route.origin in remaining_surplus
                and route.destination in deficit_names
            ):
                destination_routes = routes_by_destination.setdefault(
                    route.destination, {}
                )

                current_route = destination_routes.get(route.origin)

                if (
                    current_route is None
                    or route.distance < current_route.distance
                ):
                    destination_routes[route.origin] = route

    allocations = []

    for deficit_planet, deficit_amount in deficit_planets:
        available_routes = list(
            routes_by_destination.get(deficit_planet.name, {}).values()
        )

        available_routes.sort(
            key=lambda route: surplus_order[route.origin]
        )

        for route in available_routes:
            surplus_amount = remaining_surplus[route.origin]

            if surplus_amount <= 0:
                continue

            amount = min(
                surplus_amount,
                deficit_amount,
                route.capacity
            )

            if amount > 0:
                allocations.append({
                    "from": route.origin,
                    "to": deficit_planet.name,
                    "resource": resource,
                    "amount": amount,
                    "distance": route.distance
                })

                remaining_surplus[route.origin] -= amount
                deficit_amount -= amount

                if deficit_amount <= 0:
                    break

    return allocations

