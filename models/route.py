class Route:
    def __init__(
        self,
        origin,
        destination,
        distance,
        travel_time,
        fuel_consumption,
        risk,
        capacity,
        reliability,
        is_available
    ):
        self.origin = origin
        self.destination = destination
        self.distance = distance
        self.travel_time = travel_time
        self.fuel_consumption = fuel_consumption
        self.risk = risk
        self.capacity = capacity
        self.reliability = reliability
        self.is_available = is_available

    def is_suitable(self, cargo_amount):
        return self.is_available and self.capacity >= cargo_amount

    def calculate_failure_probability(self):
        return 1 - self.reliability