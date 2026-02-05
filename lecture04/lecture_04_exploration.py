import marimo

__generated_with = "0.19.6"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import numpy as np
    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle
    from scipy import special
    return Rectangle, mo, np, plt, special


@app.cell
def _(mo):
    mo.md(r"""
    # Lecture 4: Physical Layer - Wireless Communications Interactive Exploration

    **EC 441 - Introduction to Computer Networking**

    This notebook contains interactive demonstrations and experiments to explore wireless communication concepts including path loss, link budgets, QAM modulation, spectrum allocation, and cellular frequency reuse.
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ---

    ## Cell 1: Free Space Path Loss Calculator

    Free space path loss (FSPL) describes signal attenuation in ideal conditions with no obstacles.

    **Friis equation:**

    $$L_{\text{FSPL}} (\text{dB}) = 32.45 + 20\log_{10}(f_{\text{MHz}}) + 20\log_{10}(d_{\text{km}})$$

    **Key insight:** Path loss increases 20 dB per decade of distance or frequency.
    """)
    return


@app.cell
def _(mo):
    # Free space path loss controls
    fspl_frequency = mo.ui.slider(
        start=100,
        stop=100000,
        step=100,
        value=2400,
        label="Frequency (MHz):",
        show_value=True
    )

    fspl_distance = mo.ui.slider(
        start=1,
        stop=100000,
        step=10,
        value=100,
        label="Distance (m):",
        show_value=True
    )

    fspl_tx_power = mo.ui.slider(
        start=-20,
        stop=40,
        step=1,
        value=20,
        label="Transmit power (dBm):",
        show_value=True
    )

    fspl_tx_gain = mo.ui.slider(
        start=0,
        stop=30,
        step=1,
        value=2,
        label="TX antenna gain (dBi):",
        show_value=True
    )

    fspl_rx_gain = mo.ui.slider(
        start=0,
        stop=30,
        step=1,
        value=2,
        label="RX antenna gain (dBi):",
        show_value=True
    )

    mo.vstack([
        fspl_frequency,
        fspl_distance,
        fspl_tx_power,
        fspl_tx_gain,
        fspl_rx_gain
    ])
    return (
        fspl_distance,
        fspl_frequency,
        fspl_rx_gain,
        fspl_tx_gain,
        fspl_tx_power,
    )


@app.cell
def _(
    fspl_distance,
    fspl_frequency,
    fspl_rx_gain,
    fspl_tx_gain,
    fspl_tx_power,
    np,
    plt,
):
    def calculate_fspl(freq_mhz, dist_m):
        """Calculate free space path loss."""
        dist_km = dist_m / 1000
        if dist_km <= 0 or freq_mhz <= 0:
            return 0
        fspl = 32.45 + 20 * np.log10(freq_mhz) + 20 * np.log10(dist_km)
        return fspl

    # Get values
    freq_mhz_fspl = fspl_frequency.value
    dist_m_fspl = fspl_distance.value
    tx_pwr_fspl = fspl_tx_power.value
    tx_gain_fspl = fspl_tx_gain.value
    rx_gain_fspl = fspl_rx_gain.value

    # Calculate
    c = 3e8  # speed of light
    wavelength_m = c / (freq_mhz_fspl * 1e6)
    path_loss_fspl = calculate_fspl(freq_mhz_fspl, dist_m_fspl)
    rx_power_fspl = tx_pwr_fspl + tx_gain_fspl + rx_gain_fspl - path_loss_fspl

    # Create visualizations
    fig_fspl, (ax_fspl1, ax_fspl2) = plt.subplots(1, 2, figsize=(14, 5))

    # Plot 1: Path loss vs. distance for multiple frequencies
    dist_range = np.logspace(0, 4, 100)  # 1m to 10km
    frequencies = [900, 2400, 5000, 28000, 60000]  # MHz
    freq_labels = ['900 MHz (Cellular)', '2.4 GHz (WiFi)', '5 GHz (WiFi)',
                   '28 GHz (5G mmWave)', '60 GHz (WiGig)']

    for freq_val, freq_label in zip(frequencies, freq_labels):
        path_loss_range = [calculate_fspl(freq_val, d) for d in dist_range]
        ax_fspl1.semilogx(dist_range, path_loss_range, linewidth=2, label=freq_label)

    # Mark current point
    ax_fspl1.semilogx(dist_m_fspl, path_loss_fspl, 'ro', markersize=10,
                     label=f'Current: {path_loss_fspl:.1f} dB')

    ax_fspl1.grid(True, alpha=0.3, which='both')
    ax_fspl1.set_xlabel('Distance (m)', fontsize=11)
    ax_fspl1.set_ylabel('Path Loss (dB)', fontsize=11)
    ax_fspl1.set_title('Free Space Path Loss vs. Distance', fontsize=12)
    ax_fspl1.legend(fontsize=9, loc='upper left')

    # Plot 2: Path loss vs. frequency for multiple distances
    freq_range = np.logspace(2, 5, 100)  # 100 MHz to 100 GHz
    distances = [10, 100, 1000, 10000]  # meters
    dist_labels = ['10 m', '100 m', '1 km', '10 km']

    for dist_val, dist_label in zip(distances, dist_labels):
        path_loss_freq_range = [calculate_fspl(f, dist_val) for f in freq_range]
        ax_fspl2.semilogx(freq_range, path_loss_freq_range, linewidth=2, label=dist_label)

    # Mark current point
    ax_fspl2.semilogx(freq_mhz_fspl, path_loss_fspl, 'ro', markersize=10,
                     label=f'Current: {path_loss_fspl:.1f} dB')

    ax_fspl2.grid(True, alpha=0.3, which='both')
    ax_fspl2.set_xlabel('Frequency (MHz)', fontsize=11)
    ax_fspl2.set_ylabel('Path Loss (dB)', fontsize=11)
    ax_fspl2.set_title('Free Space Path Loss vs. Frequency', fontsize=12)
    ax_fspl2.legend(fontsize=9, loc='upper left')

    plt.tight_layout()

    fig_fspl
    return (
        calculate_fspl,
        dist_m_fspl,
        freq_mhz_fspl,
        path_loss_fspl,
        rx_power_fspl,
        tx_pwr_fspl,
        wavelength_m,
    )


@app.cell
def _(
    dist_m_fspl,
    freq_mhz_fspl,
    mo,
    path_loss_fspl,
    rx_power_fspl,
    tx_pwr_fspl,
    wavelength_m,
):
    mo.md(f"""
    ### Free Space Path Loss Results

    **Parameters:**
    - Frequency: {freq_mhz_fspl} MHz (λ = {wavelength_m:.3f} m)
    - Distance: {dist_m_fspl} m

    **Results:**
    - Path loss: **{path_loss_fspl:.1f} dB**
    - Transmit power: {tx_pwr_fspl} dBm
    - Received power: **{rx_power_fspl:.1f} dBm**

    **Key insights:**
    - Doubling distance → +6 dB loss
    - 10× distance → +20 dB loss
    - Doubling frequency → +6 dB loss
    - Higher frequencies have greater path loss for same distance
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ---

    ## Cell 2: Empirical Path Loss Explorer

    Real-world propagation differs from free space due to obstacles, reflections, and scattering.

    **Empirical model:**

    $$L(d) = L_0 + 10n\log_{10}\left(\frac{d}{d_0}\right) + X_\sigma$$

    where $n$ is the path loss exponent and $X_\sigma$ is shadow fading.

    **Path loss exponent:**
    - Free space: $n = 2$
    - Urban cellular: $n = 2.7-3.5$
    - Indoor LOS: $n = 1.6-1.8$
    - Indoor NLOS: $n = 3-5$
    """)
    return


@app.cell
def _(mo):
    # Empirical path loss controls
    env_type = mo.ui.dropdown(
        ["Free Space (n=2)", "Urban Cellular (n=3)", "Indoor LOS (n=1.8)",
         "Indoor NLOS (n=4)", "Obstructed Urban (n=5)"],
        value="Urban Cellular (n=3)",
        label="Environment:"
    )

    path_loss_exp = mo.ui.slider(
        start=1.5,
        stop=6.0,
        step=0.1,
        value=3.0,
        label="Path loss exponent (n):",
        show_value=True
    )

    shadow_fading = mo.ui.slider(
        start=0,
        stop=12,
        step=1,
        value=6,
        label="Shadow fading σ (dB):",
        show_value=True
    )

    ref_distance = mo.ui.slider(
        start=1,
        stop=10,
        step=1,
        value=1,
        label="Reference distance d₀ (m):",
        show_value=True
    )

    emp_frequency = mo.ui.slider(
        start=100,
        stop=10000,
        step=100,
        value=2400,
        label="Frequency (MHz):",
        show_value=True
    )

    mo.vstack([
        env_type,
        path_loss_exp,
        shadow_fading,
        ref_distance,
        emp_frequency
    ])
    return emp_frequency, env_type, path_loss_exp, ref_distance, shadow_fading


@app.cell
def _(
    calculate_fspl,
    emp_frequency,
    env_type,
    np,
    path_loss_exp,
    plt,
    ref_distance,
    shadow_fading,
):
    def calculate_empirical_path_loss(freq_mhz, d_m, d0_m, n_exp):
        """Calculate empirical path loss with path loss exponent."""
        L0 = calculate_fspl(freq_mhz, d0_m)
        if d_m <= 0 or d0_m <= 0:
            return L0
        L_d = L0 + 10 * n_exp * np.log10(d_m / d0_m)
        return L_d

    # Get values
    env_val = env_type.value
    n_val = path_loss_exp.value
    sigma_val = shadow_fading.value
    d0_val = ref_distance.value
    freq_emp = emp_frequency.value

    # Create visualization
    fig_emp, ax_emp = plt.subplots(figsize=(12, 6))

    dist_emp_range = np.logspace(0, 4, 100)  # 1m to 10km

    # Free space reference (n=2)
    fspl_emp = [calculate_fspl(freq_emp, d) for d in dist_emp_range]
    ax_emp.semilogx(dist_emp_range, fspl_emp, 'k--', linewidth=2,
                   label='Free Space (n=2)', alpha=0.7)

    # Current empirical model (mean)
    emp_loss = [calculate_empirical_path_loss(freq_emp, d, d0_val, n_val)
                for d in dist_emp_range]
    ax_emp.semilogx(dist_emp_range, emp_loss, 'b-', linewidth=2.5,
                   label=f'Empirical (n={n_val:.1f})')

    # Shadow fading bounds (±σ and ±2σ)
    emp_loss_plus_sigma = [pl + sigma_val for pl in emp_loss]
    emp_loss_minus_sigma = [pl - sigma_val for pl in emp_loss]
    emp_loss_plus_2sigma = [pl + 2*sigma_val for pl in emp_loss]
    emp_loss_minus_2sigma = [pl - 2*sigma_val for pl in emp_loss]

    ax_emp.fill_between(dist_emp_range, emp_loss_minus_2sigma, emp_loss_plus_2sigma,
                       alpha=0.15, color='blue', label=f'±2σ ({2*sigma_val} dB)')
    ax_emp.fill_between(dist_emp_range, emp_loss_minus_sigma, emp_loss_plus_sigma,
                       alpha=0.25, color='blue', label=f'±σ ({sigma_val} dB)')

    # Common environments for comparison
    environments = {
        'Indoor LOS (n=1.8)': 1.8,
        'Urban (n=3)': 3.0,
        'Indoor NLOS (n=4)': 4.0,
        'Obstructed (n=5)': 5.0
    }

    colors_env = ['green', 'orange', 'red', 'purple']
    for (env_name, n_env), color in zip(environments.items(), colors_env):
        if n_env != n_val:  # Don't duplicate current curve
            emp_env = [calculate_empirical_path_loss(freq_emp, d, d0_val, n_env)
                      for d in dist_emp_range]
            ax_emp.semilogx(dist_emp_range, emp_env, '--', linewidth=1.5,
                           color=color, alpha=0.6, label=env_name)

    ax_emp.grid(True, alpha=0.3, which='both')
    ax_emp.set_xlabel('Distance (m)', fontsize=11)
    ax_emp.set_ylabel('Path Loss (dB)', fontsize=11)
    ax_emp.set_title(f'Empirical Path Loss Models ({freq_emp} MHz)', fontsize=12)
    ax_emp.legend(fontsize=9, loc='upper left')
    ax_emp.set_ylim([40, 200])

    plt.tight_layout()

    fig_emp
    return (
        calculate_empirical_path_loss,
        d0_val,
        env_val,
        freq_emp,
        n_val,
        sigma_val,
    )


@app.cell
def _(d0_val, env_val, freq_emp, mo, n_val, sigma_val):
    mo.md(f"""
    ### Empirical Path Loss Results

    **Configuration:**
    - Environment: {env_val}
    - Path loss exponent: n = {n_val}
    - Shadow fading: σ = {sigma_val} dB
    - Reference distance: d₀ = {d0_val} m
    - Frequency: {freq_emp} MHz

    **Observations:**
    - Higher n → steeper path loss with distance
    - n > 2: obstacles increase attenuation beyond free space
    - n < 2: waveguiding effects (rare, e.g., tunnels)
    - Shadow fading represents statistical variation (log-normal)
    - 68% of measurements within ±σ, 95% within ±2σ

    **Design impact:** Must add fading margin to link budget!
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ---

    ## Cell 3: Wireless Link Budget Calculator

    Link budget accounts for all gains and losses in a wireless link.

    **Link budget equation:**
    $$P_r (\text{dBm}) = P_t + G_t + G_r - L_{\text{path}} - L_{\text{misc}}$$

    **Margin:**
    $$\text{Margin} = P_r - S_{\text{min}} - M_{\text{fade}}$$

    where $S_{\text{min}}$ is receiver sensitivity and $M_{\text{fade}}$ is fading margin.
    """)
    return


@app.cell
def _(mo):
    # Link budget controls
    lb_tx_power = mo.ui.slider(
        start=-20,
        stop=50,
        step=1,
        value=23,
        label="Transmit power (dBm):",
        show_value=True
    )

    lb_frequency = mo.ui.slider(
        start=100,
        stop=10000,
        step=100,
        value=2400,
        label="Frequency (MHz):",
        show_value=True
    )

    lb_distance = mo.ui.slider(
        start=1,
        stop=10000,
        step=10,
        value=100,
        label="Distance (m):",
        show_value=True
    )

    lb_environment = mo.ui.dropdown(
        ["Free Space (n=2)", "Urban (n=3)", "Indoor LOS (n=1.8)",
         "Indoor NLOS (n=4)", "Obstructed (n=5)"],
        value="Indoor NLOS (n=4)",
        label="Environment:"
    )

    lb_tx_gain = mo.ui.slider(
        start=0,
        stop=30,
        step=1,
        value=5,
        label="TX antenna gain (dBi):",
        show_value=True
    )

    lb_rx_gain = mo.ui.slider(
        start=0,
        stop=30,
        step=1,
        value=2,
        label="RX antenna gain (dBi):",
        show_value=True
    )

    lb_misc_loss = mo.ui.slider(
        start=0,
        stop=20,
        step=1,
        value=3,
        label="Miscellaneous losses (dB):",
        show_value=True
    )

    lb_sensitivity = mo.ui.slider(
        start=-110,
        stop=-50,
        step=1,
        value=-80,
        label="Receiver sensitivity (dBm):",
        show_value=True
    )

    lb_fade_margin = mo.ui.slider(
        start=0,
        stop=30,
        step=1,
        value=15,
        label="Fading margin (dB):",
        show_value=True
    )

    mo.vstack([
        lb_tx_power,
        lb_frequency,
        lb_distance,
        lb_environment,
        lb_tx_gain,
        lb_rx_gain,
        lb_misc_loss,
        lb_sensitivity,
        lb_fade_margin
    ])
    return (
        lb_distance,
        lb_environment,
        lb_fade_margin,
        lb_frequency,
        lb_misc_loss,
        lb_rx_gain,
        lb_sensitivity,
        lb_tx_gain,
        lb_tx_power,
    )


@app.cell
def _(
    calculate_empirical_path_loss,
    lb_distance,
    lb_environment,
    lb_fade_margin,
    lb_frequency,
    lb_misc_loss,
    lb_rx_gain,
    lb_sensitivity,
    lb_tx_gain,
    lb_tx_power,
    np,
    plt,
):
    # Get values
    tx_pwr_lb = lb_tx_power.value
    freq_lb = lb_frequency.value
    dist_lb = lb_distance.value
    env_lb = lb_environment.value
    tx_gain_lb = lb_tx_gain.value
    rx_gain_lb = lb_rx_gain.value
    misc_loss_lb = lb_misc_loss.value
    sensitivity_lb = lb_sensitivity.value
    fade_margin_lb = lb_fade_margin.value

    # Extract path loss exponent from environment
    env_to_n = {
        "Free Space (n=2)": 2.0,
        "Urban (n=3)": 3.0,
        "Indoor LOS (n=1.8)": 1.8,
        "Indoor NLOS (n=4)": 4.0,
        "Obstructed (n=5)": 5.0
    }
    n_lb = env_to_n.get(env_lb, 3.0)

    # Calculate path loss
    path_loss_lb = calculate_empirical_path_loss(freq_lb, dist_lb, 1.0, n_lb)

    # Calculate link budget
    eirp_lb = tx_pwr_lb + tx_gain_lb
    rx_signal_lb = eirp_lb + rx_gain_lb - path_loss_lb - misc_loss_lb

    # Calculate margins
    required_signal = sensitivity_lb + fade_margin_lb
    link_margin_lb = rx_signal_lb - required_signal
    link_viable = link_margin_lb > 0

    # Create waterfall chart
    fig_lb, ax_lb = plt.subplots(figsize=(14, 7))

    components_lb = ['Tx Power', 'Tx Gain', 'Path Loss', 'Misc Loss', 'Rx Gain', 'Rx Signal']
    values_lb = [tx_pwr_lb, tx_gain_lb, -path_loss_lb, -misc_loss_lb, rx_gain_lb, 0]

    # Cumulative values
    cumulative_lb = [tx_pwr_lb]
    cumulative_lb.append(cumulative_lb[-1] + tx_gain_lb)
    cumulative_lb.append(cumulative_lb[-1] - path_loss_lb)
    cumulative_lb.append(cumulative_lb[-1] - misc_loss_lb)
    cumulative_lb.append(cumulative_lb[-1] + rx_gain_lb)

    # Colors
    colors_lb = ['green', 'green', 'red', 'red', 'green', 'blue']

    # Plot bars
    x_pos_lb = np.arange(len(components_lb))

    # First bar (Tx Power)
    ax_lb.bar(0, tx_pwr_lb, color='green', alpha=0.7, edgecolor='black', linewidth=1.5)

    # Gains and losses
    for i_lb in range(1, 5):
        bottom_lb = min(cumulative_lb[i_lb-1], cumulative_lb[i_lb])
        height_lb = abs(cumulative_lb[i_lb] - cumulative_lb[i_lb-1])
        ax_lb.bar(i_lb, height_lb, bottom=bottom_lb, color=colors_lb[i_lb],
                 alpha=0.7, edgecolor='black', linewidth=1.5)

    # Final bar (Rx Signal)
    ax_lb.bar(5, rx_signal_lb, color='blue', alpha=0.7, edgecolor='black', linewidth=2)

    # Add horizontal lines for sensitivity and required signal
    ax_lb.axhline(y=sensitivity_lb, color='orange', linestyle='--', linewidth=2,
                 label=f'Sensitivity ({sensitivity_lb} dBm)')
    ax_lb.axhline(y=required_signal, color='red', linestyle='--', linewidth=2,
                 label=f'Required Signal ({required_signal} dBm)')

    # Add value labels
    for i_lb in range(5):
        ax_lb.text(i_lb, cumulative_lb[i_lb] + 2, f'{cumulative_lb[i_lb]:.1f}',
                  ha='center', fontsize=9, fontweight='bold')

    ax_lb.text(5, rx_signal_lb + 2, f'{rx_signal_lb:.1f}',
              ha='center', fontsize=9, fontweight='bold')

    # Add margin annotation
    if link_viable:
        ax_lb.annotate('', xy=(5.3, required_signal), xytext=(5.3, rx_signal_lb),
                      arrowprops=dict(arrowstyle='<->', color='green', lw=2))
        ax_lb.text(5.5, (required_signal + rx_signal_lb)/2,
                  f'Margin\n{link_margin_lb:.1f} dB',
                  fontsize=10, color='green', fontweight='bold')

    ax_lb.set_xticks(x_pos_lb)
    ax_lb.set_xticklabels(components_lb, rotation=0)
    ax_lb.set_ylabel('Power (dBm)', fontsize=11)
    ax_lb.set_title(f'Wireless Link Budget - {env_lb}', fontsize=13)
    ax_lb.grid(True, alpha=0.3, axis='y')
    ax_lb.legend(loc='upper left')

    plt.tight_layout()

    fig_lb
    return (
        dist_lb,
        env_lb,
        fade_margin_lb,
        freq_lb,
        link_margin_lb,
        link_viable,
        path_loss_lb,
        required_signal,
        rx_signal_lb,
        sensitivity_lb,
    )


@app.cell
def _(
    dist_lb,
    env_lb,
    fade_margin_lb,
    freq_lb,
    link_margin_lb,
    link_viable,
    mo,
    path_loss_lb,
    required_signal,
    rx_signal_lb,
    sensitivity_lb,
):
    status_lb = "✓ **Link viable**" if link_viable else "✗ **Link not viable**"

    mo.md(
        f"""
        ### Wireless Link Budget Results

        **Configuration:**
        - Frequency: {freq_lb} MHz
        - Distance: {dist_lb} m
        - Environment: {env_lb}

        **Link budget:**
        - Path loss: {path_loss_lb:.1f} dB
        - Received signal: **{rx_signal_lb:.1f} dBm**
        - Sensitivity: {sensitivity_lb} dBm
        - Required (with {fade_margin_lb} dB fade margin): {required_signal} dBm

        **Link margin:** {link_margin_lb:.1f} dB

        {status_lb}

        **Recommendations:**
        - **Good margin:** ≥ 10 dB (static), ≥ 20 dB (mobile)
        - **Marginal:** 0-10 dB (may experience outages)
        - **Insufficient:** < 0 dB (increase power, gain, or reduce distance)
        """
    )
    return


@app.cell
def _(mo):
    mo.md(r"""
    ---

    ## Cell 4: QAM Constellation Visualizer

    Quadrature Amplitude Modulation (QAM) encodes data in both amplitude and phase.

    **QAM signal:**
    $$s(t) = I(t)\cos(2\pi f_c t) - Q(t)\sin(2\pi f_c t)$$

    **M-QAM:** M symbols, $\log_2(M)$ bits per symbol

    **Symbol error rate (approximate):**
    $$P_s \approx 4\left(1 - \frac{1}{\sqrt{M}}\right) Q\left(\sqrt{\frac{3}{M-1}\frac{E_s}{N_0}}\right)$$
    """)
    return


@app.cell
def _(mo):
    # QAM controls
    qam_order = mo.ui.dropdown(
        ["BPSK (2)", "QPSK (4)", "16-QAM", "64-QAM", "256-QAM", "1024-QAM"],
        value="16-QAM",
        label="Modulation:"
    )

    qam_snr = mo.ui.slider(
        start=0,
        stop=40,
        step=1,
        value=20,
        label="SNR (dB):",
        show_value=True
    )

    qam_num_symbols = mo.ui.slider(
        start=100,
        stop=5000,
        step=100,
        value=1000,
        label="Number of symbols to display:",
        show_value=True
    )

    mo.vstack([
        qam_order,
        qam_snr,
        qam_num_symbols
    ])
    return qam_num_symbols, qam_order, qam_snr


@app.cell
def _(np, plt, qam_num_symbols, qam_order, qam_snr, special):
    def generate_qam_constellation(M):
        """Generate M-QAM constellation points."""
        if M == 2:  # BPSK
            return np.array([-1, 1]) + 0j
        elif M == 4:  # QPSK
            return np.array([1+1j, -1+1j, -1-1j, 1-1j]) / np.sqrt(2)
        else:  # Square QAM
            k = int(np.sqrt(M))
            levels = np.arange(-(k-1), k, 2)
            I_q, Q_q = np.meshgrid(levels, levels)
            constellation_q = (I_q.flatten() + 1j * Q_q.flatten())
            # Normalize to unit average power
            constellation_q = constellation_q / np.sqrt(np.mean(np.abs(constellation_q)**2))
            return constellation_q

    # Get values
    qam_order_val = qam_order.value
    qam_M_map = {
        "BPSK (2)": 2,
        "QPSK (4)": 4,
        "16-QAM": 16,
        "64-QAM": 64,
        "256-QAM": 256,
        "1024-QAM": 1024
    }
    M_qam = qam_M_map[qam_order_val]
    snr_db_qam = qam_snr.value
    num_syms = qam_num_symbols.value

    # Generate constellation
    constellation_qam = generate_qam_constellation(M_qam)

    # Generate random transmitted symbols
    tx_indices = np.random.randint(0, M_qam, num_syms)
    tx_symbols = constellation_qam[tx_indices]

    # Add noise
    snr_linear_qam = 10**(snr_db_qam / 10)
    signal_power_qam = np.mean(np.abs(constellation_qam)**2)
    noise_power_qam = signal_power_qam / snr_linear_qam
    noise_std_qam = np.sqrt(noise_power_qam / 2)  # Per dimension

    noise_qam = noise_std_qam * (np.random.randn(num_syms) + 1j * np.random.randn(num_syms))
    rx_symbols = tx_symbols + noise_qam

    # Calculate theoretical SER
    if M_qam > 2:
        Q_func_qam = lambda x: 0.5 * special.erfc(x / np.sqrt(2))
        EsN0_linear = snr_linear_qam * signal_power_qam
        ser_theory = 4 * (1 - 1/np.sqrt(M_qam)) * Q_func_qam(np.sqrt(3 / (M_qam - 1) * EsN0_linear))
    else:
        # BPSK
        Q_func_qam = lambda x: 0.5 * special.erfc(x / np.sqrt(2))
        ser_theory = Q_func_qam(np.sqrt(2 * snr_linear_qam))

    ber_theory = ser_theory / np.log2(M_qam)

    # Create visualization
    fig_qam, (ax_qam1, ax_qam2) = plt.subplots(1, 2, figsize=(14, 6))

    # Plot 1: Constellation with ideal and received points
    ax_qam1.scatter(constellation_qam.real, constellation_qam.imag,
                   s=200, c='blue', marker='o', edgecolors='black',
                   linewidths=2, label='Ideal symbols', zorder=3)

    # Sample of received symbols
    sample_size = min(500, num_syms)
    ax_qam1.scatter(rx_symbols[:sample_size].real, rx_symbols[:sample_size].imag,
                   s=10, c='red', alpha=0.3, label='Received symbols')

    # Add grid lines and axes
    ax_qam1.axhline(y=0, color='k', linestyle='-', linewidth=0.5)
    ax_qam1.axvline(x=0, color='k', linestyle='-', linewidth=0.5)
    ax_qam1.grid(True, alpha=0.3)
    ax_qam1.set_xlabel('In-phase (I)', fontsize=11)
    ax_qam1.set_ylabel('Quadrature (Q)', fontsize=11)
    ax_qam1.set_title(f'{qam_order_val} Constellation (SNR = {snr_db_qam} dB)', fontsize=12)
    ax_qam1.legend(loc='upper right')
    ax_qam1.set_aspect('equal')

    # Plot 2: Required SNR vs. Modulation Order
    M_range = [2, 4, 16, 64, 256, 1024]
    M_labels = ['BPSK', 'QPSK', '16-QAM', '64-QAM', '256-QAM', '1024-QAM']

    # Required SNR for BER = 10^-6
    target_ber = 1e-6
    required_snr = []

    for M_val in M_range:
        # Search for required SNR
        snr_search = np.logspace(-1, 2, 1000)
        bers = []
        for snr_val in snr_search:
            if M_val > 2:
                ser_val = 4 * (1 - 1/np.sqrt(M_val)) * Q_func_qam(np.sqrt(3 / (M_val - 1) * snr_val))
            else:
                ser_val = Q_func_qam(np.sqrt(2 * snr_val))
            ber_val = ser_val / np.log2(M_val)
            bers.append(ber_val)

        bers_arr = np.array(bers)
        idx_qam = np.argmin(np.abs(bers_arr - target_ber))
        required_snr.append(10 * np.log10(snr_search[idx_qam]))

    bits_per_symbol = [np.log2(M_val) for M_val in M_range]

    ax_qam2.plot(bits_per_symbol, required_snr, 'bo-', linewidth=2, markersize=8)

    # Mark current modulation
    current_bits = np.log2(M_qam)
    current_idx = M_range.index(M_qam)
    ax_qam2.plot(current_bits, required_snr[current_idx], 'ro', markersize=12,
                label=f'{qam_order_val}: {required_snr[current_idx]:.1f} dB')

    ax_qam2.grid(True, alpha=0.3)
    ax_qam2.set_xlabel('Bits per Symbol', fontsize=11)
    ax_qam2.set_ylabel('Required SNR (dB) for BER = 10⁻⁶', fontsize=11)
    ax_qam2.set_title('SNR Requirement vs. Modulation Order', fontsize=12)
    ax_qam2.set_xticks(bits_per_symbol)
    ax_qam2.set_xticklabels(M_labels, rotation=15)
    ax_qam2.legend()

    plt.tight_layout()

    fig_qam
    return M_qam, ber_theory, ser_theory, snr_db_qam


@app.cell
def _(M_qam, ber_theory, mo, np, ser_theory, snr_db_qam):
    mo.md(f"""
    ### QAM Constellation Results

    **Configuration:**
    - Modulation: {int(np.log2(M_qam))} bits/symbol ({M_qam}-QAM)
    - SNR: {snr_db_qam} dB

    **Performance:**
    - Symbol Error Rate (SER): **{ser_theory:.4e}**
    - Bit Error Rate (BER): **{ber_theory:.4e}**

    **Tradeoffs:**
    - Higher M → more bits/symbol (higher spectral efficiency)
    - Higher M → smaller distance between symbols → higher SNR required
    - Each doubling of M requires ~3-4 dB more SNR for same BER

    **Practical systems:**
    - WiFi 6: BPSK to 1024-QAM (adaptive)
    - 5G: BPSK to 256-QAM
    - Selection based on channel quality (SNR)
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ---

    ## Adaptive Modulation Analyzer

    Modern wireless systems adapt modulation based on channel quality.

    **WiFi MCS (Modulation and Coding Scheme):**
    - Low SNR → Low MCS (BPSK, QPSK) → Robust, slow
    - High SNR → High MCS (256-QAM, 1024-QAM) → Fragile, fast

    **Data rate:**

    $$R = \frac{N_{\text{subcarriers}} \times N_{\text{streams}} \times \log_2(M) \times r_{\text{code}}}{T_{\text{symbol}}}$$

    where $r_{\text{code}}$ is the code rate (e.g., 1/2, 3/4, 5/6).
    """)
    return


@app.cell
def _(mo):
    # Adaptive modulation controls
    am_bandwidth = mo.ui.slider(
        start=20,
        stop=160,
        step=20,
        value=80,
        label="Channel bandwidth (MHz):",
        show_value=True
    )

    am_num_streams = mo.ui.slider(
        start=1,
        stop=4,
        step=1,
        value=1,
        label="Spatial streams:",
        show_value=True
    )

    am_target_ber = mo.ui.dropdown(
        ["1e-3", "1e-6", "1e-9"],
        value="1e-6",
        label="Target BER:"
    )

    mo.vstack([
        am_bandwidth,
        am_num_streams,
        am_target_ber
    ])
    return am_bandwidth, am_num_streams, am_target_ber


@app.cell
def _(am_bandwidth, am_num_streams, am_target_ber, np, plt):
    # WiFi 802.11ax MCS table (simplified)
    mcs_table = {
        0: {'mod': 'BPSK', 'M': 2, 'code_rate': 0.5, 'min_snr': 3},
        1: {'mod': 'QPSK', 'M': 4, 'code_rate': 0.5, 'min_snr': 6},
        2: {'mod': 'QPSK', 'M': 4, 'code_rate': 0.75, 'min_snr': 9},
        3: {'mod': '16-QAM', 'M': 16, 'code_rate': 0.5, 'min_snr': 12},
        4: {'mod': '16-QAM', 'M': 16, 'code_rate': 0.75, 'min_snr': 15},
        5: {'mod': '64-QAM', 'M': 64, 'code_rate': 0.667, 'min_snr': 18},
        6: {'mod': '64-QAM', 'M': 64, 'code_rate': 0.75, 'min_snr': 21},
        7: {'mod': '64-QAM', 'M': 64, 'code_rate': 0.833, 'min_snr': 24},
        8: {'mod': '256-QAM', 'M': 256, 'code_rate': 0.75, 'min_snr': 27},
        9: {'mod': '256-QAM', 'M': 256, 'code_rate': 0.833, 'min_snr': 30},
        10: {'mod': '1024-QAM', 'M': 1024, 'code_rate': 0.75, 'min_snr': 33},
        11: {'mod': '1024-QAM', 'M': 1024, 'code_rate': 0.833, 'min_snr': 36}
    }

    # Get values
    bw_am = am_bandwidth.value
    streams_am = am_num_streams.value
    target_ber_am = float(am_target_ber.value)

    # WiFi OFDM parameters
    if bw_am == 20:
        N_subcarriers = 234
        T_symbol = 13.6e-6
    elif bw_am == 40:
        N_subcarriers = 468
        T_symbol = 13.6e-6
    elif bw_am == 80:
        N_subcarriers = 980
        T_symbol = 13.6e-6
    elif bw_am == 160:
        N_subcarriers = 1960
        T_symbol = 13.6e-6
    else:
        N_subcarriers = 234
        T_symbol = 13.6e-6

    # Calculate data rates for each MCS
    snr_range_am = np.linspace(0, 40, 100)
    data_rates_vs_snr = []

    for snr_am in snr_range_am:
        # Select highest MCS supported at this SNR
        selected_mcs = 0
        for mcs_idx in range(12):
            if snr_am >= mcs_table[mcs_idx]['min_snr']:
                selected_mcs = mcs_idx

        # Calculate data rate
        M_am = mcs_table[selected_mcs]['M']
        code_rate_am = mcs_table[selected_mcs]['code_rate']
        bits_per_symbol_am = np.log2(M_am)

        # Data rate in Mb/s
        rate_mbps = (N_subcarriers * streams_am * bits_per_symbol_am * code_rate_am) / (T_symbol * 1e6)
        data_rates_vs_snr.append(rate_mbps)

    # Create visualizations
    fig_am, (ax_am1, ax_am2) = plt.subplots(1, 2, figsize=(14, 6))

    # Plot 1: Data rate vs. SNR
    ax_am1.plot(snr_range_am, data_rates_vs_snr, 'b-', linewidth=2.5)

    # Mark MCS transitions
    for mcs_idx in range(12):
        snr_threshold = mcs_table[mcs_idx]['min_snr']
        if snr_threshold <= 40:
            ax_am1.axvline(x=snr_threshold, color='gray', linestyle='--',
                          alpha=0.4, linewidth=1)
            # Calculate rate at this MCS
            M_mcs = mcs_table[mcs_idx]['M']
            code_rate_mcs = mcs_table[mcs_idx]['code_rate']
            rate_mcs = (N_subcarriers * streams_am * np.log2(M_mcs) * code_rate_mcs) / (T_symbol * 1e6)

            if mcs_idx % 2 == 0:  # Label every other MCS to avoid clutter
                ax_am1.text(snr_threshold + 0.5, rate_mcs, f'MCS {mcs_idx}',
                          fontsize=8, rotation=90, va='bottom')

    ax_am1.grid(True, alpha=0.3)
    ax_am1.set_xlabel('SNR (dB)', fontsize=11)
    ax_am1.set_ylabel('Data Rate (Mb/s)', fontsize=11)
    ax_am1.set_title(f'WiFi Data Rate vs. SNR ({bw_am} MHz, {streams_am} stream(s))', fontsize=12)

    # Plot 2: Spectral efficiency vs. SNR
    spectral_eff_am = [rate / bw_am for rate in data_rates_vs_snr]

    ax_am2.plot(snr_range_am, spectral_eff_am, 'g-', linewidth=2.5)

    # Shannon capacity for reference
    shannon_cap_am = [bw_am * np.log2(1 + 10**(snr/10)) for snr in snr_range_am]
    shannon_eff_am = [cap / bw_am for cap in shannon_cap_am]
    ax_am2.plot(snr_range_am, shannon_eff_am, 'r--', linewidth=2,
               label='Shannon Capacity', alpha=0.7)

    ax_am2.grid(True, alpha=0.3)
    ax_am2.set_xlabel('SNR (dB)', fontsize=11)
    ax_am2.set_ylabel('Spectral Efficiency (bits/s/Hz)', fontsize=11)
    ax_am2.set_title('Spectral Efficiency vs. SNR', fontsize=12)
    ax_am2.legend()

    plt.tight_layout()

    fig_am
    return bw_am, data_rates_vs_snr, mcs_table, streams_am


@app.cell
def _(bw_am, data_rates_vs_snr, mo, streams_am):
    max_rate_am = max(data_rates_vs_snr)

    mo.md(
        f"""
        ### Adaptive Modulation Results

        **Configuration:**
        - Bandwidth: {bw_am} MHz
        - Spatial streams: {streams_am}

        **Performance:**
        - Maximum data rate: **{max_rate_am:.1f} Mb/s** (at high SNR)
        - MCS adapts from 0 (BPSK 1/2) to 11 (1024-QAM 5/6)

        **Key insights:**
        - Data rate steps up as SNR improves
        - Low SNR: use robust modulation (BPSK, QPSK)
        - High SNR: use high-order modulation (256-QAM, 1024-QAM)
        - Real systems: measure channel quality, select best MCS
        - Practical WiFi: 50-90% of Shannon capacity

        **Why adaptive modulation?**
        - Maximize throughput while maintaining reliability
        - Channel quality varies with distance, obstacles, interference
        - Fixed modulation would be suboptimal
        """
    )
    return


@app.cell
def _(mo):
    mo.md(r"""
    ---

    ##  WiFi Rate Calculator

    Calculate WiFi data rates based on standard, bandwidth, streams, and MCS.

    **802.11 standards:**
    - 802.11n (WiFi 4): up to 600 Mb/s
    - 802.11ac (WiFi 5): up to 6.9 Gb/s
    - 802.11ax (WiFi 6): up to 9.6 Gb/s
    - 802.11be (WiFi 7): up to 46 Gb/s
    """)
    return


@app.cell
def _(mo):
    # WiFi rate calculator controls
    wifi_standard = mo.ui.dropdown(
        ["802.11n (WiFi 4)", "802.11ac (WiFi 5)", "802.11ax (WiFi 6)"],
        value="802.11ax (WiFi 6)",
        label="WiFi standard:"
    )

    wifi_channel_width = mo.ui.dropdown(
        ["20 MHz", "40 MHz", "80 MHz", "160 MHz"],
        value="80 MHz",
        label="Channel width:"
    )

    wifi_streams = mo.ui.slider(
        start=1,
        stop=8,
        step=1,
        value=2,
        label="Spatial streams:",
        show_value=True
    )

    wifi_mcs = mo.ui.slider(
        start=0,
        stop=11,
        step=1,
        value=9,
        label="MCS index:",
        show_value=True
    )

    mo.vstack([
        wifi_standard,
        wifi_channel_width,
        wifi_streams,
        wifi_mcs
    ])
    return wifi_channel_width, wifi_mcs, wifi_standard, wifi_streams


@app.cell
def _(
    mcs_table,
    np,
    plt,
    wifi_channel_width,
    wifi_mcs,
    wifi_standard,
    wifi_streams,
):
    # Get values
    standard_wifi = wifi_standard.value
    bw_wifi_str = wifi_channel_width.value
    streams_wifi = wifi_streams.value
    mcs_wifi = wifi_mcs.value

    # Extract bandwidth
    bw_wifi = int(bw_wifi_str.split()[0])

    # OFDM parameters based on bandwidth
    if bw_wifi == 20:
        N_sc_wifi = 234 if '11ax' in standard_wifi else 52
        T_sym_wifi = 13.6e-6 if '11ax' in standard_wifi else 4.0e-6
    elif bw_wifi == 40:
        N_sc_wifi = 468 if '11ax' in standard_wifi else 108
        T_sym_wifi = 13.6e-6 if '11ax' in standard_wifi else 4.0e-6
    elif bw_wifi == 80:
        N_sc_wifi = 980 if '11ax' in standard_wifi else 234
        T_sym_wifi = 13.6e-6 if '11ax' in standard_wifi else 4.0e-6
    elif bw_wifi == 160:
        N_sc_wifi = 1960 if '11ax' in standard_wifi else 468
        T_sym_wifi = 13.6e-6 if '11ax' in standard_wifi else 4.0e-6
    else:
        N_sc_wifi = 234
        T_sym_wifi = 13.6e-6

    # Get MCS parameters
    mcs_params = mcs_table[mcs_wifi]
    M_wifi = mcs_params['M']
    code_rate_wifi = mcs_params['code_rate']
    min_snr_wifi = mcs_params['min_snr']
    mod_wifi = mcs_params['mod']

    # Calculate data rate
    bits_per_sym_wifi = np.log2(M_wifi)
    rate_wifi = (N_sc_wifi * streams_wifi * bits_per_sym_wifi * code_rate_wifi) / (T_sym_wifi * 1e6)

    # Create visualization: rate vs. MCS for different channel widths
    fig_wifi, ax_wifi = plt.subplots(figsize=(12, 6))

    channel_widths = [20, 40, 80, 160]
    colors_wifi = ['blue', 'green', 'orange', 'red']

    for bw_w, color_w in zip(channel_widths, colors_wifi):
        rates_w = []

        # Parameters for this bandwidth
        if bw_w == 20:
            N_sc_w = 234 if '11ax' in standard_wifi else 52
            T_sym_w = 13.6e-6 if '11ax' in standard_wifi else 4.0e-6
        elif bw_w == 40:
            N_sc_w = 468 if '11ax' in standard_wifi else 108
            T_sym_w = 13.6e-6 if '11ax' in standard_wifi else 4.0e-6
        elif bw_w == 80:
            N_sc_w = 980 if '11ax' in standard_wifi else 234
            T_sym_w = 13.6e-6 if '11ax' in standard_wifi else 4.0e-6
        elif bw_w == 160:
            N_sc_w = 1960 if '11ax' in standard_wifi else 468
            T_sym_w = 13.6e-6 if '11ax' in standard_wifi else 4.0e-6

        for mcs_w in range(12):
            params_w = mcs_table[mcs_w]
            bits_w = np.log2(params_w['M'])
            rate_w = (N_sc_w * streams_wifi * bits_w * params_w['code_rate']) / (T_sym_w * 1e6)
            rates_w.append(rate_w)

        ax_wifi.plot(range(12), rates_w, 'o-', linewidth=2, color=color_w,
                    label=f'{bw_w} MHz', markersize=6)

    # Mark current configuration
    ax_wifi.plot(mcs_wifi, rate_wifi, 'r*', markersize=20,
                label=f'Current: {rate_wifi:.1f} Mb/s')

    ax_wifi.grid(True, alpha=0.3)
    ax_wifi.set_xlabel('MCS Index', fontsize=11)
    ax_wifi.set_ylabel('Data Rate (Mb/s)', fontsize=11)
    ax_wifi.set_title(f'{standard_wifi} Data Rate vs. MCS ({streams_wifi} stream(s))', fontsize=12)
    ax_wifi.set_xticks(range(12))
    ax_wifi.legend(loc='upper left')

    plt.tight_layout()

    fig_wifi
    return (
        bw_wifi,
        code_rate_wifi,
        mcs_wifi,
        min_snr_wifi,
        mod_wifi,
        rate_wifi,
        standard_wifi,
        streams_wifi,
    )


@app.cell
def _(
    bw_wifi,
    code_rate_wifi,
    mcs_wifi,
    min_snr_wifi,
    mo,
    mod_wifi,
    rate_wifi,
    standard_wifi,
    streams_wifi,
):
    mo.md(f"""
    ### WiFi Rate Calculator Results

    **Configuration:**
    - Standard: {standard_wifi}
    - Channel width: {bw_wifi} MHz
    - Spatial streams: {streams_wifi}
    - MCS index: {mcs_wifi}

    **MCS {mcs_wifi} details:**
    - Modulation: {mod_wifi}
    - Code rate: {code_rate_wifi}
    - Minimum SNR: ~{min_snr_wifi} dB

    **Data rate:** **{rate_wifi:.1f} Mb/s**

    **Key factors affecting rate:**
    - **Bandwidth:** Wider channels → higher rates
    - **Streams:** More spatial streams (MIMO) → higher rates
    - **MCS:** Higher MCS → higher rates (needs better SNR)
    - **Standard:** Newer standards (WiFi 6) more efficient

    **Practical note:** Actual throughput ≈ 50-70% of PHY rate (MAC overhead)
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ---

    ## Spectrum Allocation Viewer

    Radio spectrum is divided into licensed and unlicensed bands.

    **Licensed bands:**
    - Cellular (exclusive use, auctioned)
    - TV broadcast
    - Satellite

    **Unlicensed bands (ISM):**
    - 2.4 GHz: WiFi, Bluetooth, Zigbee
    - 5 GHz: WiFi
    - 6 GHz: WiFi 6E
    """)
    return


@app.cell
def _(mo):
    # Spectrum allocation controls
    spec_freq_min = mo.ui.slider(
        start=0,
        stop=40,
        step=1,
        value=0,
        label="Min frequency (GHz):",
        show_value=True
    )

    spec_freq_max = mo.ui.slider(
        start=1,
        stop=50,
        step=1,
        value=10,
        label="Max frequency (GHz):",
        show_value=True
    )

    show_cellular = mo.ui.checkbox(value=True, label="Cellular")
    show_wifi = mo.ui.checkbox(value=True, label="WiFi")
    show_bluetooth = mo.ui.checkbox(value=True, label="Bluetooth")
    show_gps = mo.ui.checkbox(value=True, label="GPS")
    show_satellite = mo.ui.checkbox(value=True, label="Satellite")

    mo.vstack([
        mo.md("**Frequency range:**"),
        spec_freq_min,
        spec_freq_max,
        mo.md("**Show services:**"),
        show_cellular,
        show_wifi,
        show_bluetooth,
        show_gps,
        show_satellite
    ])
    return (
        show_bluetooth,
        show_cellular,
        show_gps,
        show_satellite,
        show_wifi,
        spec_freq_max,
        spec_freq_min,
    )


@app.cell
def _(
    Rectangle,
    mo,
    plt,
    show_bluetooth,
    show_cellular,
    show_gps,
    show_satellite,
    show_wifi,
    spec_freq_max,
    spec_freq_min,
):
    # Define spectrum allocations
    spectrum_bands = []

    # Cellular bands
    if show_cellular.value:
        spectrum_bands.extend([
            {'name': '700 MHz LTE', 'start': 0.699, 'end': 0.746, 'service': 'Cellular', 'licensed': True},
            {'name': 'Band 2 (PCS)', 'start': 1.850, 'end': 1.990, 'service': 'Cellular', 'licensed': True},
            {'name': 'Band 4 (AWS)', 'start': 1.710, 'end': 1.755, 'service': 'Cellular', 'licensed': True},
            {'name': 'Band 4 (AWS) DL', 'start': 2.110, 'end': 2.155, 'service': 'Cellular', 'licensed': True},
            {'name': '5G C-band', 'start': 3.7, 'end': 3.98, 'service': 'Cellular', 'licensed': True},
            {'name': '5G mmWave', 'start': 24.25, 'end': 24.45, 'service': 'Cellular', 'licensed': True},
            {'name': '5G mmWave', 'start': 28.0, 'end': 28.35, 'service': 'Cellular', 'licensed': True},
        ])

    # WiFi bands
    if show_wifi.value:
        spectrum_bands.extend([
            {'name': 'WiFi 2.4 GHz', 'start': 2.400, 'end': 2.483, 'service': 'WiFi', 'licensed': False},
            {'name': 'WiFi 5 GHz', 'start': 5.150, 'end': 5.825, 'service': 'WiFi', 'licensed': False},
            {'name': 'WiFi 6E', 'start': 5.925, 'end': 7.125, 'service': 'WiFi', 'licensed': False},
        ])

    # Bluetooth
    if show_bluetooth.value:
        spectrum_bands.append(
            {'name': 'Bluetooth', 'start': 2.400, 'end': 2.483, 'service': 'Bluetooth', 'licensed': False}
        )

    # GPS
    if show_gps.value:
        spectrum_bands.extend([
            {'name': 'GPS L1', 'start': 1.5754, 'end': 1.5754, 'service': 'GPS', 'licensed': True},
            {'name': 'GPS L2', 'start': 1.2276, 'end': 1.2276, 'service': 'GPS', 'licensed': True},
        ])

    # Satellite
    if show_satellite.value:
        spectrum_bands.extend([
            {'name': 'Satellite C-band', 'start': 3.7, 'end': 4.2, 'service': 'Satellite', 'licensed': True},
            {'name': 'Satellite Ku-band', 'start': 12.0, 'end': 18.0, 'service': 'Satellite', 'licensed': True},
        ])

    # Filter by frequency range
    freq_min_spec = spec_freq_min.value
    freq_max_spec = spec_freq_max.value

    filtered_bands = [b for b in spectrum_bands
                     if b['start'] <= freq_max_spec and b['end'] >= freq_min_spec]

    # Create visualization
    fig_spec, ax_spec = plt.subplots(figsize=(14, 8))

    # Color mapping
    service_colors = {
        'Cellular': 'blue',
        'WiFi': 'green',
        'Bluetooth': 'purple',
        'GPS': 'orange',
        'Satellite': 'red'
    }

    # Plot bands
    y_pos_spec = 0
    service_positions = {}

    for band in filtered_bands:
        service = band['service']

        if service not in service_positions:
            service_positions[service] = y_pos_spec
            y_pos_spec += 1

        y = service_positions[service]
        color_spec = service_colors.get(service, 'gray')
        alpha_spec = 0.7 if band['licensed'] else 0.4

        # Draw rectangle
        width = band['end'] - band['start']
        if width > 0.001:  # Regular band
            rect = Rectangle((band['start'], y - 0.4), width, 0.8,
                           facecolor=color_spec, alpha=alpha_spec,
                           edgecolor='black', linewidth=1.5)
            ax_spec.add_patch(rect)

            # Add label
            label_pos = band['start'] + width / 2
            ax_spec.text(label_pos, y, band['name'],
                       ha='center', va='center', fontsize=8, fontweight='bold')
        else:  # Point frequency (like GPS)
            ax_spec.plot(band['start'], y, 'o', color=color_spec, markersize=10)
            ax_spec.text(band['start'], y + 0.2, band['name'],
                       ha='center', va='bottom', fontsize=8, fontweight='bold')

    # Set axes
    ax_spec.set_xlim([freq_min_spec, freq_max_spec])
    ax_spec.set_ylim([-0.5, y_pos_spec - 0.5])
    ax_spec.set_xlabel('Frequency (GHz)', fontsize=12)
    ax_spec.set_yticks(range(len(service_positions)))
    ax_spec.set_yticklabels(list(service_positions.keys()))
    ax_spec.set_title('Radio Frequency Spectrum Allocation', fontsize=13)
    ax_spec.grid(True, alpha=0.3, axis='x')

    # Add legend
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor='gray', alpha=0.7, edgecolor='black', label='Licensed'),
        Patch(facecolor='gray', alpha=0.4, edgecolor='black', label='Unlicensed (ISM)')
    ]
    ax_spec.legend(handles=legend_elements, loc='upper right')

    plt.tight_layout()

    if len(filtered_bands) > 0:
        result_spec = fig_spec
    else:
        result_spec = mo.md("**No spectrum allocations in selected range. Adjust frequency range or enable services.**")

    result_spec
    return


@app.cell
def _(mo):
    mo.md(r"""
    ---

    ## Cellular Frequency Reuse Analyzer

    Cellular networks divide coverage area into cells and reuse frequencies.

    **Cluster size $N$:** Number of cells before frequency reuse

    **Reuse distance:**

    $$D = R\sqrt{3N}$$

    **Carrier-to-Interference ratio (C/I):**

    $$\frac{C}{I} = \frac{(3N)^{n/2}}{6}$$

    where $n$ is the path loss exponent.
    """)
    return


@app.cell
def _(mo):
    # Cellular reuse controls
    cluster_size = mo.ui.dropdown(
        ["1", "3", "4", "7"],
        value="3",
        label="Cluster size N:"
    )

    cell_radius = mo.ui.slider(
        start=100,
        stop=5000,
        step=100,
        value=1000,
        label="Cell radius R (m):",
        show_value=True
    )

    reuse_path_loss = mo.ui.slider(
        start=2.0,
        stop=5.0,
        step=0.5,
        value=4.0,
        label="Path loss exponent n:",
        show_value=True
    )

    mo.vstack([
        cluster_size,
        cell_radius,
        reuse_path_loss
    ])
    return cell_radius, cluster_size, reuse_path_loss


@app.cell
def _(cell_radius, cluster_size, np, plt, reuse_path_loss):
    # Get values
    N_cluster = int(cluster_size.value)
    R_cell = cell_radius.value
    n_reuse = reuse_path_loss.value

    # Calculate reuse distance
    D_reuse = R_cell * np.sqrt(3 * N_cluster)

    # Calculate C/I ratio
    CI_ratio_linear = (3 * N_cluster)**(n_reuse / 2) / 6
    CI_ratio_db = 10 * np.log10(CI_ratio_linear)

    # Generate hexagonal cell pattern
    def generate_hex_centers(n_tiers, spacing):
        """Generate hexagonal cell center coordinates."""
        centers = [(0, 0)]

        for tier in range(1, n_tiers + 1):
            # Start at (tier * spacing, 0) and go around
            for i_hex in range(6):
                angle = i_hex * np.pi / 3
                for j_hex in range(tier):
                    x_hex = spacing * (tier - j_hex) * np.cos(angle) + spacing * j_hex * np.cos(angle + np.pi/3)
                    y_hex = spacing * (tier - j_hex) * np.sin(angle) + spacing * j_hex * np.sin(angle + np.pi/3)
                    centers.append((x_hex, y_hex))

        return centers

    # Create visualization
    fig_reuse, (ax_reuse1, ax_reuse2) = plt.subplots(1, 2, figsize=(14, 6))

    # Plot 1: Hexagonal pattern with frequency assignment
    spacing_hex = 2 * R_cell
    centers_hex = generate_hex_centers(2, spacing_hex)

    # Frequency assignment based on cluster size
    freq_colors = ['red', 'blue', 'green', 'yellow', 'orange', 'purple', 'cyan']

    for idx_cell, (x_c, y_c) in enumerate(centers_hex):
        freq_idx = idx_cell % N_cluster
        color_hex = freq_colors[freq_idx % len(freq_colors)]

        # Draw hexagon
        angles = np.linspace(0, 2*np.pi, 7)
        x_hex_pts = x_c + R_cell * np.cos(angles)
        y_hex_pts = y_c + R_cell * np.sin(angles)
        ax_reuse1.fill(x_hex_pts, y_hex_pts, color=color_hex, alpha=0.5, edgecolor='black', linewidth=1.5)

        # Label
        ax_reuse1.text(x_c, y_c, f'F{freq_idx}', ha='center', va='center',
                      fontsize=10, fontweight='bold')

    # Mark reuse distance
    if N_cluster > 1 and len(centers_hex) > N_cluster:
        ax_reuse1.plot([0, centers_hex[N_cluster][0]], [0, centers_hex[N_cluster][1]],
                      'r-', linewidth=3, label=f'D = {D_reuse:.0f} m')
        ax_reuse1.plot(0, 0, 'ko', markersize=10)
        ax_reuse1.plot(centers_hex[N_cluster][0], centers_hex[N_cluster][1], 'ko', markersize=10)

    ax_reuse1.set_aspect('equal')
    ax_reuse1.set_xlabel('Distance (m)', fontsize=11)
    ax_reuse1.set_ylabel('Distance (m)', fontsize=11)
    ax_reuse1.set_title(f'Cellular Frequency Reuse Pattern (N = {N_cluster})', fontsize=12)
    ax_reuse1.legend()
    ax_reuse1.grid(True, alpha=0.3)

    # Plot 2: C/I vs. Cluster Size for different path loss exponents
    N_range = [1, 3, 4, 7, 12]
    n_values = [3.0, 4.0, 5.0]
    n_labels = ['n=3 (urban)', 'n=4 (typical)', 'n=5 (obstructed)']

    for n_pl, n_label in zip(n_values, n_labels):
        CI_vals = [10 * np.log10((3 * N_val)**(n_pl / 2) / 6) for N_val in N_range]
        ax_reuse2.plot(N_range, CI_vals, 'o-', linewidth=2, markersize=8, label=n_label)

    # Mark current configuration
    ax_reuse2.plot(N_cluster, CI_ratio_db, 'r*', markersize=20,
                  label=f'Current: {CI_ratio_db:.1f} dB')

    # Reference lines
    ax_reuse2.axhline(y=18, color='orange', linestyle='--', alpha=0.5, label='18 dB (acceptable)')
    ax_reuse2.axhline(y=30, color='green', linestyle='--', alpha=0.5, label='30 dB (good)')

    ax_reuse2.grid(True, alpha=0.3)
    ax_reuse2.set_xlabel('Cluster Size N', fontsize=11)
    ax_reuse2.set_ylabel('C/I Ratio (dB)', fontsize=11)
    ax_reuse2.set_title('Carrier-to-Interference Ratio vs. Cluster Size', fontsize=12)
    ax_reuse2.set_xticks(N_range)
    ax_reuse2.legend()

    plt.tight_layout()

    fig_reuse
    return CI_ratio_db, D_reuse, N_cluster, R_cell, n_reuse


@app.cell
def _(CI_ratio_db, D_reuse, N_cluster, R_cell, mo, n_reuse):
    mo.md(f"""
    ### Cellular Frequency Reuse Results

    **Configuration:**
    - Cluster size: N = {N_cluster}
    - Cell radius: R = {R_cell} m
    - Path loss exponent: n = {n_reuse}

    **Results:**
    - Reuse distance: D = **{D_reuse:.0f} m** (= {D_reuse/R_cell:.2f} × R)
    - C/I ratio: **{CI_ratio_db:.1f} dB**
    - Capacity per area: ∝ 1/N

    **Tradeoffs:**
    - **Larger N:** Better C/I, lower interference, but less capacity per area
    - **Smaller N:** More capacity per area, but more interference
    - N=1 (modern systems): All cells use all frequencies with advanced interference management

    **Historical note:**
    - Early cellular (AMPS): N=7 (good C/I, low capacity)
    - Modern 4G/5G: N=1 with OFDMA, interference coordination, beamforming
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ---

    ## Sectoring Benefits Calculator

    Cell sectoring divides omnidirectional cells into directional sectors.

    **Typical configuration:** 3 sectors per cell (120° each)

    **Benefits:**
    - **Capacity:** 3× increase (3 sectors)
    - **Antenna gain:** Directional antennas provide gain
    - **Interference:** Reduced (directional transmission/reception)
    """)
    return


@app.cell
def _(mo):
    # Sectoring controls
    sectors_per_cell = mo.ui.dropdown(
        ["1 (Omni)", "3", "6"],
        value="3",
        label="Sectors per cell:"
    )

    sector_antenna_gain = mo.ui.slider(
        start=0,
        stop=21,
        step=1,
        value=17,
        label="Antenna gain per sector (dBi):",
        show_value=True
    )

    sector_beamwidth = mo.ui.slider(
        start=30,
        stop=360,
        step=10,
        value=120,
        label="Beamwidth (degrees):",
        show_value=True
    )

    mo.vstack([
        sectors_per_cell,
        sector_antenna_gain,
        sector_beamwidth
    ])
    return sector_antenna_gain, sector_beamwidth, sectors_per_cell


@app.cell
def _(np, plt, sector_antenna_gain, sector_beamwidth, sectors_per_cell):
    # Get values
    sectors_val = int(sectors_per_cell.value.split()[0])
    gain_sector = sector_antenna_gain.value
    beamwidth_sector = sector_beamwidth.value

    # Calculate benefits
    capacity_multiplier = sectors_val
    interference_reduction_db = 10 * np.log10(sectors_val) if sectors_val > 1 else 0

    # Create visualization
    fig_sector, (ax_sector1, ax_sector2) = plt.subplots(1, 2, figsize=(14, 6),
                                                         subplot_kw=dict(projection='polar'))

    # Plot 1: Antenna pattern
    theta_sector = np.linspace(0, 2*np.pi, 360)

    if sectors_val == 1:
        # Omnidirectional
        pattern_sector = np.ones_like(theta_sector)
        ax_sector1.plot(theta_sector, pattern_sector, 'b-', linewidth=2)
        ax_sector1.fill(theta_sector, pattern_sector, alpha=0.3, color='blue')
    else:
        # Sectored
        sector_angle = 2 * np.pi / sectors_val
        beamwidth_rad = np.deg2rad(beamwidth_sector)

        for i_sector in range(sectors_val):
            center_angle = i_sector * sector_angle

            # Simplified sector pattern
            pattern_sector_i = np.zeros_like(theta_sector)
            for j_sector, theta_val in enumerate(theta_sector):
                angle_diff = abs(((theta_val - center_angle + np.pi) % (2*np.pi)) - np.pi)
                if angle_diff <= beamwidth_rad / 2:
                    # Cosine rolloff within beamwidth
                    pattern_sector_i[j_sector] = np.cos(angle_diff / (beamwidth_rad/2) * np.pi/2)**2

            ax_sector1.plot(theta_sector, pattern_sector_i, linewidth=2)
            ax_sector1.fill(theta_sector, pattern_sector_i, alpha=0.3)

    ax_sector1.set_ylim([0, 1.2])
    ax_sector1.set_title(f'Antenna Pattern ({sectors_val} sector(s))', fontsize=12, pad=20)
    ax_sector1.grid(True)

    # Plot 2: Coverage and interference comparison
    # Show relative interference based on sectoring
    theta_interf = np.linspace(0, 2*np.pi, 360)

    # Omnidirectional interference (constant)
    interference_omni = np.ones_like(theta_interf)
    ax_sector2.plot(theta_interf, interference_omni, 'r--', linewidth=2,
                   label='Omni (no sectoring)', alpha=0.7)

    # Sectored interference (reduced)
    if sectors_val > 1:
        interference_sectored = interference_omni / sectors_val
        ax_sector2.plot(theta_interf, interference_sectored, 'g-', linewidth=2,
                       label=f'{sectors_val} sectors')
        ax_sector2.fill(theta_interf, interference_sectored, alpha=0.3, color='green')

    ax_sector2.set_ylim([0, 1.5])
    ax_sector2.set_title('Relative Interference Level', fontsize=12, pad=20)
    ax_sector2.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))
    ax_sector2.grid(True)

    plt.tight_layout()

    fig_sector
    return (
        beamwidth_sector,
        capacity_multiplier,
        gain_sector,
        interference_reduction_db,
        sectors_val,
    )


@app.cell
def _(
    beamwidth_sector,
    capacity_multiplier,
    gain_sector,
    interference_reduction_db,
    mo,
    sectors_val,
):
    mo.md(f"""
    ### Sectoring Benefits Results

    **Configuration:**
    - Sectors per cell: {sectors_val}
    - Antenna gain: {gain_sector} dBi
    - Beamwidth: {beamwidth_sector}°

    **Benefits:**
    - **Capacity increase:** {capacity_multiplier}× (each sector serves independent users)
    - **Antenna gain:** {gain_sector} dBi (improves link budget)
    - **Interference reduction:** ~{interference_reduction_db:.1f} dB (directional antennas)

    **Typical deployment:**
    - Most cell towers use 3-sector configuration (120° each)
    - Each sector has independent radios and antennas
    - Antenna gain: 17-21 dBi (directional panel antennas)
    - Multiple bands per sector (e.g., 700 MHz, 1900 MHz, 2.5 GHz, 3.5 GHz)

    **Design tradeoffs:**
    - More sectors → more hardware, more complexity
    - 6 sectors used in very high-capacity urban deployments
    - Beamwidth vs. gain: narrower beam → higher gain → better link budget
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ---

    ## WiFi Channel Allocator

    WiFi uses unlicensed ISM bands with specific channel allocations.

    **2.4 GHz band:**
    - Channels 1-11 (US), 1-13 (EU)
    - 20 MHz channels (overlapping!)
    - Non-overlapping: 1, 6, 11 (US)

    **5 GHz band:**
    - Many non-overlapping channels
    - 20, 40, 80, 160 MHz widths
    - Some channels require DFS (radar avoidance)

    **6 GHz band (WiFi 6E):**
    - 1200 MHz of spectrum!
    - Up to 320 MHz channels
    """)
    return


@app.cell
def _(mo):
    # WiFi channel controls
    wifi_band = mo.ui.dropdown(
        ["2.4 GHz", "5 GHz", "6 GHz"],
        value="5 GHz",
        label="WiFi band:"
    )

    wifi_ch_width = mo.ui.dropdown(
        ["20 MHz", "40 MHz", "80 MHz", "160 MHz"],
        value="80 MHz",
        label="Channel width:"
    )

    wifi_region = mo.ui.dropdown(
        ["US", "EU", "JP"],
        value="US",
        label="Region:"
    )

    mo.vstack([
        wifi_band,
        wifi_ch_width,
        wifi_region
    ])
    return wifi_band, wifi_ch_width, wifi_region


@app.cell
def _(plt, wifi_band, wifi_ch_width, wifi_region):
    # Get values
    band_wifi_ch = wifi_band.value
    ch_width_wifi = int(wifi_ch_width.value.split()[0])
    region_wifi = wifi_region.value

    # Define channels
    if band_wifi_ch == "2.4 GHz":
        # 2.4 GHz channels (US: 1-11, EU: 1-13)
        max_ch = 11 if region_wifi == "US" else 13
        channels_list = []
        for ch in range(1, max_ch + 1):
            center_freq = 2.407 + (ch * 0.005)  # GHz
            channels_list.append({
                'number': ch,
                'center': center_freq,
                'width': 0.020,  # 20 MHz
                'dfs': False
            })

        # Non-overlapping channels
        if region_wifi == "US":
            non_overlap = [1, 6, 11]
        else:
            non_overlap = [1, 6, 11, 14] if max_ch >= 14 else [1, 6, 11]

        band_name = "2.4 GHz (2.400-2.483 GHz)"

    elif band_wifi_ch == "5 GHz":
        # 5 GHz channels (simplified)
        channels_5ghz = [36, 40, 44, 48, 52, 56, 60, 64, 100, 104, 108, 112, 116, 120,
                        124, 128, 132, 136, 140, 144, 149, 153, 157, 161, 165]

        channels_list = []
        for ch in channels_5ghz:
            center_freq = 5.0 + (ch * 0.005)  # GHz
            # DFS channels (weather radar)
            dfs = (52 <= ch <= 144)
            channels_list.append({
                'number': ch,
                'center': center_freq,
                'width': ch_width_wifi / 1000,  # Convert MHz to GHz
                'dfs': dfs
            })

        # Non-overlapping depends on width
        if ch_width_wifi == 20:
            non_overlap = [36, 40, 44, 48, 149, 153, 157, 161, 165]
        elif ch_width_wifi == 40:
            non_overlap = [36, 44, 149, 157]
        elif ch_width_wifi == 80:
            non_overlap = [36, 149]
        else:  # 160 MHz
            non_overlap = [36]

        band_name = "5 GHz (5.150-5.825 GHz)"

    else:  # 6 GHz
        # 6 GHz channels (WiFi 6E)
        # Simplified: show primary channels for different widths
        if ch_width_wifi == 20:
            channels_6ghz = list(range(1, 234, 4))  # Every 4th channel
        elif ch_width_wifi == 40:
            channels_6ghz = list(range(1, 234, 8))
        elif ch_width_wifi == 80:
            channels_6ghz = list(range(1, 234, 16))
        else:  # 160 MHz
            channels_6ghz = list(range(1, 234, 32))

        channels_list = []
        for ch in channels_6ghz[:15]:  # Limit display
            center_freq = 5.955 + (ch * 0.005)  # GHz
            channels_list.append({
                'number': ch,
                'center': center_freq,
                'width': ch_width_wifi / 1000,
                'dfs': False
            })

        non_overlap = [ch['number'] for ch in channels_list]
        band_name = "6 GHz (5.925-7.125 GHz)"

    # Create visualization
    fig_ch, ax_ch = plt.subplots(figsize=(14, 6))

    # Plot channels
    for ch_info in channels_list:
        ch_num = ch_info['number']
        center = ch_info['center']
        width_val = ch_info['width']
        is_dfs = ch_info['dfs']

        # Color code
        if ch_num in non_overlap:
            color_ch = 'green'
            alpha_ch = 0.6
        elif is_dfs:
            color_ch = 'orange'
            alpha_ch = 0.4
        else:
            color_ch = 'blue'
            alpha_ch = 0.4

        # Draw channel
        left = center - width_val / 2
        right = center + width_val / 2
        ax_ch.axvspan(left, right, alpha=alpha_ch, color=color_ch)

        # Label (only for non-overlapping or every few channels)
        if ch_num in non_overlap or len(channels_list) < 20:
            ax_ch.text(center, 0.5, str(ch_num), ha='center', va='center',
                      fontsize=9, fontweight='bold')

    # Add legend
    from matplotlib.patches import Patch as Patch2
    legend_ch = [
        Patch2(facecolor='green', alpha=0.6, label='Non-overlapping'),
    ]
    if any(ch['dfs'] for ch in channels_list):
        legend_ch.append(Patch2(facecolor='orange', alpha=0.4, label='DFS (radar avoidance)'))
    if band_wifi_ch != "6 GHz":
        legend_ch.append(Patch2(facecolor='blue', alpha=0.4, label='Overlapping'))

    ax_ch.legend(handles=legend_ch, loc='upper right')

    ax_ch.set_xlabel('Frequency (GHz)', fontsize=12)
    ax_ch.set_ylabel('', fontsize=12)
    ax_ch.set_title(f'WiFi Channel Allocation - {band_name} ({ch_width_wifi} MHz channels)',
                   fontsize=13)
    ax_ch.set_ylim([0, 1])
    ax_ch.set_yticks([])
    ax_ch.grid(True, alpha=0.3, axis='x')

    plt.tight_layout()

    fig_ch
    return band_wifi_ch, ch_width_wifi, non_overlap, region_wifi


@app.cell
def _(band_wifi_ch, ch_width_wifi, mo, non_overlap, region_wifi):
    mo.md(f"""
    ### WiFi Channel Allocation Results

    **Configuration:**
    - Band: {band_wifi_ch}
    - Channel width: {ch_width_wifi} MHz
    - Region: {region_wifi}

    **Non-overlapping channels:** {', '.join(map(str, non_overlap))}

    **Key points:**

    **2.4 GHz:**
    - Only 3 non-overlapping 20 MHz channels (1, 6, 11 in US)
    - Very crowded (WiFi, Bluetooth, microwaves, etc.)
    - Better range (lower frequency)

    **5 GHz:**
    - Many non-overlapping channels
    - Less crowded, higher capacity
    - Some channels require DFS (Dynamic Frequency Selection) to avoid radar
    - Shorter range (higher frequency)

    **6 GHz (WiFi 6E):**
    - Brand new spectrum (2020)
    - No legacy devices → less interference
    - Up to 7 non-overlapping 160 MHz channels
    - Future: 320 MHz channels (WiFi 7)

    **Best practices:**
    - Use non-overlapping channels to avoid interference
    - 2.4 GHz: stick to channels 1, 6, 11
    - 5 GHz: many options, use channel scanner to find least used
    - Wider channels → higher rates, but fewer non-overlapping options
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ---

    ## Summary

    This notebook explored key wireless communication concepts:

    1. **Free Space Path Loss** - Signal attenuation increases with distance and frequency
    2. **Empirical Path Loss** - Real-world environments have higher loss (n > 2)
    3. **Link Budget** - Accounting for all gains and losses to ensure viable link
    4. **QAM Modulation** - Higher orders → more bits/symbol but require better SNR
    5. **Adaptive Modulation** - Modern systems adjust MCS based on channel quality
    6. **WiFi Rates** - Depend on bandwidth, streams, and MCS
    7. **Spectrum Allocation** - Licensed vs. unlicensed bands for different services
    8. **Cellular Reuse** - Frequency reuse with cluster size N, tradeoff C/I vs. capacity
    9. **Sectoring** - Directional antennas increase capacity and reduce interference
    10. **WiFi Channels** - Non-overlapping channel selection critical for performance

    **Key insights:**
    - Wireless design involves many tradeoffs: power, bandwidth, range, capacity
    - Path loss drives coverage and power requirements
    - Modulation selection balances throughput and reliability
    - Spectrum is a scarce resource requiring careful management
    - Modern systems use adaptive techniques to optimize performance
    """)
    return


if __name__ == "__main__":
    app.run()
