#!/usr/bin/env python3
"""
Generate RF spectrum allocation chart for Lecture 4.

Shows cellular, WiFi, Bluetooth, GPS, satellite bands with
licensed vs unlicensed color coding from 0-50 GHz.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# Define spectrum allocations (frequency in GHz, bandwidth, name, type)
# Format: (center_freq_GHz, bandwidth_GHz, name, type, color)
spectrum_bands = [
    # AM Radio
    (0.001, 0.001, 'AM Radio\n540-1600 kHz', 'Licensed', '#FF6B6B'),

    # FM Radio
    (0.095, 0.020, 'FM Radio\n88-108 MHz', 'Licensed', '#FF6B6B'),

    # TV Broadcast (VHF/UHF)
    (0.200, 0.100, 'TV Broadcast\n174-216 MHz', 'Licensed', '#FF6B6B'),
    (0.600, 0.300, 'TV/UHF\n470-806 MHz', 'Licensed', '#FF6B6B'),

    # Cellular: 800 MHz (2G/3G)
    (0.850, 0.050, 'Cellular 850\n(2G/3G/LTE)', 'Licensed', '#4ECDC4'),

    # GSM 900
    (0.925, 0.050, 'GSM 900', 'Licensed', '#4ECDC4'),

    # GPS L1
    (1.575, 0.010, 'GPS L1', 'Licensed', '#95E1D3'),

    # Cellular: 1800 MHz (GSM/LTE)
    (1.850, 0.100, 'PCS 1900\n(2G/3G/LTE)', 'Licensed', '#4ECDC4'),

    # WiFi 2.4 GHz (ISM band)
    (2.450, 0.100, 'WiFi 2.4 GHz\n(802.11b/g/n/ax)\nBluetooth', 'Unlicensed', '#FFE66D'),

    # Cellular: 2.5 GHz (LTE)
    (2.600, 0.100, 'LTE Band 7\n2.5-2.7 GHz', 'Licensed', '#4ECDC4'),

    # 5G: 3.5 GHz (CBRS)
    (3.550, 0.150, '5G/CBRS\n3.5 GHz', 'Shared', '#AA96DA'),

    # Satellite (C-band)
    (4.500, 1.000, 'C-band Satellite\n3.7-4.2 GHz', 'Licensed', '#95E1D3'),

    # WiFi 5 GHz (UNII bands)
    (5.500, 0.500, 'WiFi 5 GHz\n(802.11a/n/ac/ax)\n5.15-5.85 GHz', 'Unlicensed', '#FFE66D'),

    # 5G: mmWave 24 GHz
    (24.500, 0.750, '5G mmWave\n24.25-25 GHz', 'Licensed', '#4ECDC4'),

    # 5G: mmWave 28 GHz
    (28.000, 0.850, '5G mmWave\n27.5-28.35 GHz', 'Licensed', '#4ECDC4'),

    # Satellite (Ka-band)
    (20.000, 10.000, 'Ka-band Satellite\n18-40 GHz', 'Licensed', '#95E1D3'),

    # 5G: mmWave 39 GHz
    (39.000, 1.400, '5G mmWave\n37-40 GHz', 'Licensed', '#4ECDC4'),

    # WiFi 6E (6 GHz)
    (6.500, 1.200, 'WiFi 6E\n(802.11ax)\n5.925-7.125 GHz', 'Unlicensed', '#FFE66D'),

    # 60 GHz unlicensed (WiGig)
    (60.000, 7.000, 'WiGig/802.11ad\n60 GHz band', 'Unlicensed', '#FFE66D'),
]

# Sort by center frequency
spectrum_bands.sort(key=lambda x: x[0])

# Create figure
fig, ax = plt.subplots(figsize=(16, 10))

# Plot each band as a horizontal bar
y_positions = []
bar_height = 0.8

for i, (center_freq, bandwidth, name, band_type, color) in enumerate(spectrum_bands):
    # Calculate start and end frequencies
    start_freq = center_freq - bandwidth / 2
    end_freq = center_freq + bandwidth / 2

    y_pos = i
    y_positions.append(y_pos)

    # Draw bar
    ax.barh(y_pos, bandwidth, left=start_freq, height=bar_height,
           color=color, edgecolor='black', linewidth=1.5, alpha=0.8)

    # Add label
    label_x = center_freq
    label_text = name

    # Text color (white for dark backgrounds, black for light)
    text_color = 'black'

    ax.text(label_x, y_pos, label_text, ha='center', va='center',
           fontsize=8, fontweight='bold', color=text_color)

    # Add frequency range annotation
    freq_range = f'{start_freq:.3f}-{end_freq:.3f} GHz'
    ax.text(end_freq + 0.5, y_pos, freq_range, ha='left', va='center',
           fontsize=7, style='italic')

# Formatting
ax.set_xlabel('Frequency (GHz)', fontsize=13, fontweight='bold')
ax.set_ylabel('Spectrum Allocation', fontsize=13, fontweight='bold')
ax.set_title('RF Spectrum Allocation (0-70 GHz)\nCellular, WiFi, Bluetooth, GPS, Satellite',
            fontsize=14, fontweight='bold')

# Set x-axis to log scale for better visualization
ax.set_xscale('log')
ax.set_xlim(0.0005, 70)

# Set y-axis
ax.set_ylim(-1, len(spectrum_bands))
ax.set_yticks([])

# Add grid
ax.grid(True, axis='x', alpha=0.3, which='both')

# Add vertical lines for common frequency markers
markers = [0.001, 0.1, 1, 2.4, 5, 10, 24, 28, 39, 60]
for freq in markers:
    ax.axvline(x=freq, color='gray', linestyle=':', linewidth=1, alpha=0.4)

# Create legend
legend_patches = [
    mpatches.Patch(color='#4ECDC4', alpha=0.8, label='Licensed (Cellular)'),
    mpatches.Patch(color='#FFE66D', alpha=0.8, label='Unlicensed (WiFi/ISM)'),
    mpatches.Patch(color='#95E1D3', alpha=0.8, label='Licensed (Satellite/GPS)'),
    mpatches.Patch(color='#AA96DA', alpha=0.8, label='Shared (CBRS)'),
    mpatches.Patch(color='#FF6B6B', alpha=0.8, label='Licensed (Broadcast)'),
]
ax.legend(handles=legend_patches, loc='upper left', fontsize=11, framealpha=0.9)

# Add annotations for major bands
ax.annotate('Sub-6 GHz\n(Good propagation)', xy=(3, len(spectrum_bands)-2),
           xytext=(3, len(spectrum_bands)+2),
           fontsize=11, fontweight='bold', ha='center',
           bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.7))

ax.annotate('mmWave\n(High capacity, short range)', xy=(30, len(spectrum_bands)-2),
           xytext=(30, len(spectrum_bands)+2),
           fontsize=11, fontweight='bold', ha='center',
           bbox=dict(boxstyle='round', facecolor='lightcoral', alpha=0.7))

plt.tight_layout()
plt.savefig('spectrum_allocation.png', dpi=300, bbox_inches='tight')
print("Generated: spectrum_allocation.png")

# Create detailed table for key wireless bands
fig2, ax = plt.subplots(figsize=(14, 10))
ax.axis('tight')
ax.axis('off')

table_data = [
    ['Technology', 'Frequency Band', 'Bandwidth', 'Type', 'Range', 'Use Case'],
    ['AM Radio', '540-1600 kHz', '1.06 MHz', 'Licensed', '~100 km', 'Broadcast audio'],
    ['FM Radio', '88-108 MHz', '20 MHz', 'Licensed', '~50 km', 'Broadcast audio'],
    ['Cellular (850)', '824-894 MHz', '70 MHz', 'Licensed', '~10 km', '2G/3G/LTE'],
    ['GSM 900', '890-960 MHz', '70 MHz', 'Licensed', '~10 km', '2G/3G'],
    ['GPS L1', '1575.42 MHz', '~2 MHz', 'Licensed', 'Global', 'Navigation'],
    ['PCS/LTE', '1850-1990 MHz', '140 MHz', 'Licensed', '~5 km', '2G/3G/LTE'],
    ['WiFi 2.4', '2.4-2.5 GHz', '83.5 MHz', 'Unlicensed', '~50 m', 'WiFi, Bluetooth'],
    ['LTE Band 7', '2.5-2.7 GHz', '200 MHz', 'Licensed', '~3 km', '4G LTE'],
    ['5G CBRS', '3.55-3.7 GHz', '150 MHz', 'Shared', '~2 km', '5G, private LTE'],
    ['WiFi 5', '5.15-5.85 GHz', '700 MHz', 'Unlicensed', '~30 m', 'WiFi 802.11ac/ax'],
    ['WiFi 6E', '5.925-7.125 GHz', '1200 MHz', 'Unlicensed', '~30 m', 'WiFi 802.11ax'],
    ['5G mmWave (24)', '24.25-25 GHz', '750 MHz', 'Licensed', '~500 m', '5G high-capacity'],
    ['5G mmWave (28)', '27.5-28.35 GHz', '850 MHz', 'Licensed', '~500 m', '5G high-capacity'],
    ['5G mmWave (39)', '37-40 GHz', '1.4 GHz', 'Licensed', '~300 m', '5G high-capacity'],
    ['WiGig', '57-71 GHz', '14 GHz', 'Unlicensed', '~10 m', '802.11ad/ay'],
]

table = ax.table(cellText=table_data, loc='center', cellLoc='left')
table.auto_set_font_size(False)
table.set_fontsize(10)
table.scale(1, 2.2)

# Style header row
for i in range(6):
    table[(0, i)].set_facecolor('#4472C4')
    table[(0, i)].set_text_props(weight='bold', color='white')

# Color code rows by type
for i in range(1, len(table_data)):
    band_type = table_data[i][3]
    if 'Licensed' in band_type:
        if 'Cellular' in table_data[i][0] or '5G' in table_data[i][0]:
            row_color = '#E0F2F7'  # Light blue for cellular
        else:
            row_color = '#F0F0F0'  # Light gray for other licensed
    elif 'Unlicensed' in band_type:
        row_color = '#FFF9E6'  # Light yellow for unlicensed
    elif 'Shared' in band_type:
        row_color = '#F3E5F5'  # Light purple for shared
    else:
        row_color = '#FFFFFF'

    for j in range(6):
        table[(i, j)].set_facecolor(row_color)

# Adjust column widths
table.auto_set_column_width([0, 1, 2, 3, 4, 5])

plt.title('Wireless Spectrum Bands - Detailed Reference',
         fontsize=14, fontweight='bold', pad=20)
plt.savefig('spectrum_allocation_table.png', dpi=300, bbox_inches='tight')
print("Generated: spectrum_allocation_table.png")

# Create frequency vs wavelength plot
fig3, ax = plt.subplots(figsize=(12, 6))

# Frequency range
freq_ghz = np.logspace(-3, 2, 1000)  # 1 MHz to 100 GHz
c = 3e8  # speed of light in m/s
wavelength_m = c / (freq_ghz * 1e9)

# Plot
ax.loglog(freq_ghz, wavelength_m, 'b-', linewidth=2.5)

# Mark key frequencies
key_freqs = {
    0.001: 'AM Radio (1 MHz)',
    0.1: 'FM Radio (100 MHz)',
    0.9: 'Cellular 900',
    2.4: 'WiFi 2.4 GHz',
    5.0: 'WiFi 5 GHz',
    28: '5G mmWave',
    60: 'WiGig 60 GHz',
}

for freq, label in key_freqs.items():
    wavelength = c / (freq * 1e9)
    ax.plot(freq, wavelength, 'ro', markersize=8)
    ax.annotate(label, xy=(freq, wavelength), xytext=(10, 10),
               textcoords='offset points', fontsize=9,
               bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.7))

ax.set_xlabel('Frequency (GHz)', fontsize=12, fontweight='bold')
ax.set_ylabel('Wavelength (m)', fontsize=12, fontweight='bold')
ax.set_title('Frequency vs. Wavelength\nλ = c/f where c = 3×10⁸ m/s',
            fontsize=13, fontweight='bold')
ax.grid(True, which='both', alpha=0.3)

# Add annotation
ax.annotate('Higher frequency\n→ smaller wavelength\n→ smaller antennas\n→ more path loss',
           xy=(28, 0.01), xytext=(10, 0.1),
           arrowprops=dict(arrowstyle='->', color='black', lw=1.5),
           fontsize=10, fontweight='bold',
           bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.7))

plt.tight_layout()
plt.savefig('frequency_wavelength.png', dpi=300, bbox_inches='tight')
print("Generated: frequency_wavelength.png")

plt.show()
