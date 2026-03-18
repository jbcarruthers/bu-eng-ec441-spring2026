"""
demo_ipaddress_l14.py
=====================
EC 441 – Introduction to Computer Networking
Lecture 14: IP Addressing, CIDR, and Subnetting
Boston University, Spring 2026

Standalone demos for the Python ipaddress module (stdlib – no install needed).
Run with:  python -u demo_ipaddress_l14.py

Sections
--------
1. Basic network arithmetic      – network address, broadcast, mask, host range
2. Subnetting with .subnets()    – divide a /24 into equal /26s
3. Subnet membership check       – are two hosts on the same subnet?
4. Special address classification – RFC 1918, loopback, link-local, multicast
5. Subnet info helper            – one-stop summary for any CIDR block
"""

import ipaddress

SEP = "-" * 60


# ──────────────────────────────────────────────────────────────
# 1. Basic network arithmetic
# ──────────────────────────────────────────────────────────────
print(SEP)
print("1. Basic network arithmetic")
print(SEP)

net = ipaddress.IPv4Network("192.168.10.0/24")

print(f"Network:          {net.network_address}")
print(f"Broadcast:        {net.broadcast_address}")
print(f"Subnet mask:      {net.netmask}")
print(f"Prefix length:    /{net.prefixlen}")
print(f"Total addresses:  {net.num_addresses}")

hosts = list(net.hosts())
print(f"Usable hosts:     {len(hosts)}")
print(f"First host:       {hosts[0]}")
print(f"Last host:        {hosts[-1]}")


# ──────────────────────────────────────────────────────────────
# 2. Subnetting with .subnets()
# ──────────────────────────────────────────────────────────────
print()
print(SEP)
print("2. Subnetting: divide 192.168.10.0/24 into four /26s")
print(SEP)

parent = ipaddress.IPv4Network("192.168.10.0/24")
subnets = list(parent.subnets(prefixlen_diff=2))   # borrow 2 bits → /26

for i, s in enumerate(subnets):
    h = list(s.hosts())
    print(f"  Subnet {i}: {str(s):<22}  hosts {h[0]} – {h[-1]}  ({len(h)} usable)")


# ──────────────────────────────────────────────────────────────
# 3. Subnet membership check
# ──────────────────────────────────────────────────────────────
print()
print(SEP)
print("3. Subnet membership: are two hosts on the same /26?")
print(SEP)


def same_subnet(addr_a: str, addr_b: str, prefixlen: int) -> bool:
    """Return True if addr_a and addr_b are in the same /<prefixlen> subnet."""
    net_a = ipaddress.IPv4Interface(f"{addr_a}/{prefixlen}").network
    net_b = ipaddress.IPv4Interface(f"{addr_b}/{prefixlen}").network
    return net_a == net_b


pairs = [
    ("192.168.10.75",  "192.168.10.100", 26),   # same /26
    ("192.168.10.75",  "192.168.10.130", 26),   # different /26
    ("10.0.0.1",       "10.0.0.254",     24),   # same /24
    ("10.0.0.1",       "10.0.1.1",       24),   # different /24
]

for a, b, plen in pairs:
    result = same_subnet(a, b, plen)
    verdict = "same subnet  → communicate directly" if result else "diff subnet  → must route"
    print(f"  {a} vs {b} (/{plen}): {verdict}")


# ──────────────────────────────────────────────────────────────
# 4. Special address classification
# ──────────────────────────────────────────────────────────────
print()
print(SEP)
print("4. Special address classification")
print(SEP)

addresses = [
    "10.0.0.1",       # RFC 1918
    "172.17.0.5",     # RFC 1918 (Docker's default network)
    "192.168.1.42",   # RFC 1918
    "127.0.0.1",      # loopback
    "169.254.1.1",    # link-local (APIPA)
    "224.0.0.5",      # multicast (OSPF all-routers)
    "8.8.8.8",        # Google Public DNS – public
    "1.1.1.1",        # Cloudflare DNS – public
]

print(f"  {'Address':<18} {'private':<9} {'loopback':<10} {'link_local':<12} {'multicast':<10} {'global'}")
print(f"  {'-'*18} {'-'*8} {'-'*9} {'-'*11} {'-'*9} {'-'*6}")
for s in addresses:
    a = ipaddress.IPv4Address(s)
    print(
        f"  {s:<18} {str(a.is_private):<9} {str(a.is_loopback):<10}"
        f" {str(a.is_link_local):<12} {str(a.is_multicast):<10} {a.is_global}"
    )

print()
print("  Note: is_private=True covers RFC 1918 AND other IANA special-use ranges.")
print("  Use is_global for a strict 'publicly routable' test.")


# ──────────────────────────────────────────────────────────────
# 5. Subnet info helper
# ──────────────────────────────────────────────────────────────
print()
print(SEP)
print("5. Subnet info helper – summary for any CIDR block")
print(SEP)


def subnet_info(cidr: str) -> None:
    """Print a one-stop summary for the given CIDR block."""
    net = ipaddress.IPv4Network(cidr, strict=False)
    hosts = list(net.hosts())
    print(f"  CIDR:      {net}")
    print(f"  Network:   {net.network_address}")
    print(f"  Broadcast: {net.broadcast_address}")
    print(f"  Mask:      {net.netmask}")
    print(f"  Addresses: {net.num_addresses} total, {len(hosts)} usable")
    if hosts:
        print(f"  Range:     {hosts[0]} – {hosts[-1]}")
    print()


for block in ["10.0.0.0/8", "172.16.0.0/12", "192.168.0.0/16",
              "192.168.10.0/24", "192.168.10.64/26", "10.0.0.1/30"]:
    subnet_info(block)
