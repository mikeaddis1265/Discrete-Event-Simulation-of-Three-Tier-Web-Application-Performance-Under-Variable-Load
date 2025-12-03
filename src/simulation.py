"""
Discrete-Event Simulation Engine for Three-Tier Web Application with Caching
Implements request generation and processing logic
"""

import simpy
import numpy as np
from typing import Generator
from models import ThreeTierSystem, Server


def request_process(env: simpy.Environment, request_id: int, system: ThreeTierSystem,
                    arrival_time: float) -> Generator:
    """
    Simulate a single request through the three-tier system with caching and load balancing

    Args:
        env: SimPy environment
        request_id: Unique request identifier
        system: ThreeTierSystem instance
        arrival_time: Time when request arrived at system
    """
    # Select application server using load balancer
    app_server = system.load_balancer.select_server(system.app_servers)

    # Process at selected application server
    app_arrival_time = env.now
    app_server.arrivals += 1
    app_server.record_queue_length()

    with app_server.resource.request() as req:
        wait_start = env.now
        yield req
        wait_time = env.now - wait_start
        app_server.total_wait_time += wait_time

        # Service time at app server
        service_time = app_server.get_service_time()
        yield env.timeout(service_time)
        app_server.total_service_time += service_time
        app_server.service_times.append(service_time)
        app_server.response_times.append(wait_time + service_time)
        app_server.departures += 1
        app_server.record_queue_length()

    # Check cache if enabled
    cache_hit = False
    if system.cache_enabled:
        request_key = f"req_{request_id % 1000}"  # Simulate limited dataset
        cache_hit = system.cache.access(request_key)

        if cache_hit:
            # Process at cache server (fast)
            system.cache_server.arrivals += 1
            system.cache_server.record_queue_length()

            with system.cache_server.resource.request() as req:
                wait_start = env.now
                yield req
                wait_time = env.now - wait_start
                system.cache_server.total_wait_time += wait_time

                # Service time at cache server (very fast)
                service_time = system.cache_server.get_service_time()
                yield env.timeout(service_time)
                system.cache_server.total_service_time += service_time
                system.cache_server.service_times.append(service_time)
                system.cache_server.response_times.append(wait_time + service_time)
                system.cache_server.departures += 1
                system.cache_server.record_queue_length()

    # Process at database server only if cache miss or cache disabled
    if not cache_hit:
        db_arrival_time = env.now
        system.db_server.arrivals += 1
        system.db_server.record_queue_length()

        with system.db_server.resource.request() as req:
            wait_start = env.now
            yield req
            wait_time = env.now - wait_start
            system.db_server.total_wait_time += wait_time

            # Service time at db server
            service_time = system.db_server.get_service_time()
            yield env.timeout(service_time)
            system.db_server.total_service_time += service_time
            system.db_server.service_times.append(service_time)
            system.db_server.response_times.append(wait_time + service_time)
            system.db_server.departures += 1
            system.db_server.record_queue_length()

    # Record end-to-end metrics
    end_to_end_time = env.now - arrival_time
    system.end_to_end_times.append(end_to_end_time)
    system.completed_requests += 1


def request_generator(env: simpy.Environment, system: ThreeTierSystem,
                      arrival_rate: float, simulation_time: float) -> Generator:
    """
    Generate requests according to Poisson process

    Args:
        env: SimPy environment
        system: ThreeTierSystem instance
        arrival_rate: Mean arrival rate (λ) in requests/minute
        simulation_time: Total simulation duration in minutes
    """
    request_id = 0

    while env.now < simulation_time:
        # Generate inter-arrival time from exponential distribution
        inter_arrival_time = np.random.exponential(1.0 / arrival_rate)
        yield env.timeout(inter_arrival_time)

        # Check if we're still within simulation time
        if env.now < simulation_time:
            system.total_requests += 1
            arrival_time = env.now
            env.process(request_process(env, request_id, system, arrival_time))
            request_id += 1


def run_simulation(arrival_rate: float, app_service_rate: float = 60,
                   db_service_rate: float = 30, simulation_time: float = 60,
                   cache_enabled: bool = True, cache_hit_rate: float = 0.3,
                   cache_service_rate: float = 300, num_app_servers: int = 1,
                   load_balancing_strategy: str = 'round_robin', random_seed: int = None) -> dict:
    """
    Run a single simulation experiment

    Args:
        arrival_rate: Mean arrival rate (λ) in requests/minute
        app_service_rate: Application server service rate (μ) in requests/minute
        db_service_rate: Database server service rate (μ) in requests/minute
        simulation_time: Duration of simulation in minutes
        cache_enabled: Whether caching is enabled
        cache_hit_rate: Cache hit probability (0.0 to 1.0)
        cache_service_rate: Cache server service rate (req/min)
        num_app_servers: Number of application servers
        load_balancing_strategy: Load balancing strategy ('round_robin', 'random', 'least_connections')
        random_seed: Random seed for reproducibility

    Returns:
        Dictionary containing simulation metrics
    """
    if random_seed is not None:
        np.random.seed(random_seed)

    # Create simulation environment
    env = simpy.Environment()

    # Create three-tier system with caching and load balancing
    system = ThreeTierSystem(env, app_service_rate, db_service_rate,
                            cache_enabled, cache_hit_rate, cache_service_rate,
                            num_app_servers, load_balancing_strategy)

    # Start request generator
    env.process(request_generator(env, system, arrival_rate, simulation_time))

    # Run simulation
    env.run(until=simulation_time)

    # Collect and return metrics
    metrics = system.get_metrics()
    metrics['parameters'] = {
        'arrival_rate': arrival_rate,
        'app_service_rate': app_service_rate,
        'db_service_rate': db_service_rate,
        'cache_enabled': cache_enabled,
        'cache_hit_rate': cache_hit_rate if cache_enabled else None,
        'cache_service_rate': cache_service_rate if cache_enabled else None,
        'num_app_servers': num_app_servers,
        'load_balancing_strategy': load_balancing_strategy,
        'simulation_time': simulation_time,
        'random_seed': random_seed
    }

    return metrics


def run_multiple_replications(arrival_rate: float, num_replications: int = 10,
                               app_service_rate: float = 60, db_service_rate: float = 30,
                               simulation_time: float = 60, cache_enabled: bool = True,
                               cache_hit_rate: float = 0.3, cache_service_rate: float = 300,
                               num_app_servers: int = 1, load_balancing_strategy: str = 'round_robin') -> list:
    """
    Run multiple replications of the simulation

    Args:
        arrival_rate: Mean arrival rate (λ) in requests/minute
        num_replications: Number of independent replications
        app_service_rate: Application server service rate (μ) in requests/minute
        db_service_rate: Database server service rate (μ) in requests/minute
        simulation_time: Duration of each simulation in minutes
        cache_enabled: Whether caching is enabled
        cache_hit_rate: Cache hit probability (0.0 to 1.0)
        cache_service_rate: Cache server service rate (req/min)
        num_app_servers: Number of application servers
        load_balancing_strategy: Load balancing strategy ('round_robin', 'random', 'least_connections')

    Returns:
        List of metric dictionaries, one per replication
    """
    results = []

    for i in range(num_replications):
        metrics = run_simulation(
            arrival_rate=arrival_rate,
            app_service_rate=app_service_rate,
            db_service_rate=db_service_rate,
            simulation_time=simulation_time,
            cache_enabled=cache_enabled,
            cache_hit_rate=cache_hit_rate,
            cache_service_rate=cache_service_rate,
            num_app_servers=num_app_servers,
            load_balancing_strategy=load_balancing_strategy,
            random_seed=i
        )
        results.append(metrics)

    return results
