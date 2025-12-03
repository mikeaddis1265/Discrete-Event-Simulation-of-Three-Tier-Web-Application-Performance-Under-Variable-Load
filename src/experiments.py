"""
Experiment Runner for Three-Tier Web Application Simulation
Defines and executes simulation scenarios
"""

import numpy as np
import pandas as pd
from typing import Dict, List
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.dirname(__file__))

from simulation import run_simulation, run_multiple_replications
from outputs import aggregate_replications, calculate_confidence_intervals, plot_response_time_vs_load, plot_utilization_comparison


class ExperimentConfig:
    """Configuration for simulation experiments"""

    def __init__(self, name: str, arrival_rate: float, app_service_rate: float = 60,
                 db_service_rate: float = 30, cache_enabled: bool = True,
                 cache_hit_rate: float = 0.3, cache_service_rate: float = 300,
                 num_app_servers: int = 1, load_balancing_strategy: str = 'round_robin',
                 simulation_time: float = 60, num_replications: int = 10):
        """
        Initialize experiment configuration

        Args:
            name: Experiment/scenario name
            arrival_rate: Mean arrival rate (λ) in requests/minute
            app_service_rate: Application server service rate (μ) in requests/minute
            db_service_rate: Database server service rate (μ) in requests/minute
            cache_enabled: Whether caching is enabled
            cache_hit_rate: Cache hit probability (0.0 to 1.0)
            cache_service_rate: Cache server service rate (req/min)
            num_app_servers: Number of application servers
            load_balancing_strategy: Load balancing strategy ('round_robin', 'random', 'least_connections')
            simulation_time: Duration of simulation in minutes
            num_replications: Number of independent replications
        """
        self.name = name
        self.arrival_rate = arrival_rate
        self.app_service_rate = app_service_rate
        self.db_service_rate = db_service_rate
        self.cache_enabled = cache_enabled
        self.cache_hit_rate = cache_hit_rate
        self.cache_service_rate = cache_service_rate
        self.num_app_servers = num_app_servers
        self.load_balancing_strategy = load_balancing_strategy
        self.simulation_time = simulation_time
        self.num_replications = num_replications

    def to_dict(self) -> Dict:
        """Convert configuration to dictionary"""
        return {
            'name': self.name,
            'arrival_rate': self.arrival_rate,
            'app_service_rate': self.app_service_rate,
            'db_service_rate': self.db_service_rate,
            'cache_enabled': self.cache_enabled,
            'cache_hit_rate': self.cache_hit_rate,
            'cache_service_rate': self.cache_service_rate,
            'num_app_servers': self.num_app_servers,
            'load_balancing_strategy': self.load_balancing_strategy,
            'simulation_time': self.simulation_time,
            'num_replications': self.num_replications
        }


def run_experiment(config: ExperimentConfig) -> Dict:
    """
    Run a complete experiment with multiple replications

    Args:
        config: ExperimentConfig instance

    Returns:
        Dictionary with raw results, aggregated DataFrame, and summary statistics
    """
    print(f"\nRunning experiment: {config.name}")
    print(f"  Arrival rate: {config.arrival_rate} req/min")
    print(f"  Number of app servers: {config.num_app_servers}")
    print(f"  Load balancing: {config.load_balancing_strategy}")
    print(f"  Cache enabled: {config.cache_enabled}")
    if config.cache_enabled:
        print(f"  Cache hit rate: {config.cache_hit_rate}")
    print(f"  Replications: {config.num_replications}")

    # Run multiple replications
    results = run_multiple_replications(
        arrival_rate=config.arrival_rate,
        num_replications=config.num_replications,
        app_service_rate=config.app_service_rate,
        db_service_rate=config.db_service_rate,
        simulation_time=config.simulation_time,
        cache_enabled=config.cache_enabled,
        cache_hit_rate=config.cache_hit_rate,
        cache_service_rate=config.cache_service_rate,
        num_app_servers=config.num_app_servers,
        load_balancing_strategy=config.load_balancing_strategy
    )

    # Aggregate results
    df = aggregate_replications(results)

    # Calculate confidence intervals
    summary = calculate_confidence_intervals(df)

    print(f"  Completed {config.num_replications} replications")
    print(f"  Mean end-to-end response time: {summary[summary['metric'] == 'system_avg_end_to_end_time']['mean'].values[0]:.4f} min")

    return {
        'config': config.to_dict(),
        'raw_results': results,
        'replications_df': df,
        'summary': summary,
        'parameters': config.to_dict()
    }


def run_standard_scenarios() -> Dict:
    """
    Run the three standard scenarios: low, medium, high load

    Returns:
        Dictionary mapping scenario names to experiment results
    """
    scenarios = {
        'low_load': ExperimentConfig(
            name='Low Load',
            arrival_rate=10,  # 10 req/min
            cache_enabled=True,
            cache_hit_rate=0.3,
            num_replications=10
        ),
        'medium_load': ExperimentConfig(
            name='Medium Load',
            arrival_rate=50,  # 50 req/min
            cache_enabled=True,
            cache_hit_rate=0.3,
            num_replications=10
        ),
        'high_load': ExperimentConfig(
            name='High Load',
            arrival_rate=200,  # 200 req/min
            cache_enabled=True,
            cache_hit_rate=0.3,
            num_replications=10
        )
    }

    results = {}

    for scenario_name, config in scenarios.items():
        results[scenario_name] = run_experiment(config)

    return results


def run_cache_comparison() -> Dict:
    """
    Compare performance with and without caching

    Returns:
        Dictionary with comparison results
    """
    load_rates = [10, 50, 100, 200]
    results = {'with_cache': {}, 'without_cache': {}}

    for rate in load_rates:
        # With cache
        config_cached = ExperimentConfig(
            name=f'Cached-{rate}req/min',
            arrival_rate=rate,
            cache_enabled=True,
            cache_hit_rate=0.3,
            num_replications=10
        )
        results['with_cache'][rate] = run_experiment(config_cached)

        # Without cache
        config_uncached = ExperimentConfig(
            name=f'Uncached-{rate}req/min',
            arrival_rate=rate,
            cache_enabled=False,
            num_replications=10
        )
        results['without_cache'][rate] = run_experiment(config_uncached)

    return results


def run_cache_hit_rate_sensitivity() -> Dict:
    """
    Analyze sensitivity to cache hit rate

    Returns:
        Dictionary with sensitivity analysis results
    """
    hit_rates = [0.0, 0.2, 0.4, 0.6, 0.8]
    arrival_rate = 100  # Medium load
    results = {}

    for hit_rate in hit_rates:
        config = ExperimentConfig(
            name=f'CacheHitRate-{hit_rate}',
            arrival_rate=arrival_rate,
            cache_enabled=True if hit_rate > 0 else False,
            cache_hit_rate=hit_rate,
            num_replications=10
        )
        results[hit_rate] = run_experiment(config)

    return results


def save_experiment_results(results: Dict, output_dir: str = '../results'):
    """
    Save experiment results to CSV files

    Args:
        results: Dictionary with experiment results
        output_dir: Output directory path
    """
    os.makedirs(output_dir, exist_ok=True)

    for scenario_name, result in results.items():
        # Save replication data
        rep_path = os.path.join(output_dir, f'{scenario_name}_replications.csv')
        result['replications_df'].to_csv(rep_path, index=False)

        # Save summary statistics
        summary_path = os.path.join(output_dir, f'{scenario_name}_summary.csv')
        result['summary'].to_csv(summary_path, index=False)

    print(f"\nResults saved to {output_dir}")


if __name__ == '__main__':
    print("=" * 60)
    print("Three-Tier Web Application Performance Simulation")
    print("Discrete-Event Simulation with Caching")
    print("=" * 60)

    # Run standard scenarios
    print("\n### Running Standard Scenarios ###")
    scenario_results = run_standard_scenarios()

    # Save results
    save_experiment_results(scenario_results, output_dir='../results')

    # Generate plots
    print("\n### Generating Plots ###")
    os.makedirs('../results/plots', exist_ok=True)

    plot_response_time_vs_load(scenario_results,
                               output_path='../results/plots/response_time_vs_load.png')
    plot_utilization_comparison(scenario_results,
                                output_path='../results/plots/utilization_comparison.png')

    print("\nPlots saved to ../results/plots")

    # Print summary
    print("\n" + "=" * 60)
    print("SUMMARY OF RESULTS")
    print("=" * 60)

    for scenario_name, result in scenario_results.items():
        print(f"\n{result['config']['name']}:")
        summary = result['summary']

        metrics_to_show = [
            'system_avg_end_to_end_time',
            'app_utilization',
            'db_utilization',
            'app_avg_queue_length',
            'db_avg_queue_length'
        ]

        if 'cache_hit_rate' in summary['metric'].values:
            metrics_to_show.append('cache_hit_rate')

        for metric in metrics_to_show:
            row = summary[summary['metric'] == metric]
            if not row.empty:
                mean = row['mean'].values[0]
                ci_lower = row['ci_lower'].values[0]
                ci_upper = row['ci_upper'].values[0]
                print(f"  {metric}: {mean:.4f} (95% CI: [{ci_lower:.4f}, {ci_upper:.4f}])")

    print("\n" + "=" * 60)
    print("Experiment completed successfully!")
    print("=" * 60)
