"""
CSMA Collision: Space-Time Diagram for EC 441 Lecture 07.

Shows how two nodes can collide under CSMA even with carrier sensing.
Node A begins transmitting at t=0. Node B senses the channel idle just
before A's signal arrives and begins transmitting — collision results.

The space-time diagram shows frame propagation as parallelograms (rhombuses).
X-axis: position along the channel (A on left, B on right).
Y-axis: time, increasing downward (standard network timing diagram convention).

Usage:
    python plot_csma_collision.py
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# --- Parameters ---
tau = 1.0      # propagation delay A→B (normalized)
T = 2.5        # frame transmission time (T >> tau)
eps = 0.15     # B starts this long before A's signal arrives (worst case)
pos_A = 0.0
pos_B = 1.0    # normalized distance

t_B = tau - eps   # time B starts transmitting

fig, ax = plt.subplots(figsize=(7, 5.5))

# --- Frame parallelograms ---
# A's frame: transmits from t=0 to t=T at position 0;
#   leading bit reaches B at tau, trailing bit at T+tau.
A_verts = [(pos_A, 0), (pos_B, tau), (pos_B, T + tau), (pos_A, T)]
A_patch = plt.Polygon(A_verts, closed=True,
                      facecolor='#3a86ff', edgecolor='#023e8a',
                      alpha=0.35, linewidth=1.5, zorder=2)

# B's frame: transmits from t=t_B to t=t_B+T at position 1 (toward A);
#   leading bit reaches A at t_B+tau, trailing at t_B+T+tau.
B_verts = [(pos_B, t_B), (pos_A, t_B + tau), (pos_A, t_B + T + tau), (pos_B, t_B + T)]
B_patch = plt.Polygon(B_verts, closed=True,
                      facecolor='#ff6b6b', edgecolor='#9d0208',
                      alpha=0.35, linewidth=1.5, zorder=2)

ax.add_patch(A_patch)
ax.add_patch(B_patch)

# --- Key event markers ---
# Dashed horizontal lines for key times
for t, label, color in [
    (0,          't = 0',   '#023e8a'),
    (t_B,        f't = τ − ε', '#9d0208'),
    (tau,        't = τ',   '#023e8a'),
    (t_B + tau,  't ≈ 2τ',  '#9d0208'),
]:
    ax.axhline(y=t, color=color, linestyle=':', alpha=0.55, linewidth=1.0, zorder=1)
    ax.text(-0.07, t, label, ha='right', va='center', fontsize=8.5, color=color)

# --- Annotations ---
ax.annotate('A begins\ntransmitting', xy=(pos_A, 0),
            xytext=(-0.25, -0.35), fontsize=8.5,
            ha='center', color='#023e8a',
            arrowprops=dict(arrowstyle='->', color='#023e8a', lw=1.0))

ax.annotate("B senses channel idle\n(A's signal not yet arrived)\nB begins transmitting",
            xy=(pos_B, t_B),
            xytext=(1.22, t_B - 0.3), fontsize=8.5,
            ha='left', color='#9d0208',
            arrowprops=dict(arrowstyle='->', color='#9d0208', lw=1.0))

ax.annotate("A's signal arrives at B\n(collision already started)",
            xy=(pos_B, tau),
            xytext=(1.22, tau + 0.3), fontsize=8.5,
            ha='left', color='#023e8a',
            arrowprops=dict(arrowstyle='->', color='#023e8a', lw=1.0))

ax.annotate("B's signal reaches A\nA detects collision",
            xy=(pos_A, t_B + tau),
            xytext=(-0.25, t_B + tau + 0.4), fontsize=8.5,
            ha='center', color='#9d0208',
            arrowprops=dict(arrowstyle='->', color='#9d0208', lw=1.0))

# --- Node labels ---
for x, lbl in [(pos_A, 'Node A'), (pos_B, 'Node B')]:
    ax.axvline(x=x, color='gray', linestyle='--', alpha=0.4, linewidth=0.8, zorder=0)
    ax.text(x, -0.55, lbl, ha='center', va='top', fontsize=10, fontweight='bold')

# --- Axes formatting ---
ax.set_xlim(-0.55, 1.75)
ax.set_ylim(-0.7, T + tau + 0.5)
ax.invert_yaxis()
ax.set_xlabel('Position', fontsize=11)
ax.set_ylabel('Time  (increasing downward)', fontsize=11)
ax.set_title('CSMA: Collision in Space–Time\n'
             r'Both frames wasted for full duration $T$',
             fontsize=11, fontweight='bold')
ax.set_xticks([pos_A, pos_B])
ax.set_xticklabels(['A', 'B'], fontsize=11)
ax.set_yticks([])

# --- Legend ---
legend_handles = [
    mpatches.Patch(facecolor='#3a86ff', alpha=0.5, edgecolor='#023e8a', label="A's frame (propagating →)"),
    mpatches.Patch(facecolor='#ff6b6b', alpha=0.5, edgecolor='#9d0208', label="B's frame (propagating ←)"),
]
ax.legend(handles=legend_handles, loc='lower right', fontsize=8.5)

plt.tight_layout()
plt.savefig('/Users/jeffreycarruthers/networking/notes/topic6_mac/csma_collision.png',
            dpi=150, bbox_inches='tight')
plt.close()
print("Saved csma_collision.png")
