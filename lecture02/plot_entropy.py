#!/usr/bin/env python3
"""
Plot entropy H(p) for a Bernoulli random variable with parameter p.

For a Bernoulli random variable X with P(X=1) = p:
H(p) = -p*log2(p) - (1-p)*log2(1-p)

This shows that maximum entropy occurs at p=0.5 (maximum uncertainty),
while entropy approaches 0 as p approaches 0 or 1 (certainty).
"""

import numpy as np
import matplotlib.pyplot as plt

def entropy(p):
    """
    Calculate entropy H(p) for Bernoulli random variable.

    H(p) = -p*log2(p) - (1-p)*log2(1-p)

    Uses convention that 0*log2(0) = 0 at boundaries.
    """
    # Handle edge cases where p=0 or p=1
    result = np.zeros_like(p)

    # Only calculate where 0 < p < 1
    mask = (p > 0) & (p < 1)
    p_valid = p[mask]

    result[mask] = -(p_valid * np.log2(p_valid) +
                     (1 - p_valid) * np.log2(1 - p_valid))

    return result

# Generate p values from 0 to 1
p = np.linspace(0, 1, 1000)
H_p = entropy(p)

# Create the plot
plt.figure(figsize=(10, 6))
plt.plot(p, H_p, 'b-', linewidth=2)
plt.grid(True, alpha=0.3)
plt.xlabel('p (probability)', fontsize=12)
plt.ylabel('H(p) (bits)', fontsize=12)
plt.title('Entropy of Bernoulli Random Variable: H(p) = -p log₂(p) - (1-p) log₂(1-p)',
          fontsize=13)

# Mark the maximum
plt.plot(0.5, 1.0, 'ro', markersize=8, label='Maximum: H(0.5) = 1 bit')

# Add annotations
plt.annotate('Maximum entropy\nat p = 0.5',
             xy=(0.5, 1.0), xytext=(0.65, 0.85),
             arrowprops=dict(arrowstyle='->', color='red'),
             fontsize=11, color='red')

plt.annotate('Certainty: H(0) = 0',
             xy=(0, 0), xytext=(0.15, 0.15),
             arrowprops=dict(arrowstyle='->', color='green'),
             fontsize=10, color='green')

plt.annotate('Certainty: H(1) = 0',
             xy=(1, 0), xytext=(0.75, 0.15),
             arrowprops=dict(arrowstyle='->', color='green'),
             fontsize=10, color='green')

plt.xlim(-0.05, 1.05)
plt.ylim(-0.05, 1.1)
plt.legend(loc='upper left', fontsize=10)

# Save the figure
plt.tight_layout()
plt.savefig('entropy_plot.png', dpi=150, bbox_inches='tight')
print("Saved entropy plot to entropy_plot.png")

# Also show some key values
print("\nKey entropy values:")
print(f"H(0.0) = {entropy(np.array([0.0]))[0]:.4f} bits")
print(f"H(0.1) = {entropy(np.array([0.1]))[0]:.4f} bits")
print(f"H(0.25) = {entropy(np.array([0.25]))[0]:.4f} bits")
print(f"H(0.5) = {entropy(np.array([0.5]))[0]:.4f} bits")
print(f"H(0.75) = {entropy(np.array([0.75]))[0]:.4f} bits")
print(f"H(0.9) = {entropy(np.array([0.9]))[0]:.4f} bits")
print(f"H(1.0) = {entropy(np.array([1.0]))[0]:.4f} bits")
