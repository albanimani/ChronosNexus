def apply_dynamic_event(galaxy, event):
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

    return False

