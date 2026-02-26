import marimo

__generated_with = "0.19.6"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import numpy as np
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    from matplotlib.patches import FancyBboxPatch
    return mo, mpatches, np, plt, FancyBboxPatch


@app.cell
def _(mo):
    mo.md(r"""
    # Lecture 8: Ethernet — Interactive Exploration

    **EC 441 - Introduction to Computer Networking**

    This notebook explores Ethernet concepts interactively:

    1. **Ethernet Frame Anatomy** — field-by-field breakdown of a real frame
    2. **MAC Address Decoder** — OUI, I/G bit, U/L bit, address type
    3. **ARP Exchange Simulator** — step through an ARP request/reply on a LAN
    4. **Switch Self-Learning** — watch a forwarding table build up interactively
    5. **Ethernet Technology Timeline** — speed vs. year across generations
    """)
    return


# ─────────────────────────────────────────────────────────────────────────────
# Part 1: Ethernet Frame Anatomy
# ─────────────────────────────────────────────────────────────────────────────

@app.cell
def _(mo):
    mo.md(r"""
    ---
    ## Part 1: Ethernet Frame Anatomy

    An Ethernet frame consists of these fields (preamble + SFD often called "8-byte preamble"):

    | Field | Size | Purpose |
    |-------|------|---------|
    | Preamble + SFD | 8 B | Clock sync; marks frame start |
    | Destination MAC | 6 B | Link-layer destination address |
    | Source MAC | 6 B | Link-layer source address |
    | EtherType | 2 B | Encapsulated protocol (IPv4=0x0800, ARP=0x0806, IPv6=0x86DD) |
    | Payload | 46–1500 B | Data (IP datagram, ARP message, …) |
    | FCS | 4 B | CRC-32 error check |

    **Minimum frame**: 64 bytes (with 46-byte minimum payload, or padding to reach it)
    **Maximum frame**: 1518 bytes (1500-byte payload + headers)

    The 64-byte minimum comes from the CSMA/CD constraint: at 10 Mb/s with max 500 m cable,
    $L_{\min} = 2\tau R = 51.2\,\mu\text{s} \times 10\,\text{Mb/s} = 512\,\text{bits} = 64\,\text{bytes}$.
    """)
    return


@app.cell
def _(mo):
    payload_size_slider = mo.ui.slider(
        start=0, stop=1500, step=1, value=100,
        label="Payload size (bytes):", show_value=True
    )
    payload_size_slider
    return (payload_size_slider,)


@app.cell
def _(FancyBboxPatch, mo, payload_size_slider, plt):
    payload_bytes = payload_size_slider.value
    padded_payload = max(46, payload_bytes)
    padding = padded_payload - payload_bytes
    total_frame = 8 + 6 + 6 + 2 + padded_payload + 4

    # Build field list: (label, size, color)
    fields = [
        ("Preamble\n+SFD", 8, "#d3d3d3"),
        ("Dst\nMAC", 6, "#aec6e8"),
        ("Src\nMAC", 6, "#b5d9a8"),
        ("Type", 2, "#ffe599"),
        ("Payload", payload_bytes, "#ffffff"),
    ]
    if padding > 0:
        fields.append(("Pad", padding, "#f4b9b8"))
    fields.append(("FCS", 4, "#f4b9b8"))

    fig_frame, ax_frame = plt.subplots(figsize=(12, 1.8))
    ax_frame.set_xlim(0, total_frame)
    ax_frame.set_ylim(0, 1)
    ax_frame.axis("off")

    x = 0
    for label, size, color in fields:
        rect = FancyBboxPatch(
            (x, 0.1), size, 0.8,
            boxstyle="square,pad=0.01",
            linewidth=1.2, edgecolor="black", facecolor=color
        )
        ax_frame.add_patch(rect)
        ax_frame.text(
            x + size / 2, 0.5, label,
            ha="center", va="center", fontsize=8, fontweight="bold"
        )
        ax_frame.text(
            x + size / 2, 0.05, f"{size}B",
            ha="center", va="bottom", fontsize=7, color="#555555"
        )
        x += size

    status = "✓ valid" if payload_bytes >= 46 else f"⚠ padded (+{padding}B to reach 46B minimum)"
    ax_frame.set_title(
        f"Frame total: {total_frame} bytes  |  payload: {payload_bytes} B  |  {status}",
        fontsize=10
    )
    plt.tight_layout()

    note = mo.md(
        f"**Frame breakdown**: {total_frame} bytes total. "
        + (f"Payload is {payload_bytes} bytes — below the 46-byte minimum, so {padding} pad byte(s) added."
           if padding > 0 else
           f"Payload is {payload_bytes} bytes — no padding needed.")
        + (" Frame is within the 1518-byte maximum." if total_frame <= 1518 else
           f" ⚠ Frame exceeds the 1518-byte maximum ({total_frame} bytes)!")
    )
    mo.vstack([fig_frame, note])
    return (
        ax_frame,
        color,
        fields,
        fig_frame,
        label,
        note,
        padded_payload,
        padding,
        payload_bytes,
        rect,
        size,
        status,
        total_frame,
        x,
    )


# ─────────────────────────────────────────────────────────────────────────────
# Part 2: MAC Address Decoder
# ─────────────────────────────────────────────────────────────────────────────

@app.cell
def _(mo):
    mo.md(r"""
    ---
    ## Part 2: MAC Address Decoder

    Enter a MAC address in colon-separated hex format.
    The decoder will identify the OUI, address type (unicast/multicast/broadcast),
    and administrative scope (globally/locally administered).

    **Examples to try**:
    - `A4:C3:F0:85:AC:2D` — Apple device (globally administered unicast)
    - `FF:FF:FF:FF:FF:FF` — Ethernet broadcast
    - `01:00:5E:7F:00:01` — IPv4 multicast (224.127.0.1)
    - `02:00:00:00:00:01` — locally administered unicast
    - `33:33:00:00:00:01` — IPv6 all-nodes multicast
    """)
    return


@app.cell
def _(mo):
    mac_input = mo.ui.text(
        value="A4:C3:F0:85:AC:2D",
        label="MAC address (hex, colon-separated):",
        placeholder="XX:XX:XX:XX:XX:XX"
    )
    mac_input
    return (mac_input,)


@app.cell
def _(mac_input, mo):
    # Well-known OUI prefixes (first 3 bytes as upper-case hex, no colons)
    _KNOWN_OUIS = {
        "A4C3F0": "Apple",
        "3C5AB4": "Apple",
        "F0189B": "Apple",
        "000C29": "VMware",
        "001A11": "Google",
        "0050F2": "Microsoft",
        "8CAEBD": "Dell",
        "5405DB": "Dell",
        "D89EF3": "Intel",
        "001B21": "Intel",
        "00163E": "Xen / Amazon AWS",
        "020000": "Locally administered",
        "484D7E": "Raspberry Pi Foundation",
        "DC:A6:32": "Raspberry Pi",
        "B8:27:EB": "Raspberry Pi",
    }

    def _decode_mac(mac_str):
        mac_str = mac_str.strip()
        # Accept colons or hyphens
        parts = mac_str.replace("-", ":").split(":")
        if len(parts) != 6:
            return None, "Invalid format: expected 6 colon-separated hex bytes"
        try:
            bytes_val = [int(p, 16) for p in parts]
        except ValueError:
            return None, "Invalid hex digits in address"
        if any(b < 0 or b > 255 for b in bytes_val):
            return None, "Byte value out of range"
        return bytes_val, None

    def _analyze_mac(bytes_val):
        b0 = bytes_val[0]
        ig_bit = b0 & 0x01       # I/G: 0=unicast, 1=multicast
        ul_bit = (b0 >> 1) & 0x01  # U/L: 0=global, 1=local

        is_broadcast = all(b == 0xFF for b in bytes_val)
        is_multicast = bool(ig_bit) and not is_broadcast
        is_unicast = not ig_bit
        is_local = bool(ul_bit)
        is_global = not is_local

        oui_key = "".join(f"{b:02X}" for b in bytes_val[:3])
        # Strip I/G and U/L bits from OUI for lookup
        oui_canonical_b0 = b0 & 0xFC  # clear lower 2 bits
        oui_key_clean = f"{oui_canonical_b0:02X}" + "".join(f"{b:02X}" for b in bytes_val[1:3])
        vendor = _KNOWN_OUIS.get(oui_key, _KNOWN_OUIS.get(oui_key_clean, "Unknown manufacturer"))

        if is_broadcast:
            addr_type = "**Broadcast** (all-ones; received by every device on the LAN)"
        elif is_multicast:
            addr_type = "**Multicast** (I/G bit = 1; received by a group of devices)"
        else:
            addr_type = "**Unicast** (I/G bit = 0; addressed to a single interface)"

        admin = "**Locally administered** (U/L bit = 1; overridden by software)" if is_local \
                else "**Globally administered** (U/L bit = 0; factory-assigned OUI)"

        binary_b0 = f"{b0:08b}"
        oui_display = ":".join(f"{b:02X}" for b in bytes_val[:3])
        nic_display = ":".join(f"{b:02X}" for b in bytes_val[3:])

        return {
            "addr_type": addr_type,
            "admin": admin,
            "vendor": vendor,
            "oui": oui_display,
            "nic": nic_display,
            "binary_b0": binary_b0,
            "ig": ig_bit,
            "ul": ul_bit,
        }

    _bytes, _err = _decode_mac(mac_input.value)
    if _err:
        result_display = mo.callout(mo.md(f"**Error**: {_err}"), kind="danger")
    else:
        _info = _analyze_mac(_bytes)
        result_display = mo.md(f"""
**Address type**: {_info['addr_type']}

**Administrative scope**: {_info['admin']}

**OUI** (bytes 1–3): `{_info['oui']}` → {_info['vendor']}

**NIC-specific** (bytes 4–6): `{_info['nic']}`

**First byte in binary**: `{_info['binary_b0']}`
- Bit 0 (I/G): `{_info['ig']}` → {"multicast/broadcast" if _info['ig'] else "unicast"}
- Bit 1 (U/L): `{_info['ul']}` → {"locally administered" if _info['ul'] else "globally administered"}
""")
    result_display
    return (
        mac_input,
        mo,
        result_display,
    )


# ─────────────────────────────────────────────────────────────────────────────
# Part 3: ARP Exchange Simulator
# ─────────────────────────────────────────────────────────────────────────────

@app.cell
def _(mo):
    mo.md(r"""
    ---
    ## Part 3: ARP Exchange Simulator

    Simulate an ARP exchange on a small LAN. Use the step buttons to advance through the protocol.
    The LAN has four hosts connected to a switch.
    """)
    return


@app.cell
def _(mo):
    arp_hosts = {
        "Host A": {"ip": "192.168.1.10", "mac": "AA:AA:AA:AA:AA:AA", "port": 1},
        "Host B": {"ip": "192.168.1.20", "mac": "BB:BB:BB:BB:BB:BB", "port": 2},
        "Host C": {"ip": "192.168.1.30", "mac": "CC:CC:CC:CC:CC:CC", "port": 3},
        "Router": {"ip": "192.168.1.1",  "mac": "RR:RR:RR:RR:RR:RR", "port": 4},
    }

    arp_requester = mo.ui.dropdown(
        options=list(arp_hosts.keys()),
        value="Host A",
        label="Requester (wants to send a frame):"
    )
    arp_target_ip = mo.ui.dropdown(
        options=[h["ip"] for h in arp_hosts.values()],
        value="192.168.1.20",
        label="Target IP address:"
    )
    mo.hstack([arp_requester, arp_target_ip])
    return arp_host_sel, arp_hosts, arp_requester, arp_target_ip


@app.cell
def _(arp_hosts, arp_requester, arp_target_ip, mo):
    _req_name = arp_requester.value
    _req = arp_hosts[_req_name]
    _tgt_ip = arp_target_ip.value

    # Find target host
    _tgt_host = None
    _tgt_name = None
    for _name, _h in arp_hosts.items():
        if _h["ip"] == _tgt_ip:
            _tgt_host = _h
            _tgt_name = _name
            break

    if _tgt_host is None:
        arp_display = mo.callout(mo.md("Target IP not found on this LAN."), kind="warn")
    elif _tgt_ip == _req["ip"]:
        arp_display = mo.callout(mo.md("Requester and target are the same host."), kind="warn")
    else:
        _other_names = [n for n in arp_hosts if n not in (_req_name, _tgt_name)]
        _steps = mo.md(f"""
### ARP Exchange: {_req_name} → target IP {_tgt_ip}

**Step 0 — Before ARP**

{_req_name} needs to send a frame to `{_tgt_ip}` but doesn't know its MAC address.
ARP table for {_req_name}: *(empty for this destination)*

---

**Step 1 — ARP Request (broadcast)**

{_req_name} sends a broadcast frame:
```
Ethernet:  src={_req['mac']}  dst=FF:FF:FF:FF:FF:FF
ARP:  "Who has {_tgt_ip}?  Tell {_req['ip']} ({_req['mac']})"
```
All hosts on the LAN receive this:
- **{_tgt_name}** (`{_tgt_ip}`): *this is for me — I will reply*
- **{_other_names[0] if _other_names else '(none)'}**: *not for me — discard* (but I can cache `{_req['ip']} → {_req['mac']}`)

---

**Step 2 — ARP Reply (unicast)**

{_tgt_name} sends a unicast reply directly back to {_req_name}:
```
Ethernet:  src={_tgt_host['mac']}  dst={_req['mac']}
ARP:  "I am {_tgt_ip}; my MAC is {_tgt_host['mac']}"
```

---

**Step 3 — ARP Table Updated**

{_req_name}'s ARP table:
| IP Address | MAC Address | TTL |
|---|---|---|
| `{_tgt_ip}` | `{_tgt_host['mac']}` | ~20 min |

---

**Step 4 — Frame Sent**

{_req_name} can now send the original frame:
```
Ethernet:  src={_req['mac']}  dst={_tgt_host['mac']}
IP:        src={_req['ip']}   dst={_tgt_ip}
```
""")
        arp_display = _steps

    arp_display
    return (
        arp_display,
        arp_hosts,
        arp_requester,
        arp_target_ip,
        mo,
    )


# ─────────────────────────────────────────────────────────────────────────────
# Part 4: Switch Self-Learning
# ─────────────────────────────────────────────────────────────────────────────

@app.cell
def _(mo):
    mo.md(r"""
    ---
    ## Part 4: Switch Self-Learning

    Simulate a switch with 4 ports, one host per port.
    Send frames between hosts and watch the forwarding table build up.

    **Rule**: on each arriving frame, the switch:
    1. **Learns** the source MAC → ingress port
    2. **Forwards** to the known port (or **floods** all other ports if unknown)
    """)
    return


@app.cell
def _(mo):
    _sw_hosts = ["Host A (port 1)", "Host B (port 2)", "Host C (port 3)", "Host D (port 4)"]

    sw_src = mo.ui.dropdown(options=_sw_hosts, value="Host A (port 1)", label="Source:")
    sw_dst = mo.ui.dropdown(options=_sw_hosts + ["Broadcast"], value="Host B (port 2)", label="Destination:")
    sw_send_btn = mo.ui.run_button(label="Send frame")

    mo.hstack([sw_src, sw_dst, sw_send_btn])
    return sw_dst, sw_send_btn, sw_src


@app.cell
def _(mo, sw_dst, sw_send_btn, sw_src):
    import copy

    # State stored in reactive cell — resets when notebook reloads
    # We use a mutable container captured by closure
    _state = {"table": {}, "log": []}

    # Parse port from label "Host X (port N)"
    def _port_of(label):
        return int(label.split("port ")[1].rstrip(")"))

    def _mac_of(label):
        letter = label.split(" ")[1]  # "A", "B", "C", "D"
        return f"{letter}{letter}:{letter}{letter}:{letter}{letter}:{letter}{letter}:{letter}{letter}:{letter}{letter}"

    # ── rebuild display from button clicks ──────────────────────────────────
    # marimo reactive model: every cell re-runs when its dependencies change.
    # We accumulate state via a module-level dict that persists across re-runs.
    import sys
    _MODULE = sys.modules[__name__]
    if not hasattr(_MODULE, "_sw_table"):
        _MODULE._sw_table = {}
        _MODULE._sw_log = []

    if sw_send_btn.value:
        src_label = sw_src.value
        dst_label = sw_dst.value
        src_port = _port_of(src_label)
        src_mac = _mac_of(src_label)

        # Learn source
        _MODULE._sw_table[src_mac] = src_port

        if dst_label == "Broadcast":
            dst_mac = "FF:FF:FF:FF:FF:FF"
            action = f"**Flood** (broadcast) → all ports except {src_port}"
        else:
            dst_port = _port_of(dst_label)
            dst_mac = _mac_of(dst_label)
            if dst_mac in _MODULE._sw_table:
                action = f"**Forward** → port {_MODULE._sw_table[dst_mac]} only"
            else:
                action = f"**Flood** (unknown dst) → all ports except {src_port}"

        _MODULE._sw_log.append(
            f"| `{src_mac}` (p{src_port}) → `{dst_mac}` | Learn src→p{src_port} | {action} |"
        )

    # Build table markdown
    if _MODULE._sw_table:
        _table_rows = "\n".join(
            f"| `{mac}` | {port} |"
            for mac, port in sorted(_MODULE._sw_table.items())
        )
        _table_md = f"""
**Forwarding Table:**

| MAC Address | Port |
|---|---|
{_table_rows}
"""
    else:
        _table_md = "**Forwarding Table:** *(empty — no frames sent yet)*"

    if _MODULE._sw_log:
        _log_md = "**Frame Log:**\n\n| Frame | Switch learns | Action |\n|---|---|---|\n" + "\n".join(_MODULE._sw_log)
    else:
        _log_md = "**Frame Log:** *(no frames sent yet)*"

    _reset_hint = mo.md("*Reload the notebook to reset the switch table.*")

    mo.vstack([mo.md(_table_md), mo.md(_log_md), _reset_hint])
    return (
        copy,
        mo,
        sw_dst,
        sw_send_btn,
        sw_src,
    )


# ─────────────────────────────────────────────────────────────────────────────
# Part 5: Ethernet Technology Timeline
# ─────────────────────────────────────────────────────────────────────────────

@app.cell
def _(mo):
    mo.md(r"""
    ---
    ## Part 5: Ethernet Technology Timeline

    Ethernet has scaled by roughly 10× every 5–7 years. The chart below plots speed (log scale)
    against year of IEEE standard ratification.
    """)
    return


@app.cell
def _(mpatches, plt):
    _standards = [
        # (year, speed_Mbs, label, category)
        (1980, 10,        "10BASE-5\n(Thicknet)",      "copper-bus"),
        (1985, 10,        "10BASE-2\n(Thinnet)",        "copper-bus"),
        (1990, 10,        "10BASE-T\n(UTP hub)",        "copper-utp"),
        (1995, 100,       "100BASE-TX\n(Fast Ethernet)", "copper-utp"),
        (1998, 1_000,     "1000BASE-SX\n(fiber)",        "fiber"),
        (1999, 1_000,     "1000BASE-T\n(Gigabit UTP)",   "copper-utp"),
        (2002, 10_000,    "10GBASE-SR\n(fiber)",         "fiber"),
        (2006, 10_000,    "10GBASE-T\n(UTP)",            "copper-utp"),
        (2010, 40_000,    "40GBASE-SR4\n(fiber)",        "fiber"),
        (2010, 100_000,   "100GBASE-SR4\n(fiber)",       "fiber"),
        (2016, 25_000,    "25GBASE-SR\n(fiber)",         "fiber"),
        (2017, 400_000,   "400GBASE-SR8\n(fiber)",       "fiber"),
    ]

    _colors = {
        "copper-bus": "#c0392b",
        "copper-utp": "#2980b9",
        "fiber":      "#27ae60",
    }
    _markers = {
        "copper-bus": "s",
        "copper-utp": "o",
        "fiber":      "^",
    }

    _fig, _ax = plt.subplots(figsize=(11, 5))

    for _year, _speed, _label, _cat in _standards:
        _ax.scatter(_year, _speed, color=_colors[_cat], marker=_markers[_cat],
                    s=90, zorder=5)
        _y_offset = _speed * 1.3
        _ax.annotate(_label, (_year, _speed),
                     xytext=(_year + 0.2, _y_offset),
                     fontsize=7, va="bottom",
                     arrowprops=dict(arrowstyle="-", color="gray", lw=0.5))

    _ax.set_yscale("log")
    _ax.set_xlabel("Year of IEEE ratification", fontsize=11)
    _ax.set_ylabel("Speed (Mb/s, log scale)", fontsize=11)
    _ax.set_title("Ethernet Standards: Speed vs. Year", fontsize=13)
    _ax.set_xlim(1977, 2022)
    _ax.set_ylim(5, 1_000_000)
    _ax.yaxis.set_major_formatter(
        plt.FuncFormatter(lambda v, _: f"{int(v):,}" if v < 1000 else
                          (f"{int(v/1000):,} Gb/s" if v >= 1_000_000 else
                           f"{int(v/1000)} Gb/s"))
    )
    _ax.grid(True, which="both", alpha=0.3, linestyle="--")

    # Legend
    _legend_items = [
        mpatches.Patch(color=_colors["copper-bus"], label="Coaxial bus (historical)"),
        mpatches.Patch(color=_colors["copper-utp"], label="Twisted-pair UTP (copper)"),
        mpatches.Patch(color=_colors["fiber"],      label="Fiber optic"),
    ]
    _ax.legend(handles=_legend_items, loc="upper left", fontsize=9)

    plt.tight_layout()
    _fig
    return (
        mpatches,
        plt,
    )


@app.cell
def _(mo):
    mo.md(r"""
    **Key observations:**
    - Speed has scaled by roughly **10× every 5–7 years** (log scale is approximately linear over time)
    - Coaxial bus Ethernet is historical — twisted-pair (UTP) and fiber dominate today
    - Fiber is required above ~10 Gb/s for most deployments; 400 Gb/s is found in hyperscale data centers
    - The same Ethernet **frame format** has been used across all generations
    """)
    return


if __name__ == "__main__":
    app.run()
