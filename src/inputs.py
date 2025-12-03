"""
Input Data Generation and Analysis
Generates synthetic Poisson arrivals and analyzes distributions
"""

import numpy as np
import pandas as pd
from scipy import stats
from typing import Tuple, Dict


def generate_poisson_arrivals(arrival_rate: float, duration: float,
                               random_seed: int = 42) -> pd.DataFrame:
    """
    Generate synthetic Poisson arrival process

    Args:
        arrival_rate: Mean arrival rate (λ) in requests/minute
        duration: Time duration in minutes
        random_seed: Random seed for reproducibility

    Returns:
        DataFrame with arrival times and inter-arrival times
    """
    np.random.seed(random_seed)

    arrivals = []
    current_time = 0.0

    while current_time < duration:
        # Generate inter-arrival time from exponential distribution
        inter_arrival_time = np.random.exponential(1.0 / arrival_rate)
        current_time += inter_arrival_time

        if current_time < duration:
            arrivals.append({
                'arrival_time': current_time,
                'inter_arrival_time': inter_arrival_time
            })

    df = pd.DataFrame(arrivals)
    df['request_id'] = range(len(df))

    return df


def fit_exponential_distribution(data: np.ndarray) -> Tuple[float, Dict]:
    """
    Fit exponential distribution to data and perform goodness-of-fit test

    Args:
        data: Array of inter-arrival times or service times

    Returns:
        Tuple of (fitted rate parameter, test statistics dict)
    """
    # Fit exponential distribution
    loc, scale = stats.expon.fit(data, floc=0)
    fitted_rate = 1.0 / scale

    # Kolmogorov-Smirnov test
    ks_statistic, ks_pvalue = stats.kstest(data, 'expon', args=(loc, scale))

    # Chi-square goodness-of-fit test with robust error handling
    try:
        hist, bin_edges = np.histogram(data, bins=20)
        expected_freq = len(data) * np.diff(stats.expon.cdf(bin_edges, loc, scale))

        # Filter out bins with expected frequency < 5 first
        valid_bins = expected_freq >= 5

        if np.sum(valid_bins) > 1:
            obs = hist[valid_bins].astype(float)
            exp = expected_freq[valid_bins].astype(float)

            # Ensure sums match exactly by normalizing
            if exp.sum() > 0:
                exp = exp * (obs.sum() / exp.sum())

            # Use ddof parameter to avoid the sum mismatch error
            chi2_statistic, chi2_pvalue = stats.chisquare(obs, exp, ddof=0)
        else:
            chi2_statistic, chi2_pvalue = np.nan, np.nan
    except (ValueError, RuntimeWarning, Exception) as e:
        # If any error occurs, skip chi-square test
        chi2_statistic, chi2_pvalue = np.nan, np.nan

    test_results = {
        'fitted_rate': fitted_rate,
        'fitted_scale': scale,
        'ks_statistic': ks_statistic,
        'ks_pvalue': ks_pvalue,
        'chi2_statistic': chi2_statistic,
        'chi2_pvalue': chi2_pvalue,
        'mean': np.mean(data),
        'std': np.std(data),
        'theoretical_mean': scale,
        'theoretical_std': scale
    }

    return fitted_rate, test_results


def fit_poisson_distribution(data: np.ndarray, interval: float = 1.0) -> Tuple[float, Dict]:
    """
    Fit Poisson distribution to arrival count data

    Args:
        data: Array of arrival counts per interval
        interval: Time interval in minutes

    Returns:
        Tuple of (fitted arrival rate, test statistics dict)
    """
    # Fit Poisson distribution
    fitted_lambda = np.mean(data)

    # Chi-square goodness-of-fit test
    unique_counts, observed_freq = np.unique(data, return_counts=True)
    max_count = int(np.max(unique_counts))

    # Calculate expected frequencies
    expected_freq = []
    for k in range(max_count + 1):
        expected_freq.append(len(data) * stats.poisson.pmf(k, fitted_lambda))

    expected_freq = np.array(expected_freq)

    # Combine bins with expected frequency < 5
    combined_observed = []
    combined_expected = []
    temp_obs = 0
    temp_exp = 0

    for i in range(len(expected_freq)):
        temp_exp += expected_freq[i]
        if i < len(observed_freq):
            temp_obs += observed_freq[i]

        if temp_exp >= 5 or i == len(expected_freq) - 1:
            combined_observed.append(temp_obs)
            combined_expected.append(temp_exp)
            temp_obs = 0
            temp_exp = 0

    if len(combined_observed) > 1:
        try:
            # Normalize to ensure sums match
            combined_expected = np.array(combined_expected)
            combined_observed = np.array(combined_observed)
            combined_expected = combined_expected * (combined_observed.sum() / combined_expected.sum())

            chi2_statistic, chi2_pvalue = stats.chisquare(combined_observed, combined_expected)
        except (ValueError, ZeroDivisionError):
            chi2_statistic, chi2_pvalue = np.nan, np.nan
    else:
        chi2_statistic, chi2_pvalue = np.nan, np.nan

    test_results = {
        'fitted_lambda': fitted_lambda,
        'arrival_rate': fitted_lambda / interval,
        'chi2_statistic': chi2_statistic,
        'chi2_pvalue': chi2_pvalue,
        'mean': np.mean(data),
        'variance': np.var(data),
        'theoretical_mean': fitted_lambda,
        'theoretical_variance': fitted_lambda
    }

    return fitted_lambda / interval, test_results


def analyze_arrivals(df: pd.DataFrame, interval: float = 1.0) -> Dict:
    """
    Comprehensive analysis of arrival data

    Args:
        df: DataFrame with arrival times
        interval: Time interval for counting arrivals (minutes)

    Returns:
        Dictionary with analysis results
    """
    # Inter-arrival time analysis
    inter_arrival_times = df['inter_arrival_time'].values
    fitted_rate, exponential_stats = fit_exponential_distribution(inter_arrival_times)

    # Count arrivals per interval
    max_time = df['arrival_time'].max()
    bins = np.arange(0, max_time + interval, interval)
    arrival_counts, _ = np.histogram(df['arrival_time'], bins=bins)

    # Poisson distribution analysis
    poisson_rate, poisson_stats = fit_poisson_distribution(arrival_counts, interval)

    return {
        'exponential_fit': exponential_stats,
        'poisson_fit': poisson_stats,
        'total_arrivals': len(df),
        'duration': max_time,
        'empirical_arrival_rate': len(df) / max_time
    }


def generate_synthetic_data(output_path: str = None) -> pd.DataFrame:
    """
    Generate synthetic arrival data for the simulation project

    Args:
        output_path: Path to save CSV file (optional)

    Returns:
        DataFrame with synthetic arrival data
    """
    # Generate data for different load scenarios
    scenarios = {
        'low_load': 10,    # 10 req/min
        'medium_load': 50, # 50 req/min
        'high_load': 200   # 200 req/min
    }

    all_data = []

    for scenario_name, rate in scenarios.items():
        df = generate_poisson_arrivals(arrival_rate=rate, duration=60)
        df['scenario'] = scenario_name
        df['theoretical_rate'] = rate
        all_data.append(df)

    combined_df = pd.concat(all_data, ignore_index=True)

    if output_path:
        combined_df.to_csv(output_path, index=False)

    return combined_df
