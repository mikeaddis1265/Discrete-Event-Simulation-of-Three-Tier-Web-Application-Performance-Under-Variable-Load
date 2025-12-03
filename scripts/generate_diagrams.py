"""
Generate diagrams for the LaTeX report
Creates conceptual and system architecture diagrams as PNG files
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle, Rectangle, Ellipse
import numpy as np
import os

# Set style
plt.rcParams['figure.facecolor'] = 'white'
plt.rcParams['axes.facecolor'] = 'white'
plt.rcParams['font.size'] = 10
plt.rcParams['font.family'] = 'sans-serif'

# Create output directory - adjust path based on where script is run from
script_dir = os.path.dirname(os.path.abspath(__file__))
# Script is in three_tier_web_sim/scripts/, so go up one level to three_tier_web_sim/
project_root = os.path.dirname(script_dir)
output_dir = os.path.join(project_root, 'results', 'plots')
os.makedirs(output_dir, exist_ok=True)


def generate_system_architecture_diagram():
    """Generate professional vertical system architecture diagram showing three-tier structure"""
    fig, ax = plt.subplots(figsize=(12, 14))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 13)
    ax.axis('off')
    
    # Professional color palette - subtle, modern
    color_lb = '#2C3E50'      # Dark blue-gray for load balancer
    color_app = '#34495E'      # Medium gray-blue for app servers
    color_cache = '#E67E22'    # Professional orange for cache
    color_db = '#8E44AD'       # Professional purple for database
    color_arrow = '#34495E'    # Dark gray for arrows
    color_hit = '#27AE60'      # Green for cache hit
    color_miss = '#E74C3C'     # Red for cache miss
    color_text = '#2C3E50'     # Dark text
    color_subtext = '#7F8C8D'  # Light gray for subtext
    color_container = '#ECF0F1' # Light gray for container
    
    # Set background
    fig.patch.set_facecolor('white')
    ax.set_facecolor('white')
    
    # Title section at top
    title_box = FancyBboxPatch((1, 11.5), 8, 0.8,
                               boxstyle="round,pad=0.05",
                               facecolor='#ECF0F1',
                               edgecolor='#BDC3C7',
                               linewidth=1.5)
    ax.add_patch(title_box)
    ax.text(5, 12.1, 'Three-Tier Web Application Architecture', 
            ha='center', va='center', fontsize=16, fontweight='bold', color=color_text)
    ax.text(5, 11.75, 'Discrete-Event Simulation Model', 
            ha='center', va='center', fontsize=11, color=color_subtext, style='italic')
    
    # Row 1: Clients (Top)
    client_box = FancyBboxPatch((3.5, 10.2), 3, 0.8,
                               boxstyle="round,pad=0.08",
                               facecolor='#ECF0F1',
                               edgecolor='#95A5A6',
                               linewidth=2)
    ax.add_patch(client_box)
    ax.text(5, 10.7, 'CLIENTS', ha='center', va='center',
            fontsize=12, fontweight='bold', color=color_text)
    ax.text(5, 10.4, 'Poisson Arrivals: λ req/min', ha='center', va='center',
            fontsize=9, color=color_subtext)
    
    # Arrow from Clients to Load Balancer
    arrow1 = FancyArrowPatch((5, 10.2), (5, 9.5),
                            arrowstyle='->', mutation_scale=30,
                            color=color_arrow, linewidth=3)
    ax.add_patch(arrow1)
    
    # Row 2: Load Balancer (Presentation Tier)
    lb_box = FancyBboxPatch((2.5, 8.5), 5, 1.0,
                            boxstyle="round,pad=0.1",
                            facecolor=color_lb,
                            edgecolor='#1A252F',
                            linewidth=2.5)
    ax.add_patch(lb_box)
    ax.text(5, 9.3, 'LOAD BALANCER', ha='center', va='center',
            fontsize=13, fontweight='bold', color='white')
    ax.text(5, 8.95, 'Presentation Tier', ha='center', va='center',
            fontsize=10, color='#ECF0F1')
    ax.text(5, 8.65, 'Round-Robin | Random | Least-Connections', ha='center', va='center',
            fontsize=8, color='#BDC3C7', style='italic')
    
    # Arrow from Load Balancer to Application Tier
    arrow2 = FancyArrowPatch((5, 8.5), (5, 7.2),
                            arrowstyle='->', mutation_scale=30,
                            color=color_arrow, linewidth=3)
    ax.add_patch(arrow2)
    
    # Row 3: Application Tier Container with 3 App Servers
    # Container box
    container_box = FancyBboxPatch((1, 5.5), 8, 1.6,
                                  boxstyle="round,pad=0.15",
                                  facecolor=color_container,
                                  edgecolor='#BDC3C7',
                                  linewidth=2)
    ax.add_patch(container_box)
    
    # Container label
    ax.text(5, 6.95, 'APPLICATION TIER', ha='center', va='center',
            fontsize=10, fontweight='bold', color=color_text)
    
    # Three App Servers inside container
    app_servers = []
    num_servers = 3
    server_width = 1.8
    server_height = 1.0
    total_width = num_servers * server_width + (num_servers - 1) * 0.4
    start_x = 5 - total_width / 2
    
    for i in range(num_servers):
        x_pos = start_x + i * (server_width + 0.4)
        y_pos = 5.7
        
        # Server box
        app_box = FancyBboxPatch((x_pos, y_pos), server_width, server_height,
                                boxstyle="round,pad=0.08",
                                facecolor=color_app,
                                edgecolor='#1A252F',
                                linewidth=2)
        ax.add_patch(app_box)
        
        # Server label
        ax.text(x_pos + server_width/2, y_pos + server_height - 0.25, 
                f'APP SERVER {i+1}', ha='center', va='center',
                fontsize=9, fontweight='bold', color='white')
        
        # Service rate
        ax.text(x_pos + server_width/2, y_pos + server_height/2 - 0.1,
                'M/M/1 Queue', ha='center', va='center',
                fontsize=8, color='#ECF0F1')
        ax.text(x_pos + server_width/2, y_pos + server_height/2 - 0.35,
                'μ = 60 req/min', ha='center', va='center',
                fontsize=7, color='#BDC3C7', style='italic')
        
        app_servers.append((x_pos + server_width/2, y_pos))
    
    # Arrows from App Servers to Cache
    arrow3 = FancyArrowPatch((5, 5.5), (5, 4.5),
                            arrowstyle='->', mutation_scale=30,
                            color=color_arrow, linewidth=3)
    ax.add_patch(arrow3)
    
    # Row 4: Cache Layer
    cache_box = FancyBboxPatch((2.5, 3.5), 5, 1.0,
                               boxstyle="round,pad=0.1",
                               facecolor=color_cache,
                               edgecolor='#D35400',
                               linewidth=2.5)
    ax.add_patch(cache_box)
    ax.text(5, 4.3, 'CACHE LAYER', ha='center', va='center',
            fontsize=13, fontweight='bold', color='white')
    ax.text(5, 3.95, 'LRU Cache Strategy', ha='center', va='center',
            fontsize=10, color='#ECF0F1')
    ax.text(5, 3.65, 'Hit Rate: h | μ = 300 req/min', ha='center', va='center',
            fontsize=8, color='#FAD7A0', style='italic')
    
    # Two paths from Cache
    # Path 1: Cache Miss to Database
    arrow_miss = FancyArrowPatch((5, 3.5), (5, 2.5),
                                arrowstyle='->', mutation_scale=30,
                                color=color_miss, linewidth=3)
    ax.add_patch(arrow_miss)
    miss_label = FancyBboxPatch((5.8, 2.8), 1.2, 0.3,
                               boxstyle="round,pad=0.05",
                               facecolor='white',
                               edgecolor=color_miss,
                               linewidth=2)
    ax.add_patch(miss_label)
    ax.text(6.4, 2.95, 'Cache Miss', ha='center', va='center',
            fontsize=8, fontweight='bold', color=color_miss)
    
    # Path 2: Cache Hit to Response (bypass DB) - L-shaped arrow
    # First segment: straight down from right side of cache
    arrow_hit_down = FancyArrowPatch((7.5, 3.5), (7.5, 0.5),
                                    arrowstyle='->', mutation_scale=30,
                                    color=color_hit, linewidth=2.5, linestyle='--')
    ax.add_patch(arrow_hit_down)
    # Second segment: turn right to response box
    arrow_hit_right = FancyArrowPatch((7.5, 0.5), (6.5, 0.5),
                                     arrowstyle='->', mutation_scale=30,
                                     color=color_hit, linewidth=2.5, linestyle='--')
    ax.add_patch(arrow_hit_right)
    hit_label = FancyBboxPatch((7.8, 1.8), 1.0, 0.25,
                               boxstyle="round,pad=0.05",
                               facecolor='white',
                               edgecolor=color_hit,
                               linewidth=2)
    ax.add_patch(hit_label)
    ax.text(8.3, 1.925, 'Cache Hit', ha='center', va='center',
            fontsize=8, fontweight='bold', color=color_hit)
    
    # Row 5: Database Server (Data Tier)
    db_box = FancyBboxPatch((3.5, 1.5), 3, 1.0,
                            boxstyle="round,pad=0.1",
                            facecolor=color_db,
                            edgecolor='#6C3483',
                            linewidth=2.5)
    ax.add_patch(db_box)
    ax.text(5, 2.3, 'DATABASE', ha='center', va='center',
            fontsize=13, fontweight='bold', color='white')
    ax.text(5, 1.95, 'Data Tier', ha='center', va='center',
            fontsize=10, color='#ECF0F1')
    ax.text(5, 1.65, 'M/M/1 Queue | μ = 30 req/min', ha='center', va='center',
            fontsize=8, color='#D2B4DE', style='italic')
    
    # Arrow from Database to Response
    arrow_db = FancyArrowPatch((5, 1.5), (5, 0.5),
                              arrowstyle='->', mutation_scale=30,
                              color=color_arrow, linewidth=3)
    ax.add_patch(arrow_db)
    
    # Row 6: Response (Bottom)
    response_box = FancyBboxPatch((3.5, 0.1), 3, 0.4,
                                 boxstyle="round,pad=0.08",
                                 facecolor='#ECF0F1',
                                 edgecolor='#95A5A6',
                                 linewidth=2)
    ax.add_patch(response_box)
    ax.text(5, 0.3, 'RESPONSE', ha='center', va='center',
            fontsize=11, fontweight='bold', color=color_text)
    
    # Legend on the right side
    legend_x = 8.3
    legend_y_start = 9.5
    legend_box = FancyBboxPatch((legend_x - 0.2, 7.2), 1.4, 2.8,
                               boxstyle="round,pad=0.1",
                               facecolor='#F8F9FA',
                               edgecolor='#DEE2E6',
                               linewidth=1.5)
    ax.add_patch(legend_box)
    ax.text(legend_x + 0.5, 9.8, 'LEGEND', ha='center', va='center',
            fontsize=10, fontweight='bold', color=color_text)
    
    # Legend items
    legend_items = [
        (color_lb, 'Presentation'),
        (color_app, 'Application'),
        (color_cache, 'Cache Layer'),
        (color_db, 'Data Tier')
    ]
    
    for i, (color, label) in enumerate(legend_items):
        y_pos = legend_y_start - i * 0.5
        # Color box - aligned properly
        legend_color_box = Rectangle((legend_x + 0.05, y_pos - 0.1), 0.25, 0.2,
                                    facecolor=color, edgecolor='#2C3E50', linewidth=1)
        ax.add_patch(legend_color_box)
        # Text - aligned with color box
        ax.text(legend_x + 0.4, y_pos, label, ha='left', va='center',
                fontsize=8, color=color_text)
    
    # Performance metrics box on the right
    metrics_box = FancyBboxPatch((legend_x - 0.2, 4.5), 1.4, 2.0,
                                boxstyle="round,pad=0.1",
                                facecolor='#F8F9FA',
                                edgecolor='#DEE2E6',
                                linewidth=1.5)
    ax.add_patch(metrics_box)
    ax.text(legend_x + 0.5, 6.3, 'TRACKED', ha='center', va='center',
            fontsize=9, fontweight='bold', color=color_text)
    ax.text(legend_x + 0.5, 6.0, 'METRICS', ha='center', va='center',
            fontsize=9, fontweight='bold', color=color_text)
    metrics = ['• Response Time', '• Throughput', '• Queue Length', '• Utilization']
    for i, metric in enumerate(metrics):
        ax.text(legend_x + 0.5, 5.5 - i * 0.25, metric, ha='center', va='center',
                fontsize=7, color=color_subtext)
    
    plt.tight_layout()
    output_path = os.path.join(output_dir, 'system_architecture.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white', 
                edgecolor='none', pad_inches=0.2)
    print(f"Generated: {output_path}")
    plt.close()


def generate_conceptual_diagram():
    """Generate conceptual diagram showing simulation flow and components"""
    fig, ax = plt.subplots(figsize=(12, 10))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # Colors
    color_input = '#E8F4F8'
    color_process = '#FFF4E6'
    color_output = '#F0F8E8'
    color_arrow = '#333333'
    
    # Title
    ax.text(5, 9.5, 'Discrete-Event Simulation Conceptual Model', 
            ha='center', fontsize=14, fontweight='bold')
    
    # Input Section
    input_box = FancyBboxPatch((0.5, 7), 2.5, 1.5,
                              boxstyle="round,pad=0.2",
                              facecolor=color_input,
                              edgecolor='black',
                              linewidth=2)
    ax.add_patch(input_box)
    ax.text(1.75, 8.2, 'INPUT', ha='center', fontsize=11, fontweight='bold')
    ax.text(1.75, 7.8, '• Arrival Rate (λ)', ha='center', fontsize=9)
    ax.text(1.75, 7.5, '• Service Rates (μ)', ha='center', fontsize=9)
    ax.text(1.75, 7.2, '• Cache Hit Rate', ha='center', fontsize=9)
    
    # Simulation Engine
    sim_box = FancyBboxPatch((3.5, 6), 3, 2.5,
                            boxstyle="round,pad=0.2",
                            facecolor=color_process,
                            edgecolor='black',
                            linewidth=2)
    ax.add_patch(sim_box)
    ax.text(5, 8.2, 'SIMULATION ENGINE', ha='center', fontsize=11, fontweight='bold')
    ax.text(5, 7.8, '(SimPy)', ha='center', fontsize=9, style='italic')
    
    # Components inside simulation
    comp_y = 7.4
    components = [
        '• Request Generator (Poisson)',
        '• Load Balancer',
        '• App Servers (M/M/1)',
        '• Cache Layer',
        '• DB Server (M/M/1)'
    ]
    for i, comp in enumerate(components):
        ax.text(5, comp_y - i*0.15, comp, ha='center', fontsize=8)
    
    # Output Section
    output_box = FancyBboxPatch((7, 7), 2.5, 1.5,
                               boxstyle="round,pad=0.2",
                               facecolor=color_output,
                               edgecolor='black',
                               linewidth=2)
    ax.add_patch(output_box)
    ax.text(8.25, 8.2, 'OUTPUT', ha='center', fontsize=11, fontweight='bold')
    ax.text(8.25, 7.8, '• Response Time', ha='center', fontsize=9)
    ax.text(8.25, 7.5, '• Utilization', ha='center', fontsize=9)
    ax.text(8.25, 7.2, '• Queue Length', ha='center', fontsize=9)
    
    # Arrows
    arrow1 = FancyArrowPatch((3, 7.75), (3.5, 7.75),
                            arrowstyle='->', mutation_scale=20,
                            color=color_arrow, linewidth=2)
    ax.add_patch(arrow1)
    
    arrow2 = FancyArrowPatch((6.5, 7.75), (7, 7.75),
                            arrowstyle='->', mutation_scale=20,
                            color=color_arrow, linewidth=2)
    ax.add_patch(arrow2)
    
    # Validation Section
    val_box = FancyBboxPatch((1, 4), 3, 1.5,
                            boxstyle="round,pad=0.2",
                            facecolor='#F8E8E8',
                            edgecolor='black',
                            linewidth=2)
    ax.add_patch(val_box)
    ax.text(2.5, 5.2, 'VALIDATION', ha='center', fontsize=11, fontweight='bold')
    ax.text(2.5, 4.8, 'Compare with', ha='center', fontsize=9)
    ax.text(2.5, 4.5, 'M/M/1 Formulas', ha='center', fontsize=9)
    
    # Analysis Section
    analysis_box = FancyBboxPatch((5, 4), 3, 1.5,
                                 boxstyle="round,pad=0.2",
                                 facecolor='#E8E8F8',
                                 edgecolor='black',
                                 linewidth=2)
    ax.add_patch(analysis_box)
    ax.text(6.5, 5.2, 'ANALYSIS', ha='center', fontsize=11, fontweight='bold')
    ax.text(6.5, 4.8, 'Statistical Tests', ha='center', fontsize=9)
    ax.text(6.5, 4.5, 'Confidence Intervals', ha='center', fontsize=9)
    
    # Arrows from output to validation/analysis
    arrow3 = FancyArrowPatch((8.25, 7), (2.5, 5.5),
                            arrowstyle='->', mutation_scale=15,
                            color=color_arrow, linewidth=1.5, linestyle='--')
    ax.add_patch(arrow3)
    
    arrow4 = FancyArrowPatch((8.25, 7), (6.5, 5.5),
                            arrowstyle='->', mutation_scale=15,
                            color=color_arrow, linewidth=1.5, linestyle='--')
    ax.add_patch(arrow4)
    
    # Queuing Theory Box
    qt_box = FancyBboxPatch((2, 1.5), 6, 1.5,
                           boxstyle="round,pad=0.2",
                           facecolor='#FFFACD',
                           edgecolor='black',
                           linewidth=2)
    ax.add_patch(qt_box)
    ax.text(5, 2.7, 'QUEUING THEORY FOUNDATION', ha='center', fontsize=11, fontweight='bold')
    ax.text(5, 2.3, 'M/M/1 Queues: Poisson Arrivals, Exponential Service Times', ha='center', fontsize=9)
    ax.text(5, 2, 'Little\'s Law: L = λW, L_q = λW_q', ha='center', fontsize=9)
    ax.text(5, 1.7, 'Utilization: ρ = λ/μ', ha='center', fontsize=9)
    
    # Arrow from validation to queuing theory
    arrow5 = FancyArrowPatch((2.5, 4), (3.5, 3),
                            arrowstyle='->', mutation_scale=15,
                            color=color_arrow, linewidth=1.5)
    ax.add_patch(arrow5)
    
    # Arrow from analysis to queuing theory
    arrow6 = FancyArrowPatch((6.5, 4), (6.5, 3),
                            arrowstyle='->', mutation_scale=15,
                            color=color_arrow, linewidth=1.5)
    ax.add_patch(arrow6)
    
    plt.tight_layout()
    output_path = os.path.join(output_dir, 'conceptual_diagram.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"Generated: {output_path}")
    plt.close()


def generate_request_flow_diagram():
    """Generate request flow diagram showing the path of a request"""
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 4)
    ax.axis('off')
    
    # Title
    ax.text(6, 3.5, 'Request Flow Through Three-Tier System', 
            ha='center', fontsize=13, fontweight='bold')
    
    # Stages
    stages = [
        ('Arrival\n(Poisson)', 1, 2, '#E8F4F8'),
        ('Load\nBalancer', 3, 2, '#4A90E2'),
        ('App Server\n(M/M/1)', 5.5, 2, '#50C878'),
        ('Cache\nCheck', 8, 2, '#FFD700'),
        ('Database\n(M/M/1)', 10.5, 2, '#FF6B6B'),
        ('Response', 12, 2, '#E8F4F8')
    ]
    
    boxes = []
    for label, x, y, color in stages:
        box = FancyBboxPatch((x-0.6, y-0.5), 1.2, 1,
                            boxstyle="round,pad=0.1",
                            facecolor=color,
                            edgecolor='black',
                            linewidth=2)
        ax.add_patch(box)
        ax.text(x, y, label, ha='center', va='center',
                fontsize=9, fontweight='bold')
        boxes.append((x, y))
    
    # Arrows
    for i in range(len(boxes) - 1):
        x1, y1 = boxes[i]
        x2, y2 = boxes[i+1]
        arrow = FancyArrowPatch((x1 + 0.6, y1), (x2 - 0.6, y2),
                               arrowstyle='->', mutation_scale=20,
                               color='#333333', linewidth=2)
        ax.add_patch(arrow)
    
    # Cache hit/miss paths
    # Cache hit path (bypass DB)
    cache_hit_arrow = FancyArrowPatch((8.6, 2), (11.4, 2),
                                     arrowstyle='->', mutation_scale=15,
                                     color='#28a745', linewidth=2, linestyle='--')
    ax.add_patch(cache_hit_arrow)
    ax.text(10, 2.4, 'Cache Hit', ha='center', fontsize=8,
            bbox=dict(boxstyle='round,pad=0.2', facecolor='white', edgecolor='#28a745'))
    
    # Cache miss path (to DB)
    ax.text(9.25, 1.5, 'Cache Miss', ha='center', fontsize=8,
            bbox=dict(boxstyle='round,pad=0.2', facecolor='white', edgecolor='#333333'))
    
    # Timing labels
    ax.text(1, 0.8, 't=0', ha='center', fontsize=8, style='italic')
    ax.text(5.5, 0.8, 't₁', ha='center', fontsize=8, style='italic')
    ax.text(8, 0.8, 't₂', ha='center', fontsize=8, style='italic')
    ax.text(10.5, 0.8, 't₃', ha='center', fontsize=8, style='italic')
    ax.text(12, 0.8, 't_end', ha='center', fontsize=8, style='italic')
    
    plt.tight_layout()
    output_path = os.path.join(output_dir, 'request_flow_diagram.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"Generated: {output_path}")
    plt.close()


if __name__ == '__main__':
    print("Generating diagrams for LaTeX report...")
    print("=" * 50)
    
    generate_system_architecture_diagram()
    generate_conceptual_diagram()
    generate_request_flow_diagram()
    
    print("=" * 50)
    print("All diagrams generated successfully!")
    print(f"Output directory: {output_dir}")

