import marimo

__generated_with = "0.10.3"
app = marimo.App(width="medium")


@app.cell
def __():
    import marimo as mo
    import numpy as np
    import matplotlib.pyplot as plt
    from scipy import special
    from scipy.signal import gausspulse
    return mo, np, plt, special, gausspulse


@app.cell
def __(mo):
    mo.md(
        r"""
        # Lecture 3: Physical Layer - Interactive Exploration

        **EC 441 - Introduction to Computer Networking**

        This notebook contains interactive demonstrations and experiments to explore physical layer concepts including attenuation, link budgets, Shannon capacity, noise, pulse shaping, matched filtering, and modulation.
        """
    )
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        ---

        ## Cell 1: Attenuation Calculator

        Attenuation varies by medium type, distance, and frequency. For copper media, higher frequencies experience greater loss.

        **Attenuation models:**
        - **Cat 6 Cable**: ~20 dB/100m at 100 MHz (frequency dependent)
        - **Coax RG-6**: ~3 dB/100m at 100 MHz (frequency dependent)
        - **Fiber SMF 1550nm**: 0.2 dB/km (frequency independent)
        - **Fiber MMF 850nm**: 2.5 dB/km (frequency independent)
        """
    )
    return


@app.cell
def __(mo):
    # Attenuation controls
    medium_type = mo.ui.dropdown(
        ["Cat 6", "Coax RG-6", "Fiber SMF 1550nm", "Fiber MMF 850nm"],
        value="Cat 6",
        label="Medium type:"
    )

    distance_slider = mo.ui.slider(
        start=1,
        stop=10000,
        step=10,
        value=100,
        label="Distance (m):",
        show_value=True
    )

    frequency_slider = mo.ui.slider(
        start=1,
        stop=10000,
        step=10,
        value=100,
        label="Frequency (MHz) - for copper only:",
        show_value=True
    )

    tx_power_slider = mo.ui.slider(
        start=-20,
        stop=30,
        step=1,
        value=0,
        label="Transmit power (dBm):",
        show_value=True
    )

    mo.vstack([
        medium_type,
        distance_slider,
        frequency_slider,
        tx_power_slider
    ])
    return distance_slider, frequency_slider, medium_type, tx_power_slider


@app.cell
def __(distance_slider, frequency_slider, medium_type, mo, np, plt, tx_power_slider):
    def calculate_attenuation(medium, distance_m, freq_mhz):
        """Calculate attenuation in dB for given medium, distance, and frequency."""
        if medium == "Cat 6":
            # Approximate model: attenuation increases with sqrt(f)
            # At 100 MHz: ~20 dB/100m
            atten_per_100m = 20 * np.sqrt(freq_mhz / 100)
            return atten_per_100m * (distance_m / 100)
        elif medium == "Coax RG-6":
            # At 100 MHz: ~3 dB/100m
            atten_per_100m = 3 * np.sqrt(freq_mhz / 100)
            return atten_per_100m * (distance_m / 100)
        elif medium == "Fiber SMF 1550nm":
            # 0.2 dB/km, frequency independent
            return 0.2 * (distance_m / 1000)
        elif medium == "Fiber MMF 850nm":
            # 2.5 dB/km, frequency independent
            return 2.5 * (distance_m / 1000)
        return 0

    medium_val = medium_type.value
    distance_val = distance_slider.value
    freq_val = frequency_slider.value
    tx_power = tx_power_slider.value

    # Calculate attenuation for selected medium
    attenuation_db = calculate_attenuation(medium_val, distance_val, freq_val)
    rx_power_dbm = tx_power - attenuation_db

    # Calculate for all media types at this distance for comparison
    comparison_distance = distance_val
    comparison_freq = 100  # Use 100 MHz for fair comparison

    media_types = ["Cat 6", "Coax RG-6", "Fiber SMF 1550nm", "Fiber MMF 850nm"]
    attenuations = [calculate_attenuation(m, comparison_distance, comparison_freq)
                    for m in media_types]

    # Create bar chart
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

    # Bar chart comparing media types
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']
    bars = ax1.bar(media_types, attenuations, color=colors, alpha=0.7, edgecolor='black')

    # Highlight the selected medium
    selected_idx = media_types.index(medium_val)
    bars[selected_idx].set_alpha(1.0)
    bars[selected_idx].set_linewidth(2)

    ax1.set_ylabel('Attenuation (dB)', fontsize=11)
    ax1.set_title(f'Media Comparison at {comparison_distance} m (100 MHz)', fontsize=12)
    ax1.grid(True, alpha=0.3, axis='y')
    ax1.tick_params(axis='x', rotation=15)

    # Add value labels on bars
    for bar, atten in zip(bars, attenuations):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height,
                f'{atten:.1f} dB',
                ha='center', va='bottom', fontsize=9)

    # Power budget visualization
    stages = ['Tx Power', 'Attenuation', 'Rx Power']
    values = [tx_power, -attenuation_db, rx_power_dbm]
    colors_budget = ['green', 'red', 'blue']

    bars2 = ax2.bar(stages, [abs(v) for v in values], color=colors_budget, alpha=0.7)

    # Add sign indicators
    for _i, (_bar, _val) in enumerate(zip(bars2, values)):
        _height = _bar.get_height()
        sign = '+' if _val >= 0 else '-'
        ax2.text(_bar.get_x() + _bar.get_width()/2., _height,
                f'{sign}{abs(_val):.1f} dBm',
                ha='center', va='bottom', fontsize=10, fontweight='bold')

    ax2.set_ylabel('Power (dBm)', fontsize=11)
    ax2.set_title(f'Power Budget for {medium_val}', fontsize=12)
    ax2.grid(True, alpha=0.3, axis='y')

    plt.tight_layout()

    fig
    return (
        attenuation_db,
        attenuations,
        ax1,
        ax2,
        bars,
        bars2,
        calculate_attenuation,
        colors,
        colors_budget,
        comparison_distance,
        comparison_freq,
        distance_val,
        fig,
        freq_val,
        media_types,
        medium_val,
        rx_power_dbm,
        selected_idx,
        sign,
        stages,
        tx_power,
        values,
    )


@app.cell
def __(attenuation_db, distance_val, freq_val, medium_val, mo, rx_power_dbm, tx_power):
    is_copper = medium_val in ["Cat 6", "Coax RG-6"]
    freq_note = f" at {freq_val} MHz" if is_copper else " (frequency independent)"

    sensitivity_threshold = -90  # Typical receiver sensitivity in dBm
    link_margin = rx_power_dbm - sensitivity_threshold

    mo.md(
        f"""
        ### Attenuation Results

        **Selected medium:** {medium_val}
        **Distance:** {distance_val} m{freq_note}

        **Power budget:**
        - Transmit power: **{tx_power:.1f} dBm**
        - Attenuation: **{attenuation_db:.2f} dB**
        - Received power: **{rx_power_dbm:.2f} dBm**

        **Link margin:** {link_margin:.1f} dB (vs. {sensitivity_threshold} dBm sensitivity)

        {'✓ **Link viable**' if link_margin > 0 else '✗ **Link not viable** - increase power or reduce distance'}
        """
    )
    return freq_note, is_copper, link_margin, sensitivity_threshold


@app.cell
def __(mo):
    mo.md(
        r"""
        ---

        ## Cell 2: Link Budget Calculator

        A complete link budget accounts for transmit power, antenna gains, cable losses, path loss, and receiver sensitivity.

        **Path loss (Friis equation):**
        $$L_{path} = 20\log_{10}(d) + 20\log_{10}(f) + 20\log_{10}\left(\frac{4\pi}{c}\right)$$

        where $d$ is distance in meters, $f$ is frequency in Hz, and $c$ is the speed of light.
        """
    )
    return


@app.cell
def __(mo):
    # Link budget controls
    lb_tx_power = mo.ui.slider(
        start=-20,
        stop=30,
        step=1,
        value=20,
        label="Tx power (dBm):",
        show_value=True
    )

    lb_distance = mo.ui.slider(
        start=1,
        stop=10000,
        step=50,
        value=1000,
        label="Distance (m):",
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

    lb_tx_gain = mo.ui.slider(
        start=0,
        stop=30,
        step=1,
        value=3,
        label="Tx antenna gain (dBi):",
        show_value=True
    )

    lb_rx_gain = mo.ui.slider(
        start=0,
        stop=30,
        step=1,
        value=3,
        label="Rx antenna gain (dBi):",
        show_value=True
    )

    lb_cable_type = mo.ui.dropdown(
        ["Cat 6", "Coax RG-6", "Fiber SMF 1550nm"],
        value="Coax RG-6",
        label="Cable type:"
    )

    lb_cable_length = mo.ui.slider(
        start=0,
        stop=100,
        step=5,
        value=10,
        label="Cable length (m):",
        show_value=True
    )

    mo.vstack([
        lb_tx_power,
        lb_distance,
        lb_frequency,
        lb_tx_gain,
        lb_rx_gain,
        lb_cable_type,
        lb_cable_length
    ])
    return (
        lb_cable_length,
        lb_cable_type,
        lb_distance,
        lb_frequency,
        lb_rx_gain,
        lb_tx_gain,
        lb_tx_power,
    )


@app.cell
def __(
    calculate_attenuation,
    lb_cable_length,
    lb_cable_type,
    lb_distance,
    lb_frequency,
    lb_rx_gain,
    lb_tx_gain,
    lb_tx_power,
    mo,
    np,
    plt,
):
    def calculate_path_loss(distance_m, freq_mhz):
        """Calculate free space path loss using Friis equation."""
        freq_hz = freq_mhz * 1e6
        c = 3e8  # speed of light
        if distance_m <= 0:
            return 0
        path_loss = 20*np.log10(distance_m) + 20*np.log10(freq_hz) + 20*np.log10(4*np.pi/c)
        return path_loss

    # Get values
    tx_pwr = lb_tx_power.value
    dist_m = lb_distance.value
    freq_mhz = lb_frequency.value
    tx_gain = lb_tx_gain.value
    rx_gain = lb_rx_gain.value
    cable_type = lb_cable_type.value
    cable_len = lb_cable_length.value

    # Calculate link budget components
    eirp_dbm = tx_pwr + tx_gain  # Effective Isotropic Radiated Power
    path_loss_db = calculate_path_loss(dist_m, freq_mhz)
    cable_loss_db = calculate_attenuation(cable_type, cable_len, freq_mhz)

    # Received signal strength
    rx_signal_dbm = eirp_dbm - path_loss_db - cable_loss_db + rx_gain

    # Link margin
    rx_sensitivity = -90  # dBm
    margin_db = rx_signal_dbm - rx_sensitivity

    # Create stacked bar chart showing power budget breakdown
    fig_lb, ax_lb = plt.subplots(figsize=(12, 6))

    # Components of the link budget
    components = ['Tx Power', 'Tx Gain', 'Path Loss', 'Cable Loss', 'Rx Gain', 'Rx Power']
    values_lb = [tx_pwr, tx_gain, -path_loss_db, -cable_loss_db, rx_gain, rx_signal_dbm]

    # Cumulative values for waterfall chart
    cumulative = [tx_pwr]
    cumulative.append(cumulative[-1] + tx_gain)
    cumulative.append(cumulative[-1] - path_loss_db)
    cumulative.append(cumulative[-1] - cable_loss_db)
    cumulative.append(cumulative[-1] + rx_gain)

    # Create waterfall chart
    x_pos = np.arange(len(components))
    colors_lb = ['green', 'green', 'red', 'red', 'green', 'blue']

    for _i in range(len(components) - 1):
        _start = cumulative[_i] if _i > 0 else 0
        _height2 = values_lb[_i+1] if _i == 0 else (cumulative[_i] - cumulative[_i-1] if _i > 0 else values_lb[0])

        if _i == 0:
            ax_lb.bar(_i, values_lb[0], color=colors_lb[0], alpha=0.7, edgecolor='black')
        else:
            _bottom = min(cumulative[_i-1], cumulative[_i])
            _height = abs(cumulative[_i] - cumulative[_i-1])
            ax_lb.bar(_i, _height, bottom=_bottom, color=colors_lb[_i], alpha=0.7, edgecolor='black')

    # Final bar for received power
    ax_lb.bar(len(components)-1, rx_signal_dbm, color='blue', alpha=0.7, edgecolor='black', linewidth=2)

    # Add horizontal line for sensitivity
    ax_lb.axhline(y=rx_sensitivity, color='red', linestyle='--', linewidth=2, label=f'Sensitivity ({rx_sensitivity} dBm)')

    # Add value labels
    for _i, (_comp, _val) in enumerate(zip(components[:-1], cumulative)):
        ax_lb.text(_i, _val + 2, f'{_val:.1f} dBm', ha='center', fontsize=9, fontweight='bold')

    ax_lb.text(len(components)-1, rx_signal_dbm + 2, f'{rx_signal_dbm:.1f} dBm',
              ha='center', fontsize=9, fontweight='bold')

    ax_lb.set_xticks(x_pos)
    ax_lb.set_xticklabels(components, rotation=0)
    ax_lb.set_ylabel('Power (dBm)', fontsize=11)
    ax_lb.set_title('Link Budget Waterfall Chart', fontsize=13)
    ax_lb.grid(True, alpha=0.3, axis='y')
    ax_lb.legend()

    plt.tight_layout()

    fig_lb
    return (
        ax_lb,
        cable_len,
        cable_loss_db,
        cable_type,
        calculate_path_loss,
        components,
        cumulative,
        dist_m,
        eirp_dbm,
        fig_lb,
        freq_mhz,
        margin_db,
        path_loss_db,
        rx_gain,
        rx_sensitivity,
        rx_signal_dbm,
        tx_gain,
        tx_pwr,
        values_lb,
        x_pos,
        colors_lb,
    )


@app.cell
def __(
    cable_len,
    cable_loss_db,
    cable_type,
    dist_m,
    eirp_dbm,
    freq_mhz,
    margin_db,
    mo,
    path_loss_db,
    rx_sensitivity,
    rx_signal_dbm,
    tx_pwr,
):
    mo.md(
        f"""
        ### Link Budget Results

        **Configuration:**
        - Distance: {dist_m} m at {freq_mhz} MHz
        - Cable: {cable_type}, {cable_len} m

        **Power budget breakdown:**
        - Tx power: {tx_pwr:.1f} dBm
        - EIRP (with Tx antenna): {eirp_dbm:.1f} dBm
        - Path loss (free space): {path_loss_db:.1f} dB
        - Cable loss: {cable_loss_db:.1f} dB
        - Rx signal: **{rx_signal_dbm:.1f} dBm**

        **Link margin:** {margin_db:.1f} dB (vs. {rx_sensitivity} dBm sensitivity)

        {'✓ **Link viable** with ' + f'{margin_db:.1f} dB margin' if margin_db > 0 else '✗ **Link not viable**'}

        **Note:** Path loss increases with distance (20 dB/decade) and frequency (20 dB/decade).
        """
    )
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        ---

        ## Cell 3: Shannon Capacity Explorer

        Shannon's theorem gives the theoretical maximum channel capacity:

        $$C = B \log_2(1 + \text{SNR})$$

        where $C$ is capacity in bits/s, $B$ is bandwidth in Hz, and SNR is the linear signal-to-noise ratio.

        **Spectral efficiency:** $\eta = C/B$ (bits/s/Hz)
        """
    )
    return


@app.cell
def __(mo):
    # Shannon capacity controls
    sc_bandwidth = mo.ui.slider(
        start=1,
        stop=100,
        step=1,
        value=20,
        label="Bandwidth (MHz):",
        show_value=True
    )

    sc_snr_db = mo.ui.slider(
        start=-10,
        stop=40,
        step=1,
        value=20,
        label="SNR (dB):",
        show_value=True
    )

    mo.vstack([
        sc_bandwidth,
        sc_snr_db
    ])
    return sc_bandwidth, sc_snr_db


@app.cell
def __(mo, np, plt, sc_bandwidth, sc_snr_db):
    # Get values
    bw_mhz = sc_bandwidth.value
    snr_db = sc_snr_db.value

    # Convert to linear
    bw_hz = bw_mhz * 1e6
    snr_linear = 10**(snr_db / 10)

    # Calculate capacity
    capacity_bps = bw_hz * np.log2(1 + snr_linear)
    capacity_mbps = capacity_bps / 1e6
    spectral_efficiency = np.log2(1 + snr_linear)

    # Create 3D surface plot
    fig_shannon = plt.figure(figsize=(14, 10))

    # 3D surface
    ax1_3d = fig_shannon.add_subplot(2, 2, 1, projection='3d')

    bw_range = np.linspace(1, 100, 50)
    snr_range = np.linspace(-10, 40, 50)
    BW, SNR = np.meshgrid(bw_range, snr_range)

    SNR_linear = 10**(SNR / 10)
    CAPACITY = BW * np.log2(1 + SNR_linear)

    surf = ax1_3d.plot_surface(BW, SNR, CAPACITY, cmap='viridis', alpha=0.8, edgecolor='none')
    ax1_3d.scatter([bw_mhz], [snr_db], [capacity_mbps], color='red', s=100, marker='o')

    ax1_3d.set_xlabel('Bandwidth (MHz)', fontsize=10)
    ax1_3d.set_ylabel('SNR (dB)', fontsize=10)
    ax1_3d.set_zlabel('Capacity (Mb/s)', fontsize=10)
    ax1_3d.set_title('Shannon Capacity Surface', fontsize=12)
    fig_shannon.colorbar(surf, ax=ax1_3d, shrink=0.5)

    # 2D cross-section: Capacity vs. Bandwidth (fixed SNR)
    ax2_2d = fig_shannon.add_subplot(2, 2, 2)

    cap_vs_bw = bw_range * np.log2(1 + snr_linear)
    ax2_2d.plot(bw_range, cap_vs_bw, 'b-', linewidth=2)
    ax2_2d.plot(bw_mhz, capacity_mbps, 'ro', markersize=10, label=f'Current: {capacity_mbps:.1f} Mb/s')
    ax2_2d.grid(True, alpha=0.3)
    ax2_2d.set_xlabel('Bandwidth (MHz)', fontsize=10)
    ax2_2d.set_ylabel('Capacity (Mb/s)', fontsize=10)
    ax2_2d.set_title(f'Capacity vs. Bandwidth (SNR = {snr_db} dB)', fontsize=11)
    ax2_2d.legend()

    # 2D cross-section: Capacity vs. SNR (fixed bandwidth)
    ax3_2d = fig_shannon.add_subplot(2, 2, 3)

    snr_linear_range = 10**(snr_range / 10)
    cap_vs_snr = bw_mhz * np.log2(1 + snr_linear_range)
    ax3_2d.plot(snr_range, cap_vs_snr, 'g-', linewidth=2)
    ax3_2d.plot(snr_db, capacity_mbps, 'ro', markersize=10, label=f'Current: {capacity_mbps:.1f} Mb/s')
    ax3_2d.grid(True, alpha=0.3)
    ax3_2d.set_xlabel('SNR (dB)', fontsize=10)
    ax3_2d.set_ylabel('Capacity (Mb/s)', fontsize=10)
    ax3_2d.set_title(f'Capacity vs. SNR (BW = {bw_mhz} MHz)', fontsize=11)
    ax3_2d.legend()

    # Spectral efficiency vs. SNR
    ax4_2d = fig_shannon.add_subplot(2, 2, 4)

    spec_eff = np.log2(1 + snr_linear_range)
    ax4_2d.plot(snr_range, spec_eff, 'm-', linewidth=2)
    ax4_2d.plot(snr_db, spectral_efficiency, 'ro', markersize=10,
               label=f'Current: {spectral_efficiency:.2f} bits/s/Hz')
    ax4_2d.grid(True, alpha=0.3)
    ax4_2d.set_xlabel('SNR (dB)', fontsize=10)
    ax4_2d.set_ylabel('Spectral Efficiency (bits/s/Hz)', fontsize=10)
    ax4_2d.set_title('Spectral Efficiency vs. SNR', fontsize=11)
    ax4_2d.legend()

    plt.tight_layout()

    fig_shannon
    return (
        BW,
        CAPACITY,
        SNR,
        SNR_linear,
        ax1_3d,
        ax2_2d,
        ax3_2d,
        ax4_2d,
        bw_hz,
        bw_mhz,
        bw_range,
        cap_vs_bw,
        cap_vs_snr,
        capacity_bps,
        capacity_mbps,
        fig_shannon,
        snr_db,
        snr_linear,
        snr_linear_range,
        snr_range,
        spec_eff,
        spectral_efficiency,
        surf,
    )


@app.cell
def __(bw_mhz, capacity_mbps, mo, snr_db, spectral_efficiency):
    mo.md(
        f"""
        ### Shannon Capacity Results

        **Parameters:**
        - Bandwidth: {bw_mhz} MHz
        - SNR: {snr_db} dB

        **Results:**
        - Channel capacity: **{capacity_mbps:.2f} Mb/s**
        - Spectral efficiency: **{spectral_efficiency:.2f} bits/s/Hz**

        **Key insights:**
        - Capacity increases **linearly** with bandwidth
        - Capacity increases **logarithmically** with SNR
        - To double capacity: double bandwidth OR increase SNR by 6 dB
        - Practical systems achieve 50-90% of Shannon capacity
        """
    )
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        ---

        ## Cell 4: Thermal Noise Calculator

        Thermal noise power is given by:

        $$P_N = kTB$$

        where:
        - $k = 1.38 \times 10^{-23}$ J/K (Boltzmann's constant)
        - $T$ is temperature in Kelvin
        - $B$ is bandwidth in Hz

        In dBm: $P_N = 10\log_{10}(kTB \times 1000)$

        At room temperature (290K): $N_0 = kT = -174$ dBm/Hz
        """
    )
    return


@app.cell
def __(mo):
    # Noise calculator controls
    noise_temp = mo.ui.slider(
        start=1,
        stop=1000,
        step=10,
        value=290,
        label="Temperature (K):",
        show_value=True
    )

    noise_bw = mo.ui.slider(
        start=0.001,
        stop=100,
        step=0.1,
        value=20,
        label="Bandwidth (MHz):",
        show_value=True
    )

    mo.vstack([
        noise_temp,
        noise_bw
    ])
    return noise_bw, noise_temp


@app.cell
def __(mo, noise_bw, noise_temp, np, plt):
    # Constants
    k_boltzmann = 1.38e-23  # J/K

    # Get values
    temp_k = noise_temp.value
    bw_noise_mhz = noise_bw.value
    bw_noise_hz = bw_noise_mhz * 1e6

    # Calculate noise power
    noise_power_watts = k_boltzmann * temp_k * bw_noise_hz
    noise_power_dbm = 10 * np.log10(noise_power_watts * 1000)

    # Noise spectral density
    n0_dbm_hz = 10 * np.log10(k_boltzmann * temp_k * 1000)

    # Create visualization
    fig_noise, (ax_noise1, ax_noise2) = plt.subplots(1, 2, figsize=(14, 5))

    # Plot 1: Noise power vs. bandwidth
    bw_range_noise = np.logspace(-3, 2, 100)  # 0.001 to 100 MHz
    noise_power_range = 10 * np.log10(k_boltzmann * temp_k * bw_range_noise * 1e6 * 1000)

    ax_noise1.semilogx(bw_range_noise, noise_power_range, 'b-', linewidth=2)
    ax_noise1.semilogx(bw_noise_mhz, noise_power_dbm, 'ro', markersize=10,
                      label=f'Current: {noise_power_dbm:.1f} dBm')

    # Add typical signal levels for reference
    ax_noise1.axhline(y=-90, color='green', linestyle='--', label='Strong signal (-90 dBm)', alpha=0.7)
    ax_noise1.axhline(y=-110, color='orange', linestyle='--', label='Weak signal (-110 dBm)', alpha=0.7)

    ax_noise1.grid(True, alpha=0.3)
    ax_noise1.set_xlabel('Bandwidth (MHz)', fontsize=11)
    ax_noise1.set_ylabel('Noise Power (dBm)', fontsize=11)
    ax_noise1.set_title(f'Noise Power vs. Bandwidth (T = {temp_k} K)', fontsize=12)
    ax_noise1.legend()

    # Plot 2: Noise floor comparison at different temperatures
    temps = [77, 290, 373, 500, 1000]  # Liquid nitrogen, room temp, boiling water, hot, very hot
    temp_labels = ['77K\n(LN2)', '290K\n(Room)', '373K\n(Boiling)', '500K\n(Hot)', '1000K\n(Very hot)']
    noise_floors = [10 * np.log10(k_boltzmann * t * bw_noise_hz * 1000) for t in temps]

    colors_noise = ['cyan', 'green', 'orange', 'red', 'darkred']
    bars_noise = ax_noise2.bar(temp_labels, noise_floors, color=colors_noise, alpha=0.7, edgecolor='black')

    # Highlight current temperature
    current_temp_idx = min(range(len(temps)), key=lambda i: abs(temps[i] - temp_k))
    if abs(temps[current_temp_idx] - temp_k) < 50:
        bars_noise[current_temp_idx].set_linewidth(3)
        bars_noise[current_temp_idx].set_edgecolor('blue')

    # Add value labels
    for bar_n, nf in zip(bars_noise, noise_floors):
        height_n = bar_n.get_height()
        ax_noise2.text(bar_n.get_x() + bar_n.get_width()/2., height_n,
                f'{nf:.1f} dBm',
                ha='center', va='bottom', fontsize=9)

    ax_noise2.set_ylabel('Noise Power (dBm)', fontsize=11)
    ax_noise2.set_title(f'Noise Floor Comparison (BW = {bw_noise_mhz} MHz)', fontsize=12)
    ax_noise2.grid(True, alpha=0.3, axis='y')

    plt.tight_layout()

    fig_noise
    return (
        ax_noise1,
        ax_noise2,
        bar_n,
        bars_noise,
        bw_noise_hz,
        bw_noise_mhz,
        bw_range_noise,
        colors_noise,
        current_temp_idx,
        fig_noise,
        height_n,
        k_boltzmann,
        n0_dbm_hz,
        nf,
        noise_floors,
        noise_power_dbm,
        noise_power_range,
        noise_power_watts,
        temp_k,
        temp_labels,
        temps,
    )


@app.cell
def __(bw_noise_mhz, mo, n0_dbm_hz, noise_power_dbm, temp_k):
    mo.md(
        f"""
        ### Thermal Noise Results

        **Parameters:**
        - Temperature: {temp_k} K
        - Bandwidth: {bw_noise_mhz} MHz

        **Noise power:**
        - Noise spectral density: **{n0_dbm_hz:.1f} dBm/Hz**
        - Total noise power: **{noise_power_dbm:.1f} dBm**

        **Reference values:**
        - Room temp (290K): N₀ = -174 dBm/Hz
        - Typical receiver sensitivity: -90 to -110 dBm
        - SNR required for detection: typically 10-20 dB

        **Key insight:** Wider bandwidth = more noise power (proportional to BW)
        """
    )
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        ---

        ## Cell 5: Pulse Shape Visualizer

        Different pulse shapes have different spectral properties:

        **Rectangular pulse:**
        - $g(t) = 1$ for $|t| < T/2$, else $0$
        - $G(f) = T \cdot \text{sinc}(fT)$
        - Bandwidth: $\infty$ (first null at $1/T$)

        **Raised cosine pulse:**
        - Roll-off factor $\alpha \in [0, 1]$
        - Bandwidth: $B = \frac{1 + \alpha}{2T}$
        - Smooth in time and frequency domains
        """
    )
    return


@app.cell
def __(mo):
    # Pulse shape controls
    pulse_type = mo.ui.dropdown(
        ["Rectangular", "Raised Cosine"],
        value="Raised Cosine",
        label="Pulse type:"
    )

    alpha_slider = mo.ui.slider(
        start=0,
        stop=1,
        step=0.05,
        value=0.5,
        label="Roll-off α (for Raised Cosine):",
        show_value=True
    )

    symbol_rate_slider = mo.ui.slider(
        start=1,
        stop=100,
        step=1,
        value=10,
        label="Symbol rate (Msymb/s):",
        show_value=True
    )

    mo.vstack([
        pulse_type,
        alpha_slider,
        symbol_rate_slider
    ])
    return alpha_slider, pulse_type, symbol_rate_slider


@app.cell
def __(alpha_slider, mo, np, plt, pulse_type, symbol_rate_slider):
    def raised_cosine_freq(f, T, alpha):
        """Raised cosine frequency response."""
        G = np.zeros_like(f)
        for i, freq in enumerate(f):
            abs_f = abs(freq)
            if abs_f <= (1 - alpha) / (2 * T):
                G[i] = T
            elif abs_f <= (1 + alpha) / (2 * T):
                G[i] = (T / 2) * (1 + np.cos(np.pi * T / alpha * (abs_f - (1 - alpha) / (2 * T))))
            else:
                G[i] = 0
        return G

    def raised_cosine_time(t, T, alpha):
        """Raised cosine time response (approximation)."""
        g = np.zeros_like(t)
        for i, time in enumerate(t):
            if abs(time) < 1e-10:
                g[i] = 1.0
            else:
                numerator = np.sin(np.pi * time / T)
                denominator = (np.pi * time / T) * (1 - (2 * alpha * time / T)**2)
                if abs(denominator) > 1e-10:
                    g[i] = numerator / denominator * np.cos(np.pi * alpha * time / T)
                else:
                    g[i] = 0
        return g

    # Get values
    p_type = pulse_type.value
    alpha = alpha_slider.value
    symbol_rate = symbol_rate_slider.value  # Msymb/s
    T_symbol = 1 / symbol_rate  # microseconds

    # Time domain
    t = np.linspace(-5 * T_symbol, 5 * T_symbol, 1000)

    if p_type == "Rectangular":
        g_t = np.where(np.abs(t) <= T_symbol / 2, 1.0, 0.0)
    else:
        g_t = raised_cosine_time(t, T_symbol, alpha)

    # Frequency domain
    f = np.linspace(-3 / T_symbol, 3 / T_symbol, 1000)

    if p_type == "Rectangular":
        # sinc function
        G_f = T_symbol * np.sinc(f * T_symbol)
    else:
        G_f = raised_cosine_freq(f, T_symbol, alpha)

    # Calculate bandwidth (first null or -3dB point)
    if p_type == "Rectangular":
        bandwidth = 1 / T_symbol  # First null
    else:
        bandwidth = (1 + alpha) / (2 * T_symbol)  # Raised cosine BW

    # Create plots
    fig_pulse, (ax_time, ax_freq) = plt.subplots(1, 2, figsize=(14, 5))

    # Time domain
    ax_time.plot(t, g_t, 'b-', linewidth=2)
    ax_time.axhline(y=0, color='k', linestyle='-', linewidth=0.5)
    ax_time.axvline(x=0, color='k', linestyle='-', linewidth=0.5)
    ax_time.grid(True, alpha=0.3)
    ax_time.set_xlabel('Time (μs)', fontsize=11)
    ax_time.set_ylabel('g(t)', fontsize=11)
    ax_time.set_title(f'{p_type} Pulse - Time Domain', fontsize=12)
    ax_time.set_ylim([-0.3, 1.2])

    # Mark symbol period
    ax_time.axvline(x=-T_symbol/2, color='red', linestyle='--', alpha=0.5, label=f'T = {T_symbol:.2f} μs')
    ax_time.axvline(x=T_symbol/2, color='red', linestyle='--', alpha=0.5)
    ax_time.legend()

    # Frequency domain
    ax_freq.plot(f, G_f, 'r-', linewidth=2)
    ax_freq.axhline(y=0, color='k', linestyle='-', linewidth=0.5)
    ax_freq.axvline(x=0, color='k', linestyle='-', linewidth=0.5)
    ax_freq.grid(True, alpha=0.3)
    ax_freq.set_xlabel('Frequency (MHz)', fontsize=11)
    ax_freq.set_ylabel('|G(f)|', fontsize=11)
    ax_freq.set_title(f'{p_type} Pulse - Frequency Domain', fontsize=12)

    # Mark bandwidth
    ax_freq.axvline(x=bandwidth, color='green', linestyle='--', alpha=0.7,
                   label=f'BW = {bandwidth:.2f} MHz')
    ax_freq.axvline(x=-bandwidth, color='green', linestyle='--', alpha=0.7)
    ax_freq.legend()

    plt.tight_layout()

    fig_pulse
    return (
        G_f,
        T_symbol,
        alpha,
        ax_freq,
        ax_time,
        bandwidth,
        denominator,
        f,
        fig_pulse,
        freq,
        g,
        g_t,
        i,
        numerator,
        p_type,
        raised_cosine_freq,
        raised_cosine_time,
        symbol_rate,
        t,
        time,
    )


@app.cell
def __(T_symbol, alpha, bandwidth, mo, p_type, symbol_rate):
    mo.md(
        f"""
        ### Pulse Shape Results

        **Configuration:**
        - Pulse type: {p_type}
        - Symbol rate: {symbol_rate} Msymb/s (T = {T_symbol:.3f} μs)
        {f'- Roll-off factor: α = {alpha}' if p_type == 'Raised Cosine' else ''}

        **Bandwidth:**
        - {p_type} bandwidth: **{bandwidth:.2f} MHz**

        **Observations:**
        - Rectangular: narrow in time, wide in frequency (sinc spectrum)
        - Raised cosine: smooth in both domains, controlled bandwidth
        - Larger α: wider bandwidth, better time localization
        - Smaller α: narrower bandwidth, more ISI risk

        **Spectral efficiency:** {symbol_rate / bandwidth:.2f} symbols/s/Hz
        """
    )
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        ---

        ## Cell 6: Matched Filter Demo

        A matched filter maximizes SNR by correlating the received signal with the known pulse shape.

        **Matched filter:** $h(t) = g^*(T - t)$ (time-reversed, conjugate pulse)

        **Output:** $y(t) = r(t) * h(t) = s(t) * h(t) + n(t) * h(t)$

        The filter output is sampled at symbol intervals to recover transmitted bits.
        """
    )
    return


@app.cell
def __(mo):
    # Matched filter controls
    mf_pulse_shape = mo.ui.dropdown(
        ["Rectangular", "Raised Cosine"],
        value="Raised Cosine",
        label="Pulse shape:"
    )

    mf_snr_db = mo.ui.slider(
        start=-10,
        stop=30,
        step=2,
        value=10,
        label="SNR (dB):",
        show_value=True
    )

    mf_bit_pattern = mo.ui.text(
        value="10110100",
        label="Bit pattern (0s and 1s):"
    )

    mo.vstack([
        mf_pulse_shape,
        mf_snr_db,
        mf_bit_pattern
    ])
    return mf_bit_pattern, mf_pulse_shape, mf_snr_db


@app.cell
def __(mf_bit_pattern, mf_pulse_shape, mf_snr_db, mo, np, plt):
    # Get values
    mf_pulse = mf_pulse_shape.value
    mf_snr = mf_snr_db.value
    bit_string = mf_bit_pattern.value

    # Parse bit pattern
    bits_mf = [int(b) for b in bit_string if b in ['0', '1']]
    if len(bits_mf) == 0:
        bits_mf = [1, 0, 1, 1, 0, 1, 0, 0]  # Default

    # Parameters
    samples_per_symbol = 20
    T_sym = 1.0
    alpha_mf = 0.5

    # Generate pulse shape
    t_pulse = np.linspace(-2*T_sym, 2*T_sym, 4*samples_per_symbol)
    if mf_pulse == "Rectangular":
        pulse = np.where(np.abs(t_pulse) <= T_sym/2, 1.0, 0.0)
    else:
        # Simplified raised cosine
        pulse = np.sinc(t_pulse / T_sym) * np.cos(np.pi * alpha_mf * t_pulse / T_sym) / (1 - (2 * alpha_mf * t_pulse / T_sym)**2 + 1e-10)
        pulse = np.nan_to_num(pulse)

    # Normalize
    pulse = pulse / np.sqrt(np.sum(pulse**2))

    # Generate transmitted signal (bipolar: 0 -> -1, 1 -> +1)
    signal_bipolar = 2 * np.array(bits_mf) - 1

    # Upsample and convolve with pulse
    upsampled = np.zeros(len(bits_mf) * samples_per_symbol)
    upsampled[::samples_per_symbol] = signal_bipolar

    # Pad pulse
    pulse_len = len(pulse)
    transmitted = np.convolve(upsampled, pulse, mode='same')

    # Add noise
    snr_linear_mf = 10**(mf_snr / 10)
    signal_power = np.mean(transmitted**2)
    noise_power_mf = signal_power / snr_linear_mf
    noise = np.sqrt(noise_power_mf) * np.random.randn(len(transmitted))
    received = transmitted + noise

    # Matched filter (time-reversed pulse)
    matched_filter = pulse[::-1]
    filtered = np.convolve(received, matched_filter, mode='same')

    # Sample at symbol times
    sample_indices = np.arange(len(bits_mf)) * samples_per_symbol + samples_per_symbol // 2
    sample_indices = sample_indices[sample_indices < len(filtered)]
    sampled_values = filtered[sample_indices]

    # Make decisions
    decisions = (sampled_values > 0).astype(int)

    # Calculate BER
    num_errors = np.sum(decisions[:len(bits_mf)] != np.array(bits_mf))
    ber = num_errors / len(bits_mf) if len(bits_mf) > 0 else 0

    # Create multi-panel visualization
    fig_mf, axes_mf = plt.subplots(5, 1, figsize=(14, 12))

    t_axis = np.arange(len(transmitted)) / samples_per_symbol

    # Panel 1: Transmitted signal
    axes_mf[0].plot(t_axis, transmitted, 'b-', linewidth=1)
    axes_mf[0].set_ylabel('Tx Signal', fontsize=10)
    axes_mf[0].set_title('Matched Filter Demonstration', fontsize=12)
    axes_mf[0].grid(True, alpha=0.3)
    axes_mf[0].set_xlim([0, len(bits_mf)])

    # Panel 2: Received signal (with noise)
    axes_mf[1].plot(t_axis, received, 'r-', linewidth=1, alpha=0.7)
    axes_mf[1].set_ylabel('Rx Signal', fontsize=10)
    axes_mf[1].grid(True, alpha=0.3)
    axes_mf[1].set_xlim([0, len(bits_mf)])

    # Panel 3: Matched filter output
    axes_mf[2].plot(t_axis, filtered, 'g-', linewidth=1.5)
    axes_mf[2].scatter(sample_indices / samples_per_symbol, sampled_values,
                      color='red', s=50, zorder=5, label='Samples')
    axes_mf[2].axhline(y=0, color='k', linestyle='--', linewidth=1)
    axes_mf[2].set_ylabel('Filter Output', fontsize=10)
    axes_mf[2].grid(True, alpha=0.3)
    axes_mf[2].legend()
    axes_mf[2].set_xlim([0, len(bits_mf)])

    # Panel 4: Sampled values
    axes_mf[3].stem(np.arange(len(sampled_values)), sampled_values, basefmt=' ')
    axes_mf[3].axhline(y=0, color='k', linestyle='--', linewidth=1)
    axes_mf[3].set_ylabel('Sampled', fontsize=10)
    axes_mf[3].set_xlabel('Symbol Index', fontsize=10)
    axes_mf[3].grid(True, alpha=0.3)
    axes_mf[3].set_xlim([-0.5, len(bits_mf) - 0.5])

    # Panel 5: Bit decisions vs. original
    x_bits = np.arange(len(bits_mf))
    axes_mf[4].step(x_bits, bits_mf, 'b-', linewidth=2, label='Original', where='mid')
    axes_mf[4].step(x_bits[:len(decisions)], decisions, 'r--', linewidth=2, label='Decoded', where='mid')

    # Mark errors
    errors_idx = np.where(decisions[:len(bits_mf)] != np.array(bits_mf))[0]
    if len(errors_idx) > 0:
        axes_mf[4].scatter(errors_idx, np.array(bits_mf)[errors_idx], color='red',
                          s=100, marker='x', linewidths=3, label='Errors', zorder=5)

    axes_mf[4].set_ylabel('Bits', fontsize=10)
    axes_mf[4].set_xlabel('Bit Index', fontsize=10)
    axes_mf[4].set_ylim([-0.2, 1.2])
    axes_mf[4].legend()
    axes_mf[4].grid(True, alpha=0.3)
    axes_mf[4].set_xlim([-0.5, len(bits_mf) - 0.5])

    plt.tight_layout()

    fig_mf
    return (
        axes_mf,
        ber,
        bit_string,
        bits_mf,
        decisions,
        errors_idx,
        fig_mf,
        filtered,
        matched_filter,
        mf_pulse,
        mf_snr,
        noise,
        noise_power_mf,
        num_errors,
        pulse,
        pulse_len,
        received,
        sample_indices,
        sampled_values,
        samples_per_symbol,
        signal_bipolar,
        signal_power,
        snr_linear_mf,
        t_axis,
        t_pulse,
        transmitted,
        upsampled,
        x_bits,
    )


@app.cell
def __(ber, bits_mf, decisions, mf_pulse, mf_snr, mo, num_errors):
    mo.md(
        f"""
        ### Matched Filter Results

        **Configuration:**
        - Pulse shape: {mf_pulse}
        - SNR: {mf_snr} dB
        - Input bits: {len(bits_mf)} bits

        **Performance:**
        - Errors: {num_errors}/{len(bits_mf)}
        - BER: **{ber:.3f}** ({ber*100:.1f}%)

        **Decoded bits:** {''.join(map(str, decisions[:len(bits_mf)]))}

        **Observations:**
        - Matched filter maximizes SNR at sampling instant
        - Higher SNR → fewer errors
        - Eye diagram would show vertical opening at sampling times
        - Raised cosine reduces ISI compared to rectangular
        """
    )
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        ---

        ## Cell 7: BER Curve Plotter

        Bit Error Rate (BER) curves show the probability of bit error vs. signal-to-noise ratio.

        **Theoretical BER:**
        - **Unipolar (OOK):** $P_e = Q\left(\sqrt{\frac{E_b}{2N_0}}\right)$
        - **Bipolar (BPSK):** $P_e = Q\left(\sqrt{\frac{2E_b}{N_0}}\right)$
        - **M-PAM:** $P_e \approx \frac{2(M-1)}{M \log_2 M} Q\left(\sqrt{\frac{6\log_2 M}{M^2-1} \frac{E_s}{N_0}}\right)$

        where $Q(x) = \frac{1}{\sqrt{2\pi}} \int_x^\infty e^{-u^2/2} du$
        """
    )
    return


@app.cell
def __(mo):
    # BER curve controls
    mod_unipolar = mo.ui.checkbox(value=True, label="Unipolar (OOK)")
    mod_bipolar = mo.ui.checkbox(value=True, label="Bipolar (BPSK)")
    mod_4pam = mo.ui.checkbox(value=True, label="4-PAM")
    mod_8pam = mo.ui.checkbox(value=False, label="8-PAM")

    ebn0_min = mo.ui.slider(
        start=-5,
        stop=5,
        step=1,
        value=0,
        label="Min Eb/N0 (dB):",
        show_value=True
    )

    ebn0_max = mo.ui.slider(
        start=5,
        stop=25,
        step=1,
        value=15,
        label="Max Eb/N0 (dB):",
        show_value=True
    )

    mo.vstack([
        mo.md("**Select modulation types:**"),
        mod_unipolar,
        mod_bipolar,
        mod_4pam,
        mod_8pam,
        mo.md("**Eb/N0 range:**"),
        ebn0_min,
        ebn0_max
    ])
    return ebn0_max, ebn0_min, mod_4pam, mod_8pam, mod_bipolar, mod_unipolar


@app.cell
def __(
    ebn0_max,
    ebn0_min,
    mod_4pam,
    mod_8pam,
    mod_bipolar,
    mod_unipolar,
    mo,
    np,
    plt,
    special,
):
    # Get values
    eb_min = ebn0_min.value
    eb_max = ebn0_max.value

    # Generate Eb/N0 range
    ebn0_db_range = np.linspace(max(eb_min, -5), min(eb_max, 25), 100)
    ebn0_linear_ber = 10**(ebn0_db_range / 10)

    # Q-function
    def Q_func(x):
        return 0.5 * special.erfc(x / np.sqrt(2))

    # BER functions
    def ber_unipolar(ebn0):
        return Q_func(np.sqrt(ebn0 / 2))

    def ber_bipolar(ebn0):
        return Q_func(np.sqrt(2 * ebn0))

    def ber_mpam(ebn0, M):
        # Symbol energy to bit energy: Es = Eb * log2(M)
        esn0 = ebn0 * np.log2(M)
        return 2 * (M - 1) / (M * np.log2(M)) * Q_func(np.sqrt(6 * np.log2(M) / (M**2 - 1) * esn0))

    # Create plot
    fig_ber, ax_ber = plt.subplots(figsize=(12, 7))

    # Plot selected modulations
    if mod_unipolar.value:
        ber_uni = ber_unipolar(ebn0_linear_ber)
        ax_ber.semilogy(ebn0_db_range, ber_uni, 'b-', linewidth=2, label='Unipolar (OOK)')

    if mod_bipolar.value:
        ber_bi = ber_bipolar(ebn0_linear_ber)
        ax_ber.semilogy(ebn0_db_range, ber_bi, 'g-', linewidth=2, label='Bipolar (BPSK)')

    if mod_4pam.value:
        ber_4 = ber_mpam(ebn0_linear_ber, 4)
        ax_ber.semilogy(ebn0_db_range, ber_4, 'r-', linewidth=2, label='4-PAM')

    if mod_8pam.value:
        ber_8 = ber_mpam(ebn0_linear_ber, 8)
        ax_ber.semilogy(ebn0_db_range, ber_8, 'm-', linewidth=2, label='8-PAM')

    # Mark typical operating points
    target_bers = [1e-3, 1e-6, 1e-9]
    for target_ber in target_bers:
        ax_ber.axhline(y=target_ber, color='gray', linestyle='--', alpha=0.5, linewidth=1)
        ax_ber.text(eb_max - 1, target_ber * 1.5, f'BER = {target_ber:.0e}',
                   fontsize=8, color='gray')

    ax_ber.grid(True, alpha=0.3, which='both')
    ax_ber.set_xlabel('Eb/N0 (dB)', fontsize=12)
    ax_ber.set_ylabel('Bit Error Rate (BER)', fontsize=12)
    ax_ber.set_title('BER Performance Curves', fontsize=13)
    ax_ber.legend(loc='upper right', fontsize=11)
    ax_ber.set_ylim([1e-12, 1])
    ax_ber.set_xlim([eb_min, eb_max])

    plt.tight_layout()

    fig_ber
    return (
        Q_func,
        ax_ber,
        ber_4,
        ber_8,
        ber_bi,
        ber_bipolar,
        ber_mpam,
        ber_uni,
        ber_unipolar,
        eb_max,
        eb_min,
        ebn0_db_range,
        ebn0_linear_ber,
        esn0,
        fig_ber,
        target_ber,
        target_bers,
    )


@app.cell
def __(Q_func, eb_min, mo, np):
    # Calculate required Eb/N0 for target BERs
    targets = [1e-3, 1e-6, 1e-9]

    # Numerical search for required Eb/N0
    def find_ebn0_for_ber(ber_func, target_ber):
        ebn0_search = np.logspace(-1, 3, 1000)
        bers = ber_func(ebn0_search)
        idx = np.argmin(np.abs(bers - target_ber))
        return 10 * np.log10(ebn0_search[idx])

    # BPSK as reference
    ebn0_bpsk = [find_ebn0_for_ber(lambda x: Q_func(np.sqrt(2*x)), t) for t in targets]

    table_ber_data = {
        'Target BER': [f'{t:.0e}' for t in targets],
        'BPSK Eb/N0 (dB)': [f'{e:.1f}' for e in ebn0_bpsk],
        'Application': ['Voice (tolerable)', 'Data (good)', 'Optical (excellent)']
    }

    ber_table = mo.ui.table(table_ber_data)

    mo.vstack([
        mo.md("### Required Eb/N0 for Target BER (BPSK)"),
        ber_table,
        mo.md(
            f"""
            **Observations:**
            - BPSK requires ~3 dB less than unipolar (2× power efficiency)
            - Higher-order PAM needs more SNR for same BER
            - Each factor of 1000 reduction in BER requires ~2-3 dB more Eb/N0
            - Typical operating range: {eb_min} to 15 dB Eb/N0
            """
        )
    ])
    return (
        ber_table,
        ebn0_bpsk,
        ebn0_search,
        find_ebn0_for_ber,
        idx,
        t,
        table_ber_data,
        targets,
    )


@app.cell
def __(mo):
    mo.md(
        r"""
        ---

        ## Cell 8: Q-Function Explorer

        The Q-function represents the tail probability of a standard normal distribution:

        $$Q(x) = \frac{1}{\sqrt{2\pi}} \int_x^\infty e^{-u^2/2} du = P(Z > x) \text{ where } Z \sim \mathcal{N}(0,1)$$

        **Approximation:** $Q(x) \approx \frac{1}{x\sqrt{2\pi}} e^{-x^2/2}$ for large $x$

        **Relation to error function:** $Q(x) = \frac{1}{2}\text{erfc}\left(\frac{x}{\sqrt{2}}\right)$
        """
    )
    return


@app.cell
def __(mo):
    # Q-function controls
    q_x = mo.ui.slider(
        start=0,
        stop=6,
        step=0.1,
        value=2.0,
        label="x value:",
        show_value=True
    )

    q_x
    return (q_x,)


@app.cell
def __(Q_func, mo, np, plt, q_x, special):
    # Get value
    x_val = q_x.value
    q_val = Q_func(x_val)

    # Create visualization
    fig_q, (ax_q1, ax_q2) = plt.subplots(1, 2, figsize=(14, 5))

    # Plot 1: Q-function
    x_range_q = np.linspace(0, 6, 200)
    q_range = Q_func(x_range_q)

    ax_q1.semilogy(x_range_q, q_range, 'b-', linewidth=2, label='Q(x)')
    ax_q1.semilogy(x_val, q_val, 'ro', markersize=10, label=f'Q({x_val:.1f}) = {q_val:.2e}')

    # Approximation
    q_approx = 1 / (x_range_q * np.sqrt(2 * np.pi)) * np.exp(-x_range_q**2 / 2)
    ax_q1.semilogy(x_range_q, q_approx, 'g--', linewidth=1.5, alpha=0.7, label='Approximation')

    ax_q1.grid(True, alpha=0.3, which='both')
    ax_q1.set_xlabel('x', fontsize=11)
    ax_q1.set_ylabel('Q(x)', fontsize=11)
    ax_q1.set_title('Q-Function', fontsize=12)
    ax_q1.legend()
    ax_q1.set_ylim([1e-12, 1])

    # Plot 2: Standard normal PDF with shaded tail
    x_pdf = np.linspace(-4, 6, 500)
    pdf = 1/np.sqrt(2*np.pi) * np.exp(-x_pdf**2 / 2)

    ax_q2.plot(x_pdf, pdf, 'b-', linewidth=2, label='N(0,1) PDF')

    # Shade tail area
    x_tail = x_pdf[x_pdf >= x_val]
    pdf_tail = 1/np.sqrt(2*np.pi) * np.exp(-x_tail**2 / 2)
    ax_q2.fill_between(x_tail, 0, pdf_tail, alpha=0.3, color='red',
                       label=f'Area = Q({x_val:.1f}) = {q_val:.2e}')

    ax_q2.axvline(x=x_val, color='red', linestyle='--', linewidth=2)
    ax_q2.grid(True, alpha=0.3)
    ax_q2.set_xlabel('x', fontsize=11)
    ax_q2.set_ylabel('Probability Density', fontsize=11)
    ax_q2.set_title('Standard Normal Distribution', fontsize=12)
    ax_q2.legend()
    ax_q2.set_xlim([-4, 6])

    plt.tight_layout()

    fig_q
    return (
        ax_q1,
        ax_q2,
        fig_q,
        pdf,
        pdf_tail,
        q_approx,
        q_range,
        q_val,
        x_pdf,
        x_range_q,
        x_tail,
        x_val,
    )


@app.cell
def __(mo, q_val, x_val):
    # Interpretation
    sigma_level = x_val
    ber_interpretation = q_val

    # Common reference points
    if abs(x_val - 3.0) < 0.2:
        ref = "~3σ (99.7% within ±3σ)"
    elif abs(x_val - 4.0) < 0.2:
        ref = "~4σ (very low error rate)"
    elif abs(x_val - 5.0) < 0.2:
        ref = "~5σ (excellent link)"
    elif abs(x_val - 6.0) < 0.2:
        ref = "~6σ (exceptional link)"
    else:
        ref = f"{x_val:.1f}σ"

    mo.md(
        f"""
        ### Q-Function Results

        **Input:** x = {x_val:.2f}

        **Output:** Q({x_val:.2f}) = **{q_val:.4e}**

        **Interpretation:**
        - Probability that standard normal r.v. exceeds {x_val:.1f}
        - In BER context: error probability with {ref} decision margin
        - As BER: {ber_interpretation:.2e} ({ber_interpretation * 100:.4f}%)

        **Reference values:**
        - Q(2) ≈ 2.3 × 10⁻² (98% correct)
        - Q(3) ≈ 1.4 × 10⁻³ (99.9% correct)
        - Q(4) ≈ 3.2 × 10⁻⁵
        - Q(5) ≈ 2.9 × 10⁻⁷
        - Q(6) ≈ 9.9 × 10⁻¹⁰
        """
    )
    return ber_interpretation, ref, sigma_level


@app.cell
def __(mo):
    mo.md(
        r"""
        ---

        ## Cell 9: M-ary PAM Analyzer

        M-ary Pulse Amplitude Modulation (M-PAM) uses $M$ discrete amplitude levels to transmit $\log_2 M$ bits per symbol.

        **Constellation:** $\{-(M-1), -(M-3), \ldots, -1, +1, \ldots, +(M-3), +(M-1)\} \times A$

        **Symbol Error Rate (SER):**
        $$P_s \approx 2\left(1 - \frac{1}{M}\right) Q\left(\sqrt{\frac{6\log_2 M}{M^2-1} \frac{E_s}{N_0}}\right)$$

        **Minimum distance:** $d_{min} = 2A$
        """
    )
    return


@app.cell
def __(mo):
    # M-PAM controls
    M_dropdown = mo.ui.dropdown(
        ["2", "4", "8", "16"],
        value="4",
        label="M (number of levels):"
    )

    Es_slider = mo.ui.slider(
        start=-10,
        stop=30,
        step=1,
        value=10,
        label="Es (symbol energy, dB):",
        show_value=True
    )

    N0_slider = mo.ui.slider(
        start=-20,
        stop=10,
        step=1,
        value=-10,
        label="N0 (noise PSD, dBm/Hz):",
        show_value=True
    )

    mo.vstack([
        M_dropdown,
        Es_slider,
        N0_slider
    ])
    return Es_slider, M_dropdown, N0_slider


@app.cell
def __(Es_slider, M_dropdown, N0_slider, Q_func, mo, np, plt):
    # Get values
    M_pam = int(M_dropdown.value)
    Es_db = Es_slider.value
    N0_db = N0_slider.value

    # Convert to linear
    Es_linear = 10**(Es_db / 10)
    N0_linear = 10**(N0_db / 10)
    EsN0_linear = Es_linear / N0_linear
    EsN0_db = Es_db - N0_db

    # PAM constellation points (normalized)
    constellation = np.arange(-(M_pam-1), M_pam, 2)

    # Average symbol energy (normalized): E_s = (M^2 - 1) / 3
    avg_energy_norm = (M_pam**2 - 1) / 3

    # Scale constellation to match desired Es
    A = np.sqrt(Es_linear / avg_energy_norm)
    constellation_scaled = constellation * A

    # Minimum distance
    d_min = 2 * A

    # SER
    ser = 2 * (1 - 1/M_pam) * Q_func(np.sqrt(6 * np.log2(M_pam) / (M_pam**2 - 1) * EsN0_linear))

    # BER (approximate for Gray coding)
    ber_pam = ser / np.log2(M_pam)

    # Spectral efficiency
    spec_eff_pam = np.log2(M_pam)  # bits/symbol

    # Create visualization
    fig_pam, (ax_const, ax_noise) = plt.subplots(1, 2, figsize=(14, 6))

    # Constellation diagram with decision thresholds
    ax_const.scatter(constellation_scaled, np.zeros(M_pam), s=200, c='blue',
                    marker='o', edgecolors='black', linewidths=2, label='Constellation points')

    # Decision thresholds (midpoints between symbols)
    thresholds = (constellation_scaled[:-1] + constellation_scaled[1:]) / 2
    for thresh in thresholds:
        ax_const.axvline(x=thresh, color='red', linestyle='--', alpha=0.5, linewidth=1.5)

    # Add labels
    for _i_pam, _point_pam in enumerate(constellation_scaled):
        # Convert index to Gray-coded bits
        _bits_pam = format(_i_pam, f'0{int(np.log2(M_pam))}b')
        ax_const.text(_point_pam, 0.5, _bits_pam, ha='center', fontsize=10, fontweight='bold')

    ax_const.set_xlabel('Amplitude', fontsize=11)
    ax_const.set_ylabel('', fontsize=11)
    ax_const.set_title(f'{M_pam}-PAM Constellation Diagram', fontsize=12)
    ax_const.set_ylim([-1, 1])
    ax_const.grid(True, alpha=0.3, axis='x')
    ax_const.legend(loc='upper right')
    ax_const.axhline(y=0, color='black', linewidth=0.5)

    # Show minimum distance
    ax_const.annotate('', xy=(constellation_scaled[1], -0.3),
                     xytext=(constellation_scaled[0], -0.3),
                     arrowprops=dict(arrowstyle='<->', color='green', lw=2))
    ax_const.text((constellation_scaled[0] + constellation_scaled[1])/2, -0.5,
                 f'd_min = {d_min:.2f}', ha='center', color='green', fontweight='bold')

    # Noise clouds
    noise_std = np.sqrt(N0_linear / 2)  # Noise standard deviation
    x_range_pam = np.linspace(constellation_scaled.min() - 3*noise_std,
                              constellation_scaled.max() + 3*noise_std, 1000)

    for point in constellation_scaled:
        pdf_noise = 1/(noise_std * np.sqrt(2*np.pi)) * np.exp(-(x_range_pam - point)**2 / (2*noise_std**2))
        ax_noise.plot(x_range_pam, pdf_noise, linewidth=1.5, alpha=0.7)

    # Decision thresholds
    for thresh in thresholds:
        ax_noise.axvline(x=thresh, color='red', linestyle='--', alpha=0.5, linewidth=1.5)

    ax_noise.set_xlabel('Amplitude', fontsize=11)
    ax_noise.set_ylabel('Probability Density', fontsize=11)
    ax_noise.set_title('Noise Distributions and Decision Regions', fontsize=12)
    ax_noise.grid(True, alpha=0.3)

    plt.tight_layout()

    fig_pam
    return (
        A,
        Es_db,
        Es_linear,
        EsN0_db,
        EsN0_linear,
        M_pam,
        N0_db,
        N0_linear,
        avg_energy_norm,
        ax_const,
        ax_noise,
        ber_pam,
        constellation,
        constellation_scaled,
        d_min,
        fig_pam,
        noise_std,
        pdf_noise,
        ser,
        spec_eff_pam,
        thresholds,
        x_range_pam,
    )


@app.cell
def __(
    EsN0_db,
    M_pam,
    ber_pam,
    d_min,
    mo,
    ser,
    spec_eff_pam,
):
    mo.md(
        f"""
        ### M-ary PAM Results

        **Configuration:**
        - M = {M_pam} levels ({int(np.log2(M_pam))} bits/symbol)
        - Es/N0 = {EsN0_db:.1f} dB

        **Performance:**
        - Minimum distance: d_min = {d_min:.3f}
        - Symbol Error Rate (SER): **{ser:.4e}**
        - Bit Error Rate (BER): **{ber_pam:.4e}** (assuming Gray coding)
        - Spectral efficiency: **{spec_eff_pam:.1f} bits/s/Hz**

        **Tradeoffs:**
        - Higher M → more bits/symbol (higher spectral efficiency)
        - Higher M → smaller d_min → higher error rate (for fixed power)
        - To maintain BER: M doubles → need ~6 dB more Es/N0

        **Decision rule:** Choose symbol closest to received amplitude
        """
    )
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        ---

        ## Cell 10: Power-Bandwidth Tradeoff

        For a target data rate $R$ bps with bandwidth $B$ Hz:

        **Required M:** $M = 2^{R/B}$

        **Required SNR:** From BER requirement and M-PAM formula

        **Required Tx power:** $P_{tx} = E_b R + \text{losses} + \text{margin}$

        This demonstrates the fundamental tradeoff: more bandwidth → lower M → less power needed.
        """
    )
    return


@app.cell
def __(mo):
    # Power-bandwidth tradeoff controls
    target_rate = mo.ui.slider(
        start=1,
        stop=100,
        step=1,
        value=40,
        label="Target data rate (Mb/s):",
        show_value=True
    )

    available_bw = mo.ui.slider(
        start=1,
        stop=100,
        step=1,
        value=20,
        label="Available bandwidth (MHz):",
        show_value=True
    )

    n0_psd = mo.ui.slider(
        start=-180,
        stop=-150,
        step=1,
        value=-174,
        label="N0 (dBm/Hz):",
        show_value=True
    )

    target_ber_dropdown = mo.ui.dropdown(
        ["1e-3", "1e-6", "1e-9"],
        value="1e-6",
        label="Target BER:"
    )

    mo.vstack([
        target_rate,
        available_bw,
        n0_psd,
        target_ber_dropdown
    ])
    return available_bw, n0_psd, target_ber_dropdown, target_rate


@app.cell
def __(
    Q_func,
    available_bw,
    mo,
    n0_psd,
    np,
    plt,
    target_ber_dropdown,
    target_rate,
):
    # Get values
    R_mbps = target_rate.value
    B_mhz = available_bw.value
    N0_dbm_hz = n0_psd.value
    target_ber_str = target_ber_dropdown.value
    target_ber_val = float(target_ber_str)

    # Calculate required M
    spectral_eff_req = R_mbps / B_mhz  # bits/s/Hz
    M_required = 2**spectral_eff_req
    M_actual = 2**np.ceil(np.log2(M_required))  # Round up to power of 2

    # Actual spectral efficiency and data rate
    actual_spec_eff = np.log2(M_actual)
    actual_rate = B_mhz * actual_spec_eff

    # Required Eb/N0 for target BER (using M-PAM formula)
    # Solve: BER = (2(M-1)/(M log2(M))) * Q(sqrt(arg)) = target_BER
    # Approximate search
    def find_required_ebn0(M, target_ber):
        # Search for Eb/N0 that gives target BER
        ebn0_search_range = np.logspace(-1, 3, 1000)
        for ebn0 in ebn0_search_range:
            esn0 = ebn0 * np.log2(M)
            ber_est = 2 * (M - 1) / (M * np.log2(M)) * Q_func(np.sqrt(6 * np.log2(M) / (M**2 - 1) * esn0))
            if ber_est <= target_ber:
                return 10 * np.log10(ebn0)
        return np.nan

    required_ebn0_db = find_required_ebn0(M_actual, target_ber_val)

    # Required transmit power
    N0_linear_mw = 10**(N0_dbm_hz / 10)
    R_hz = R_mbps * 1e6
    total_noise_power_dbm = N0_dbm_hz + 10*np.log10(B_mhz * 1e6)

    # Eb = Eb/N0 * N0
    eb_dbm = required_ebn0_db + N0_dbm_hz
    tx_power_dbm = eb_dbm + 10*np.log10(R_hz)

    # Create comparison table
    comparison_table_data = {
        'Bandwidth (MHz)': [],
        'Required M': [],
        'Eb/N0 (dB)': [],
        'Tx Power (dBm)': []
    }

    bw_options = [10, 20, 40, 80]
    for bw_opt in bw_options:
        spec_eff_opt = R_mbps / bw_opt
        M_opt = 2**np.ceil(np.log2(2**spec_eff_opt))
        ebn0_opt = find_required_ebn0(M_opt, target_ber_val)
        eb_opt = ebn0_opt + N0_dbm_hz
        tx_opt = eb_opt + 10*np.log10(R_hz)

        comparison_table_data['Bandwidth (MHz)'].append(f'{bw_opt}')
        comparison_table_data['Required M'].append(f'{int(M_opt)}')
        comparison_table_data['Eb/N0 (dB)'].append(f'{ebn0_opt:.1f}')
        comparison_table_data['Tx Power (dBm)'].append(f'{tx_opt:.1f}')

    comparison_table = mo.ui.table(comparison_table_data)

    # Create tradeoff plot
    fig_tradeoff, (ax_tr1, ax_tr2) = plt.subplots(1, 2, figsize=(14, 6))

    # Plot 1: Required M vs. Bandwidth
    bw_range_tr = np.linspace(5, 100, 50)
    M_range_tr = [2**np.ceil(np.log2(2**(R_mbps / bw))) for bw in bw_range_tr]

    ax_tr1.semilogy(bw_range_tr, M_range_tr, 'b-', linewidth=2)
    ax_tr1.semilogy(B_mhz, M_actual, 'ro', markersize=10, label=f'Current: M={int(M_actual)}')
    ax_tr1.grid(True, alpha=0.3, which='both')
    ax_tr1.set_xlabel('Bandwidth (MHz)', fontsize=11)
    ax_tr1.set_ylabel('Required M', fontsize=11)
    ax_tr1.set_title(f'Modulation Order vs. Bandwidth (R = {R_mbps} Mb/s)', fontsize=12)
    ax_tr1.legend()

    # Plot 2: Required Tx Power vs. Bandwidth
    tx_power_range = []
    for bw in bw_range_tr:
        M_bw = 2**np.ceil(np.log2(2**(R_mbps / bw)))
        ebn0_bw = find_required_ebn0(M_bw, target_ber_val)
        eb_bw = ebn0_bw + N0_dbm_hz
        tx_bw = eb_bw + 10*np.log10(R_hz)
        tx_power_range.append(tx_bw)

    ax_tr2.plot(bw_range_tr, tx_power_range, 'g-', linewidth=2)
    ax_tr2.plot(B_mhz, tx_power_dbm, 'ro', markersize=10, label=f'Current: {tx_power_dbm:.1f} dBm')
    ax_tr2.grid(True, alpha=0.3)
    ax_tr2.set_xlabel('Bandwidth (MHz)', fontsize=11)
    ax_tr2.set_ylabel('Required Tx Power (dBm)', fontsize=11)
    ax_tr2.set_title(f'Transmit Power vs. Bandwidth (R = {R_mbps} Mb/s, BER = {target_ber_str})', fontsize=12)
    ax_tr2.legend()

    plt.tight_layout()

    result_tradeoff = mo.vstack([
        mo.md("### Power-Bandwidth Tradeoff Comparison"),
        comparison_table,
        mo.md("### Tradeoff Curves"),
        fig_tradeoff
    ])

    result_tradeoff
    return (
        B_mhz,
        M_actual,
        M_bw,
        M_opt,
        M_range_tr,
        M_required,
        N0_dbm_hz,
        N0_linear_mw,
        R_hz,
        R_mbps,
        actual_rate,
        actual_spec_eff,
        ax_tr1,
        ax_tr2,
        bw,
        bw_opt,
        bw_options,
        bw_range_tr,
        comparison_table,
        comparison_table_data,
        eb_bw,
        eb_dbm,
        eb_opt,
        ebn0_bw,
        ebn0_opt,
        ebn0_search_range,
        fig_tradeoff,
        find_required_ebn0,
        total_noise_power_dbm,
        required_ebn0_db,
        result_tradeoff,
        spec_eff_opt,
        spectral_eff_req,
        target_ber_str,
        target_ber_val,
        tx_bw,
        tx_opt,
        tx_power_dbm,
        tx_power_range,
    )


@app.cell
def __(
    B_mhz,
    M_actual,
    R_mbps,
    actual_rate,
    mo,
    required_ebn0_db,
    target_ber_str,
    tx_power_dbm,
):
    mo.md(
        f"""
        ### Power-Bandwidth Tradeoff Results

        **Requirements:**
        - Data rate: {R_mbps} Mb/s
        - Bandwidth: {B_mhz} MHz
        - Target BER: {target_ber_str}

        **Solution:**
        - Required M: **{int(M_actual)}-PAM**
        - Actual rate: {actual_rate:.1f} Mb/s
        - Required Eb/N0: **{required_ebn0_db:.1f} dB**
        - Required Tx power: **{tx_power_dbm:.1f} dBm**

        **Key tradeoffs:**
        - **More bandwidth** → smaller M → less power needed → easier to achieve
        - **Less bandwidth** → larger M → more power needed → harder to achieve
        - Doubling bandwidth typically saves ~6 dB in required Tx power
        - Limited bandwidth forces use of higher-order modulation

        **Practical consideration:** M > 64 becomes challenging due to noise sensitivity
        """
    )
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        ---

        ## Summary

        This notebook explored key physical layer concepts:

        1. **Attenuation** - Different media have vastly different loss characteristics
        2. **Link budgets** - Accounting for all gains and losses in a communication link
        3. **Shannon capacity** - Theoretical maximum data rate given bandwidth and SNR
        4. **Thermal noise** - Fundamental noise floor limiting receiver sensitivity
        5. **Pulse shaping** - Controlling time and frequency characteristics of signals
        6. **Matched filtering** - Optimal detection in the presence of noise
        7. **BER curves** - Quantifying error probability vs. SNR for different modulations
        8. **Q-function** - Statistical tool for calculating error probabilities
        9. **M-ary PAM** - Trading spectral efficiency for power efficiency
        10. **Power-bandwidth tradeoff** - Fundamental engineering tradeoff in communication systems

        **Key insights:**
        - Physical layer design involves balancing multiple competing constraints
        - Bandwidth and power are interchangeable resources (to a degree)
        - Noise sets fundamental limits on achievable performance
        - Practical systems operate well below Shannon capacity due to implementation constraints
        """
    )
    return


if __name__ == "__main__":
    app.run()
