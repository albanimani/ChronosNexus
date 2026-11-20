
class Planet:
    def __init__(
        self,
        name,
        population,
        resource_production,
        resource_consumption,
        inventory,
        storage_capacity,
        technology_level,
        defense_level,
        strategic_importance,
        x,
        y
    ):
        self.name = name
        self.population = population
        self.resource_production = resource_production
        self.resource_consumption = resource_consumption
        self.inventory = inventory
        self.storage_capacity = storage_capacity
        self.technology_level = technology_level
        self.defense_level = defense_level
        self.strategic_importance = strategic_importance
        self.x = x
        self.y = y

    def get_resource_balance(self, resource):
        production = self.resource_production.get(resource, 0)
        consumption = self.resource_consumption.get(resource, 0)

        return production - consumption

    def get_available_storage(self):
        used_storage = sum(self.inventory.values())

        return self.storage_capacity - used_storage
