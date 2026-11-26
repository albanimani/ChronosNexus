
import random
import time

from models.galaxy import Galaxy
from models.planet import Planet
from models.route import Route
from models.spacecraft import Spacecraft
from models.mission import Mission
import tracemalloc
from algorithms.route_planning import a_star_search
from algorithms.resource_allocation import allocate_resources
from algorithms.mission_scheduling import schedule_missions
from algorithms import route_planning
from algorithms.resource_allocation import plan_proactive_resource_supply


def generate_galaxy(
    num_planets,
    num_routes,
    num_spacecraft,
    num_missions
):
    if num_planets < 2:
        raise ValueError("At least 2 planets are required")

    galaxy = Galaxy()

    random.seed(42)

    for i in range(num_planets):
        planet = Planet(
            name=f"Planet-{i}",
            population=random.randint(1000, 1000000),
            resource_production={"energy": random.randint(50, 500)},
            resource_consumption={"energy": random.randint(20, 400)},
            inventory={"energy": random.randint(100, 1000)},
            storage_capacity=2000,
            technology_level=random.randint(1, 10),
            defense_level=random.randint(1, 10),
            strategic_importance=random.randint(1, 10),
            x=random.uniform(0, 1000),
            y=random.uniform(0, 1000)
        )

        galaxy.add_planet(planet)

    for i in range(num_routes):
        origin = f"Planet-{random.randint(0, num_planets - 1)}"
        destination = f"Planet-{random.randint(0, num_planets - 1)}"

        while destination == origin:
            destination = f"Planet-{random.randint(0, num_planets - 1)}"

        route = Route(
            origin=origin,
            destination=destination,
            distance=random.uniform(10, 1000),
            travel_time=random.uniform(1, 100),
            fuel_consumption=random.uniform(10, 500),
            risk=random.uniform(0, 1),
            capacity=random.randint(100, 1000),
            reliability=random.uniform(0.7, 1),
            is_available=True
        )

        galaxy.add_route(route)

    for i in range(num_spacecraft):
        spacecraft = Spacecraft(
            name=f"Spacecraft-{i}",
            current_location=f"Planet-{random.randint(0, num_planets - 1)}",
            cargo_capacity=random.randint(100, 1000),
            fuel_capacity=2000,
            current_fuel=random.randint(500, 2000),
            speed=random.randint(10, 100),
            reliability=random.uniform(0.7, 1),
            operating_cost=random.randint(100, 1000),
            capabilities=["transport", "exploration"],
            available_at=0
        )

        galaxy.add_spacecraft(spacecraft)

    for i in range(num_missions):
        origin = f"Planet-{random.randint(0, num_planets - 1)}"
        destination = f"Planet-{random.randint(0, num_planets - 1)}"

        while destination == origin:
            destination = f"Planet-{random.randint(0, num_planets - 1)}"

        mission = Mission(
            name=f"Mission-{i}",
            origin=origin,
            destination=destination,
            cargo_type="energy",
            cargo_amount=random.randint(50, 200),
            deadline=random.randint(100, 1000),
            priority=random.randint(1, 10),
            importance=random.randint(1, 10),
            required_capabilities=["transport"]
        )

        galaxy.add_mission(mission)

    return galaxy


def measure_execution_time(
    num_planets,
    num_routes,
    num_spacecraft,
    num_missions
):
    start_time = time.perf_counter()

    galaxy = generate_galaxy(
        num_planets,
        num_routes,
        num_spacecraft,
        num_missions
    )

    end_time = time.perf_counter()

    execution_time = end_time - start_time


    return execution_time, galaxy

def measure_memory(
    num_planets,
    num_routes,
    num_spacecraft,
    num_missions
):
    tracemalloc.start()

    galaxy = generate_galaxy(
        num_planets,
        num_routes,
        num_spacecraft,
        num_missions
    )

    weights = {
        "distance": 1,
        "fuel": 1,
        "time": 1,
        "risk": 1
    }

    a_star_search(
        galaxy,
        "Planet-0",
        f"Planet-{len(galaxy.planets) - 1}",
        weights
    )

    allocate_resources(galaxy, "energy")

    schedule_missions(
    galaxy,
    list(galaxy.missions.values()),
    0
)

    current_memory, peak_memory = tracemalloc.get_traced_memory()

    tracemalloc.stop()

    memory_mb = peak_memory / (1024 * 1024)

    return memory_mb, galaxy

def measure_route_planning(galaxy):
    weights = {
        "distance": 1,
        "fuel": 1,
        "time": 1,
        "risk": 1
    }

    start_time = time.perf_counter()

    result = a_star_search(
        galaxy,
        "Planet-0",
        f"Planet-{len(galaxy.planets) - 1}",
        weights
    )

    end_time = time.perf_counter()

    execution_time = end_time - start_time

    return execution_time, result

def measure_resource_allocation(galaxy):
    start_time = time.perf_counter()

    result = allocate_resources(galaxy, "energy")

    end_time = time.perf_counter()

    execution_time = end_time - start_time

    start_time = time.perf_counter()

    proactive_result = plan_proactive_resource_supply(
        galaxy, "energy", 10
    )

    end_time = time.perf_counter()

    proactive_execution_time = end_time - start_time

    return (
        execution_time,
        result,
        proactive_execution_time,
        proactive_result
    )

def measure_mission_scheduling(galaxy):
    missions = list(galaxy.missions.values())

    route_planning.search_count = 0

    start_time = time.perf_counter()

    result = schedule_missions(galaxy, missions, 0)

    searches = route_planning.search_count

    end_time = time.perf_counter()

    execution_time = end_time - start_time

    return execution_time, result, searches

def run_benchmarks():
    datasets = {
        "Small": (100, 500, 50, 50),
        "Medium": (1000, 10000, 100, 500),
        "Large": (10000, 100000, 500, 5000)
    }
    results = {}

    for name, values in datasets.items():
        num_planets, num_routes, num_spacecraft, num_missions = values
        execution_time, galaxy = measure_execution_time(*values)
        memory, _ = measure_memory(*values)
        route_planning_time, route_result = measure_route_planning(galaxy)
        (
            resource_allocation_time,
            allocation_result,
            proactive_resource_time,
            proactive_result
        ) = measure_resource_allocation(galaxy)
        scheduling_galaxy = generate_galaxy(*values)
        mission_scheduling_time, scheduling_result, searches = measure_mission_scheduling(scheduling_galaxy)

        results[name] = {
            "planets": len(galaxy.planets),
            "routes": sum(len(r) for r in galaxy.routes.values()),
            "spacecraft": len(galaxy.spacecraft),
            "missions": len(galaxy.missions),
            "execution_time": execution_time,
            "memory_mb": memory,
            "route_planning_time": route_planning_time,
            "route_found": route_result is not None,
            "resource_allocation_time": resource_allocation_time,
            "allocations_count": len(allocation_result),
            "proactive_resource_time": proactive_resource_time,
            "proactive_allocations_count": len(proactive_result),
            "mission_scheduling_time": mission_scheduling_time,
            "scheduled_missions_count": len(scheduling_result),
            "route_searches": searches
        }

    return results

if __name__ == "__main__":
    results = run_benchmarks()

    for name, data in results.items():
        print(f"\n{name} Dataset")
        print("-" * 30)

        for metric, value in data.items():
            print(f"{metric}: {value}")


