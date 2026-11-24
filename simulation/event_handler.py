
def apply_dynamic_event(galaxy, event):
    if event.status != "pending":
        return False

    if event.event_type == "route_blockage":
        for routes in galaxy.routes.values():
            for route in routes:
                route_name = f"{route.origin}-{route.destination}"

                if route_name == event.affected_location:
                    route.is_available = False

                    event.activate_event()
                    galaxy.add_event(event)
                    return True

    elif event.event_type == "route_risk_increase":
        for routes in galaxy.routes.values():
            for route in routes:
                route_name = f"{route.origin}-{route.destination}"

                if route_name == event.affected_location:
                    route.risk = min(1.0, route.risk + event.impact)

                    event.activate_event()
                    galaxy.add_event(event)
                    return True

    elif event.event_type == "production_decrease":
        planet = galaxy.planets.get(event.affected_location)

        if planet is not None:
            for resource in planet.resource_production:
                planet.resource_production[resource] *= (
                    1 - event.impact
                )

            event.activate_event()
            galaxy.add_event(event)
            return True

    elif event.event_type == "spacecraft_destroyed":
        spacecraft = galaxy.spacecraft.get(event.affected_location)

        if spacecraft is not None:
            spacecraft.is_operational = False

            event.activate_event()
            galaxy.add_event(event)
            return True

    return False
