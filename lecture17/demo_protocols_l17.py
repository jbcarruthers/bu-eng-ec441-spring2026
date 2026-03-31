"""
demo_protocols_l17.py
=====================
EC 441 – Introduction to Computer Networking
Lecture 17: IPv4, IPv6, NAT, and ICMP
Boston University, Spring 2026

Standalone demos exploring IPv4/IPv6 headers, ICMP, and address formats
using only the Python standard library (no install needed).
Run with:  python -u demo_protocols_l17.py

Sections
--------
1. IPv4 header parsing          – decode a raw IPv4 header byte by byte
2. ICMP message types           – map Type/Code to human-readable names
3. Fragmentation arithmetic     – compute fragment offsets for a large datagram
4. NAT translation table        – simulate port-address translation
5. IPv6 address formatting      – expansion, compression, address classification
6. IPv4 vs. IPv6 header comparison
"""

import ipaddress
import struct
import socket

SEP = "-" * 60


# ──────────────────────────────────────────────────────────────
# 1. IPv4 header parsing
# ──────────────────────────────────────────────────────────────
print(SEP)
print("1. IPv4 header parsing – decode a raw 20-byte header")
print(SEP)

# Construct a sample IPv4 header (ICMP Echo Request, TTL=64)
#   Version=4, IHL=5, DSCP=0, ECN=0, Total Length=84
#   Identification=0xABCD, Flags=DF (0x40), Fragment Offset=0
#   TTL=64, Protocol=1 (ICMP), Checksum=0x0000 (placeholder)
#   Source: 10.0.0.2, Destination: 142.250.80.46 (google.com)
sample_header = struct.pack(
    "!BBHHHBBH4s4s",
    0x45,           # Version (4) + IHL (5)
    0x00,           # DSCP (0) + ECN (0)
    84,             # Total Length
    0xABCD,         # Identification
    0x4000,         # Flags (DF) + Fragment Offset (0)
    64,             # TTL
    1,              # Protocol (ICMP)
    0x0000,         # Header Checksum (placeholder)
    socket.inet_aton("10.0.0.2"),          # Source IP
    socket.inet_aton("142.250.80.46"),     # Destination IP
)

# Parse it back
ver_ihl = sample_header[0]
version = (ver_ihl >> 4) & 0xF
ihl = ver_ihl & 0xF
header_len_bytes = ihl * 4

dscp_ecn = sample_header[1]
dscp = (dscp_ecn >> 2) & 0x3F
ecn = dscp_ecn & 0x3

total_length = struct.unpack("!H", sample_header[2:4])[0]
identification = struct.unpack("!H", sample_header[4:6])[0]

flags_offset = struct.unpack("!H", sample_header[6:8])[0]
flags = (flags_offset >> 13) & 0x7
df_flag = bool(flags & 0x2)
mf_flag = bool(flags & 0x1)
frag_offset = flags_offset & 0x1FFF

ttl = sample_header[8]
protocol = sample_header[9]
checksum = struct.unpack("!H", sample_header[10:12])[0]
src_ip = socket.inet_ntoa(sample_header[12:16])
dst_ip = socket.inet_ntoa(sample_header[16:20])

PROTOCOL_NAMES = {1: "ICMP", 6: "TCP", 17: "UDP", 89: "OSPF"}

print(f"  Version:          {version}")
print(f"  IHL:              {ihl} ({header_len_bytes} bytes)")
print(f"  DSCP:             {dscp} ({'Best Effort' if dscp == 0 else f'Class {dscp}'})")
print(f"  ECN:              {ecn}")
print(f"  Total Length:     {total_length} bytes")
print(f"  Identification:   0x{identification:04X}")
print(f"  Don't Fragment:   {df_flag}")
print(f"  More Fragments:   {mf_flag}")
print(f"  Fragment Offset:  {frag_offset} (×8 = {frag_offset * 8} bytes)")
print(f"  TTL:              {ttl}")
print(f"  Protocol:         {protocol} ({PROTOCOL_NAMES.get(protocol, 'Unknown')})")
print(f"  Header Checksum:  0x{checksum:04X}")
print(f"  Source IP:        {src_ip}")
print(f"  Destination IP:   {dst_ip}")
print(f"  Payload size:     {total_length - header_len_bytes} bytes")


# ──────────────────────────────────────────────────────────────
# 2. ICMP message types
# ──────────────────────────────────────────────────────────────
print()
print(SEP)
print("2. ICMP message types – the network layer's error reporter")
print(SEP)

ICMP_TYPES = {
    (0, 0): "Echo Reply (ping response)",
    (3, 0): "Destination Unreachable: Network",
    (3, 1): "Destination Unreachable: Host",
    (3, 3): "Destination Unreachable: Port",
    (3, 4): "Fragmentation Needed, DF Set (used by PMTUD)",
    (8, 0): "Echo Request (ping)",
    (11, 0): "Time Exceeded: TTL expired (used by traceroute)",
    (11, 1): "Time Exceeded: Fragment reassembly timeout",
}

print("  Type  Code  Meaning")
print("  ----  ----  -------")
for (t, c), name in ICMP_TYPES.items():
    print(f"  {t:4d}  {c:4d}  {name}")

print()
print("  How ping works:")
print("    1. Host sends ICMP Echo Request (Type 8) in an IP datagram (Protocol=1)")
print("    2. Destination replies with ICMP Echo Reply (Type 0)")
print("    3. Sender measures round-trip time (RTT)")
print()
print("  How traceroute works:")
print("    1. Send packet with TTL=1 → first router sends ICMP Time Exceeded (Type 11)")
print("    2. Increment TTL each round to discover each router along the path")
print("    3. Destination sends ICMP Port Unreachable (Type 3, Code 3) when reached")


# ──────────────────────────────────────────────────────────────
# 3. Fragmentation arithmetic
# ──────────────────────────────────────────────────────────────
print()
print(SEP)
print("3. Fragmentation arithmetic – splitting a large datagram")
print(SEP)


def fragment_datagram(total_size: int, header_size: int, mtu: int) -> list[dict]:
    """Compute fragments for a datagram given an MTU."""
    payload = total_size - header_size
    max_payload_per_frag = ((mtu - header_size) // 8) * 8  # must be multiple of 8
    fragments = []
    offset = 0
    while offset < payload:
        frag_payload = min(max_payload_per_frag, payload - offset)
        is_last = (offset + frag_payload >= payload)
        fragments.append({
            "fragment": len(fragments) + 1,
            "total_length": header_size + frag_payload,
            "mf_flag": 0 if is_last else 1,
            "offset_units": offset // 8,
            "offset_bytes": offset,
            "payload_range": f"bytes {offset}–{offset + frag_payload - 1}",
        })
        offset += frag_payload
    return fragments


# Example: 4000-byte datagram on Ethernet (MTU 1500)
original_size = 4000
header = 20
mtu = 1500

print(f"  Original datagram: {original_size} bytes (header={header}, payload={original_size - header})")
print(f"  Link MTU: {mtu} bytes")
print(f"  Max payload per fragment: {((mtu - header) // 8) * 8} bytes (must be multiple of 8)")
print()

frags = fragment_datagram(original_size, header, mtu)
print(f"  {'Frag':>4}  {'TotalLen':>8}  {'MF':>2}  {'Offset(×8)':>10}  {'OffsetBytes':>11}  Payload")
print(f"  {'----':>4}  {'--------':>8}  {'--':>2}  {'----------':>10}  {'-----------':>11}  -------")
for f in frags:
    print(f"  {f['fragment']:4d}  {f['total_length']:8d}  {f['mf_flag']:2d}  "
          f"{f['offset_units']:10d}  {f['offset_bytes']:11d}  {f['payload_range']}")

print()
print(f"  Total fragments: {len(frags)}")
print(f"  Total bytes on wire: {sum(f['total_length'] for f in frags)} "
      f"(original was {original_size} — overhead from extra headers: "
      f"{sum(f['total_length'] for f in frags) - original_size} bytes)")


# ──────────────────────────────────────────────────────────────
# 4. NAT translation table simulation
# ──────────────────────────────────────────────────────────────
print()
print(SEP)
print("4. NAT translation table – port-address translation (PAT)")
print(SEP)

nat_public_ip = "128.197.10.1"
nat_port_pool_start = 40001

# Simulated internal hosts
internal_hosts = [
    ("10.0.0.2", 5001, "google.com", 443),
    ("10.0.0.3", 5002, "amazon.com", 443),
    ("10.0.0.4", 5003, "youtube.com", 80),
    ("10.0.0.2", 5010, "github.com", 443),  # same host, different connection
]

print(f"  NAT Router Public IP: {nat_public_ip}")
print()

nat_table: list[dict] = []
for i, (src_ip, src_port, dst, dst_port) in enumerate(internal_hosts):
    wan_port = nat_port_pool_start + i
    nat_table.append({
        "lan": f"{src_ip}:{src_port}",
        "wan": f"{nat_public_ip}:{wan_port}",
        "destination": f"{dst}:{dst_port}",
    })

print("  NAT Translation Table:")
print(f"  {'LAN Side':<20}  {'WAN Side':<25}  {'Destination':<20}")
print(f"  {'--------':<20}  {'--------':<25}  {'-----------':<20}")
for entry in nat_table:
    print(f"  {entry['lan']:<20}  {entry['wan']:<25}  {entry['destination']:<20}")

print()
print("  Outgoing: NAT rewrites source IP:port")
print("    Before NAT:  10.0.0.2:5001 → google.com:443")
print(f"    After NAT:   {nat_public_ip}:{nat_port_pool_start} → google.com:443")
print()
print("  Incoming reply: NAT reverses the translation")
print(f"    Before NAT:  google.com:443 → {nat_public_ip}:{nat_port_pool_start}")
print("    After NAT:   google.com:443 → 10.0.0.2:5001")
print()
print("  One public IP can support ~65,000 simultaneous connections (16-bit port space)")


# ──────────────────────────────────────────────────────────────
# 5. IPv6 address formatting and classification
# ──────────────────────────────────────────────────────────────
print()
print(SEP)
print("5. IPv6 addresses – formatting, compression, and classification")
print(SEP)

ipv6_examples = [
    "2001:0db8:85a3:0000:0000:8a2e:0370:7334",
    "fe80:0000:0000:0000:1a2b:3cff:fe4d:5e6f",
    "::1",
    "ff02::1",
    "2607:f8b0:4006:080e:0000:0000:0000:200e",
    "fc00::1",
]

print(f"  {'Full Address':<42}  {'Compressed':<30}  {'Type'}")
print(f"  {'-' * 42}  {'-' * 30}  {'-' * 20}")

for addr_str in ipv6_examples:
    addr = ipaddress.IPv6Address(addr_str)
    full = addr.exploded
    compressed = addr.compressed

    if addr.is_loopback:
        addr_type = "Loopback"
    elif addr.is_link_local:
        addr_type = "Link-Local"
    elif addr.is_multicast:
        addr_type = "Multicast"
    elif addr.is_private:
        addr_type = "Unique Local"
    elif addr.is_global:
        addr_type = "Global Unicast"
    else:
        addr_type = "Other"

    print(f"  {full:<42}  {compressed:<30}  {addr_type}")

print()
print("  Compression rules:")
print("    1. Leading zeros in each group can be omitted: 0db8 → db8")
print("    2. One sequence of all-zero groups can be replaced by :: (once per address)")
print()

# IPv6 network operations
net6 = ipaddress.IPv6Network("2001:db8::/32")
print(f"  Example network:   {net6}")
print(f"  Network address:   {net6.network_address}")
print(f"  Prefix length:     /{net6.prefixlen}")
print(f"  Total addresses:   2^{128 - net6.prefixlen} = {net6.num_addresses:,}")
print()

# Every interface has at least two addresses
print("  Key difference from IPv4:")
print("    Every IPv6 interface has AT LEAST two addresses:")
print("      • Link-local (fe80::/10) — always present, auto-generated")
print("      • Global unicast (2000::/3) — if the network provides one")
print("    There is NO broadcast in IPv6 — multicast replaces it:")
print("      • ff02::1 = all nodes (replaces subnet broadcast)")
print("      • ff02::2 = all routers")


# ──────────────────────────────────────────────────────────────
# 6. IPv4 vs. IPv6 header comparison
# ──────────────────────────────────────────────────────────────
print()
print(SEP)
print("6. IPv4 vs. IPv6 header comparison")
print(SEP)

comparison = [
    ("Address size",    "32 bits (4.3B addrs)", "128 bits (3.4×10³⁸)"),
    ("Header size",     "20–60 bytes (variable)", "40 bytes (fixed)"),
    ("Header checksum", "Yes (recomputed every hop)", "REMOVED"),
    ("Fragmentation",   "In base header; routers fragment", "REMOVED; only source fragments"),
    ("Options",         "In base header (variable IHL)", "Extension headers"),
    ("TTL",             "Time to Live", "Hop Limit (renamed)"),
    ("Protocol field",  "Protocol (8 bits)", "Next Header (same + chains extensions)"),
    ("Broadcast",       "Yes (255.255.255.255)", "NO broadcast — multicast only"),
    ("Auto-config",     "DHCP required", "SLAAC (stateless)"),
]

print(f"  {'Feature':<20}  {'IPv4':<35}  {'IPv6':<35}")
print(f"  {'-' * 20}  {'-' * 35}  {'-' * 35}")
for feature, v4, v6 in comparison:
    print(f"  {feature:<20}  {v4:<35}  {v6:<35}")

print()
print("  Why remove the header checksum?")
print("    • Link-layer CRCs catch bit errors on each link")
print("    • Transport-layer checksums (TCP/UDP) catch end-to-end corruption")
print("    • IP header checksum was redundant work at every router hop")
print()
print("  Why remove in-transit fragmentation?")
print("    • Losing one fragment = losing entire datagram")
print("    • Security vulnerabilities (Ping of Death, Teardrop)")
print("    • Simplifies router fast path significantly")
print("    • Path MTU Discovery handles sizing at the source")
