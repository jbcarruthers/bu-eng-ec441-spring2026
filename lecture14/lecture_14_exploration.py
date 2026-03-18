import marimo

__generated_with = "0.19.6"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import numpy as np
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    import ipaddress
    import subprocess
    import sys
    from ipwhois import IPWhois
    return IPWhois, ipaddress, mo, mpatches, np, plt, subprocess, sys


@app.cell
def _(mo):
    mo.md("""
    # Lecture 14: IP Addressing, CIDR, and Subnetting — Interactive Exploration

    **EC 441 - Introduction to Computer Networking**
    Boston University, Spring 2026

    This notebook has five interactive parts:

    1. **IPv4 Address Anatomy** — dissect any IPv4 address into bits, classify it, and visualize network vs. host portions
    2. **Subnet Calculator** — enter a CIDR block and see all derived subnet parameters
    3. **Subnetting Explorer** — split a block into equal subnets and check address membership
    4. **IPv4 Address Space Map** — a visual tour of the 256 /8 blocks and their allocations
    5. **Your Network Interfaces** — read the actual interfaces on this machine and classify their addresses
    6. **Who Owns This Block?** — live RDAP/whois lookup: find the organization behind any IP address

    Work through these in order, or jump to any section that interests you.
    """)
    return


@app.cell
def _(mo):
    mo.md("""
    ---
    ## Part 1: IPv4 Address Anatomy
    """)
    return


@app.cell
def _(mo):
    mo.md("""
    ### Dissecting a 32-bit address

    An IPv4 address is a 32-bit integer, written in **dotted-decimal** notation as four
    8-bit octets separated by dots (e.g., `192.168.1.42`).  With a **prefix length** (e.g., `/24`),
    the address splits into two parts:

    - **Network bits** (the leading `/N` bits) — shared by all addresses in the same subnet.
    - **Host bits** (the remaining `32 − N` bits) — identify a specific interface within the subnet.

    The **network address** has all host bits set to 0; the **broadcast address** has all host bits set to 1.

    Enter any IPv4 address and adjust the prefix length to explore the structure.
    """)
    return


@app.cell
def _(mo):
    ip_input = mo.ui.text(value="192.168.1.42", label="IPv4 address:")
    prefix_slider = mo.ui.slider(start=0, stop=32, step=1, value=24,
                                 label="Prefix length (/N):", show_value=True)
    mo.vstack([ip_input, prefix_slider])
    return ip_input, prefix_slider


@app.cell
def _(ip_input, ipaddress, mo, mpatches, plt, prefix_slider):
    addr_str = ip_input.value.strip()
    pfx_len = prefix_slider.value

    try:
        addr = ipaddress.IPv4Address(addr_str)
        addr_valid = True
        addr_error = None
    except ValueError as e:
        addr = None
        addr_valid = False
        addr_error = str(e)

    if not addr_valid:
        part1_display = mo.md(f"**Invalid IPv4 address**: `{addr_str}` — {addr_error}")
    else:
        # --- classification ---
        classifications = []
        if addr.is_loopback:
            classifications.append("loopback (127.0.0.0/8)")
        if addr.is_private:
            classifications.append("RFC 1918 private")
        if addr.is_link_local:
            classifications.append("link-local (169.254.0.0/16)")
        if addr.is_multicast:
            classifications.append("multicast (224.0.0.0/4)")
        if not classifications:
            classifications.append("public (globally routable)")
        class_str = ", ".join(classifications)

        # --- binary breakdown ---
        octets = list(addr.packed)
        bin_strs = [f"{o:08b}" for o in octets]

        # network / host bit split
        net_bits = pfx_len          # first pfx_len bits are network
        host_bits = 32 - pfx_len

        # Derive network and broadcast
        network = ipaddress.IPv4Network(f"{addr_str}/{pfx_len}", strict=False)
        net_addr = network.network_address
        bcast_addr = network.broadcast_address
        n_addresses = network.num_addresses
        # usable hosts: 0 and 1 hosts for /32 and /31 respectively
        if pfx_len >= 31:
            usable = n_addresses
            first_host = net_addr
            last_host = bcast_addr
        else:
            usable = n_addresses - 2
            first_host = net_addr + 1
            last_host = bcast_addr - 1

        # --- matplotlib: 32-bit block diagram ---
        plt.close('all')
        fig1, axes = plt.subplots(2, 1, figsize=(10, 3.8),
                                  gridspec_kw={'height_ratios': [1, 0.55]})

        ax_bits = axes[0]
        ax_bits.set_xlim(0, 32)
        ax_bits.set_ylim(0, 1)
        ax_bits.axis('off')

        _NET_COLOR  = "#5DADE2"   # blue  — network bits
        _HOST_COLOR = "#82E0AA"   # green — host bits
        _ADDR_COLOR = "#F39C12"   # orange — the actual address bit

        bit_str_full = "".join(bin_strs)

        for bit_pos in range(32):
            bit_val = bit_str_full[bit_pos]
            is_net = (bit_pos < net_bits)
            face = _NET_COLOR if is_net else _HOST_COLOR
            rect = plt.Rectangle((bit_pos, 0.15), 0.92, 0.7,
                                  facecolor=face, edgecolor='#555555', linewidth=0.7, zorder=2)
            ax_bits.add_patch(rect)
            ax_bits.text(bit_pos + 0.46, 0.51, bit_val,
                         ha='center', va='center', fontsize=7.5, fontweight='bold', zorder=3)

        # Octet separators and labels
        for sep_pos in [8, 16, 24]:
            ax_bits.axvline(x=sep_pos, ymin=0.05, ymax=0.95,
                            color='#333333', linewidth=2.0, zorder=4)

        octet_centers = [4, 12, 20, 28]
        for _idx, (_cx, oval, bval) in enumerate(zip(octet_centers, octets, bin_strs)):
            ax_bits.text(_cx, 1.05, f"Octet {_idx+1}: {oval}",
                         ha='center', va='bottom', fontsize=8.5, fontweight='bold')

        # Prefix boundary indicator
        if 0 < pfx_len < 32:
            ax_bits.axvline(x=pfx_len, ymin=0.0, ymax=1.1,
                            color='#E74C3C', linewidth=2.5, linestyle='--', zorder=5,
                            clip_on=False)
            ax_bits.text(pfx_len, -0.12, f"/{pfx_len}",
                         ha='center', va='top', fontsize=9, color='#E74C3C', fontweight='bold')

        ax_bits.set_title(
            f"{addr_str}  —  32-bit layout  (/{pfx_len})",
            fontsize=12, fontweight='bold', pad=4
        )

        # Legend
        legend_handles1 = [
            mpatches.Patch(facecolor=_NET_COLOR,  label=f"Network bits ({net_bits} bits)"),
            mpatches.Patch(facecolor=_HOST_COLOR, label=f"Host bits ({host_bits} bits)"),
        ]
        ax_bits.legend(handles=legend_handles1, loc='lower right',
                       fontsize=8.5, bbox_to_anchor=(1.0, -0.25), ncol=2, frameon=True)

        # Second row: summary table as text
        ax_tbl = axes[1]
        ax_tbl.axis('off')
        summary_items = [
            ("Address",        str(addr)),
            ("Prefix length",  f"/{pfx_len}"),
            ("Network",        str(net_addr)),
            ("Broadcast",      str(bcast_addr)),
            ("First host",     str(first_host)),
            ("Last host",      str(last_host)),
            ("# addresses",    f"{n_addresses:,}"),
            ("Usable hosts",   f"{max(0, usable):,}"),
            ("Class",          class_str),
        ]
        col_labels = [item[0] for item in summary_items]
        col_values = [item[1] for item in summary_items]
        tbl1 = ax_tbl.table(
            cellText=[col_values],
            colLabels=col_labels,
            cellLoc='center',
            loc='center',
        )
        tbl1.auto_set_font_size(False)
        tbl1.set_fontsize(8)
        tbl1.scale(1, 1.8)

        plt.tight_layout()

        # Binary breakdown as markdown
        bin_rows = "\n".join(
            f"| Octet {i+1} | `{oval}` | `{bval}` |"
            for i, (oval, bval) in enumerate(zip(octets, bin_strs))
        )
        bin_md = mo.md(
            f"**Binary breakdown of `{addr_str}`:**\n\n"
            f"| Octet | Decimal | Binary |\n"
            f"|-------|---------|--------|\n"
            f"{bin_rows}\n\n"
            f"**Full 32-bit string:** `{'  '.join(bin_strs)}` "
            f"(spaces mark octet boundaries)"
        )

        part1_display = mo.vstack([fig1, bin_md])

    part1_display
    return


@app.cell
def _(mo):
    mo.md("""
    ---
    ## Part 2: Subnet Calculator
    """)
    return


@app.cell
def _(mo):
    mo.md("""
    ### CIDR notation and subnet parameters

    **CIDR** (Classless Inter-Domain Routing, RFC 4632) replaced the old class-based addressing
    system.  Instead of fixed /8, /16, /24 boundaries, any prefix length from /0 to /32 is valid.

    A CIDR block is written as `address/prefix_length`, e.g., `192.168.10.0/24`.  The address is
    typically the **network address** (all host bits zero), though the calculator will correct it
    if you enter a host address.

    Key parameters:
    - **Netmask**: the prefix written as a 32-bit mask with the leading N bits set to 1
      (e.g., /24 → `255.255.255.0`)
    - **Wildcard mask**: the complement of the netmask — used in ACLs and some routing protocols
    - **Number of addresses**: 2^(32−N); number of **usable hosts** is 2^(32−N) − 2
      (subtract network address and broadcast; not applicable for /31 point-to-point and /32 host routes)

    Enter a CIDR block below.
    """)
    return


@app.cell
def _(mo):
    cidr_input = mo.ui.text(value="192.168.10.0/24", label="CIDR block (address/prefix):")
    cidr_input
    return (cidr_input,)


@app.cell
def _(cidr_input, ipaddress, mo, mpatches, plt):
    cidr_str = cidr_input.value.strip()

    try:
        net2 = ipaddress.IPv4Network(cidr_str, strict=False)
        cidr_valid = True
        cidr_error = None
    except ValueError as e:
        net2 = None
        cidr_valid = False
        cidr_error = str(e)

    if not cidr_valid:
        part2_display = mo.md(f"**Invalid CIDR block**: `{cidr_str}` — {cidr_error}")
    else:
        pfx2 = net2.prefixlen
        host_bits2 = 32 - pfx2
        n_addr2 = net2.num_addresses
        netmask2 = str(net2.netmask)
        wildcard2 = str(net2.hostmask)
        net_addr2 = net2.network_address
        bcast2 = net2.broadcast_address

        if pfx2 >= 31:
            usable2 = n_addr2
            first2 = net_addr2
            last2 = bcast2
        else:
            usable2 = n_addr2 - 2
            first2 = net_addr2 + 1
            last2 = bcast2 - 1

        # --- bar diagram of address space ---
        plt.close('all')
        fig2, ax2 = plt.subplots(figsize=(10, 2.2))
        ax2.set_xlim(0, n_addr2)
        ax2.set_ylim(0, 1)
        ax2.axis('off')

        _BAR_COLOR = "#5DADE2"
        _NET_MARK   = "#E74C3C"
        _BCAST_MARK = "#8E44AD"
        _HOST_COLOR2 = "#82E0AA"

        # Full bar
        ax2.add_patch(plt.Rectangle((0, 0.2), n_addr2, 0.6,
                                    facecolor=_BAR_COLOR, edgecolor='#333333', linewidth=1.5))

        # Network address block
        ax2.add_patch(plt.Rectangle((0, 0.2), 1, 0.6,
                                    facecolor=_NET_MARK, edgecolor='#333333', linewidth=1.0, zorder=3))
        ax2.text(0.5, 0.5, "net", ha='center', va='center',
                 fontsize=7, color='white', fontweight='bold', zorder=4)

        if n_addr2 > 1:
            # Broadcast address block
            ax2.add_patch(plt.Rectangle((n_addr2 - 1, 0.2), 1, 0.6,
                                        facecolor=_BCAST_MARK, edgecolor='#333333', linewidth=1.0, zorder=3))
            ax2.text(n_addr2 - 0.5, 0.5, "bc", ha='center', va='center',
                     fontsize=7, color='white', fontweight='bold', zorder=4)

        # Labels for key addresses
        _label_y = 0.06
        ax2.text(0.5,         _label_y, str(net_addr2), ha='center', va='top', fontsize=7.5, color=_NET_MARK)
        ax2.text(n_addr2/2,   _label_y, f"← {max(0,usable2):,} usable hosts →",
                 ha='center', va='top', fontsize=8)
        ax2.text(n_addr2-0.5, _label_y, str(bcast2),    ha='center', va='top', fontsize=7.5, color=_BCAST_MARK)

        ax2.set_title(f"Address space of {net2}  ({n_addr2:,} addresses total)",
                      fontsize=11, fontweight='bold')

        legend_h2 = [
            mpatches.Patch(facecolor=_NET_MARK,    label="Network address"),
            mpatches.Patch(facecolor=_HOST_COLOR2, label="Usable host addresses"),
            mpatches.Patch(facecolor=_BCAST_MARK,  label="Broadcast address"),
        ]
        ax2.legend(handles=legend_h2, loc='upper right', fontsize=8.5,
                   bbox_to_anchor=(1.0, 1.5), ncol=3, frameon=True)

        plt.tight_layout()

        # Summary table
        rows2 = [
            ("Network address",  str(net_addr2)),
            ("Broadcast",        str(bcast2)),
            ("Netmask",          netmask2),
            ("Wildcard mask",    wildcard2),
            ("Prefix length",    f"/{pfx2}"),
            ("Host bits",        str(host_bits2)),
            ("Total addresses",  f"{n_addr2:,}"),
            ("Usable hosts",     f"{max(0, usable2):,}"),
            ("First host",       str(first2)),
            ("Last host",        str(last2)),
        ]
        row_header = "| Parameter | Value |\n|-----------|-------|\n"
        row_body = "\n".join(f"| {k} | `{v}` |" for k, v in rows2)
        summary_md2 = mo.md("### Subnet parameters\n\n" + row_header + row_body)

        part2_display = mo.vstack([summary_md2, fig2])

    part2_display
    return


@app.cell
def _(mo):
    mo.md("""
    ---
    ## Part 3: Subnetting Explorer
    """)
    return


@app.cell
def _(mo):
    mo.md("""
    ### Dividing a block into equal subnets

    **Subnetting** means borrowing additional bits from the host portion to create smaller,
    equal-sized sub-blocks.  If you start with a /24 block and borrow 2 bits, you get
    2² = 4 subnets, each a /26.

    In general: borrowing *k* bits from a /N block produces **2^k** subnets of size **/(N+k)**.

    The visualization below shows the parent block divided into colored equal-width sub-blocks.
    The **subnet membership checker** at the bottom takes two host IP addresses and reports
    whether they land in the same subnet.
    """)
    return


@app.cell
def _(mo):
    subnet_cidr_input = mo.ui.text(value="192.168.10.0/24",
                                   label="Parent CIDR block:")
    prefix_diff_slider = mo.ui.slider(start=1, stop=4, step=1, value=2,
                                      label="Bits to borrow (k):", show_value=True)
    mo.vstack([subnet_cidr_input, prefix_diff_slider])
    return prefix_diff_slider, subnet_cidr_input


@app.cell
def _(ipaddress, mo, mpatches, plt, prefix_diff_slider, subnet_cidr_input):
    sc_str = subnet_cidr_input.value.strip()
    k = prefix_diff_slider.value

    try:
        parent_net = ipaddress.IPv4Network(sc_str, strict=False)
        sc_valid = True
        sc_error = None
    except ValueError as e:
        parent_net = None
        sc_valid = False
        sc_error = str(e)

    if not sc_valid:
        subnet_display = mo.md(f"**Invalid CIDR block**: `{sc_str}` — {sc_error}")
    elif parent_net.prefixlen + k > 32:
        subnet_display = mo.md(
            f"**Cannot borrow {k} bits** from /{parent_net.prefixlen}: "
            f"that would require a /{parent_net.prefixlen + k} prefix, which exceeds /32."
        )
    else:
        new_pfx = parent_net.prefixlen + k
        subnets = list(parent_net.subnets(prefixlen_diff=k))
        n_subnets = len(subnets)

        # Palette — cycle if needed
        PALETTE = [
            "#5DADE2", "#82E0AA", "#F39C12", "#E74C3C",
            "#AF7AC5", "#1ABC9C", "#F1948A", "#A9CCE3",
            "#A9DFBF", "#FAD7A0", "#D7BDE2", "#A2D9CE",
            "#F9E79F", "#FADBD8", "#D6EAF8", "#D5F5E3",
        ]
        colors = [PALETTE[i % len(PALETTE)] for i in range(n_subnets)]

        total_addrs = parent_net.num_addresses
        sub_size = total_addrs // n_subnets  # equal by definition

        # --- matplotlib block diagram ---
        plt.close('all')
        fig3, ax3 = plt.subplots(figsize=(10, 2.8))
        ax3.set_xlim(0, total_addrs)
        ax3.set_ylim(0, 1)
        ax3.axis('off')

        for _sn_idx, sn in enumerate(subnets):
            _sn_offset = int(sn.network_address) - int(parent_net.network_address)
            ax3.add_patch(plt.Rectangle((_sn_offset, 0.15), sub_size, 0.7,
                                        facecolor=colors[_sn_idx],
                                        edgecolor='#333333', linewidth=1.2))
            _sn_cx = _sn_offset + sub_size / 2
            label_lines = [f"/{new_pfx}", str(sn.network_address)]
            ax3.text(_sn_cx, 0.52, "\n".join(label_lines),
                     ha='center', va='center', fontsize=max(5, 8 - n_subnets // 4),
                     fontweight='bold', multialignment='center')

        ax3.set_title(
            f"{parent_net}  divided into {n_subnets} equal subnets  (/{new_pfx}, {sub_size:,} addresses each)",
            fontsize=11, fontweight='bold'
        )
        plt.tight_layout()

        # --- subnet table ---
        _tbl_header3 = "| # | Network | Broadcast | First host | Last host | Usable |\n"
        _tbl_sep3    = "|---|---------|-----------|------------|-----------|--------|\n"
        _tbl_rows3 = []
        for _sn_idx, sn in enumerate(subnets):
            if new_pfx >= 31:
                fh = str(sn.network_address)
                lh = str(sn.broadcast_address)
                uh = sn.num_addresses
            else:
                fh = str(sn.network_address + 1)
                lh = str(sn.broadcast_address - 1)
                uh = sn.num_addresses - 2
            _tbl_rows3.append(
                f"| {_sn_idx} | `{sn.network_address}/{new_pfx}` | `{sn.broadcast_address}` "
                f"| `{fh}` | `{lh}` | {uh:,} |"
            )
        subnet_table_md = mo.md(
            f"### {n_subnets} subnets of /{new_pfx} within {parent_net}\n\n"
            + _tbl_header3 + _tbl_sep3 + "\n".join(_tbl_rows3)
        )

        subnet_display = mo.vstack([fig3, subnet_table_md])

    subnet_display
    return k, parent_net, sc_valid, subnets


@app.cell
def _(mo):
    mo.md("""
    ### Subnet membership checker
    """)
    return


@app.cell
def _(mo):
    check_ip1 = mo.ui.text(value="192.168.10.5",  label="IP address A:")
    check_ip2 = mo.ui.text(value="192.168.10.200", label="IP address B:")
    mo.vstack([check_ip1, check_ip2])
    return check_ip1, check_ip2


@app.cell
def _(check_ip1, check_ip2, ipaddress, mo, parent_net, sc_valid, subnets):
    if not sc_valid:
        membership_display = mo.md("_Fix the CIDR block above first._")
    else:
        ip_a_str = check_ip1.value.strip()
        ip_b_str = check_ip2.value.strip()
        errors = []
        try:
            ip_a = ipaddress.IPv4Address(ip_a_str)
        except ValueError as e:
            ip_a = None
            errors.append(f"Address A: {e}")
        try:
            ip_b = ipaddress.IPv4Address(ip_b_str)
        except ValueError as e:
            ip_b = None
            errors.append(f"Address B: {e}")

        if errors:
            membership_display = mo.md("**Invalid address(es):**\n\n" + "\n\n".join(errors))
        else:
            def _find_subnet(ip, sn_list):
                for sn in sn_list:
                    if ip in sn:
                        return sn
                return None

            sn_a = _find_subnet(ip_a, subnets)
            sn_b = _find_subnet(ip_b, subnets)

            in_parent_a = ip_a in parent_net
            in_parent_b = ip_b in parent_net

            lines = []
            if not in_parent_a:
                lines.append(f"`{ip_a_str}` is **outside** the parent block {parent_net}.")
            else:
                lines.append(f"`{ip_a_str}` → subnet **{sn_a}**")

            if not in_parent_b:
                lines.append(f"`{ip_b_str}` is **outside** the parent block {parent_net}.")
            else:
                lines.append(f"`{ip_b_str}` → subnet **{sn_b}**")

            if in_parent_a and in_parent_b:
                if sn_a == sn_b:
                    verdict = f"**Same subnet** ({sn_a}) — these two hosts can communicate directly (same L2 segment)."
                else:
                    verdict = f"**Different subnets** ({sn_a} vs. {sn_b}) — traffic between them must pass through a router."
                lines.append(verdict)

            membership_display = mo.md("\n\n".join(lines))

    membership_display
    return


@app.cell
def _(mo):
    mo.md("""
    ---
    ## Part 4: IPv4 Address Space Map
    """)
    return


@app.cell
def _(mo):
    mo.md("""
    ### The 256 /8 blocks

    The entire IPv4 address space is 2³² ≈ 4.3 billion addresses.  Dividing it into 256
    /8 blocks (each containing 2²⁴ ≈ 16.7 million addresses) gives a convenient top-level map.

    Several of these blocks are **reserved** by IANA for special purposes and are never
    routed on the public Internet:

    | Color | Category | Blocks |
    |-------|----------|--------|
    | Blue | **RFC 1918 private** (10/8, 172.16-31, 192.168/16) | 10, 172, 192 |
    | Red | **Loopback** (127.0.0.0/8) | 127 |
    | Gold | **Link-local** (169.254.0.0/16) | 169 |
    | Purple | **Multicast** (224.0.0.0/4) | 224–239 |
    | Orange | **CGN / Shared address space** (100.64.0.0/10, RFC 6598) | 100 |
    | Dark red | **"This network"** (0.0.0.0/8) and **Documentation/TEST-NET** (192.0.2, 198.51.100, 203.0.113) | 0, 198, 203 |
    | Pink | **Reserved / future use** (240.0.0.0/4) | 240–255 |
    | Green | **Public (globally routable)** — everything else | all others |

    Note that 172 and 192 blocks are only *partially* reserved — most addresses in those /8s
    are public.  The bar chart shows the full /8 block; the reservation applies only to
    the sub-range noted above.
    """)
    return


@app.cell
def _(mpatches, plt):
    plt.close('all')
    fig4, ax4 = plt.subplots(figsize=(12, 4.5))

    # Category definitions  (block index → category string)
    def _classify_slash8(b):
        if b == 0:
            return "special"
        if b == 10:
            return "rfc1918"
        if b == 100:
            return "cgn"
        if b == 127:
            return "loopback"
        if b == 169:
            return "link_local"
        if b in (172, 192):
            return "rfc1918_partial"
        if 224 <= b <= 239:
            return "multicast"
        if 240 <= b <= 255:
            return "reserved"
        if b in (198, 203):
            return "documentation"
        return "public"

    CAT_COLORS = {
        "rfc1918":          "#5DADE2",   # blue
        "rfc1918_partial":  "#A9D6E5",   # light blue (partial)
        "loopback":         "#E74C3C",   # red
        "link_local":       "#F39C12",   # gold
        "multicast":        "#8E44AD",   # purple
        "cgn":              "#E67E22",   # orange
        "special":          "#922B21",   # dark red
        "documentation":    "#922B21",   # dark red (same)
        "reserved":         "#F1948A",   # pink
        "public":           "#82E0AA",   # green
    }

    for b in range(256):
        cat = _classify_slash8(b)
        color = CAT_COLORS[cat]
        ax4.bar(b, 1, width=1, color=color, edgecolor='none')

    # Annotation for notable blocks
    annotations = [
        (0,   "0/8"),
        (10,  "10/8\n(RFC 1918)"),
        (100, "100/8\n(CGN)"),
        (127, "127/8\n(loopback)"),
        (169, "169/8\n(link-local)"),
        (172, "172/8\n(partial\nRFC 1918)"),
        (192, "192/8\n(partial\nRFC 1918)"),
        (224, "224–239/8\n(multicast)"),
        (240, "240–255/8\n(reserved)"),
    ]
    for bx, label in annotations:
        ax4.text(bx + 0.5, 1.03, label, ha='center', va='bottom',
                 fontsize=6, rotation=90, color='#222222')

    ax4.set_xlim(0, 256)
    ax4.set_ylim(0, 1)
    ax4.set_xlabel("First octet (0–255)", fontsize=10)
    ax4.set_yticks([])
    ax4.set_title("IPv4 Address Space Map — 256 /8 Blocks", fontsize=13, fontweight='bold')
    ax4.set_xticks(range(0, 257, 16))

    legend_items4 = [
        mpatches.Patch(facecolor=CAT_COLORS["public"],          label="Public (globally routable)"),
        mpatches.Patch(facecolor=CAT_COLORS["rfc1918"],         label="RFC 1918 private (10/8)"),
        mpatches.Patch(facecolor=CAT_COLORS["rfc1918_partial"], label="RFC 1918 partial (172/8, 192/8)"),
        mpatches.Patch(facecolor=CAT_COLORS["loopback"],        label="Loopback (127/8)"),
        mpatches.Patch(facecolor=CAT_COLORS["link_local"],      label="Link-local (169/8)"),
        mpatches.Patch(facecolor=CAT_COLORS["multicast"],       label="Multicast (224–239/8)"),
        mpatches.Patch(facecolor=CAT_COLORS["cgn"],             label="CGN / Shared (100/8, RFC 6598)"),
        mpatches.Patch(facecolor=CAT_COLORS["special"],         label="Special / Documentation (0/8, 198/8, 203/8)"),
        mpatches.Patch(facecolor=CAT_COLORS["reserved"],        label="Reserved / future (240–255/8)"),
    ]
    ax4.legend(handles=legend_items4, loc='upper center',
               bbox_to_anchor=(0.5, -0.15), ncol=3, fontsize=8, frameon=True)

    plt.tight_layout()
    fig4
    return


@app.cell
def _(mo):
    mo.md("""
    ### Why so many addresses are reserved

    Of the 4.3 billion possible IPv4 addresses, only roughly **3.7 billion** are globally
    routable — about 85%.  The rest are reserved for special purposes.  This mattered
    enormously once IPv4 exhaustion became real:

    - **RFC 1918 private addresses** (`10/8`, `172.16.0.0/12`, `192.168.0.0/16`) let millions
      of home and enterprise networks reuse the same address ranges internally.  Combined with
      **NAT** (Network Address Translation), a single public IP can serve an entire household
      or corporation.  We will cover NAT in detail later.
    - **CGNAT** (`100.64.0.0/10`, RFC 6598) is a second layer of NAT used by ISPs — a carrier
      assigns RFC 6598 addresses to customers, then NATs those to a pool of public IPs.
    - **Loopback** (`127.0.0.0/8`) lets processes on the same host communicate via IP without
      touching the network.  In practice only `127.0.0.1` is used; the rest of the /8 is wasted.
    - **Link-local** (`169.254.0.0/16`, RFC 3927) is auto-assigned when DHCP fails — you may
      have seen `169.254.x.x` on a Windows machine that cannot reach a DHCP server.
    - **Multicast** (`224.0.0.0/4`) delivers one packet to many receivers without separate
      unicast copies — used by routing protocols (OSPF, RIP), mDNS, and some media streaming.
    - **Reserved** (`240.0.0.0/4`): originally "class E", never deployed.  Some proposals
      to reclaim these for unicast have not gained traction.
    """)
    return


@app.cell
def _(mo):
    mo.md("""
    ---
    ## Part 5: Your Network Interfaces
    """)
    return


@app.cell
def _(mo):
    mo.md("""
    ### What addresses does this machine have?

    Every host has at least one IP address for each active network interface.  Common interfaces:

    - **lo / lo0** — the loopback interface (`127.0.0.1`); always present, never routed
    - **eth0 / en0** — the primary wired Ethernet interface
    - **wlan0 / en1** — the primary WiFi interface
    - **docker0, virbr0, utun**** — virtual interfaces for containers, VPNs, etc.

    The command `ip addr show` (Linux) or `ifconfig -a` (macOS/BSD) lists all interfaces
    and their addresses.  Each IPv4 address is shown in CIDR form: `address/prefix_length`.

    Click the button below to read your machine's interfaces.
    """)
    return


@app.cell
def _(mo):
    iface_btn = mo.ui.run_button(label="Read Network Interfaces")
    iface_btn
    return (iface_btn,)


@app.cell
def _(iface_btn, ipaddress, mo, subprocess, sys):
    if not iface_btn.value:
        iface_display = mo.md(
            "_Click **Read Network Interfaces** above to inspect the interfaces on this machine._"
        )
    else:
        try:
            if sys.platform.startswith("linux"):
                _result = subprocess.run(
                    ["ip", "addr", "show"],
                    capture_output=True, text=True, timeout=10
                )
                platform_label = "ip addr show"
            else:
                # macOS / BSD
                _result = subprocess.run(
                    ["ifconfig", "-a"],
                    capture_output=True, text=True, timeout=10
                )
                platform_label = "ifconfig -a"

            if _result.returncode != 0 or not _result.stdout.strip():
                iface_display = mo.md(
                    f"**Command failed or returned no output.**\n\n"
                    f"stderr: `{_result.stderr.strip()}`"
                )
            else:
                raw_iface = _result.stdout

                # --- parse interfaces ---
                # We look for lines of the form:
                #   Linux:  "    inet 192.168.1.5/24 ..."  (after "N: ifname:")
                #   macOS:  "    inet 192.168.1.5 netmask 0xffffff00 ..."
                import re as _re

                iface_records = []   # list of (iface_name, ip_str, prefix_len)
                current_iface = "unknown"

                for line in raw_iface.splitlines():
                    # Detect interface name line
                    # Linux:  "2: eth0: <FLAGS> ..."
                    # macOS:  "en0: flags=..."
                    m_iface_linux = _re.match(r'^\d+:\s+([\w@.-]+):', line)
                    m_iface_macos = _re.match(r'^([\w.]+):\s+flags=', line)
                    if m_iface_linux:
                        current_iface = m_iface_linux.group(1).split('@')[0]
                    elif m_iface_macos:
                        current_iface = m_iface_macos.group(1)

                    # Linux: "    inet 192.168.1.5/24 brd ..."
                    m_linux_inet = _re.match(r'\s+inet\s+([\d.]+)/(\d+)', line)
                    if m_linux_inet:
                        iface_records.append((current_iface,
                                              m_linux_inet.group(1),
                                              int(m_linux_inet.group(2))))
                        continue

                    # macOS: "    inet 192.168.1.5 netmask 0xffffff00 ..."
                    m_macos_inet = _re.match(
                        r'\s+inet\s+([\d.]+)\s+netmask\s+(0x[0-9a-fA-F]+)', line
                    )
                    if m_macos_inet:
                        ip_str = m_macos_inet.group(1)
                        mask_hex = int(m_macos_inet.group(2), 16)
                        # count leading 1-bits in mask_hex
                        pfx = bin(mask_hex).count('1')
                        iface_records.append((current_iface, ip_str, pfx))

                # --- classify each address ---
                def _classify_ip(ip_str):
                    try:
                        a = ipaddress.IPv4Address(ip_str)
                    except ValueError:
                        return "unknown"
                    if a.is_loopback:
                        return "loopback"
                    if a.is_link_local:
                        return "link-local"
                    if a.is_private:
                        return "RFC 1918 private"
                    if a.is_multicast:
                        return "multicast"
                    return "public"

                if not iface_records:
                    iface_display = mo.md(
                        "**No IPv4 addresses found** in the command output.\n\n"
                        "```\n" + raw_iface[:800] + "\n```"
                    )
                else:
                    n_private = sum(1 for _, ip, _ in iface_records
                                    if _classify_ip(ip) in ("RFC 1918 private", "loopback", "link-local"))
                    n_public  = sum(1 for _, ip, _ in iface_records
                                    if _classify_ip(ip) == "public")

                    _tbl_header5 = "| Interface | IPv4 Address | Prefix | Category |\n"
                    _tbl_sep5    = "|-----------|-------------|--------|----------|\n"
                    _tbl_rows5   = "\n".join(
                        f"| `{iname}` | `{ip}` | `/{pfx}` | {_classify_ip(ip)} |"
                        for iname, ip, pfx in iface_records
                    )

                    _summary_line = (
                        f"**This machine has {len(iface_records)} IPv4 address(es) across "
                        f"{len(set(r[0] for r in iface_records))} interface(s): "
                        f"{n_private} private/local, {n_public} public.**"
                    )

                    iface_display = mo.vstack([
                        mo.md(f"### Network interfaces (`{platform_label}`)"),
                        mo.md(_tbl_header5 + _tbl_sep5 + _tbl_rows5),
                        mo.md(_summary_line),
                        mo.md("**Raw output:**"),
                        mo.md(f"```\n{raw_iface.strip()}\n```"),
                    ])

        except FileNotFoundError as e:
            iface_display = mo.md(
                f"**Command not found**: `{e}`.  "
                "Try running this on a Linux or macOS machine."
            )
        except subprocess.TimeoutExpired:
            iface_display = mo.md("**Timed out** reading interface information.")
        except Exception as e:
            iface_display = mo.md(f"**Unexpected error**: `{e}`")

    iface_display
    return


@app.cell
def _(mo):
    mo.md("""
    ---
    ## Summary

    In this notebook we explored five core concepts from Lecture 14:

    1. **IPv4 Address Anatomy**: A 32-bit address splits into a *network* portion (leading N bits,
       shared by all hosts on the subnet) and a *host* portion (remaining 32−N bits, unique within
       the subnet).  The prefix length determines the boundary.

    2. **Subnet Calculator**: Given a CIDR block, we can immediately derive the network address,
       broadcast address, netmask, wildcard mask, number of total addresses, and number of usable
       host addresses (total − 2 for /0–/30).

    3. **Subnetting Explorer**: Borrowing k bits from a /N block yields 2^k equal subnets of
       size /(N+k).  The subnet membership check illustrates why hosts on different subnets
       require a router to communicate.

    4. **IPv4 Address Space Map**: Of the 4.3 billion addresses, roughly 600 million are reserved
       for private use, loopback, link-local, multicast, CGN, documentation, and future use.
       NAT lets private addresses serve far more hosts than the raw count suggests.

    5. **Your Network Interfaces**: Real machines typically have a loopback address (`127.0.0.1`)
       and one or more RFC 1918 private addresses on their active interfaces.  A public IP, if
       present, is usually assigned by the ISP via DHCP.

    6. **Who Owns This Block?**: Every public IP address is registered with a Regional Internet
       Registry (RIR).  The RDAP protocol lets you query that registry in real time to find the
       organization, country, and CIDR block associated with any IP.

    ---
    **Coming up:**

    - **L15–L16** — Routing algorithms: link-state (Dijkstra / OSPF) and distance-vector (Bellman-Ford / RIP)
    - **L17** — Inter-domain routing and BGP: how the ~80,000 autonomous systems of the Internet
      exchange reachability information
    - **L18** — NAT, DHCP, and the transition to IPv6
    """)
    return


@app.cell
def _(mo):
    mo.md("""
    ---
    ## Part 6: Who Owns This Block?
    """)
    return


@app.cell
def _(mo):
    mo.md("""
    ### RDAP: the Registry Data Access Protocol

    Every public IP address is registered with one of the five Regional Internet Registries
    (ARIN, RIPE NCC, APNIC, LACNIC, AFRINIC).  The **RDAP** protocol lets you query that
    registry to find the organization, country, and prefix assigned to any IP.

    This is the modern replacement for the old `whois` command.  Under the hood,
    `ipwhois` queries IANA's RDAP bootstrap endpoint, which redirects to the correct RIR.

    Try the notable Class A holders from the slides — some answers will surprise you.
    """)
    return


@app.cell
def _(mo):
    _presets = {
        "20.0.0.0  — Microsoft": "20.0.0.0",
        "17.0.0.0  — Apple": "17.0.0.0",
        "18.0.0.0  — MIT": "18.0.0.0",
        "19.0.0.0  — Ford Motor": "19.0.0.0",
        "9.0.0.0   — IBM": "9.0.0.0",
        "3.0.0.0   — formerly GE, now Amazon": "3.0.0.0",
        "8.8.8.8   — Google Public DNS": "8.8.8.8",
        "1.1.1.1   — Cloudflare DNS": "1.1.1.1",
        "128.197.1.1 — Boston University": "128.197.1.1",
        "140.247.0.1 — Harvard University": "140.247.0.1",
    }
    whois_dropdown = mo.ui.dropdown(
        options=_presets,
        value="20.0.0.0",
        label="Choose an address:",
    )
    whois_btn = mo.ui.run_button(label="Look up")
    mo.vstack([whois_dropdown, whois_btn])
    return whois_btn, whois_dropdown


@app.cell
def _(IPWhois, mo, whois_btn, whois_dropdown):
    if not whois_btn.value:
        _result = mo.md(
            "_Select an address above and click **Look up** to query the registry._"
        )
    else:
        _ip = whois_dropdown.value
        try:
            _obj = IPWhois(_ip)
            _data = _obj.lookup_rdap(depth=1)
            _net = _data.get("network", {})

            _org     = _data.get("asn_description", "unknown")
            _country = _data.get("asn_country_code", "unknown")
            _cidr    = _net.get("cidr", _data.get("asn_cidr", "unknown"))
            _name    = _net.get("name", "unknown")
            _registry = _data.get("asn_registry", "unknown").upper()
            _start   = _net.get("start_address", "")
            _end     = _net.get("end_address", "")

            _result = mo.vstack([
                mo.md(f"### RDAP result for `{_ip}`"),
                mo.md(f"""
| Field | Value |
|---|---|
| **Organization** | {_org} |
| **Network name** | {_name} |
| **CIDR block** | `{_cidr}` |
| **Range** | `{_start}` – `{_end}` |
| **Country** | {_country} |
| **Registry** | {_registry} |
"""),
            ])
        except Exception as _e:
            _result = mo.md(
                f"**Lookup failed for `{_ip}`**: `{_e}`\n\n"
                "Private/reserved addresses cannot be looked up — try a public IP."
            )
    _result
    return


if __name__ == "__main__":
    app.run()
