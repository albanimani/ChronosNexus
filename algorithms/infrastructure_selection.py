
def calculate_infrastructure_value(infrastructure):
    return (
        infrastructure.strategic_value
        + infrastructure.development_value
    )


def can_build_infrastructure(infrastructure, budget):
    return infrastructure.fits_budget(budget)


def filter_affordable_infrastructures(infrastructures, budget):
    return [
        infrastructure
        for infrastructure in infrastructures
        if can_build_infrastructure(infrastructure, budget)
    ]


def select_infrastructure(infrastructures, budget):
    if budget < 0:
        raise ValueError("Budget cannot be negative")

    count = len(infrastructures)

    dp = [
        [0] * (budget + 1)
        for _ in range(count + 1)
    ]

    for i in range(1, count + 1):
        infrastructure = infrastructures[i - 1]
        cost = infrastructure.construction_cost
        value = calculate_infrastructure_value(infrastructure)

        for current_budget in range(budget + 1):
            dp[i][current_budget] = dp[i - 1][current_budget]

            if cost <= current_budget:
                dp[i][current_budget] = max(
                    dp[i][current_budget],
                    value + dp[i - 1][current_budget - cost]
                )

    selected = []
    remaining_budget = budget

    for i in range(count, 0, -1):
        if dp[i][remaining_budget] != dp[i - 1][remaining_budget]:
            infrastructure = infrastructures[i - 1]
            selected.append(infrastructure)
            remaining_budget -= infrastructure.construction_cost

    selected.reverse()

    total_cost = sum(
        infrastructure.construction_cost
        for infrastructure in selected
    )

    return {
        "selected": selected,
        "total_value": dp[count][budget],
        "total_cost": total_cost
    }
