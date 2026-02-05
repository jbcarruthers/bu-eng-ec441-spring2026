#!/usr/bin/env python3
"""
Generate QAM constellation diagrams for Lecture 4.

Shows BPSK, QPSK, 16-QAM, 64-QAM, 256-QAM, and 1024-QAM with
decision boundaries and noise clouds at different SNR levels.
"""

import numpy as np
import matplotlib.pyplot as plt

def generate_qam_symbols(M):
    """
    Generate M-QAM constellation points (square constellations).

    Parameters:
    - M: constellation size (4, 16, 64, 256, 1024)

    Returns:
    - complex array of symbol locations
    """
    if M == 2:  # BPSK
        return np.array([-1, 1])
    elif M == 4:  # QPSK
        return np.array([1+1j, -1+1j, 1-1j, -1-1j]) / np.sqrt(2)
    else:
        # Square QAM
        k = int(np.sqrt(M))
        assert k * k == M, "M must be a perfect square for QAM"

        # Generate I and Q coordinates
        coords = np.arange(k) - (k - 1) / 2
        I, Q = np.meshgrid(coords, coords)
        symbols = (I.ravel() + 1j * Q.ravel())

        # Normalize to unit average power
        symbols = symbols / np.sqrt(np.mean(np.abs(symbols)**2))

        return symbols

def plot_qam_constellation(ax, M, SNR_dB=25, show_noise=True, show_grid=True):
    """
    Plot M-QAM constellation with decision boundaries and noise.

    Parameters:
    - ax: matplotlib axis
    - M: constellation size
    - SNR_dB: SNR in dB for noise clouds
    - show_noise: whether to show noise clouds
    - show_grid: whether to show decision boundaries
    """
    symbols = generate_qam_symbols(M)

    # Plot constellation points
    if M == 2:  # BPSK (1D)
        ax.plot(symbols.real, np.zeros_like(symbols.real), 'ro',
               markersize=10, markeredgewidth=2, markerfacecolor='red')
        y_lim = 1.5
    else:
        ax.plot(symbols.real, symbols.imag, 'ro', markersize=10,
               markeredgewidth=2, markerfacecolor='red', label='Symbols')
        y_lim = max(np.abs(symbols.imag)) * 1.5

    # Add noise clouds if requested
    if show_noise and SNR_dB is not None:
        SNR_linear = 10**(SNR_dB / 10)
        Es = np.mean(np.abs(symbols)**2)
        sigma = np.sqrt(Es / (2 * SNR_linear))  # per dimension

        for sym in symbols:
            n_samples = 150 if M <= 64 else 50
            if M == 2:
                noise_real = np.random.normal(sym.real, sigma, n_samples)
                noise_imag = np.random.normal(0, 0.02, n_samples)
            else:
                noise_real = np.random.normal(sym.real, sigma, n_samples)
                noise_imag = np.random.normal(sym.imag, sigma, n_samples)

            ax.plot(noise_real, noise_imag, 'b.', alpha=0.15, markersize=3)

    # Draw decision boundaries (grid)
    if show_grid and M > 2:
        k = int(np.sqrt(M))
        # Normalize same as symbols
        temp_coords = np.arange(k) - (k - 1) / 2
        temp_symbols = temp_coords / np.sqrt(np.mean(temp_coords**2) * 2)

        # Thresholds are midpoints
        if k > 1:
            thresholds = [(temp_symbols[i] + temp_symbols[i+1]) / 2
                         for i in range(k-1)]
            x_lim = max(np.abs(symbols.real)) * 1.5

            for thresh in thresholds:
                ax.axvline(x=thresh, color='blue', linestyle='--',
                          linewidth=1, alpha=0.5)
                ax.axhline(y=thresh, color='blue', linestyle='--',
                          linewidth=1, alpha=0.5)

    # Formatting
    ax.axhline(y=0, color='k', linewidth=0.8)
    ax.axvline(x=0, color='k', linewidth=0.8)
    ax.set_xlabel('In-Phase (I)', fontsize=10, fontweight='bold')
    ax.set_ylabel('Quadrature (Q)', fontsize=10, fontweight='bold')

    # Title with bits per symbol
    bits_per_symbol = int(np.log2(M))
    if M == 2:
        title = f'BPSK\n{bits_per_symbol} bit/symbol'
    elif M == 4:
        title = f'QPSK\n{bits_per_symbol} bits/symbol'
    else:
        title = f'{M}-QAM\n{bits_per_symbol} bits/symbol'

    ax.set_title(title, fontsize=11, fontweight='bold')

    x_lim = max(np.abs(symbols.real)) * 1.5
    ax.set_xlim(-x_lim, x_lim)
    ax.set_ylim(-y_lim, y_lim)
    ax.grid(True, alpha=0.2, linestyle=':')
    ax.set_aspect('equal')

    # Add info text with SNR if noise is shown
    if show_noise and SNR_dB is not None:
        info_text = f'SNR = {SNR_dB} dB'
        ax.text(0.02, 0.98, info_text, transform=ax.transAxes,
               ha='left', va='top', fontsize=9,
               bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

# Create figure with 6 constellations
fig, axes = plt.subplots(2, 3, figsize=(15, 10))

# Different SNR for different modulations (higher order needs higher SNR)
modulations = [2, 4, 16, 64, 256, 1024]
snr_values = [15, 20, 25, 30, 35, 40]

for ax, M, snr in zip(axes.ravel(), modulations, snr_values):
    plot_qam_constellation(ax, M, SNR_dB=snr, show_noise=True, show_grid=True)

plt.suptitle('QAM Constellation Diagrams with Decision Boundaries\n(with noise clouds)',
             fontsize=14, fontweight='bold', y=0.995)
plt.tight_layout()
plt.savefig('qam_constellations.png', dpi=300, bbox_inches='tight')
print("Generated: qam_constellations.png")

# Create comparison plot: different SNR levels for 64-QAM
fig2, axes2 = plt.subplots(1, 3, figsize=(15, 5))
snr_levels = [15, 25, 35]

for ax, snr in zip(axes2, snr_levels):
    plot_qam_constellation(ax, 64, SNR_dB=snr, show_noise=True, show_grid=True)

plt.suptitle('64-QAM Constellation at Different SNR Levels',
             fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('qam_snr_comparison.png', dpi=300, bbox_inches='tight')
print("Generated: qam_snr_comparison.png")

# Create spectral efficiency vs. required SNR plot
fig3, ax = plt.subplots(figsize=(10, 6))

M_values = np.array([2, 4, 16, 64, 256, 1024])
bits_per_symbol = np.log2(M_values)

# Theoretical SNR required for BER = 10^-6 (approximate)
# Using approximation: SNR_req ≈ (2^k - 1) * Q^-2(BER/k)
# Simplified empirical formula
snr_required = 10 * np.log10(M_values - 1) + 10  # Rough approximation in dB

# Plot
ax.plot(bits_per_symbol, snr_required, 'bo-', linewidth=2.5, markersize=10)

# Annotate each point
labels = ['BPSK', 'QPSK', '16-QAM', '64-QAM', '256-QAM', '1024-QAM']
for k, snr, label in zip(bits_per_symbol, snr_required, labels):
    ax.annotate(label, xy=(k, snr), xytext=(5, 5),
               textcoords='offset points', fontsize=10, fontweight='bold')

ax.set_xlabel('Spectral Efficiency (bits/symbol)', fontsize=12, fontweight='bold')
ax.set_ylabel('Required SNR (dB) for BER < 10⁻⁶', fontsize=12, fontweight='bold')
ax.set_title('QAM Modulation: Spectral Efficiency vs. SNR Requirement',
            fontsize=13, fontweight='bold')
ax.grid(True, alpha=0.3)
ax.set_xlim(0, 11)

# Add annotation explaining tradeoff (moved down and right to avoid overlap)
ax.annotate('Higher spectral efficiency\n→ requires higher SNR',
           xy=(8, 35), xytext=(7, 20),
           arrowprops=dict(arrowstyle='->', color='red', lw=2),
           fontsize=11, fontweight='bold',
           bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.7))

plt.tight_layout()
plt.savefig('qam_efficiency_vs_snr.png', dpi=300, bbox_inches='tight')
print("Generated: qam_efficiency_vs_snr.png")

plt.show()
