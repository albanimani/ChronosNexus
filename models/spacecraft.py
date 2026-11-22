
class Spacecraft:
    def __init__(
        self,
        name,
        current_location,
        cargo_capacity,
        fuel_capacity,
        current_fuel,
        speed,
        reliability,
        operating_cost,
        capabilities,
        available_at
    ):
        self.name = name
        self.current_location = current_location
        self.cargo_capacity = cargo_capacity
        self.fuel_capacity = fuel_capacity
        self.current_fuel = current_fuel
        self.speed = speed
        self.reliability = reliability
        self.operating_cost = operating_cost
        self.capabilities = capabilities
        self.available_at = available_at
        self.is_operational = True

    def has_enough_fuel(self, required_fuel):
        return self.current_fuel >= required_fuel

    def has_enough_capacity(self, cargo_amount):
        return self.cargo_capacity >= cargo_amount

    def has_capability(self, required_capabilities):
        return set(required_capabilities).issubset(self.capabilities)

    def is_available(self, departure_time):
        return self.available_at <= departure_time
