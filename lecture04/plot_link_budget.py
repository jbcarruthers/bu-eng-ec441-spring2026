#!/usr/bin/env python3
"""
Generate link budget waterfall chart for Lecture 4.

This script creates waterfall charts showing WiFi and cellular link budget
calculations with power gains, losses, and margins.
"""

import numpy as np
import matplotlib.pyplot as plt

def plot_link_budget_waterfall(ax, budget_items, title):
    """
    Create a waterfall chart for link budget.

    Parameters:
    - ax: matplotlib axis
    - budget_items: list of (label, value_dB, color) tuples
    - title: chart title
    """
    positions = np.arange(len(budget_items))
    labels = [item[0] for item in budget_items]
    values = [item[1] for item in budget_items]
    colors = [item[2] for item in budget_items]

    # Calculate cumulative values
    cumulative = [values[0]]
    for v in values[1:]:
        cumulative.append(cumulative[-1] + v)

    # Plot bars
    bottoms = [0]
    for i in range(1, len(values)):
        bottoms.append(cumulative[i-1])

    bars = ax.bar(positions, values, bottom=bottoms, color=colors,
                   edgecolor='black', linewidth=1.5, alpha=0.8)

    # Add value labels on bars
    for i, (pos, val, bot, cum) in enumerate(zip(positions, values, bottoms, cumulative)):
        # Value label inside bar
        if abs(val) > 5:  # Only show if bar is tall enough
            label_y = bot + val/2
            ax.text(pos, label_y, f'{val:+.1f} dB',
                   ha='center', va='center', fontsize=10, fontweight='bold',
                   color='white' if abs(val) > 10 else 'black')

        # Cumulative value label at top
        ax.text(pos, cum + 1, f'{cum:.1f} dBm',
               ha='center', va='bottom', fontsize=9, fontweight='bold')

        # Draw horizontal line showing cumulative level
        if i < len(positions) - 1:
            ax.plot([pos + 0.4, pos + 0.6], [cum, cum],
                   'k-', linewidth=2, alpha=0.5)

    # Formatting
    ax.set_xticks(positions)
    ax.set_xticklabels(labels, rotation=45, ha='right', fontsize=10)
    ax.set_ylabel('Power (dBm)', fontsize=12, fontweight='bold')
    ax.set_title(title, fontsize=13, fontweight='bold')
    ax.grid(True, axis='y', alpha=0.3)
    ax.axhline(y=0, color='gray', linestyle='--', linewidth=1)

    # Add legend for gain/loss
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor='green', alpha=0.8, label='Gain'),
        Patch(facecolor='red', alpha=0.8, label='Loss'),
        Patch(facecolor='blue', alpha=0.8, label='Threshold'),
        Patch(facecolor='gold', alpha=0.8, label='Margin')
    ]
    ax.legend(handles=legend_elements, loc='upper left', fontsize=9)

# Create figure with two subplots
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))

# --- WiFi Link Budget (802.11ac, indoor) ---
wifi_budget = [
    ('Tx Power', 20, 'green'),           # 20 dBm (100 mW)
    ('Tx Ant Gain', 2, 'green'),         # 2 dBi
    ('Path Loss', -75, 'red'),           # -75 dB at 20m, 5 GHz
    ('Misc Losses', -3, 'red'),          # Multipath, polarization
    ('Rx Ant Gain', 2, 'green'),         # 2 dBi
    ('Rx Threshold', 0, 'blue'),         # Reference point
]

# Calculate received power before adding threshold
wifi_rx_power = sum([item[1] for item in wifi_budget[:-1]])
# Typical sensitivity for 802.11ac MCS7 (64-QAM, rate 3/4)
wifi_sensitivity = -68  # dBm
wifi_margin = wifi_rx_power - wifi_sensitivity

# Add margin to display
wifi_budget[-1] = (f'Rx Sensitivity\n({wifi_sensitivity} dBm)', wifi_sensitivity - wifi_rx_power, 'blue')
wifi_budget.append(('Margin', wifi_margin, 'gold'))

plot_link_budget_waterfall(ax1, wifi_budget,
                           'WiFi Link Budget (802.11ac)\n5 GHz, 20m indoor, 80 MHz BW, MCS7')

# --- Cellular Link Budget (LTE) ---
cellular_budget = [
    ('Tx Power', 23, 'green'),           # 23 dBm (200 mW) - eNB
    ('Tx Ant Gain', 18, 'green'),        # 18 dBi - sector antenna
    ('Path Loss', -130, 'red'),          # -130 dB at 1 km, 1.8 GHz
    ('Misc Losses', -8, 'red'),          # Shadow fading, penetration
    ('Rx Ant Gain', 0, 'green'),         # 0 dBi - smartphone
    ('Rx Threshold', 0, 'blue'),         # Reference point
]

# Calculate received power before adding threshold
cellular_rx_power = sum([item[1] for item in cellular_budget[:-1]])
# Typical sensitivity for LTE (QPSK, rate 1/3)
cellular_sensitivity = -110  # dBm
cellular_margin = cellular_rx_power - cellular_sensitivity

# Add margin to display
cellular_budget[-1] = (f'Rx Sensitivity\n({cellular_sensitivity} dBm)',
                       cellular_sensitivity - cellular_rx_power, 'blue')
cellular_budget.append(('Margin', cellular_margin, 'gold'))

plot_link_budget_waterfall(ax2, cellular_budget,
                           'LTE Link Budget (Downlink)\n1.8 GHz, 1 km, 10 MHz BW, QPSK')

plt.tight_layout()
plt.savefig('link_budget_example.png', dpi=300, bbox_inches='tight')
print("Generated: link_budget_example.png")

# Create a detailed link budget table
fig2, (ax_w, ax_c) = plt.subplots(1, 2, figsize=(14, 8))

# WiFi table
ax_w.axis('tight')
ax_w.axis('off')

wifi_table_data = [
    ['Parameter', 'Value', 'Unit'],
    ['Transmit Power', '+20', 'dBm'],
    ['Tx Antenna Gain', '+2', 'dBi'],
    ['Path Loss (20m)', '-75', 'dB'],
    ['Miscellaneous Losses', '-3', 'dB'],
    ['Rx Antenna Gain', '+2', 'dBi'],
    ['Received Power', f'{wifi_rx_power:.1f}', 'dBm'],
    ['', '', ''],
    ['Receiver Sensitivity', f'{wifi_sensitivity}', 'dBm'],
    ['Link Margin', f'{wifi_margin:.1f}', 'dB'],
]

table_w = ax_w.table(cellText=wifi_table_data, loc='center', cellLoc='center')
table_w.auto_set_font_size(False)
table_w.set_fontsize(11)
table_w.scale(1, 2.5)

# Style WiFi table
for i in range(3):
    table_w[(0, i)].set_facecolor('#4472C4')
    table_w[(0, i)].set_text_props(weight='bold', color='white')

for i in [1, 2]:  # Gains
    table_w[(i, 0)].set_facecolor('#C6E0B4')
for i in [3, 4]:  # Losses
    table_w[(i, 0)].set_facecolor('#F4B084')
table_w[(6, 0)].set_facecolor('#D9E1F2')  # Rx power
table_w[(8, 0)].set_facecolor('#FFF2CC')  # Sensitivity
table_w[(9, 0)].set_facecolor('#FFD966')  # Margin
table_w[(9, 0)].set_text_props(weight='bold')

ax_w.set_title('WiFi Link Budget Detail\n802.11ac, 5 GHz',
              fontsize=13, fontweight='bold', pad=20)

# Cellular table
ax_c.axis('tight')
ax_c.axis('off')

cellular_table_data = [
    ['Parameter', 'Value', 'Unit'],
    ['Transmit Power', '+23', 'dBm'],
    ['Tx Antenna Gain', '+18', 'dBi'],
    ['Path Loss (1 km)', '-130', 'dB'],
    ['Miscellaneous Losses', '-8', 'dB'],
    ['Rx Antenna Gain', '0', 'dBi'],
    ['Received Power', f'{cellular_rx_power:.1f}', 'dBm'],
    ['', '', ''],
    ['Receiver Sensitivity', f'{cellular_sensitivity}', 'dBm'],
    ['Link Margin', f'{cellular_margin:.1f}', 'dB'],
]

table_c = ax_c.table(cellText=cellular_table_data, loc='center', cellLoc='center')
table_c.auto_set_font_size(False)
table_c.set_fontsize(11)
table_c.scale(1, 2.5)

# Style Cellular table
for i in range(3):
    table_c[(0, i)].set_facecolor('#4472C4')
    table_c[(0, i)].set_text_props(weight='bold', color='white')

for i in [1, 2, 3]:  # Gains
    table_c[(i, 0)].set_facecolor('#C6E0B4')
for i in [4, 5]:  # Losses
    table_c[(i, 0)].set_facecolor('#F4B084')
table_c[(6, 0)].set_facecolor('#D9E1F2')  # Rx power
table_c[(8, 0)].set_facecolor('#FFF2CC')  # Sensitivity
table_c[(9, 0)].set_facecolor('#FFD966')  # Margin
table_c[(9, 0)].set_text_props(weight='bold')

ax_c.set_title('LTE Link Budget Detail\nDownlink, 1.8 GHz',
              fontsize=13, fontweight='bold', pad=20)

plt.tight_layout()
plt.savefig('link_budget_tables.png', dpi=300, bbox_inches='tight')
print("Generated: link_budget_tables.png")

plt.show()
