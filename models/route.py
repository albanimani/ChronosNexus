
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
        if distance < 0:
            raise ValueError("Distance cannot be negative")

        if travel_time < 0:
            raise ValueError("Travel time cannot be negative")

        if fuel_consumption < 0:
            raise ValueError("Fuel consumption cannot be negative")

        if risk < 0:
            raise ValueError("Risk cannot be negative")

        if capacity < 0:
            raise ValueError("Capacity cannot be negative")

        if not 0 <= reliability <= 1:
            raise ValueError("Reliability must be between 0 and 1")

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

    def calculate_expected_travel_time(self):
        if self.reliability <= 0:
            return float("inf")

        return self.travel_time / self.reliability
