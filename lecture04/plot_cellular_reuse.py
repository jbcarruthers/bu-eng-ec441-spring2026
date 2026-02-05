#!/usr/bin/env python3
"""
Generate cellular frequency reuse pattern diagrams for Lecture 4.

Shows hexagonal cell patterns for N=3, 4, and 7 reuse patterns
with color-coded frequency assignments and reuse distance.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import RegularPolygon
import matplotlib.patches as mpatches

def hex_corners(center, radius):
    """Calculate the 6 corners of a hexagon."""
    angles = np.linspace(0, 2*np.pi, 7)  # 7 points (6 corners + close)
    x = center[0] + radius * np.cos(angles + np.pi/6)
    y = center[1] + radius * np.sin(angles + np.pi/6)
    return x, y

def hex_to_pixel(q, r, size):
    """Convert hex coordinates to pixel coordinates (flat-top hexagons)."""
    x = size * (3/2 * q)
    y = size * (np.sqrt(3)/2 * q + np.sqrt(3) * r)
    return x, y

def plot_cellular_pattern(ax, N, grid_size=5):
    """
    Plot cellular frequency reuse pattern.

    Parameters:
    - ax: matplotlib axis
    - N: reuse factor (3, 4, or 7)
    - grid_size: number of cells in each direction
    """
    hex_size = 1.0

    # Define plot boundaries (calculate before drawing)
    x_limit = grid_size * 1.3 * hex_size
    y_limit = grid_size * 1.15 * hex_size * np.sqrt(3) / 2

    # Define color schemes for different N values
    if N == 3:
        colors = ['#FF6B6B', '#4ECDC4', '#FFE66D']
    elif N == 4:
        colors = ['#FF6B6B', '#4ECDC4', '#95E1D3', '#F38181']
    elif N == 7:
        colors = ['#FF6B6B', '#4ECDC4', '#FFE66D', '#95E1D3',
                 '#F38181', '#AA96DA', '#FCBAD3']
    else:
        colors = plt.cm.Set3(np.linspace(0, 1, N))

    # Frequency assignment patterns
    # These patterns are standard for each N value
    if N == 3:
        # Pattern: repeats every sqrt(3) diagonal
        pattern = {
            (0, 0): 0, (1, 0): 1, (0, 1): 2,
            (1, 1): 0, (2, 0): 2, (0, 2): 1,
            (2, 1): 1, (1, 2): 2, (2, 2): 0,
        }
    elif N == 4:
        # Pattern: 2x2 grid
        pattern = {
            (0, 0): 0, (1, 0): 1, (0, 1): 2, (1, 1): 3,
            (2, 0): 0, (3, 0): 1, (2, 1): 2, (3, 1): 3,
            (0, 2): 0, (1, 2): 1, (0, 3): 2, (1, 3): 3,
            (2, 2): 0, (3, 2): 1, (2, 3): 2, (3, 3): 3,
        }
    elif N == 7:
        # Pattern: standard N=7 cluster
        pattern = {
            (0, 0): 0,
            (1, 0): 1, (0, 1): 2, (-1, 1): 3,
            (-1, 0): 4, (0, -1): 5, (1, -1): 6,
            (2, 0): 0, (1, 1): 1, (0, 2): 2,
            (-1, 2): 3, (-2, 1): 4, (-2, 0): 5,
            (-1, -1): 6, (0, -2): 0, (1, -2): 1,
            (2, -1): 2, (2, 1): 3, (1, 2): 4,
            (-1, 3): 5, (-2, 2): 6,
        }

    # Draw hexagons
    drawn_cells = {}
    for q in range(-grid_size, grid_size+1):
        for r in range(-grid_size, grid_size+1):
            # Calculate position
            x, y = hex_to_pixel(q, r, hex_size)

            # Determine frequency assignment
            if N == 3:
                # Use correct N=3 pattern: ensures no adjacent cells have same frequency
                # Pattern: shifts by 1 in q direction, by 2 in r direction
                freq_idx = (q - r) % N
            elif N == 4:
                freq_idx = ((q % 2) + 2 * (r % 2)) % N
            elif N == 7:
                # Use pattern lookup with wrapping
                # Find position in cluster
                q_cluster = q % 7
                r_cluster = r % 7
                # Map to standard pattern
                key = (q % 3, r % 3) if N == 3 else (q, r)
                freq_idx = pattern.get(key, (q + r) % N)
            else:
                freq_idx = (q + r) % N

            color = colors[freq_idx]

            # Draw hexagon (flat-top orientation)
            hexagon = RegularPolygon((x, y), numVertices=6, radius=hex_size,
                                    orientation=np.pi/6, facecolor=color,
                                    edgecolor='black', linewidth=2)
            ax.add_patch(hexagon)

            # Add frequency label only if within plot boundaries
            if abs(x) <= x_limit and abs(y) <= y_limit:
                ax.text(x, y, f'f{freq_idx+1}', ha='center', va='center',
                       fontsize=10, fontweight='bold', color='black')

            drawn_cells[(q, r)] = (x, y, freq_idx)

    # Mark reuse distance D
    # D = R * sqrt(3*N) where R is cell radius
    # Draw from center to a cell with same frequency
    if N == 3:
        # Reuse at (1, 1)
        x0, y0 = hex_to_pixel(0, 0, hex_size)
        x1, y1 = hex_to_pixel(1, 1, hex_size)
    elif N == 4:
        # Reuse at (2, 0)
        x0, y0 = hex_to_pixel(0, 0, hex_size)
        x1, y1 = hex_to_pixel(2, 0, hex_size)
    elif N == 7:
        # Reuse at (2, 1)
        x0, y0 = hex_to_pixel(0, 0, hex_size)
        x1, y1 = hex_to_pixel(2, 1, hex_size)

    # Draw reuse distance arrow
    ax.annotate('', xy=(x1, y1), xytext=(x0, y0),
               arrowprops=dict(arrowstyle='<->', color='red', lw=3))

    # Calculate and display D/R ratio
    D_over_R = np.sqrt(3 * N)
    mid_x, mid_y = (x0 + x1) / 2, (y0 + y1) / 2
    ax.text(mid_x, mid_y - 0.5, f'D = R√{3*N:.0f}\n≈ {D_over_R:.2f}R',
           ha='center', va='top', fontsize=11, fontweight='bold',
           color='red',
           bbox=dict(boxstyle='round', facecolor='white', alpha=0.9))

    # Formatting - use pre-calculated limits
    ax.set_aspect('equal')
    ax.set_xlim(-x_limit, x_limit)
    ax.set_ylim(-y_limit, y_limit)
    ax.axis('off')

    title = f'N = {N} Reuse Pattern\n'
    if N == 3:
        title += 'Minimum reuse, high interference'
    elif N == 4:
        title += 'Moderate interference'
    elif N == 7:
        title += 'Low interference, classic pattern'

    ax.set_title(title, fontsize=12, fontweight='bold', pad=10)

    # Create legend
    legend_patches = [mpatches.Patch(color=colors[i], label=f'Frequency f{i+1}')
                     for i in range(N)]
    ax.legend(handles=legend_patches, loc='upper right', fontsize=9)

    # Add info box
    capacity_per_cell = 1.0 / N
    info_text = f'N = {N}\nC/cell = C₀/{N}\nD/R = {D_over_R:.2f}'
    ax.text(0.02, 0.98, info_text, transform=ax.transAxes,
           ha='left', va='top', fontsize=10, fontweight='bold',
           bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))

# Create figure with three patterns
fig, axes = plt.subplots(1, 3, figsize=(18, 6))

plot_cellular_pattern(axes[0], N=3, grid_size=4)
plot_cellular_pattern(axes[1], N=4, grid_size=4)
plot_cellular_pattern(axes[2], N=7, grid_size=3)

plt.suptitle('Cellular Frequency Reuse Patterns\nHexagonal Cell Layout',
             fontsize=14, fontweight='bold', y=0.98)
plt.tight_layout()
plt.savefig('cellular_reuse_patterns.png', dpi=300, bbox_inches='tight')
print("Generated: cellular_reuse_patterns.png")

# Create comparison table
fig2, ax = plt.subplots(figsize=(10, 6))
ax.axis('tight')
ax.axis('off')

table_data = [
    ['Reuse Factor (N)', 'D/R Ratio', 'Frequencies', 'Capacity/Cell', 'Interference'],
    ['3', f'{np.sqrt(9):.2f}', '3', '33.3%', 'High'],
    ['4', f'{np.sqrt(12):.2f}', '4', '25.0%', 'Moderate'],
    ['7', f'{np.sqrt(21):.2f}', '7', '14.3%', 'Low'],
    ['12', f'{np.sqrt(36):.2f}', '12', '8.3%', 'Very Low'],
]

table = ax.table(cellText=table_data, loc='center', cellLoc='center')
table.auto_set_font_size(False)
table.set_fontsize(11)
table.scale(1, 2.5)

# Style header row
for i in range(5):
    table[(0, i)].set_facecolor('#4472C4')
    table[(0, i)].set_text_props(weight='bold', color='white')

# Style data rows with color coding
colors_table = ['#FF6B6B', '#95E1D3', '#FFE66D', '#AA96DA']
for i in range(1, 5):
    for j in range(5):
        if j == 0:
            table[(i, j)].set_facecolor(colors_table[i-1])
            table[(i, j)].set_text_props(weight='bold')
        else:
            table[(i, j)].set_facecolor('#FFFFFF')

plt.title('Frequency Reuse Pattern Comparison', fontsize=14, fontweight='bold', pad=20)
plt.savefig('cellular_reuse_table.png', dpi=300, bbox_inches='tight')
print("Generated: cellular_reuse_table.png")

# Create C/I (Carrier-to-Interference) analysis plot
fig3, ax = plt.subplots(figsize=(10, 6))

N_values = np.array([3, 4, 7, 9, 12, 13])
D_over_R = np.sqrt(3 * N_values)

# Path loss exponent n = 4 (urban environment)
n = 4
# Number of interfering cells (first tier)
num_interferers = 6

# C/I ratio in dB
# Assuming 6 interferers at distance D
C_over_I_dB = 10 * n * np.log10(D_over_R / 1.0) - 10 * np.log10(num_interferers)

# Plot
ax.plot(N_values, C_over_I_dB, 'bo-', linewidth=2.5, markersize=10)

# Annotate key points
for n_val, ci in zip(N_values, C_over_I_dB):
    ax.annotate(f'N={n_val}', xy=(n_val, ci), xytext=(5, 5),
               textcoords='offset points', fontsize=9, fontweight='bold')

ax.set_xlabel('Reuse Factor (N)', fontsize=12, fontweight='bold')
ax.set_ylabel('C/I Ratio (dB)', fontsize=12, fontweight='bold')
ax.set_title('Carrier-to-Interference Ratio vs. Reuse Factor\n(Path loss exponent n=4, 6 interferers)',
            fontsize=13, fontweight='bold')
ax.grid(True, alpha=0.3)
ax.axhline(y=18, color='red', linestyle='--', linewidth=2,
          label='Typical C/I requirement (18 dB)')
ax.legend(fontsize=11)

# Add annotation
ax.annotate('Higher N → Better C/I\nbut lower capacity per cell',
           xy=(7, 25), xytext=(9, 20),
           arrowprops=dict(arrowstyle='->', color='black', lw=1.5),
           fontsize=10, fontweight='bold',
           bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.7))

plt.tight_layout()
plt.savefig('cellular_ci_analysis.png', dpi=300, bbox_inches='tight')
print("Generated: cellular_ci_analysis.png")

plt.show()
