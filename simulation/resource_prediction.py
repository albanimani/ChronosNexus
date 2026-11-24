
def predict_resource_shortages(galaxy, periods):
    if periods < 0:
        raise ValueError("Periods cannot be negative")

    shortages = []

    for planet in galaxy.planets.values():
        resources = (
            set(planet.inventory)
            | set(planet.resource_production)
            | set(planet.resource_consumption)
        )

        for resource in resources:
            inventory = planet.inventory.get(resource, 0)
            production = planet.resource_production.get(resource, 0)
            consumption = planet.resource_consumption.get(resource, 0)

            future_amount = inventory + (
                production - consumption
            ) * periods

            if future_amount < 0:
                shortages.append({
                    "planet": planet.name,
                    "resource": resource,
                    "shortage": abs(future_amount)
                })

    return shortages
