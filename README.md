# Three-Tier Web Application Performance Simulation

**Discrete-Event Simulation of Three-Tier Web Application Performance Under Variable Load**

A comprehensive simulation project modeling a three-tier web application (Presentation → App Server → Database) with caching and load balancing capabilities. Built using Python, SimPy, and Jupyter notebooks.

---

## 📋 Project Overview

This project implements a discrete-event simulation to analyze the performance of a three-tier web application under varying load conditions. The simulation includes:

- **Presentation Tier**: Load balancer distributing requests across multiple application servers
- **Application Tier**: Multiple app servers with configurable service rates
- **Cache Layer**: LRU cache with configurable hit rates
- **Data Tier**: Database server with M/M/1 queuing model

### Key Features

✅ **Discrete-Event Simulation** using SimPy
✅ **Poisson Arrival Process** (λ: 10-1000 req/min)
✅ **M/M/1 Queuing Models** per server tier
✅ **Load Balancing**: Round-robin, Random, Least-connections strategies
✅ **Caching**: LRU cache with configurable hit rates
✅ **Statistical Analysis**: 10 replications per scenario with confidence intervals
✅ **Validation**: Comparison with analytical M/M/1 formulas
✅ **Interactive GUI**: Streamlit dashboard for real-time simulation
✅ **Comprehensive Documentation**: Jupyter notebooks + LaTeX report

---

## 📁 Project Structure

```
three_tier_web_sim/
├── README.md                           # This file
├── requirements.txt                    # Python dependencies
├── LOAD_BALANCING_UPDATE.md           # Load balancing feature documentation
├── report/
│   └── main.tex                       # LaTeX report template
├── data/
│   └── raw/
│       └── synthetic_arrivals.csv     # Generated arrival data
├── src/                               # Core simulation modules
│   ├── models.py                      # Server, Cache, LoadBalancer classes
│   ├── simulation.py                  # Discrete-event simulation engine
│   ├── inputs.py                      # Input data generation & analysis
│   ├── outputs.py                     # Output analysis & visualization
│   └── experiments.py                 # Experiment configuration & runner
├── notebooks/                         # Jupyter notebooks
│   ├── data_analysis.ipynb           # Input distribution fitting & validation
│   ├── simulation_experiments.ipynb  # Simulation experiments & results
│   └── model_validation.ipynb        # Model validation vs. analytical results
├── gui/
│   └── app.py                        # Streamlit interactive dashboard
├── tests/
│   └── test_simulation.py            # Pytest unit tests
├── docs/
│   └── user_manual.md                # User manual
└── results/                          # Simulation outputs
    ├── plots/                        # Generated plots
    └── *.csv                         # Results data
```

---

## 🚀 Installation & Setup

### Prerequisites

- Python 3.9 or higher
- pip (Python package manager)
- Git (optional, for cloning)

### Step 1: Navigate to Project Directory

```bash
cd "D:/Education/AASTU/Modules/Fifth_Year/Simulation/project 2/three_tier_web_sim"
```

### Step 2: Create Virtual Environment (Recommended)

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- simpy (discrete-event simulation)
- numpy, pandas, scipy (data analysis)
- matplotlib, seaborn (visualization)
- streamlit (GUI)
- jupyterlab (notebooks)
- pytest (testing)

---

## 🎯 How to Run

### Option 1: Run Python Experiments Directly

Run the complete simulation experiment suite:

```bash
python src/experiments.py
```

**Output:**
- Runs 3 scenarios (low/medium/high load)
- 10 replications each
- Saves results to `results/` folder
- Generates plots in `results/plots/`

### Option 2: Run Jupyter Notebooks

Start Jupyter Lab:

```bash
jupyter lab
```

Then open and run notebooks in order:

1. **`notebooks/data_analysis.ipynb`**
   - Generates synthetic Poisson arrival data
   - Fits exponential/Poisson distributions
   - Validates input assumptions
   - Creates distribution plots

2. **`notebooks/simulation_experiments.ipynb`**
   - Runs simulation scenarios
   - Analyzes performance metrics
   - Compares cache vs. no-cache
   - Generates visualization charts

3. **`notebooks/model_validation.ipynb`**
   - Validates simulation against M/M/1 analytical formulas
   - Statistical significance tests
   - Residual analysis
   - Error metrics

### Option 3: Run Streamlit GUI

Launch the interactive dashboard:

```bash
streamlit run gui/app.py
```

**GUI Features:**
- Adjust arrival rate (λ) with slider
- Configure server service rates (μ_app, μ_db)
- Enable/disable caching
- Set cache hit rate
- Choose number of app servers
- Select load balancing strategy
- Run simulations with custom parameters
- View real-time results and plots

**Access:** Opens automatically in browser at `http://localhost:8501`

### Option 4: Run Tests

Execute unit tests:

```bash
pytest tests/test_simulation.py -v
```

---

## 📊 Quick Start Example

### Python Script

```python
from src.simulation import run_simulation

# Run a single simulation
metrics = run_simulation(
    arrival_rate=50,              # 50 req/min
    app_service_rate=60,          # App server: 60 req/min
    db_service_rate=30,           # DB server: 30 req/min
    cache_enabled=True,           # Enable caching
    cache_hit_rate=0.3,           # 30% cache hit rate
    num_app_servers=3,            # 3 app servers
    load_balancing_strategy='least_connections',
    simulation_time=60,           # 60 minutes
    random_seed=42
)

# Print results
print(f"End-to-end time: {metrics['system']['avg_end_to_end_time']:.4f} min")
print(f"App utilization: {metrics['app_server']['utilization']:.2%}")
print(f"DB utilization: {metrics['db_server']['utilization']:.2%}")
print(f"Cache hit rate: {metrics['cache']['hit_rate']:.2%}")
```

### Using ExperimentConfig

```python
from src.experiments import ExperimentConfig, run_experiment

# Configure experiment
config = ExperimentConfig(
    name='High Load Test',
    arrival_rate=200,
    num_app_servers=4,
    load_balancing_strategy='round_robin',
    cache_enabled=True,
    cache_hit_rate=0.4,
    num_replications=10
)

# Run experiment
results = run_experiment(config)

# Access summary statistics
summary = results['summary']
print(summary)
```

---

## 📈 Simulation Parameters

### System Parameters

| Parameter | Description | Default | Range |
|-----------|-------------|---------|-------|
| `arrival_rate` | Mean request arrival rate (λ) | 50 | 10-1000 req/min |
| `app_service_rate` | App server service rate (μ) | 60 | 30-300 req/min |
| `db_service_rate` | DB server service rate (μ) | 30 | 10-100 req/min |
| `cache_service_rate` | Cache server service rate (μ) | 300 | 100-1000 req/min |
| `num_app_servers` | Number of app servers | 1 | 1-10 |
| `load_balancing_strategy` | Load balancing algorithm | 'round_robin' | round_robin, random, least_connections |
| `cache_enabled` | Enable/disable cache | True | True/False |
| `cache_hit_rate` | Probability of cache hit | 0.3 | 0.0-1.0 |
| `simulation_time` | Simulation duration | 60 | 10-120 minutes |
| `num_replications` | Independent replications | 10 | 1-20 |

### Standard Scenarios

1. **Low Load**: λ = 10 req/min
2. **Medium Load**: λ = 50 req/min
3. **High Load**: λ = 200 req/min

---

## 📝 Key Metrics Tracked

### System-Level Metrics
- **End-to-End Response Time**: Total time from arrival to completion
- **System Throughput**: Completed requests per minute
- **Total/Completed Requests**: Request counts

### Server-Level Metrics (per tier)
- **Utilization**: Fraction of time server is busy
- **Average Queue Length**: Mean number of requests waiting
- **Average Response Time**: Mean time in system (wait + service)
- **Throughput**: Requests processed per minute

### Cache Metrics
- **Hit Rate**: Fraction of requests served from cache
- **Hits/Misses**: Cache hit and miss counts

### Load Balancer Metrics
- **Strategy**: Load balancing algorithm used
- **Total Requests**: Requests distributed
- **Individual Server Stats**: Per-server performance

---

## 🔬 Validation & Verification

The simulation is validated against **analytical M/M/1 queuing formulas**:

- **Utilization**: ρ = λ/μ
- **Average Queue Length**: L_q = ρ²/(1-ρ)
- **Average Response Time**: W = 1/(μ-λ)

**Validation Process:**
1. Run simulations without cache (pure M/M/1)
2. Compare with analytical predictions
3. Statistical tests (paired t-tests)
4. Residual analysis
5. MAPE (Mean Absolute Percentage Error) < 5%

See `notebooks/model_validation.ipynb` for detailed validation.

---

## 📖 Documentation

- **User Manual**: `docs/user_manual.md` - Detailed usage guide
- **Load Balancing Guide**: `LOAD_BALANCING_UPDATE.md` - Load balancing feature documentation
- **Code Documentation**: Inline docstrings in all `.py` files
- **Notebooks**: Self-documenting with markdown cells
- **LaTeX Report**: `report/main.tex` - Academic report template

---

## 🧪 Testing

Run all tests:

```bash
pytest tests/ -v --tb=short
```

Run specific test class:

```bash
pytest tests/test_simulation.py::TestCache -v
```

Run with coverage:

```bash
pytest tests/ --cov=src --cov-report=html
```

---

## 📊 Expected Results

### Performance Insights

1. **Low Load (λ=10)**:
   - Minimal queuing
   - Low utilization (<20%)
   - Fast response times

2. **Medium Load (λ=50)**:
   - Moderate queuing
   - Moderate utilization (40-60%)
   - DB starts showing stress

3. **High Load (λ=200)**:
   - Significant queuing
   - DB near saturation (>80%)
   - **Bottleneck**: Database server
   - Cache provides significant relief

### Cache Impact

- **30% hit rate** reduces DB load by ~30%
- **60% hit rate** can reduce response time by 40-50%
- Most effective at medium-to-high loads

### Load Balancing Impact

- **Round Robin**: Even distribution across app servers
- **Least Connections**: Better performance under variable load
- Scalability: Adding app servers improves throughput until DB bottleneck

---

## ⚠️ Troubleshooting

### Import Errors

```
ModuleNotFoundError: No module named 'simpy'
```

**Solution:** Install dependencies
```bash
pip install -r requirements.txt
```

### Notebook Kernel Issues

**Solution:** Install Jupyter kernel
```bash
python -m ipykernel install --user --name=venv
```

### Streamlit Port Already in Use

**Solution:** Specify different port
```bash
streamlit run gui/app.py --server.port 8502
```

### Path Issues on Windows

Use raw strings or forward slashes:
```python
df = pd.read_csv('data/raw/synthetic_arrivals.csv')  # Works
```

---

## 🎓 Academic Context

**Course**: Software Engineering
**Topic**: Discrete-Event Simulation
**Project**: Three-Tier Web Application Performance Modeling

**Learning Objectives:**
- Discrete-event simulation methodology
- Queuing theory application
- Statistical analysis & validation
- Software engineering best practices
- Performance modeling & optimization

---

## 📚 References

- SimPy Documentation: https://simpy.readthedocs.io/
- Queuing Theory: M/M/1 models
- Load Balancing Algorithms
- LRU Cache Implementation

---

## 👥 Author

Software Engineering Course Project
AASTU - Fifth Year

---

## 📄 License

Educational use only - Academic project

---

## 🤝 Contributing

This is an academic project. For suggestions or improvements:
1. Review the code
2. Test changes locally
3. Document modifications

---

## 📞 Support

For issues or questions:
- Check `docs/user_manual.md`
- Review notebook documentation
- Check troubleshooting section above

---

**Last Updated**: December 2025
