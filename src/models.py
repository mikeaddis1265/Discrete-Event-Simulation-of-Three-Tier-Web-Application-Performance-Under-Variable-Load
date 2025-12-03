"""
Models for Three-Tier Web Application Simulation with Caching
Contains server, cache, and queue definitions using SimPy
"""

import simpy
import numpy as np
from typing import Dict, List
from collections import OrderedDict


class Cache:
    """LRU Cache implementation for the web application"""

    def __init__(self, capacity: int = 100, hit_rate: float = 0.3):
        """
        Initialize cache

        Args:
            capacity: Maximum number of items in cache
            hit_rate: Probability of cache hit (0.0 to 1.0)
        """
        self.capacity = capacity
        self.hit_rate = hit_rate
        self.cache_store = OrderedDict()

        # Metrics
        self.hits = 0
        self.misses = 0
        self.total_requests = 0

    def access(self, key: str) -> bool:
        """
        Simulate cache access

        Args:
            key: Cache key to access

        Returns:
            True if cache hit, False if cache miss
        """
        self.total_requests += 1

        # Simulate cache hit/miss based on hit rate
        is_hit = np.random.random() < self.hit_rate

        if is_hit:
            self.hits += 1
            # Move to end (LRU)
            if key in self.cache_store:
                self.cache_store.move_to_end(key)
            else:
                self.cache_store[key] = True
                if len(self.cache_store) > self.capacity:
                    self.cache_store.popitem(last=False)
            return True
        else:
            self.misses += 1
            # Add to cache
            self.cache_store[key] = True
            if len(self.cache_store) > self.capacity:
                self.cache_store.popitem(last=False)
            return False

    def get_hit_rate(self) -> float:
        """Calculate actual cache hit rate"""
        if self.total_requests == 0:
            return 0.0
        return self.hits / self.total_requests

    def get_metrics(self) -> Dict:
        """Get cache metrics"""
        return {
            'total_requests': self.total_requests,
            'hits': self.hits,
            'misses': self.misses,
            'hit_rate': self.get_hit_rate(),
            'capacity': self.capacity,
            'current_size': len(self.cache_store)
        }


class Server:
    """Represents a server tier in the web application (M/M/1 queue)"""

    def __init__(self, env: simpy.Environment, name: str, service_rate: float):
        """
        Initialize a server tier

        Args:
            env: SimPy environment
            name: Server tier name (e.g., 'app', 'db', 'cache')
            service_rate: Mean service rate (μ) in requests/minute
        """
        self.env = env
        self.name = name
        self.service_rate = service_rate
        self.resource = simpy.Resource(env, capacity=1)

        # Metrics tracking
        self.queue_lengths = []
        self.queue_times = []
        self.service_times = []
        self.response_times = []
        self.arrivals = 0
        self.departures = 0
        self.total_wait_time = 0
        self.total_service_time = 0

    def get_service_time(self) -> float:
        """Generate exponential service time based on service rate"""
        return np.random.exponential(1.0 / self.service_rate)

    def record_queue_length(self):
        """Record current queue length (waiting only, not being served)"""
        queue_len = len(self.resource.queue)  # Only count waiting requests (L_q), not in service
        self.queue_lengths.append((self.env.now, queue_len))

    def get_utilization(self) -> float:
        """Calculate server utilization"""
        if self.env.now == 0:
            return 0.0
        return self.total_service_time / self.env.now

    def get_avg_queue_length(self) -> float:
        """Calculate time-weighted average queue length"""
        if not self.queue_lengths or len(self.queue_lengths) < 2:
            return 0.0

        total_area = 0.0
        for i in range(1, len(self.queue_lengths)):
            time_diff = self.queue_lengths[i][0] - self.queue_lengths[i-1][0]
            total_area += self.queue_lengths[i-1][1] * time_diff

        return total_area / self.env.now if self.env.now > 0 else 0.0

    def get_avg_response_time(self) -> float:
        """Calculate average response time"""
        return np.mean(self.response_times) if self.response_times else 0.0

    def get_throughput(self) -> float:
        """Calculate throughput (departures per time unit)"""
        return self.departures / self.env.now if self.env.now > 0 else 0.0

    def get_metrics(self) -> Dict:
        """Get server metrics"""
        return {
            'utilization': self.get_utilization(),
            'avg_queue_length': self.get_avg_queue_length(),
            'avg_response_time': self.get_avg_response_time(),
            'throughput': self.get_throughput(),
            'arrivals': self.arrivals,
            'departures': self.departures
        }


class LoadBalancer:
    """Load balancer for distributing requests across multiple servers"""

    def __init__(self, strategy: str = 'round_robin'):
        """
        Initialize load balancer

        Args:
            strategy: Load balancing strategy ('round_robin', 'random', 'least_connections')
        """
        self.strategy = strategy
        self.current_index = 0
        self.total_requests = 0

    def select_server(self, servers: List[Server]) -> Server:
        """
        Select a server based on the load balancing strategy

        Args:
            servers: List of available servers

        Returns:
            Selected server
        """
        self.total_requests += 1

        if self.strategy == 'round_robin':
            server = servers[self.current_index]
            self.current_index = (self.current_index + 1) % len(servers)
            return server

        elif self.strategy == 'random':
            return np.random.choice(servers)

        elif self.strategy == 'least_connections':
            # Select server with fewest active connections
            min_connections = min(len(s.resource.queue) + len(s.resource.users) for s in servers)
            candidates = [s for s in servers if len(s.resource.queue) + len(s.resource.users) == min_connections]
            return candidates[0] if len(candidates) == 1 else np.random.choice(candidates)

        else:
            # Default to round robin
            return self.select_server(servers)


class ThreeTierSystem:
    """Represents the complete three-tier web application system with caching and load balancing"""

    def __init__(self, env: simpy.Environment, app_service_rate: float = 60,
                 db_service_rate: float = 30, cache_enabled: bool = True,
                 cache_hit_rate: float = 0.3, cache_service_rate: float = 300,
                 num_app_servers: int = 1, load_balancing_strategy: str = 'round_robin'):
        """
        Initialize the three-tier system

        Args:
            env: SimPy environment
            app_service_rate: Application server service rate (req/min)
            db_service_rate: Database server service rate (req/min)
            cache_enabled: Whether caching is enabled
            cache_hit_rate: Cache hit probability (0.0 to 1.0)
            cache_service_rate: Cache server service rate (req/min)
            num_app_servers: Number of application servers
            load_balancing_strategy: Strategy for load balancing ('round_robin', 'random', 'least_connections')
        """
        self.env = env
        self.num_app_servers = num_app_servers
        self.load_balancing_strategy = load_balancing_strategy

        # Create multiple application servers
        self.app_servers = [
            Server(env, f"app_{i}", app_service_rate)
            for i in range(num_app_servers)
        ]

        # Create load balancer
        self.load_balancer = LoadBalancer(strategy=load_balancing_strategy)

        # Single database server
        self.db_server = Server(env, "db", db_service_rate)

        # Cache configuration
        self.cache_enabled = cache_enabled
        if cache_enabled:
            self.cache = Cache(capacity=100, hit_rate=cache_hit_rate)
            self.cache_server = Server(env, "cache", cache_service_rate)
        else:
            self.cache = None
            self.cache_server = None

        self.total_requests = 0
        self.completed_requests = 0
        self.end_to_end_times = []

    def get_metrics(self) -> Dict:
        """Get comprehensive system metrics"""
        # Aggregate metrics across all app servers
        total_app_arrivals = sum(s.arrivals for s in self.app_servers)
        total_app_departures = sum(s.departures for s in self.app_servers)
        total_app_service_time = sum(s.total_service_time for s in self.app_servers)

        # Average metrics across app servers
        avg_app_utilization = np.mean([s.get_utilization() for s in self.app_servers])
        avg_app_queue_length = np.mean([s.get_avg_queue_length() for s in self.app_servers])
        avg_app_response_time = np.mean([s.get_avg_response_time() for s in self.app_servers])
        avg_app_throughput = np.mean([s.get_throughput() for s in self.app_servers])

        metrics = {
            'app_server': {
                'utilization': avg_app_utilization,
                'avg_queue_length': avg_app_queue_length,
                'avg_response_time': avg_app_response_time,
                'throughput': avg_app_throughput,
                'arrivals': total_app_arrivals,
                'departures': total_app_departures
            },
            'app_servers_individual': [
                {
                    'name': s.name,
                    **s.get_metrics()
                }
                for s in self.app_servers
            ],
            'load_balancer': {
                'strategy': self.load_balancing_strategy,
                'total_requests': self.load_balancer.total_requests,
                'num_servers': self.num_app_servers
            },
            'db_server': self.db_server.get_metrics(),
            'system': {
                'total_requests': self.total_requests,
                'completed_requests': self.completed_requests,
                'avg_end_to_end_time': np.mean(self.end_to_end_times) if self.end_to_end_times else 0.0,
                'system_throughput': self.completed_requests / self.env.now if self.env.now > 0 else 0.0
            }
        }

        if self.cache_enabled:
            metrics['cache'] = self.cache.get_metrics()
            metrics['cache_server'] = self.cache_server.get_metrics()

        return metrics
