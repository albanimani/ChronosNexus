class Galaxy:
    def __init__(self):
        self.planets = {}
        self.routes = {}
        self.spacecraft = {}
        self.missions = {}
        self.infrastructure = {}
        self.events = {}

    def add_planet(self, planet):
        self.planets[planet.name] = planet

        if planet.name not in self.routes:
            self.routes[planet.name] = []

    def add_route(self, route):
        if route.origin not in self.routes:
            self.routes[route.origin] = []

        self.routes[route.origin].append(route)

    def add_spacecraft(self, spacecraft):
        self.spacecraft[spacecraft.name] = spacecraft

    def add_mission(self, mission):
        self.missions[mission.name] = mission

    def add_infrastructure(self, infrastructure):
        self.infrastructure[infrastructure.name] = infrastructure

    def add_event(self, event):
        self.events[event.name] = event

    def get_routes_from(self, planet_name):
        return self.routes.get(planet_name, [])