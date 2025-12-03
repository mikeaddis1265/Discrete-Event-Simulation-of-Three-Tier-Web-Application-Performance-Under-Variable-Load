"""
Output Analysis and Visualization
Processes simulation results and generates plots
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from typing import List, Dict, Tuple
import os


# Set plotting style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (10, 6)


def aggregate_replications(results: List[Dict]) -> pd.DataFrame:
    """
    Aggregate results from multiple replications

    Args:
        results: List of metric dictionaries from replications

    Returns:
        DataFrame with aggregated statistics
    """
    metrics_data = []

    for i, result in enumerate(results):
        row = {
            'replication': i,
            'app_utilization': result['app_server']['utilization'],
            'app_avg_queue_length': result['app_server']['avg_queue_length'],
            'app_avg_response_time': result['app_server']['avg_response_time'],
            'app_throughput': result['app_server']['throughput'],
            'db_utilization': result['db_server']['utilization'],
            'db_avg_queue_length': result['db_server']['avg_queue_length'],
            'db_avg_response_time': result['db_server']['avg_response_time'],
            'db_throughput': result['db_server']['throughput'],
            'system_avg_end_to_end_time': result['system']['avg_end_to_end_time'],
            'system_throughput': result['system']['system_throughput'],
            'total_requests': result['system']['total_requests'],
            'completed_requests': result['system']['completed_requests']
        }

        # Add cache metrics if available
        if 'cache' in result:
            row['cache_hit_rate'] = result['cache']['hit_rate']
            row['cache_hits'] = result['cache']['hits']
            row['cache_misses'] = result['cache']['misses']
            row['cache_server_utilization'] = result['cache_server']['utilization']
            row['cache_server_avg_response_time'] = result['cache_server']['avg_response_time']

        metrics_data.append(row)

    return pd.DataFrame(metrics_data)


def calculate_confidence_intervals(df: pd.DataFrame, confidence: float = 0.95) -> pd.DataFrame:
    """
    Calculate confidence intervals for metrics

    Args:
        df: DataFrame with replication results
        confidence: Confidence level (default 0.95)

    Returns:
        DataFrame with mean, std, and confidence intervals
    """
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    numeric_cols = [col for col in numeric_cols if col != 'replication']

    summary_data = []

    for col in numeric_cols:
        data = df[col].values
        mean = np.mean(data)
        std = np.std(data, ddof=1)
        n = len(data)

        # t-distribution confidence interval
        t_critical = stats.t.ppf((1 + confidence) / 2, n - 1)
        margin_error = t_critical * (std / np.sqrt(n))

        summary_data.append({
            'metric': col,
            'mean': mean,
            'std': std,
            'ci_lower': mean - margin_error,
            'ci_upper': mean + margin_error,
            'margin_error': margin_error
        })

    return pd.DataFrame(summary_data)


def analytical_mm1_metrics(arrival_rate: float, service_rate: float) -> Dict:
    """
    Calculate analytical M/M/1 queue metrics

    Args:
        arrival_rate: Mean arrival rate (λ)
        service_rate: Mean service rate (μ)

    Returns:
        Dictionary with analytical metrics
    """
    if arrival_rate >= service_rate:
        return {
            'utilization': float('inf'),
            'avg_queue_length': float('inf'),
            'avg_response_time': float('inf'),
            'avg_waiting_time': float('inf'),
            'throughput': arrival_rate
        }

    rho = arrival_rate / service_rate  # Utilization
    L = rho / (1 - rho)  # Average number in system
    W = L / arrival_rate  # Average time in system
    Lq = rho * rho / (1 - rho)  # Average queue length
    Wq = Lq / arrival_rate  # Average waiting time in queue

    return {
        'utilization': rho,
        'avg_queue_length': Lq,
        'avg_number_in_system': L,
        'avg_response_time': W,
        'avg_waiting_time': Wq,
        'throughput': arrival_rate
    }


def compare_with_analytical(simulation_results: pd.DataFrame, arrival_rate: float,
                            app_service_rate: float, db_service_rate: float) -> pd.DataFrame:
    """
    Compare simulation results with analytical M/M/1 formulas

    Args:
        simulation_results: DataFrame with simulation metrics
        arrival_rate: Arrival rate used in simulation
        app_service_rate: Application server service rate
        db_service_rate: Database server service rate

    Returns:
        DataFrame comparing simulation and analytical results
    """
    # Calculate analytical metrics for each tier
    app_analytical = analytical_mm1_metrics(arrival_rate, app_service_rate)
    db_analytical = analytical_mm1_metrics(arrival_rate, db_service_rate)

    comparison_data = []

    # Application server comparison
    comparison_data.append({
        'tier': 'Application Server',
        'metric': 'Utilization',
        'simulation': simulation_results[simulation_results['metric'] == 'app_utilization']['mean'].values[0],
        'analytical': app_analytical['utilization'],
        'error': abs(simulation_results[simulation_results['metric'] == 'app_utilization']['mean'].values[0] - app_analytical['utilization'])
    })

    comparison_data.append({
        'tier': 'Application Server',
        'metric': 'Avg Queue Length',
        'simulation': simulation_results[simulation_results['metric'] == 'app_avg_queue_length']['mean'].values[0],
        'analytical': app_analytical['avg_queue_length'],
        'error': abs(simulation_results[simulation_results['metric'] == 'app_avg_queue_length']['mean'].values[0] - app_analytical['avg_queue_length'])
    })

    comparison_data.append({
        'tier': 'Application Server',
        'metric': 'Avg Response Time',
        'simulation': simulation_results[simulation_results['metric'] == 'app_avg_response_time']['mean'].values[0],
        'analytical': app_analytical['avg_response_time'],
        'error': abs(simulation_results[simulation_results['metric'] == 'app_avg_response_time']['mean'].values[0] - app_analytical['avg_response_time'])
    })

    # Database server comparison
    comparison_data.append({
        'tier': 'Database Server',
        'metric': 'Utilization',
        'simulation': simulation_results[simulation_results['metric'] == 'db_utilization']['mean'].values[0],
        'analytical': db_analytical['utilization'],
        'error': abs(simulation_results[simulation_results['metric'] == 'db_utilization']['mean'].values[0] - db_analytical['utilization'])
    })

    comparison_data.append({
        'tier': 'Database Server',
        'metric': 'Avg Queue Length',
        'simulation': simulation_results[simulation_results['metric'] == 'db_avg_queue_length']['mean'].values[0],
        'analytical': db_analytical['avg_queue_length'],
        'error': abs(simulation_results[simulation_results['metric'] == 'db_avg_queue_length']['mean'].values[0] - db_analytical['avg_queue_length'])
    })

    comparison_data.append({
        'tier': 'Database Server',
        'metric': 'Avg Response Time',
        'simulation': simulation_results[simulation_results['metric'] == 'db_avg_response_time']['mean'].values[0],
        'analytical': db_analytical['avg_response_time'],
        'error': abs(simulation_results[simulation_results['metric'] == 'db_avg_response_time']['mean'].values[0] - db_analytical['avg_response_time'])
    })

    return pd.DataFrame(comparison_data)


def plot_response_time_vs_load(scenario_results: Dict, output_path: str = None):
    """
    Plot response time vs load for different scenarios

    Args:
        scenario_results: Dict mapping scenario names to summary DataFrames
        output_path: Path to save plot (optional)
    """
    fig, ax = plt.subplots(figsize=(12, 6))

    scenarios = list(scenario_results.keys())
    arrival_rates = [scenario_results[s]['parameters']['arrival_rate'] for s in scenarios]

    # Plot for each tier
    app_response_times = [
        scenario_results[s]['summary'][scenario_results[s]['summary']['metric'] == 'app_avg_response_time']['mean'].values[0]
        for s in scenarios
    ]
    db_response_times = [
        scenario_results[s]['summary'][scenario_results[s]['summary']['metric'] == 'db_avg_response_time']['mean'].values[0]
        for s in scenarios
    ]
    system_response_times = [
        scenario_results[s]['summary'][scenario_results[s]['summary']['metric'] == 'system_avg_end_to_end_time']['mean'].values[0]
        for s in scenarios
    ]

    ax.plot(arrival_rates, app_response_times, marker='o', label='App Server', linewidth=2)
    ax.plot(arrival_rates, db_response_times, marker='s', label='DB Server', linewidth=2)
    ax.plot(arrival_rates, system_response_times, marker='^', label='End-to-End', linewidth=2)

    ax.set_xlabel('Arrival Rate (requests/min)', fontsize=12)
    ax.set_ylabel('Average Response Time (min)', fontsize=12)
    ax.set_title('Response Time vs. Load', fontsize=14, fontweight='bold')
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)

    plt.tight_layout()

    if output_path:
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
    else:
        return fig


def plot_utilization_comparison(scenario_results: Dict, output_path: str = None):
    """
    Plot utilization comparison across scenarios

    Args:
        scenario_results: Dict mapping scenario names to summary DataFrames
        output_path: Path to save plot (optional)
    """
    fig, ax = plt.subplots(figsize=(10, 6))

    scenarios = list(scenario_results.keys())
    x = np.arange(len(scenarios))
    width = 0.35

    app_util = [
        scenario_results[s]['summary'][scenario_results[s]['summary']['metric'] == 'app_utilization']['mean'].values[0]
        for s in scenarios
    ]
    db_util = [
        scenario_results[s]['summary'][scenario_results[s]['summary']['metric'] == 'db_utilization']['mean'].values[0]
        for s in scenarios
    ]

    ax.bar(x - width/2, app_util, width, label='App Server', alpha=0.8)
    ax.bar(x + width/2, db_util, width, label='DB Server', alpha=0.8)

    ax.set_xlabel('Scenario', fontsize=12)
    ax.set_ylabel('Utilization', fontsize=12)
    ax.set_title('Server Utilization Comparison', fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(scenarios, rotation=45, ha='right')
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3, axis='y')
    ax.set_ylim(0, 1.0)

    plt.tight_layout()

    if output_path:
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
    else:
        return fig
