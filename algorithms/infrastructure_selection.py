def calculate_infrastructure_value(infrastructure):
    return (
        infrastructure.strategic_value
        + infrastructure.development_value
    )
def can_build_infrastructure(infrastructure, budget):
    return infrastructure.fits_budget(budget)