"""
Hamming Distance and Sphere Visualization for EC 441 Lecture 05.

Generates two subplots:
1. Visual comparison of two codewords showing matching/differing bits
2. Hamming sphere diagram around codewords illustrating d_min concepts

Usage:
    python plot_hamming_distance.py
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import Circle, FancyArrowPatch


def plot_codeword_comparison(ax):
    """Subplot 1: Visual comparison of two codewords showing matching/differing bits."""
    codeword1 = [1, 0, 1, 1, 0, 0, 1]
    codeword2 = [1, 1, 0, 1, 0, 1, 1]

    n = len(codeword1)
    hamming_dist = sum(a != b for a, b in zip(codeword1, codeword2))

    bar_width = 0.35
    x = np.arange(n)

    for i in range(n):
        match = codeword1[i] == codeword2[i]
        bg_color = '#d4edda' if match else '#f8d7da'
        ax.axvspan(i - 0.45, i + 0.45, alpha=0.4, color=bg_color, zorder=0)

    bars1 = ax.bar(x - bar_width / 2, codeword1, bar_width,
                   label='Codeword 1', color='#2196F3', edgecolor='white', linewidth=1.5, zorder=2)
    bars2 = ax.bar(x + bar_width / 2, codeword2, bar_width,
                   label='Codeword 2', color='#FF9800', edgecolor='white', linewidth=1.5, zorder=2)

    for i in range(n):
        if codeword1[i] != codeword2[i]:
            ax.text(i, 1.18, '×', ha='center', va='center',
                    fontsize=16, fontweight='bold', color='red')

    for bar_group in [bars1, bars2]:
        for bar in bar_group:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2., height / 2,
                    f'{int(height)}', ha='center', va='center',
                    fontsize=11, fontweight='bold', color='white')

    ax.set_xlabel('Bit Position', fontsize=12, fontweight='bold')
    ax.set_ylabel('Bit Value', fontsize=12, fontweight='bold')
    ax.set_title(f'Hamming Distance = {hamming_dist}', fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels([f'b{i}' for i in range(n)])
    ax.set_ylim(-0.1, 1.5)
    ax.set_yticks([0, 1])
    ax.legend(loc='upper right', fontsize=10)
    ax.grid(axis='y', alpha=0.3)

    match_patch = mpatches.Patch(color='#d4edda', alpha=0.6, label='Match')
    diff_patch = mpatches.Patch(color='#f8d7da', alpha=0.6, label='Differ')
    ax.legend(handles=[bars1, bars2, match_patch, diff_patch],
              labels=['Codeword 1', 'Codeword 2', 'Match', 'Differ'],
              loc='upper right', fontsize=9)


def plot_hamming_spheres(ax):
    """Subplot 2: Hamming sphere diagram illustrating d_min, e_c, and e_d."""
    ax.set_xlim(-1, 11)
    ax.set_ylim(-2.5, 3.5)
    ax.set_aspect('equal')

    c1_x, c1_y = 2.0, 0.5
    c2_x, c2_y = 8.0, 0.5
    d_min = 5

    # Draw detection-only spheres (larger, dashed)
    ed_radius = 1.8
    circle_ed1 = Circle((c1_x, c1_y), ed_radius, fill=False,
                         linestyle='--', linewidth=1.5, edgecolor='#4CAF50', zorder=2)
    circle_ed2 = Circle((c2_x, c2_y), ed_radius, fill=False,
                         linestyle='--', linewidth=1.5, edgecolor='#4CAF50', zorder=2)
    ax.add_patch(circle_ed1)
    ax.add_patch(circle_ed2)

    # Draw correction spheres (smaller, solid, filled)
    ec_radius = 1.0
    circle_ec1 = Circle((c1_x, c1_y), ec_radius, fill=True,
                         facecolor='#BBDEFB', edgecolor='#2196F3',
                         linewidth=2, alpha=0.5, zorder=3)
    circle_ec2 = Circle((c2_x, c2_y), ec_radius, fill=True,
                         facecolor='#BBDEFB', edgecolor='#2196F3',
                         linewidth=2, alpha=0.5, zorder=3)
    ax.add_patch(circle_ec1)
    ax.add_patch(circle_ec2)

    # Draw codeword points
    ax.plot(c1_x, c1_y, 'ko', markersize=10, zorder=5)
    ax.plot(c2_x, c2_y, 'ko', markersize=10, zorder=5)
    ax.text(c1_x, c1_y - 0.35, '$C_i$', ha='center', va='top',
            fontsize=14, fontweight='bold')
    ax.text(c2_x, c2_y - 0.35, '$C_j$', ha='center', va='top',
            fontsize=14, fontweight='bold')

    # d_min arrow
    arrow = FancyArrowPatch((c1_x, c1_y + 2.2), (c2_x, c2_y + 2.2),
                            arrowstyle='<->', mutation_scale=15,
                            linewidth=2, color='#F44336', zorder=4)
    ax.add_patch(arrow)
    ax.text((c1_x + c2_x) / 2, c1_y + 2.55,
            f'$d_{{\\min}} = {d_min}$', ha='center', va='bottom',
            fontsize=13, fontweight='bold', color='#F44336')

    # e_c label
    ax.annotate('', xy=(c1_x + ec_radius, c1_y), xytext=(c1_x, c1_y),
                arrowprops=dict(arrowstyle='->', color='#2196F3', lw=1.5))
    ax.text(c1_x + ec_radius / 2, c1_y + 0.25, '$e_c$',
            ha='center', fontsize=12, color='#2196F3', fontweight='bold')

    # Detection region label
    ax.text(c2_x + ed_radius + 0.15, c2_y, '$e_d$',
            ha='left', fontsize=12, color='#4CAF50', fontweight='bold')

    # Legend
    correction_patch = mpatches.Patch(facecolor='#BBDEFB', edgecolor='#2196F3',
                                       linewidth=2, alpha=0.5, label='Correction sphere')
    detection_circle = mpatches.Patch(facecolor='none', edgecolor='#4CAF50',
                                       linewidth=1.5, linestyle='--', label='Detection boundary')
    ax.legend(handles=[correction_patch, detection_circle],
              loc='lower center', fontsize=10, ncol=2,
              bbox_to_anchor=(0.5, -0.15))

    ax.set_title('Hamming Spheres: Combined Detection & Correction',
                 fontsize=14, fontweight='bold')
    ax.axis('off')


def main():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

    plot_codeword_comparison(ax1)
    plot_hamming_spheres(ax2)

    fig.suptitle('EC 441: Hamming Distance and Error Control Spheres',
                 fontsize=16, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig('hamming_distance.png', dpi=300, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()
    print("Saved: hamming_distance.png")


if __name__ == '__main__':
    main()
