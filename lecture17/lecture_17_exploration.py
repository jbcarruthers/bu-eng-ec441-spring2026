import marimo

__generated_with = "0.19.6"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import ipaddress
    import struct
    import socket
    return ipaddress, mo, socket, struct


@app.cell
def _(mo):
    mo.md("""
# Lecture 17: IPv4, IPv6, NAT, and ICMP — Interactive Exploration

**EC 441 - Introduction to Computer Networking**
Boston University, Spring 2026

This notebook has six interactive parts:

1. **IPv4 Header Explorer** — decode raw header bytes field by field
2. **ICMP Message Type Reference** — look up Type/Code meanings
3. **Fragmentation Calculator** — compute fragment offsets for a given datagram and MTU
4. **NAT Translation Simulator** — watch port-address translation in action
5. **IPv6 Address Tool** — expand, compress, and classify IPv6 addresses
6. **IPv4 vs. IPv6 Header Comparison** — side-by-side differences
""")
    return


# ============================================================
# Part 1: IPv4 Header Explorer
# ============================================================

@app.cell
def _(mo):
    mo.md("""
---
## Part 1: IPv4 Header Explorer

Enter values for an IPv4 header and see how each field maps to the 20-byte structure.
""")
    return


@app.cell
def _(mo):
    src_ip_input = mo.ui.text(value="10.0.0.2", label="Source IP:")
    dst_ip_input = mo.ui.text(value="142.250.80.46", label="Destination IP:")
    ttl_input = mo.ui.slider(1, 255, value=64, label="TTL:", show_value=True)
    protocol_input = mo.ui.dropdown(
        {"ICMP (1)": 1, "TCP (6)": 6, "UDP (17)": 17, "OSPF (89)": 89},
        value="ICMP (1)",
        label="Protocol:",
    )
    total_len_input = mo.ui.slider(20, 65535, value=84, label="Total Length (bytes):", show_value=True)
    df_input = mo.ui.checkbox(value=True, label="Don't Fragment (DF)")
    dscp_input = mo.ui.dropdown(
        {
            "Best Effort (0)": 0,
            "Expedited Forwarding (46)": 46,
            "AF11 (10)": 10,
            "AF21 (18)": 18,
            "CS5 (40)": 40,
        },
        value="Best Effort (0)",
        label="DSCP:",
    )
    mo.vstack([
        mo.hstack([src_ip_input, dst_ip_input], justify="start"),
        mo.hstack([ttl_input, protocol_input, total_len_input], justify="start"),
        mo.hstack([df_input, dscp_input], justify="start"),
    ])
    return (
        df_input, dscp_input, dst_ip_input, protocol_input,
        src_ip_input, total_len_input, ttl_input,
    )


@app.cell
def _(
    df_input, dscp_input, dst_ip_input, mo, protocol_input,
    socket, src_ip_input, struct, total_len_input, ttl_input,
):
    PROTOCOL_NAMES = {1: "ICMP", 6: "TCP", 17: "UDP", 89: "OSPF"}

    try:
        _src = socket.inet_aton(src_ip_input.value)
        _dst = socket.inet_aton(dst_ip_input.value)
    except OSError:
        mo.stop(True, mo.md("**⚠ Invalid IP address format.**"))

    _proto = protocol_input.value
    _ttl = ttl_input.value
    _total_len = total_len_input.value
    _dscp = dscp_input.value
    _df = df_input.value

    # Build the 20-byte header
    _ver_ihl = 0x45  # Version=4, IHL=5
    _dscp_ecn = (_dscp << 2) & 0xFF
    _flags_offset = (0x4000 if _df else 0x0000)
    _ident = 0xABCD

    _header = struct.pack(
        "!BBHHHBBH4s4s",
        _ver_ihl, _dscp_ecn, _total_len,
        _ident, _flags_offset,
        _ttl, _proto, 0x0000,
        _src, _dst,
    )

    # Compute checksum
    _words = struct.unpack("!10H", _header)
    _cksum = sum(_words)
    _cksum = (_cksum >> 16) + (_cksum & 0xFFFF)
    _cksum = (~_cksum) & 0xFFFF

    _header_with_cksum = _header[:10] + struct.pack("!H", _cksum) + _header[12:]

    # Display
    _hex_bytes = " ".join(f"{b:02X}" for b in _header_with_cksum)
    _hex_rows = [_hex_bytes[i:i+47] for i in range(0, len(_hex_bytes), 12*3)]

    _dscp_label = {0: "Best Effort", 46: "EF (VoIP)", 10: "AF11", 18: "AF21", 40: "CS5"}.get(_dscp, str(_dscp))

    _result = f"""
### Decoded IPv4 Header (20 bytes)

| Field | Value | Bits |
|---|---|---|
| Version | 4 | 4 |
| IHL | 5 (20 bytes) | 4 |
| DSCP | {_dscp} ({_dscp_label}) | 6 |
| ECN | 0 | 2 |
| Total Length | {_total_len} bytes | 16 |
| Identification | 0x{_ident:04X} | 16 |
| Flags | {"DF" if _df else "none"} | 3 |
| Fragment Offset | 0 | 13 |
| TTL | {_ttl} | 8 |
| Protocol | {_proto} ({PROTOCOL_NAMES.get(_proto, "?")}) | 8 |
| Header Checksum | 0x{_cksum:04X} | 16 |
| Source Address | {src_ip_input.value} | 32 |
| Destination Address | {dst_ip_input.value} | 32 |

**Raw header (hex):**
```
{chr(10).join(_hex_rows)}
```

**Payload size:** {_total_len - 20} bytes
"""

    mo.md(_result)
    return


# ============================================================
# Part 2: ICMP Message Type Reference
# ============================================================

@app.cell
def _(mo):
    mo.md("""
---
## Part 2: ICMP Message Type Reference

Select an ICMP type to see its codes and usage. These are the messages
that `ping`, `traceroute`, and routers use for diagnostics and error reporting.
""")
    return


@app.cell
def _(mo):
    icmp_type_select = mo.ui.dropdown(
        {
            "Type 0 — Echo Reply": 0,
            "Type 3 — Destination Unreachable": 3,
            "Type 8 — Echo Request": 8,
            "Type 11 — Time Exceeded": 11,
            "Type 5 — Redirect": 5,
        },
        value="Type 3 — Destination Unreachable",
        label="ICMP Type:",
    )
    icmp_type_select
    return (icmp_type_select,)


@app.cell
def _(icmp_type_select, mo):
    ICMP_TYPES = {
        0: {
            "name": "Echo Reply",
            "description": "Response to an Echo Request (ping). Contains the same identifier, sequence number, and payload as the request.",
            "used_by": "`ping` — measures round-trip time",
            "codes": {"0": "Echo Reply"},
        },
        3: {
            "name": "Destination Unreachable",
            "description": "Sent when a router or destination host cannot deliver a packet. The body contains the original IP header + first 8 bytes of the offending packet (enough to identify the transport-layer connection).",
            "used_by": "`traceroute` (Unix — Code 3 at destination), Path MTU Discovery (Code 4)",
            "codes": {
                "0": "Network Unreachable — no route to destination network",
                "1": "Host Unreachable — can reach the network but not the host",
                "3": "Port Unreachable — host reached but no process on that port",
                "4": "Fragmentation Needed, DF Set — packet too large and DF flag prevents fragmentation (used by PMTUD)",
                "13": "Communication Administratively Prohibited — firewall blocked it",
            },
        },
        8: {
            "name": "Echo Request",
            "description": "Sent by `ping`. Expects an Echo Reply (Type 0) back. Contains an identifier and sequence number for matching requests to replies.",
            "used_by": "`ping`, `tracert` (Windows variant of traceroute)",
            "codes": {"0": "Echo Request"},
        },
        11: {
            "name": "Time Exceeded",
            "description": "Sent when a router decrements TTL to 0 (Code 0) or when fragment reassembly times out (Code 1). This is the core mechanism behind `traceroute`.",
            "used_by": "`traceroute` — each hop decrements TTL, generating Time Exceeded replies that reveal router addresses",
            "codes": {
                "0": "TTL Expired in Transit — the packet's hop counter reached 0",
                "1": "Fragment Reassembly Time Exceeded — not all fragments arrived before timeout",
            },
        },
        5: {
            "name": "Redirect",
            "description": "Sent by a router to inform a host that a better first-hop router exists for a particular destination. The host should update its routing table.",
            "used_by": "Router optimization — rarely seen in modern networks (often disabled for security)",
            "codes": {
                "0": "Redirect for Network",
                "1": "Redirect for Host",
            },
        },
    }

    _info = ICMP_TYPES[icmp_type_select.value]
    _codes_table = "\n".join(
        f"| {code} | {desc} |" for code, desc in _info["codes"].items()
    )

    mo.md(f"""
### ICMP Type {icmp_type_select.value}: {_info["name"]}

{_info["description"]}

**Used by:** {_info["used_by"]}

| Code | Meaning |
|---|---|
{_codes_table}
""")
    return


# ============================================================
# Part 3: Fragmentation Calculator
# ============================================================

@app.cell
def _(mo):
    mo.md("""
---
## Part 3: Fragmentation Calculator

Enter a datagram size and link MTU to see how the datagram gets split into fragments.
Each fragment gets its own 20-byte IP header.
""")
    return


@app.cell
def _(mo):
    dgram_size_input = mo.ui.slider(100, 10000, value=4000, step=100, label="Original datagram size (bytes):", show_value=True)
    mtu_input = mo.ui.slider(200, 9000, value=1500, step=100, label="Link MTU (bytes):", show_value=True)
    mo.hstack([dgram_size_input, mtu_input], justify="start")
    return dgram_size_input, mtu_input


@app.cell
def _(dgram_size_input, mo, mtu_input):
    _dgram = dgram_size_input.value
    _mtu = mtu_input.value
    _header_size = 20
    _payload = _dgram - _header_size

    if _dgram <= _mtu:
        mo.stop(True, mo.md(f"**No fragmentation needed.** Datagram ({_dgram} bytes) fits within MTU ({_mtu} bytes)."))

    # Max payload per fragment must be multiple of 8
    _max_frag_payload = ((_mtu - _header_size) // 8) * 8

    _fragments = []
    _offset = 0
    _remaining = _payload
    _frag_num = 1
    while _remaining > 0:
        _frag_payload = min(_max_frag_payload, _remaining)
        _mf = 1 if _remaining > _frag_payload else 0
        _fragments.append({
            "num": _frag_num,
            "total_len": _frag_payload + _header_size,
            "mf": _mf,
            "offset": _offset // 8,
            "offset_bytes": _offset,
            "payload_bytes": f"Bytes {_offset}–{_offset + _frag_payload - 1}",
            "payload_size": _frag_payload,
        })
        _offset += _frag_payload
        _remaining -= _frag_payload
        _frag_num += 1

    _table = "\n".join(
        f"| {f['num']} | {f['total_len']} | {f['mf']} | {f['offset']} (= {f['offset_bytes']}/8) | {f['payload_size']} | {f['payload_bytes']} |"
        for f in _fragments
    )

    _total_overhead = sum(20 for _ in _fragments) - 20  # extra headers beyond the original
    _total_bytes = sum(f["total_len"] for f in _fragments)

    mo.md(f"""
### Fragmentation Result

**Original datagram:** {_dgram} bytes ({_header_size}-byte header + {_payload}-byte payload)
**Link MTU:** {_mtu} bytes → max fragment payload = {_max_frag_payload} bytes (must be multiple of 8)

| Fragment | Total Length | MF | Fragment Offset | Payload Size | Payload Range |
|---|---|---|---|---|---|
{_table}

**Summary:**
- {len(_fragments)} fragments created
- Total bytes on the wire: {_total_bytes} (overhead: +{_total_overhead} bytes from extra headers)
- If **any one** fragment is lost, the entire datagram is lost
""")
    return


# ============================================================
# Part 4: NAT Translation Simulator
# ============================================================

@app.cell
def _(mo):
    mo.md("""
---
## Part 4: NAT Translation Simulator

Simulate a home router performing Port Address Translation (PAT).
Add connections from internal hosts and watch the NAT table build up.
""")
    return


@app.cell
def _(mo):
    nat_public_ip = mo.ui.text(value="128.197.10.1", label="NAT Router Public IP:")
    nat_connections = mo.ui.text_area(
        value="10.0.0.2:5001 → 142.250.80.46:443\n10.0.0.3:5002 → 93.184.216.34:80\n10.0.0.2:5003 → 93.184.216.34:80\n10.0.0.4:5004 → 142.250.80.46:443",
        label="Connections (internal_ip:port → dest_ip:port):",
        rows=6,
    )
    mo.vstack([nat_public_ip, nat_connections])
    return nat_connections, nat_public_ip


@app.cell
def _(mo, nat_connections, nat_public_ip):
    _pub_ip = nat_public_ip.value
    _next_wan_port = 40001

    _entries = []
    for _line in nat_connections.value.strip().split("\n"):
        _line = _line.strip()
        if not _line:
            continue
        try:
            _parts = _line.replace("→", "->").split("->")
            _lan_side = _parts[0].strip()
            _dest_side = _parts[1].strip()
            _lan_ip, _lan_port = _lan_side.rsplit(":", 1)
            _dest_ip, _dest_port = _dest_side.rsplit(":", 1)
            _entries.append({
                "lan_ip": _lan_ip,
                "lan_port": _lan_port,
                "wan_port": _next_wan_port,
                "dest_ip": _dest_ip,
                "dest_port": _dest_port,
            })
            _next_wan_port += 1
        except (ValueError, IndexError):
            continue

    if not _entries:
        mo.stop(True, mo.md("**No valid connections parsed.**"))

    _nat_table = "\n".join(
        f"| {_pub_ip}:{e['wan_port']} | {e['lan_ip']}:{e['lan_port']} | {e['dest_ip']}:{e['dest_port']} |"
        for e in _entries
    )

    _outgoing = "\n".join(
        f"| {e['lan_ip']}:{e['lan_port']} → {e['dest_ip']}:{e['dest_port']} | Src: {e['lan_ip']}:{e['lan_port']} → **{_pub_ip}:{e['wan_port']}** |"
        for e in _entries
    )

    mo.md(f"""
### NAT Translation Table

| WAN Side (Public) | LAN Side (Private) | Destination |
|---|---|---|
{_nat_table}

### What the NAT Router Rewrites

| Original Connection | Address Rewrite (outgoing) |
|---|---|
{_outgoing}

**Key observations:**
- All {len(_entries)} connections share the single public IP **{_pub_ip}**
- The destination sees different source ports ({', '.join(str(e['wan_port']) for e in _entries)}) — it cannot tell that multiple internal hosts are involved
- Two hosts ({_entries[0]['lan_ip']} and {_entries[2]['lan_ip'] if len(_entries) > 2 else '...'}) can connect to the **same** destination simultaneously — the NAT disambiguates by port
- Max simultaneous connections ≈ 65,535 (limited by 16-bit port space)
""")
    return


# ============================================================
# Part 5: IPv6 Address Tool
# ============================================================

@app.cell
def _(mo):
    mo.md("""
---
## Part 5: IPv6 Address Tool

Enter an IPv6 address in any valid format. The tool will expand it, compress it,
and classify its type.
""")
    return


@app.cell
def _(mo):
    ipv6_input = mo.ui.text(
        value="2001:0db8:85a3:0000:0000:8a2e:0370:7334",
        label="IPv6 Address:",
        full_width=True,
    )
    ipv6_input
    return (ipv6_input,)


@app.cell
def _(ipaddress, ipv6_input, mo):
    try:
        _addr = ipaddress.IPv6Address(ipv6_input.value.strip())
    except ipaddress.AddressValueError:
        mo.stop(True, mo.md("**⚠ Invalid IPv6 address format.** Enter a valid IPv6 address."))

    _expanded = _addr.exploded
    _compressed = _addr.compressed
    _binary = bin(int(_addr))[2:].zfill(128)
    _binary_groups = ":".join(_binary[i:i+16] for i in range(0, 128, 16))

    # Classify address type
    if _addr.is_loopback:
        _addr_type = "Loopback (::1)"
        _scope = "Host"
    elif _addr.is_link_local:
        _addr_type = "Link-Local (fe80::/10)"
        _scope = "Single link"
    elif _addr.is_site_local:
        _addr_type = "Site-Local (deprecated)"
        _scope = "Organization"
    elif _addr.is_private:
        _addr_type = "Unique Local (fc00::/7)"
        _scope = "Organization"
    elif _addr.is_multicast:
        _addr_type = "Multicast (ff00::/8)"
        _scope = "Varies"
    elif _addr.is_global:
        _addr_type = "Global Unicast (2000::/3)"
        _scope = "Internet"
    elif _addr.is_unspecified:
        _addr_type = "Unspecified (::)"
        _scope = "N/A"
    elif _addr.is_reserved:
        _addr_type = "Reserved"
        _scope = "N/A"
    else:
        _addr_type = "Other"
        _scope = "Unknown"

    # Network/host split at /64 boundary
    _network_part = _expanded[:19]  # first 4 groups = 64 bits
    _host_part = _expanded[20:]     # last 4 groups = 64 bits

    mo.md(f"""
### IPv6 Address Analysis

| Property | Value |
|---|---|
| **Input** | `{ipv6_input.value.strip()}` |
| **Expanded** | `{_expanded}` |
| **Compressed** | `{_compressed}` |
| **Address Type** | {_addr_type} |
| **Scope** | {_scope} |
| **Network prefix (/64)** | `{_network_part}` |
| **Host portion** | `{_host_part}` |

**Try these examples:**
- `::1` — loopback
- `fe80::1a2b:3c4d:5e6f:7890` — link-local
- `2001:db8::1` — documentation prefix (like 192.0.2.x for IPv4)
- `ff02::1` — all-nodes multicast (replaces IPv4 broadcast)
- `2607:f8b0:4004:800::200e` — Google's IPv6 address
""")
    return


# ============================================================
# Part 6: IPv4 vs. IPv6 Header Comparison
# ============================================================

@app.cell
def _(mo):
    mo.md("""
---
## Part 6: IPv4 vs. IPv6 Header Comparison

Side-by-side comparison showing what changed, what was removed, and why.
""")
    return


@app.cell
def _(mo):
    mo.md("""
| Feature | IPv4 | IPv6 | Why it changed |
|---|---|---|---|
| **Address size** | 32 bits (4.3 billion) | 128 bits (3.4 × 10³⁸) | IPv4 exhaustion |
| **Header size** | 20–60 bytes (variable) | 40 bytes (fixed) | Fixed size → faster router processing |
| **Header checksum** | ✅ Recomputed every hop | ❌ Removed | Redundant — link-layer and transport-layer checksums suffice |
| **Fragmentation** | Any router can fragment | ❌ Only endpoints fragment | Router simplicity; PMTUD is preferred |
| **IHL field** | Needed (variable header) | ❌ Removed | Header is always 40 bytes |
| **Options** | In base header | Extension headers | Cleaner separation; routers skip what they don't need |
| **TTL** | Time to Live | Hop Limit (renamed) | Was always a hop counter, never a timer |
| **Protocol** | Upper-layer ID | Next Header | Same idea, but also chains extension headers |
| **Broadcast** | ✅ Yes | ❌ No broadcast | Multicast only — more efficient, no "broadcast storms" |
| **NAT required?** | Effectively yes | No — enough addresses for all devices | Every device gets a global address |
| **Auto-config** | DHCP only | SLAAC + optional DHCPv6 | Hosts can self-configure without a server |

### What IPv6 Removed from IPv4

The IPv6 header is *simpler* despite being larger (40 vs. 20 bytes minimum) because
the address fields are 4× wider. The fixed header has only **8 fields** (vs. IPv4's 14):

**Removed fields:** IHL, Identification, Flags, Fragment Offset, Header Checksum, Options/Padding

**Rationale:** Every removed field either slowed down routers (checksum recomputation),
added complexity (variable header length), or was rarely needed in the common case (fragmentation, options).
""")
    return


@app.cell
def _(mo):
    mo.md("""
---
*EC 441 — Introduction to Computer Networking, Boston University, Spring 2026*
""")
    return


if __name__ == "__main__":
    app.run()
