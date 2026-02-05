#!/usr/bin/env python3
"""
Generate WiFi data rate vs. MCS index plots for Lecture 4.

This script shows 802.11ac data rates for different channel widths
and modulation schemes.
"""

import numpy as np
import matplotlib.pyplot as plt

# 802.11ac MCS index data (single spatial stream)
# Format: [MCS, Modulation, Coding Rate, 20MHz, 40MHz, 80MHz, 160MHz] in Mb/s
wifi_ac_data = [
    # MCS, Mod, Rate, 20MHz, 40MHz, 80MHz, 160MHz
    [0, 'BPSK', '1/2', 6.5, 13.5, 29.3, 58.5],
    [1, 'QPSK', '1/2', 13.0, 27.0, 58.5, 117.0],
    [2, 'QPSK', '3/4', 19.5, 40.5, 87.8, 175.5],
    [3, '16-QAM', '1/2', 26.0, 54.0, 117.0, 234.0],
    [4, '16-QAM', '3/4', 39.0, 81.0, 175.5, 351.0],
    [5, '64-QAM', '2/3', 52.0, 108.0, 234.0, 468.0],
    [6, '64-QAM', '3/4', 58.5, 121.5, 263.3, 526.5],
    [7, '64-QAM', '5/6', 65.0, 135.0, 292.5, 585.0],
    [8, '256-QAM', '3/4', 78.0, 162.0, 351.0, 702.0],
    [9, '256-QAM', '5/6', 87.0, 180.0, 390.0, 780.0],
]

# Extract data
mcs_indices = [row[0] for row in wifi_ac_data]
modulations = [row[1] for row in wifi_ac_data]
coding_rates = [row[2] for row in wifi_ac_data]
rate_20mhz = [row[3] for row in wifi_ac_data]
rate_40mhz = [row[4] for row in wifi_ac_data]
rate_80mhz = [row[5] for row in wifi_ac_data]
rate_160mhz = [row[6] for row in wifi_ac_data]

# Create figure with two subplots
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

# --- Plot 1: Data rate vs. MCS for different bandwidths ---
ax1.plot(mcs_indices, rate_20mhz, 'o-', linewidth=2.5, markersize=8,
         label='20 MHz', color='blue')
ax1.plot(mcs_indices, rate_40mhz, 's-', linewidth=2.5, markersize=8,
         label='40 MHz', color='green')
ax1.plot(mcs_indices, rate_80mhz, '^-', linewidth=2.5, markersize=8,
         label='80 MHz', color='orange')
ax1.plot(mcs_indices, rate_160mhz, 'd-', linewidth=2.5, markersize=8,
         label='160 MHz', color='red')

ax1.set_xlabel('MCS Index', fontsize=12, fontweight='bold')
ax1.set_ylabel('Data Rate (Mb/s)', fontsize=12, fontweight='bold')
ax1.set_title('802.11ac Data Rates vs. MCS Index\n(1 Spatial Stream)',
              fontsize=13, fontweight='bold')
ax1.grid(True, alpha=0.3)
ax1.legend(loc='upper left', fontsize=11)
ax1.set_xticks(mcs_indices)

# Add annotations for modulation changes
modulation_changes = {
    0: 'BPSK',
    1: 'QPSK',
    3: '16-QAM',
    5: '64-QAM',
    8: '256-QAM'
}

for mcs, mod in modulation_changes.items():
    ax1.axvline(x=mcs, color='gray', linestyle=':', alpha=0.4)
    ax1.text(mcs, 800, mod, rotation=90, va='top', ha='right',
            fontsize=9, color='gray', fontweight='bold')

# Add annotation
ax1.annotate('Higher MCS = higher modulation\n→ higher data rate\n→ requires higher SNR',
            xy=(7, 585), xytext=(4, 700),
            arrowprops=dict(arrowstyle='->', color='black', lw=1.5),
            fontsize=10, fontweight='bold',
            bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.7))

# --- Plot 2: Stacked bar chart showing modulation distribution ---
# Group by modulation
mod_groups = {'BPSK': [], 'QPSK': [], '16-QAM': [], '64-QAM': [], '256-QAM': []}
for i, mod in enumerate(modulations):
    mod_groups[mod].append(rate_80mhz[i])  # Use 80 MHz as example

# Create grouped bar chart
x_pos = np.arange(len(mcs_indices))
colors_mod = {
    'BPSK': '#1f77b4',
    'QPSK': '#ff7f0e',
    '16-QAM': '#2ca02c',
    '64-QAM': '#d62728',
    '256-QAM': '#9467bd'
}

# Color bars by modulation
bar_colors = [colors_mod[mod] for mod in modulations]
bars = ax2.bar(x_pos, rate_80mhz, color=bar_colors, edgecolor='black',
               linewidth=1.5, alpha=0.8)

# Add value labels on bars
for i, (mcs, rate, mod, code) in enumerate(zip(mcs_indices, rate_80mhz,
                                                 modulations, coding_rates)):
    ax2.text(i, rate + 10, f'{rate:.1f}', ha='center', va='bottom',
            fontsize=9, fontweight='bold')
    ax2.text(i, rate/2, f'{mod}\n{code}', ha='center', va='center',
            fontsize=8, color='white', fontweight='bold')

ax2.set_xlabel('MCS Index', fontsize=12, fontweight='bold')
ax2.set_ylabel('Data Rate (Mb/s)', fontsize=12, fontweight='bold')
ax2.set_title('802.11ac Data Rates at 80 MHz\nColor-coded by Modulation',
              fontsize=13, fontweight='bold')
ax2.grid(True, axis='y', alpha=0.3)
ax2.set_xticks(x_pos)
ax2.set_xticklabels(mcs_indices)

# Create legend for modulations
from matplotlib.patches import Patch
legend_elements = [Patch(facecolor=colors_mod[mod], label=mod, alpha=0.8)
                  for mod in ['BPSK', 'QPSK', '16-QAM', '64-QAM', '256-QAM']]
ax2.legend(handles=legend_elements, loc='upper left', fontsize=10)

plt.tight_layout()
plt.savefig('wifi_rates_vs_mcs.png', dpi=300, bbox_inches='tight')
print("Generated: wifi_rates_vs_mcs.png")

# Create detailed table
fig2, ax = plt.subplots(figsize=(12, 8))
ax.axis('tight')
ax.axis('off')

table_data = [['MCS', 'Modulation', 'Code Rate', '20 MHz', '40 MHz', '80 MHz', '160 MHz']]
for row in wifi_ac_data:
    table_data.append([
        f'{row[0]}',
        row[1],
        row[2],
        f'{row[3]:.1f} Mb/s',
        f'{row[4]:.1f} Mb/s',
        f'{row[5]:.1f} Mb/s',
        f'{row[6]:.1f} Mb/s'
    ])

table = ax.table(cellText=table_data, loc='center', cellLoc='center')
table.auto_set_font_size(False)
table.set_fontsize(10)
table.scale(1, 2.2)

# Style header row
for i in range(7):
    table[(0, i)].set_facecolor('#4472C4')
    table[(0, i)].set_text_props(weight='bold', color='white')

# Style data rows with color coding by modulation
for i in range(1, len(table_data)):
    mod = table_data[i][1]
    row_color = colors_mod.get(mod, '#FFFFFF')

    # Color first three columns with lighter shade
    for j in range(3):
        table[(i, j)].set_facecolor(row_color)
        table[(i, j)].set_text_props(color='white', weight='bold')

    # Data columns with white background
    for j in range(3, 7):
        table[(i, j)].set_facecolor('#FFFFFF')

plt.title('802.11ac Data Rates (1 Spatial Stream)\nMCS Index vs. Channel Bandwidth',
         fontsize=14, fontweight='bold', pad=20)
plt.savefig('wifi_rates_table.png', dpi=300, bbox_inches='tight')
print("Generated: wifi_rates_table.png")

# Create spectral efficiency plot
fig3, ax = plt.subplots(figsize=(10, 6))

# Calculate spectral efficiency (bits/s/Hz)
# For 80 MHz channel
spectral_eff = [rate / 80 for rate in rate_80mhz]

# Create bar chart
bars = ax.bar(mcs_indices, spectral_eff, color=bar_colors,
              edgecolor='black', linewidth=1.5, alpha=0.8)

# Add value labels
for i, (mcs, eff, mod) in enumerate(zip(mcs_indices, spectral_eff, modulations)):
    ax.text(mcs, eff + 0.1, f'{eff:.2f}', ha='center', va='bottom',
           fontsize=9, fontweight='bold')

ax.set_xlabel('MCS Index', fontsize=12, fontweight='bold')
ax.set_ylabel('Spectral Efficiency (bits/s/Hz)', fontsize=12, fontweight='bold')
ax.set_title('802.11ac Spectral Efficiency vs. MCS Index\n(80 MHz Channel)',
            fontsize=13, fontweight='bold')
ax.grid(True, axis='y', alpha=0.3)
ax.set_xticks(mcs_indices)

# Create legend
ax.legend(handles=legend_elements, loc='upper left', fontsize=10)

# Add theoretical limit line
ax.axhline(y=np.log2(256), color='red', linestyle='--', linewidth=2,
          label='Shannon limit (ideal 256-QAM)')
ax.text(9, np.log2(256) + 0.2, 'Theoretical limit\n(256-QAM: 8 bits/s/Hz)',
       fontsize=9, color='red', fontweight='bold')

plt.tight_layout()
plt.savefig('wifi_spectral_efficiency.png', dpi=300, bbox_inches='tight')
print("Generated: wifi_spectral_efficiency.png")

plt.show()
