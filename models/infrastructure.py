class Infrastructure:
    def __init__(
        self,
        name,
        facility_type,
        location,
        construction_cost,
        resource_impact,
        population_impact,
        energy_impact,
        strategic_value,
        development_value,
        construction_time
    ):
        self.name = name
        self.facility_type = facility_type
        self.location = location
        self.construction_cost = construction_cost
        self.resource_impact = resource_impact
        self.population_impact = population_impact
        self.energy_impact = energy_impact
        self.strategic_value = strategic_value
        self.development_value = development_value
        self.construction_time = construction_time

    def fits_budget(self, budget):
        return budget >= self.construction_cost