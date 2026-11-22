
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

    allocations = []

    for deficit_planet, deficit_amount in deficit_planets:
        for surplus_planet, original_amount in surplus_planets:
            surplus_amount = remaining_surplus[surplus_planet.name]

            if surplus_amount <= 0:
                continue

            available_routes = [
                route
                for route in galaxy.get_routes_from(surplus_planet.name)
                if route.destination == deficit_planet.name
                and route.is_available
            ]

            if not available_routes:
                continue

            route = min(
                available_routes,
                key=lambda route: route.distance
            )

            amount = min(
                surplus_amount,
                deficit_amount,
                route.capacity
            )

            if amount > 0:
                allocations.append({
                    "from": surplus_planet.name,
                    "to": deficit_planet.name,
                    "resource": resource,
                    "amount": amount,
                    "distance": route.distance
                })

                remaining_surplus[surplus_planet.name] -= amount
                deficit_amount -= amount

                if deficit_amount <= 0:
                    break

    return allocations
