#!/usr/bin/env python3
"""
Generate path loss vs. distance plots for Lecture 4.

This script creates path loss comparisons for free space (n=2) and
empirical models (n=3, 4) at multiple frequencies.
"""

import numpy as np
import matplotlib.pyplot as plt

def path_loss_db(d, f_MHz, n=2, d0=1.0):
    """
    Calculate path loss in dB using simplified model.

    PL(d) = PL(d0) + 10*n*log10(d/d0)
    PL(d0) = 20*log10(4*pi*d0*f/c)

    Parameters:
    - d: distance in meters
    - f_MHz: frequency in MHz
    - n: path loss exponent (2=free space, 3-4=urban)
    - d0: reference distance in meters
    """
    c = 3e8  # speed of light
    f_Hz = f_MHz * 1e6

    # Path loss at reference distance (free space)
    PL_d0 = 20 * np.log10(4 * np.pi * d0 * f_Hz / c)

    # Path loss at distance d
    PL_d = PL_d0 + 10 * n * np.log10(d / d0)

    return PL_d

# Distance range: 1 m to 10 km
distance = np.logspace(0, 4, 500)  # 1 to 10000 meters

# Frequencies
frequencies = [900, 2400, 5000]  # MHz
freq_labels = ['900 MHz', '2.4 GHz', '5 GHz']
colors = ['blue', 'green', 'red']

# Create figure with two subplots
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# --- Plot 1: Different frequencies, n=2 (free space) ---
for freq, label, color in zip(frequencies, freq_labels, colors):
    PL = path_loss_db(distance, freq, n=2, d0=1.0)
    ax1.plot(distance, PL, linewidth=2.5, label=label, color=color)

ax1.set_xlabel('Distance (m)', fontsize=12, fontweight='bold')
ax1.set_ylabel('Path Loss (dB)', fontsize=12, fontweight='bold')
ax1.set_title('Free Space Path Loss (n=2)\nMultiple Frequencies',
              fontsize=13, fontweight='bold')
ax1.grid(True, which='both', alpha=0.3)
ax1.legend(loc='upper left', fontsize=11)
ax1.set_xscale('log')
ax1.set_xlim(1, 10000)

# Add reference markers
ax1.axvline(x=100, color='gray', linestyle=':', alpha=0.5)
ax1.axvline(x=1000, color='gray', linestyle=':', alpha=0.5)
ax1.text(100, 130, '100 m', fontsize=9, rotation=90, va='top', ha='right')
ax1.text(1000, 130, '1 km', fontsize=9, rotation=90, va='top', ha='right')

# Add annotation
ax1.annotate('20 dB per decade\n(n=2)',
             xy=(100, 80), xytext=(20, 95),
             arrowprops=dict(arrowstyle='->', color='black', lw=1.5),
             fontsize=10, fontweight='bold',
             bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.7))

# --- Plot 2: Different path loss exponents at 2.4 GHz ---
exponents = [2, 3, 4]
exp_labels = ['n=2 (Free space)', 'n=3 (Urban)', 'n=4 (Dense urban)']
exp_colors = ['green', 'orange', 'red']
exp_styles = ['-', '--', '-.']

for n, label, color, style in zip(exponents, exp_labels, exp_colors, exp_styles):
    PL = path_loss_db(distance, 2400, n=n, d0=1.0)
    ax2.plot(distance, PL, linewidth=2.5, label=label, color=color, linestyle=style)

ax2.set_xlabel('Distance (m)', fontsize=12, fontweight='bold')
ax2.set_ylabel('Path Loss (dB)', fontsize=12, fontweight='bold')
ax2.set_title('Path Loss Models at 2.4 GHz\nVarying Path Loss Exponent',
              fontsize=13, fontweight='bold')
ax2.grid(True, which='both', alpha=0.3)
ax2.legend(loc='upper left', fontsize=11)
ax2.set_xscale('log')
ax2.set_xlim(1, 10000)

# Add reference markers
ax2.axvline(x=100, color='gray', linestyle=':', alpha=0.5)
ax2.axvline(x=1000, color='gray', linestyle=':', alpha=0.5)

# Add annotation showing divergence
ax2.annotate('Higher n = steeper slope\n→ faster signal decay',
             xy=(1000, 140), xytext=(2000, 120),
             arrowprops=dict(arrowstyle='->', color='black', lw=1.5),
             fontsize=10, fontweight='bold',
             bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.7))

plt.tight_layout()
plt.savefig('path_loss_comparison.png', dpi=300, bbox_inches='tight')
print("Generated: path_loss_comparison.png")

# Create a summary table
fig2, ax = plt.subplots(figsize=(10, 6))
ax.axis('tight')
ax.axis('off')

# Calculate path loss at specific distances
distances_km = [0.1, 0.5, 1.0, 5.0]
table_data = [['Frequency', 'Path Loss Exponent'] + [f'{d} km' for d in distances_km]]

for freq, label in zip(frequencies, freq_labels):
    for n, n_label in [(2, 'n=2'), (3, 'n=3'), (4, 'n=4')]:
        row = [label, n_label]
        for d_km in distances_km:
            d_m = d_km * 1000
            PL = path_loss_db(d_m, freq, n=n, d0=1.0)
            row.append(f'{PL:.1f} dB')
        table_data.append(row)

table = ax.table(cellText=table_data, loc='center', cellLoc='center')
table.auto_set_font_size(False)
table.set_fontsize(10)
table.scale(1, 2)

# Style header row
for i in range(6):
    table[(0, i)].set_facecolor('#4472C4')
    table[(0, i)].set_text_props(weight='bold', color='white')

# Style data rows with alternating colors
for i in range(1, 10):
    for j in range(6):
        if j < 2:
            table[(i, j)].set_facecolor('#D9E1F2')
        else:
            if i % 2 == 1:
                table[(i, j)].set_facecolor('#FFFFFF')
            else:
                table[(i, j)].set_facecolor('#F2F2F2')

plt.title('Path Loss Summary (dB)', fontsize=14, fontweight='bold', pad=20)
plt.savefig('path_loss_table.png', dpi=300, bbox_inches='tight')
print("Generated: path_loss_table.png")

plt.show()
