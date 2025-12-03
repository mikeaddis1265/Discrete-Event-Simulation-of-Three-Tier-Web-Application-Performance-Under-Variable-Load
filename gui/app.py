"""
Streamlit GUI for Three-Tier Web Application Simulation
Professional Black & White Dashboard
"""

import streamlit as st
import sys
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import time
from datetime import datetime

# Add src to path
current_dir = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(os.path.dirname(current_dir), 'src')
sys.path.insert(0, src_path)

from simulation import run_simulation, run_multiple_replications
from outputs import aggregate_replications, calculate_confidence_intervals, analytical_mm1_metrics

# Page configuration
st.set_page_config(
    page_title="Web App Performance Simulator",
    page_icon="◼️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Clean Black & White CSS - Professional Design
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    /* Reset and base styles */
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    /* Main background - Pure White */
    .main {
        background-color: #FFFFFF !important;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        color: #000000 !important;
    }
    
    /* Ensure main content block is visible */
    .block-container {
        background-color: #FFFFFF !important;
        padding: 2rem !important;
    }
    
    /* Remove any overlays */
    [data-testid="stAppViewContainer"] {
        background-color: #FFFFFF !important;
    }
    
    /* Main content area */
    [data-testid="stMain"] {
        background-color: #FFFFFF !important;
    }
    
    /* Ensure text is visible */
    .stMarkdown {
        color: #000000 !important;
    }
    
    /* Fix any black overlays */
    .element-container {
        background-color: transparent !important;
    }

    /* Sidebar styling - Light Gray */
    [data-testid="stSidebar"] {
        background-color: #F8F8F8 !important;
        border-right: 1px solid #E5E5E5 !important;
    }
    
    .sidebar .sidebar-content {
        background-color: #F8F8F8 !important;
    }
    
    /* Ensure sidebar text is visible */
    [data-testid="stSidebar"] * {
        color: #000000 !important;
    }

    /* Headers - Simple and clean */
    .main-title {
        font-size: 1.5rem;
        font-weight: 600;
        color: #000000;
        margin-bottom: 0.5rem;
        padding: 0.5rem 0;
        border-bottom: 1px solid #CCCCCC;
    }

    .sub-title {
        font-size: 0.9rem;
        color: #333333;
        margin-bottom: 1.5rem;
        font-weight: 400;
        line-height: 1.5;
    }

    /* Metric cards - Simple */
    .metric-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1rem;
        margin: 1.5rem 0;
    }
    
    .metric-box {
        background: #FFFFFF;
        border: 1px solid #CCCCCC;
        padding: 1rem;
        text-align: center;
    }
    
    .metric-value {
        font-size: 1.6rem;
        font-weight: 600;
        margin: 0.3rem 0;
        color: #000000;
        line-height: 1;
    }
    
    .metric-label {
        font-size: 0.85rem;
        color: #333333;
        font-weight: 500;
    }
    
    .metric-unit {
        font-size: 0.75rem;
        color: #666666;
        margin-top: 0.2rem;
    }

    /* Status indicators - Simple */
    .status-indicator {
        display: inline-block;
        padding: 0.5rem 1rem;
        border: 1px solid #CCCCCC;
        font-weight: 500;
        font-size: 0.9rem;
        background-color: #FFFFFF;
        color: #000000;
    }
    
    .status-active {
        border-color: #000000;
        background: #FFFFFF;
        color: #000000;
    }
    
    .status-inactive {
        border-color: #CCCCCC;
        background: #FFFFFF;
        color: #666666;
    }

    /* Buttons - Professional styling with visible text */
    .stButton > button {
        width: 100%;
        background-color: #2C3E50 !important;
        color: #FFFFFF !important;
        border: 1px solid #2C3E50 !important;
        border-radius: 4px;
        padding: 0.75rem 1.5rem;
        font-weight: 500;
        font-size: 0.95rem;
        transition: all 0.2s ease;
        cursor: pointer;
    }
    
    .stButton > button:hover {
        background-color: #34495E !important;
        border-color: #34495E !important;
        color: #FFFFFF !important;
    }
    
    .stButton > button:disabled {
        background-color: #BDC3C7 !important;
        border-color: #BDC3C7 !important;
        color: #FFFFFF !important;
        cursor: not-allowed;
    }
    
    /* Primary button (START) */
    button[kind="primary"] {
        background-color: #27AE60 !important;
        color: #FFFFFF !important;
        border: 1px solid #27AE60 !important;
    }
    
    button[kind="primary"]:hover {
        background-color: #229954 !important;
        border-color: #229954 !important;
        color: #FFFFFF !important;
    }
    
    button[kind="primary"]:disabled {
        background-color: #A9DFBF !important;
        border-color: #A9DFBF !important;
        color: #FFFFFF !important;
    }
    
    /* Secondary button (STOP) */
    button:not([kind="primary"]) {
        background-color: #E74C3C !important;
        color: #FFFFFF !important;
        border: 1px solid #E74C3C !important;
    }
    
    button:not([kind="primary"]):hover {
        background-color: #C0392B !important;
        border-color: #C0392B !important;
        color: #FFFFFF !important;
    }
    
    button:not([kind="primary"]):disabled {
        background-color: #F1948A !important;
        border-color: #F1948A !important;
        color: #FFFFFF !important;
    }

    /* Data tables - White background with black text */
    .dataframe {
        border: 1px solid #D5DBDB !important;
        font-family: 'Inter', sans-serif;
        background-color: #FFFFFF !important;
    }
    
    .dataframe th {
        background-color: #FFFFFF !important;
        color: #000000 !important;
        font-weight: 600 !important;
        border-bottom: 2px solid #34495E !important;
        border-top: 1px solid #D5DBDB !important;
        border-left: 1px solid #D5DBDB !important;
        border-right: 1px solid #D5DBDB !important;
    }
    
    .dataframe td {
        background-color: #FFFFFF !important;
        color: #000000 !important;
        border-bottom: 1px solid #E5E5E5 !important;
        border-left: 1px solid #E5E5E5 !important;
        border-right: 1px solid #E5E5E5 !important;
    }
    
    /* Streamlit dataframe styling */
    [data-testid="stDataFrame"] {
        background-color: #FFFFFF !important;
    }
    
    [data-testid="stDataFrame"] table {
        background-color: #FFFFFF !important;
    }
    
    [data-testid="stDataFrame"] th {
        background-color: #FFFFFF !important;
        color: #000000 !important;
    }
    
    [data-testid="stDataFrame"] td {
        background-color: #FFFFFF !important;
        color: #000000 !important;
    }
    
    /* Table elements */
    table {
        background-color: #FFFFFF !important;
        color: #000000 !important;
    }
    
    table th {
        background-color: #FFFFFF !important;
        color: #000000 !important;
    }
    
    table td {
        background-color: #FFFFFF !important;
        color: #000000 !important;
    }
    
    /* Streamlit table widget */
    [data-testid="stTable"] {
        background-color: #FFFFFF !important;
    }
    
    [data-testid="stTable"] table {
        background-color: #FFFFFF !important;
    }
    
    [data-testid="stTable"] th {
        background-color: #FFFFFF !important;
        color: #000000 !important;
    }
    
    [data-testid="stTable"] td {
        background-color: #FFFFFF !important;
        color: #000000 !important;
    }

    /* Section headers - Simple */
    h1, h2, h3 {
        color: #000000 !important;
        font-weight: 600 !important;
        margin-top: 1.5rem !important;
        margin-bottom: 0.75rem !important;
    }
    
    h1 {
        font-size: 1.4rem !important;
        border-bottom: 1px solid #CCCCCC !important;
        padding-bottom: 0.5rem !important;
    }
    
    h2 {
        font-size: 1.2rem !important;
        color: #000000 !important;
    }
    
    h3 {
        font-size: 1.05rem !important;
        color: #000000 !important;
    }

    /* Info boxes - Simple */
    .info-container {
        background-color: #FFFFFF;
        border: 1px solid #CCCCCC;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    .info-container h3 {
        color: #000000 !important;
        margin-top: 0 !important;
        margin-bottom: 0.75rem !important;
        font-size: 1rem !important;
        font-weight: 600 !important;
    }
    
    .info-container ul, .info-container ol {
        margin: 0.5rem 0;
        padding-left: 1.5rem;
    }
    
    .info-container li {
        margin: 0.4rem 0;
        line-height: 1.5;
        color: #000000;
    }
    
    .info-container p {
        margin: 0.5rem 0;
        line-height: 1.5;
        color: #000000;
    }
    
    .info-container strong {
        color: #000000;
        font-weight: 600;
    }

    /* Progress and stats */
    .stats-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0.5rem 0;
    }
    
    .stats-label {
        color: #333333;
        font-size: 0.9rem;
    }
    
    .stats-value {
        color: #000000;
        font-weight: 500;
        font-size: 0.9rem;
    }

    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0;
        border-bottom: 1px solid #CCCCCC;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: #FFFFFF;
        border: none;
        color: #333333;
        font-weight: 400;
        padding: 0.75rem 1.25rem;
        border-bottom: 2px solid transparent;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #FFFFFF;
        color: #000000 !important;
        border-bottom: 2px solid #000000;
        font-weight: 500;
    }

    /* Slider styling */
    .stSlider {
        margin: 1rem 0;
    }
    
    .stSlider label {
        color: #2C3E50 !important;
        font-weight: 500 !important;
        font-size: 0.9rem !important;
        margin-bottom: 0.3rem !important;
    }
    
    /* Checkbox styling */
    .stCheckbox label {
        color: #2C3E50 !important;
        font-weight: 400 !important;
    }
    
    /* Selectbox/Dropdown styling - Fix text visibility */
    [data-testid="stSelectbox"] {
        color: #2C3E50 !important;
    }
    
    [data-testid="stSelectbox"] label {
        color: #2C3E50 !important;
        font-weight: 500 !important;
    }
    
    /* Baseweb select component */
    [data-baseweb="select"] {
        background-color: #FFFFFF !important;
    }
    
    [data-baseweb="select"] > div {
        background-color: #FFFFFF !important;
        border: 1px solid #D5DBDB !important;
        color: #2C3E50 !important;
    }
    
    [data-baseweb="select"] > div > div {
        background-color: #FFFFFF !important;
        color: #2C3E50 !important;
    }
    
    /* Selectbox text content */
    [data-baseweb="select"] span {
        color: #2C3E50 !important;
        background-color: transparent !important;
    }
    
    [data-baseweb="select"] div[style*="color"] {
        color: #2C3E50 !important;
    }
    
    /* Selected value text */
    [data-baseweb="select"] [aria-selected="true"] {
        background-color: #FFFFFF !important;
        color: #2C3E50 !important;
    }
    
    [data-baseweb="select"] [aria-selected="true"] span {
        color: #2C3E50 !important;
    }
    
    /* Dropdown popup */
    [role="listbox"] {
        background-color: #FFFFFF !important;
        border: 1px solid #D5DBDB !important;
    }
    
    [role="option"] {
        color: #2C3E50 !important;
        background-color: #FFFFFF !important;
    }
    
    [role="option"]:hover {
        background-color: #ECF0F1 !important;
        color: #2C3E50 !important;
    }
    
    [role="option"][aria-selected="true"] {
        background-color: #D5E8D4 !important;
        color: #2C3E50 !important;
    }
    
    /* Force text color on all selectbox elements */
    [data-testid="stSelectbox"] * {
        color: #2C3E50 !important;
    }
    
    [data-baseweb="select"] * {
        color: #2C3E50 !important;
    }

    /* Divider */
    .divider {
        height: 1px;
        background-color: #CCCCCC;
        margin: 1rem 0;
    }

    /* Footer */
    .footer {
        text-align: center;
        color: #666666;
        font-size: 0.8rem;
        padding: 1rem 0;
        border-top: 1px solid #CCCCCC;
        margin-top: 1.5rem;
    }

    /* Plot styling */
    .plot-container {
        background: #FFFFFF;
        padding: 1rem;
        border: 1px solid #E5E5E5;
    }

    /* Sidebar sections */
    .sidebar-section {
        margin: 1rem 0;
        padding-bottom: 1rem;
        border-bottom: 1px solid #CCCCCC;
    }
    
    .sidebar-section:last-child {
        border-bottom: none;
    }

    /* Compact spacing */
    .compact {
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'simulation_running' not in st.session_state:
    st.session_state['simulation_running'] = False
if 'all_results' not in st.session_state:
    st.session_state['all_results'] = []
if 'simulation_count' not in st.session_state:
    st.session_state['simulation_count'] = 0
if 'start_time' not in st.session_state:
    st.session_state['start_time'] = None

# Header
st.markdown('<div class="main-title">WEB APPLICATION PERFORMANCE SIMULATOR</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Three-tier architecture simulation with discrete-event modeling</div>', unsafe_allow_html=True)

# Sidebar - Simulation Parameters
st.sidebar.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
st.sidebar.markdown('### CONFIGURATION')

st.sidebar.markdown('<div class="compact">', unsafe_allow_html=True)
arrival_rate = st.sidebar.slider(
    "Request Arrival Rate (λ)",
    min_value=10,
    max_value=1000,
    value=100,
    step=10,
    help="Requests per minute"
)
st.sidebar.markdown('</div>', unsafe_allow_html=True)

st.sidebar.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
st.sidebar.markdown('#### SERVER CONFIGURATION')

col1, col2 = st.sidebar.columns(2)
with col1:
    app_service_rate = st.sidebar.slider(
        "App Server Rate",
        min_value=30,
        max_value=300,
        value=60,
        step=10,
        key="app_rate"
    )
with col2:
    db_service_rate = st.sidebar.slider(
        "DB Server Rate",
        min_value=10,
        max_value=100,
        value=30,
        step=5,
        key="db_rate"
    )

st.sidebar.markdown('<div class="compact">', unsafe_allow_html=True)
num_app_servers = st.sidebar.slider(
    "Number of App Servers",
    min_value=1,
    max_value=10,
    value=3
)
st.sidebar.markdown('</div>', unsafe_allow_html=True)

st.sidebar.markdown('<div class="compact">', unsafe_allow_html=True)
load_balancing_strategy = st.sidebar.selectbox(
    "Load Balancing",
    ['Round Robin', 'Random', 'Least Connections'],
    index=0
)
st.sidebar.markdown('</div>', unsafe_allow_html=True)
st.sidebar.markdown('</div>', unsafe_allow_html=True)

# Cache Configuration
st.sidebar.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
st.sidebar.markdown('#### CACHE SETTINGS')

cache_enabled = st.sidebar.checkbox("Enable Cache Layer", value=True)

if cache_enabled:
    st.sidebar.markdown('<div class="compact">', unsafe_allow_html=True)
    cache_hit_rate = st.sidebar.slider(
        "Cache Hit Rate",
        min_value=0.0,
        max_value=1.0,
        value=0.3,
        step=0.05
    )
    st.sidebar.markdown('</div>', unsafe_allow_html=True)
    
    st.sidebar.markdown('<div class="compact">', unsafe_allow_html=True)
    cache_service_rate = st.sidebar.slider(
        "Cache Service Rate",
        min_value=100,
        max_value=1000,
        value=300,
        step=50
    )
    st.sidebar.markdown('</div>', unsafe_allow_html=True)
else:
    cache_hit_rate = 0.0
    cache_service_rate = 100

st.sidebar.markdown('</div>', unsafe_allow_html=True)

# Simulation Settings
st.sidebar.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
st.sidebar.markdown('#### SIMULATION SETTINGS')

simulation_time = st.sidebar.slider(
    "Duration (minutes)",
    min_value=10,
    max_value=120,
    value=60,
    step=10
)
st.sidebar.markdown('</div>', unsafe_allow_html=True)

# Control Buttons
st.sidebar.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
st.sidebar.markdown('#### CONTROLS')

col1, col2 = st.sidebar.columns(2)
with col1:
    if st.button("START", type="primary", use_container_width=True, 
                 disabled=st.session_state['simulation_running']):
        st.session_state['simulation_running'] = True
        st.session_state['start_time'] = datetime.now()
        st.rerun()

with col2:
    if st.button("STOP", use_container_width=True, 
                 disabled=not st.session_state['simulation_running']):
        st.session_state['simulation_running'] = False
        st.rerun()

st.sidebar.markdown('</div>', unsafe_allow_html=True)

# Clear Results
st.sidebar.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
if st.sidebar.button("CLEAR RESULTS", use_container_width=True):
    st.session_state['all_results'] = []
    st.session_state['simulation_count'] = 0
    st.session_state['simulation_running'] = False
    st.session_state['start_time'] = None
    st.rerun()
st.sidebar.markdown('</div>', unsafe_allow_html=True)

# Status Bar - Better layout
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
status_col1, status_col2, status_col3 = st.columns([1, 1, 1])

with status_col1:
    if st.session_state['simulation_running']:
        st.markdown('<div class="status-indicator status-active">▶ RUNNING</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="status-indicator status-inactive">⏸ STOPPED</div>', unsafe_allow_html=True)

with status_col2:
    total_runs = len(st.session_state['all_results']) if st.session_state['all_results'] else 0
    st.markdown(f'<div class="stats-row"><span class="stats-label">COMPLETED RUNS:</span><span class="stats-value">{total_runs}</span></div>', unsafe_allow_html=True)

with status_col3:
    if st.session_state['start_time']:
        elapsed = datetime.now() - st.session_state['start_time']
        elapsed_str = str(elapsed).split(".")[0]
        st.markdown(f'<div class="stats-row"><span class="stats-label">ELAPSED TIME:</span><span class="stats-value">{elapsed_str}</span></div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="stats-row"><span class="stats-label">ELAPSED TIME:</span><span class="stats-value">--:--:--</span></div>', unsafe_allow_html=True)

# Run continuous simulation
if st.session_state['simulation_running']:
    # Show progress and current results table while running
    next_run = len(st.session_state['all_results']) + 1
    progress_text = f'Running simulation run {next_run}...'
    
    # Show current results table if available
    if st.session_state['all_results']:
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        st.markdown('### CURRENT RESULTS')
        
        results_data = []
        for result in st.session_state['all_results']:
            row = {
                'Run': result['run_number'],
                'Time': result['timestamp'],
                'Response': f"{result['system']['avg_end_to_end_time']:.3f}",
                'Throughput': f"{result['system']['system_throughput']:.1f}",
                'App Util': f"{result['app_server']['utilization']:.1%}",
                'DB Util': f"{result['db_server']['utilization']:.1%}",
                'Requests': result['system']['total_requests'],
            }
            
            if cache_enabled and 'cache' in result:
                row['Cache Hit'] = f"{result['cache']['hit_rate']:.1%}"
            
            results_data.append(row)
        
        df_current = pd.DataFrame(results_data)
        st.dataframe(df_current, use_container_width=True, height=300)
    
    with st.spinner(progress_text):
        try:
            # Convert load balancing strategy to expected format
            strategy_map = {
                'Round Robin': 'round_robin',
                'Random': 'random',
                'Least Connections': 'least_connections'
            }
            strategy = strategy_map.get(load_balancing_strategy, 'round_robin')
            
            result = run_simulation(
                arrival_rate=arrival_rate,
                app_service_rate=app_service_rate,
                db_service_rate=db_service_rate,
                simulation_time=simulation_time,
                cache_enabled=cache_enabled,
                cache_hit_rate=cache_hit_rate if cache_enabled else 0.0,
                cache_service_rate=cache_service_rate if cache_enabled else 100,
                num_app_servers=num_app_servers,
                load_balancing_strategy=strategy,
                random_seed=len(st.session_state['all_results'])
            )

            result['run_number'] = len(st.session_state['all_results']) + 1
            result['timestamp'] = datetime.now().strftime('%H:%M:%S')
            
            st.session_state['all_results'].append(result)
            
            # Show success message briefly
            st.success(f'Run {result["run_number"]} completed successfully!')

            time.sleep(0.8)  # Longer delay to see the table update
            st.rerun()

        except Exception as e:
            st.error(f"Error: {str(e)}")
            st.session_state['simulation_running'] = False

# Display results if available
if st.session_state['all_results']:
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    # Latest results
    latest_result = st.session_state['all_results'][-1]
    
    st.markdown('### PERFORMANCE METRICS')
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        end_to_end = latest_result['system']['avg_end_to_end_time']
        st.markdown(f'''
        <div class="metric-box">
            <div class="metric-label">Response Time</div>
            <div class="metric-value">{end_to_end:.2f}</div>
            <div class="metric-unit">minutes</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col2:
        throughput = latest_result['system']['system_throughput']
        st.markdown(f'''
        <div class="metric-box">
            <div class="metric-label">Throughput</div>
            <div class="metric-value">{throughput:.0f}</div>
            <div class="metric-unit">req/min</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col3:
        app_util = latest_result['app_server']['utilization']
        st.markdown(f'''
        <div class="metric-box">
            <div class="metric-label">App Utilization</div>
            <div class="metric-value">{app_util:.0%}</div>
            <div class="metric-unit">capacity</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col4:
        db_util = latest_result['db_server']['utilization']
        st.markdown(f'''
        <div class="metric-box">
            <div class="metric-label">DB Utilization</div>
            <div class="metric-value">{db_util:.0%}</div>
            <div class="metric-unit">capacity</div>
        </div>
        ''', unsafe_allow_html=True)

    # Tabs for different views
    tab1, tab2, tab3 = st.tabs(["Results", "Charts", "Details"])
    
    with tab1:
        st.markdown('#### SIMULATION HISTORY')
        
        results_data = []
        for result in st.session_state['all_results']:
            row = {
                'Run': result['run_number'],
                'Time': result['timestamp'],
                'Response': f"{result['system']['avg_end_to_end_time']:.3f}",
                'Throughput': f"{result['system']['system_throughput']:.1f}",
                'App Util': f"{result['app_server']['utilization']:.1%}",
                'DB Util': f"{result['db_server']['utilization']:.1%}",
                'Requests': result['system']['total_requests'],
            }
            
            if cache_enabled and 'cache' in result:
                row['Cache Hit'] = f"{result['cache']['hit_rate']:.1%}"
            
            results_data.append(row)
        
        df_results = pd.DataFrame(results_data)
        
        # Display as plain table without gradient
        st.dataframe(df_results, use_container_width=True, height=400)
        
        # Download button
        csv = df_results.to_csv(index=False)
        st.download_button(
            label="DOWNLOAD CSV",
            data=csv,
            file_name=f'simulation_{datetime.now().strftime("%Y%m%d")}.csv',
            mime='text/csv',
            use_container_width=True
        )
    
    with tab2:
        st.markdown('#### PERFORMANCE CHARTS')
        
        if len(st.session_state['all_results']) > 1:
            runs = [r['run_number'] for r in st.session_state['all_results']]
            response_times = [r['system']['avg_end_to_end_time'] for r in st.session_state['all_results']]
            throughputs = [r['system']['system_throughput'] for r in st.session_state['all_results']]
            
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
            
            # Response time chart
            ax1.plot(runs, response_times, 'k-', marker='o', linewidth=1.5, markersize=4)
            ax1.set_xlabel('Run')
            ax1.set_ylabel('Response Time (min)')
            ax1.set_title('Response Time Trend')
            ax1.grid(True, linestyle='--', alpha=0.3)
            ax1.set_facecolor('#FFFFFF')
            
            # Throughput chart
            ax2.plot(runs, throughputs, 'k-', marker='s', linewidth=1.5, markersize=4)
            ax2.set_xlabel('Run')
            ax2.set_ylabel('Throughput (req/min)')
            ax2.set_title('Throughput Trend')
            ax2.grid(True, linestyle='--', alpha=0.3)
            ax2.set_facecolor('#FFFFFF')
            
            plt.tight_layout()
            st.pyplot(fig)
            
            # Utilization comparison
            if len(st.session_state['all_results']) >= 3:
                st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
                st.markdown('#### UTILIZATION COMPARISON')
                
                fig2, ax = plt.subplots(figsize=(10, 4))
                
                x = runs
                app_utils = [r['app_server']['utilization'] * 100 for r in st.session_state['all_results']]
                db_utils = [r['db_server']['utilization'] * 100 for r in st.session_state['all_results']]
                
                width = 0.35
                ax.bar([i - width/2 for i in range(len(x))], app_utils, width, 
                       label='App Server', color='#333333', alpha=0.8)
                ax.bar([i + width/2 for i in range(len(x))], db_utils, width, 
                       label='DB Server', color='#666666', alpha=0.8)
                
                ax.set_xlabel('Run')
                ax.set_ylabel('Utilization (%)')
                ax.set_xticks(range(len(x)))
                ax.set_xticklabels(x)
                ax.legend()
                ax.grid(True, axis='y', linestyle='--', alpha=0.3)
                ax.set_facecolor('#FFFFFF')
                
                plt.tight_layout()
                st.pyplot(fig2)
        else:
            st.info("Run multiple simulations to see charts")
    
    with tab3:
        st.markdown('#### DETAILED METRICS')
        st.markdown(f'*Showing metrics for Run {latest_result["run_number"]} completed at {latest_result["timestamp"]}*')
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('**Application Server Metrics**')
            app_metrics = {
                'Metric': ['Utilization', 'Queue Length', 'Response Time', 'Throughput', 'Total Arrivals', 'Total Departures'],
                'Value': [
                    f"{latest_result['app_server']['utilization']:.2%}",
                    f"{latest_result['app_server']['avg_queue_length']:.2f}",
                    f"{latest_result['app_server']['avg_response_time']:.3f} min",
                    f"{latest_result['app_server']['throughput']:.1f} req/min",
                    str(latest_result['app_server']['arrivals']),
                    str(latest_result['app_server']['departures'])
                ]
            }
            app_df = pd.DataFrame(app_metrics)
            st.dataframe(app_df, use_container_width=True, hide_index=True)
        
        with col2:
            st.markdown('**Database Server Metrics**')
            db_metrics = {
                'Metric': ['Utilization', 'Queue Length', 'Response Time', 'Throughput', 'Total Arrivals', 'Total Departures'],
                'Value': [
                    f"{latest_result['db_server']['utilization']:.2%}",
                    f"{latest_result['db_server']['avg_queue_length']:.2f}",
                    f"{latest_result['db_server']['avg_response_time']:.3f} min",
                    f"{latest_result['db_server']['throughput']:.1f} req/min",
                    str(latest_result['db_server']['arrivals']),
                    str(latest_result['db_server']['departures'])
                ]
            }
            db_df = pd.DataFrame(db_metrics)
            st.dataframe(db_df, use_container_width=True, hide_index=True)
        
        # Cache Performance Metrics - Always check if cache exists in result
        if 'cache' in latest_result:
            st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
            st.markdown('**Cache Performance Metrics**')
            
            try:
                cache_data = latest_result['cache']
                cache_metrics = {
                    'Metric': ['Hit Rate', 'Total Requests', 'Cache Hits', 'Cache Misses', 'Cache Size', 'Cache Capacity'],
                    'Value': [
                        f"{cache_data.get('hit_rate', 0):.2%}",
                        str(cache_data.get('total_requests', 0)),
                        str(cache_data.get('hits', 0)),
                        str(cache_data.get('misses', 0)),
                        f"{cache_data.get('current_size', 0)}/{cache_data.get('capacity', 0)}",
                        str(cache_data.get('capacity', 0))
                    ]
                }
                cache_df = pd.DataFrame(cache_metrics)
                st.dataframe(cache_df, use_container_width=True, hide_index=True)
                
                # Cache Server Metrics if available
                if 'cache_server' in latest_result:
                    st.markdown('<div style="margin-top: 1rem;"></div>', unsafe_allow_html=True)
                    st.markdown('**Cache Server Metrics**')
                    cache_server_metrics = {
                        'Metric': ['Utilization', 'Queue Length', 'Response Time', 'Throughput'],
                        'Value': [
                            f"{latest_result['cache_server'].get('utilization', 0):.2%}",
                            f"{latest_result['cache_server'].get('avg_queue_length', 0):.2f}",
                            f"{latest_result['cache_server'].get('avg_response_time', 0):.3f} min",
                            f"{latest_result['cache_server'].get('throughput', 0):.1f} req/min"
                        ]
                    }
                    cache_server_df = pd.DataFrame(cache_server_metrics)
                    st.dataframe(cache_server_df, use_container_width=True, hide_index=True)
            except Exception as e:
                st.warning(f"Cache metrics available but could not be displayed: {str(e)}")
                st.json(latest_result.get('cache', {}))
        elif cache_enabled:
            st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
            st.info("Cache is enabled but no cache metrics are available in this run.")
        
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        st.markdown('**System-Level Metrics**')
        system_metrics = {
            'Metric': ['Total Requests', 'Completed Requests', 'End-to-End Response Time', 'System Throughput'],
            'Value': [
                str(latest_result['system']['total_requests']),
                str(latest_result['system']['completed_requests']),
                f"{latest_result['system']['avg_end_to_end_time']:.3f} min",
                f"{latest_result['system']['system_throughput']:.2f} req/min"
            ]
        }
        system_df = pd.DataFrame(system_metrics)
        st.dataframe(system_df, use_container_width=True, hide_index=True)

else:
    # Welcome screen with better layout
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown('''
        <div class="info-container">
            <h3>INSTRUCTIONS</h3>
            <ol>
                <li><strong>Configure Parameters:</strong> Adjust arrival rate, service rates, and cache settings in the sidebar</li>
                <li><strong>Start Simulation:</strong> Click the START button to begin continuous simulation runs</li>
                <li><strong>View Results:</strong> Results will appear automatically below with performance metrics</li>
                <li><strong>Control:</strong> Click STOP to pause the simulation at any time</li>
                <li><strong>Analyze:</strong> Use the tabs (Results, Charts, Details) to view different data presentations</li>
                <li><strong>Export:</strong> Download results as CSV for further analysis</li>
            </ol>
        </div>
        ''', unsafe_allow_html=True)
        
        st.markdown('''
        <div class="info-container" style="margin-top: 1.5rem;">
            <h3>SYSTEM ARCHITECTURE</h3>
            <ul>
                <li><strong>Load Balancer:</strong> Distributes requests using Round-Robin, Random, or Least-Connections strategies</li>
                <li><strong>Application Servers:</strong> Multiple app servers (1-10) with M/M/1 queuing model</li>
                <li><strong>Cache Layer:</strong> Optional LRU cache with configurable hit rate (0-100%)</li>
                <li><strong>Database Server:</strong> Single database server with M/M/1 queue management</li>
            </ul>
        </div>
        ''', unsafe_allow_html=True)
    
    with col2:
        st.markdown('''
        <div class="info-container">
            <h3>QUICK CONFIG</h3>
            <p><strong>Default Settings:</strong></p>
            <ul>
                <li>Arrival Rate: 100 req/min</li>
                <li>App Servers: 3</li>
                <li>App Rate: 60 req/min</li>
                <li>DB Rate: 30 req/min</li>
                <li>Cache: Enabled (30% hit rate)</li>
                <li>Simulation: 60 minutes</li>
            </ul>
            <p style="margin-top: 1rem;"><strong>Tip:</strong> Start with default settings, then experiment with different configurations.</p>
        </div>
        ''', unsafe_allow_html=True)
        
        st.markdown('''
        <div class="info-container" style="margin-top: 1.5rem;">
            <h3>TRACKED METRICS</h3>
            <ul>
                <li>Response Time</li>
                <li>Throughput</li>
                <li>Queue Length</li>
                <li>Server Utilization</li>
                <li>Cache Hit Rate</li>
            </ul>
        </div>
        ''', unsafe_allow_html=True)

# Footer
st.markdown('<div class="footer">THREE-TIER WEB APPLICATION SIMULATOR | DISCRETE-EVENT MODELING</div>', unsafe_allow_html=True)