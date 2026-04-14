# End of Semester — Lecture Plan
## EC 441 Spring 2026 — Lectures 21–25

*Created: 2026-04-13*

---

## Overview

Five lectures following Midterm 2 (Thu Apr 16). No further formal assessments.
The mode shifts from content delivery to **hands-on, tools-first sessions**.
The goal is for students to leave the course able to actually operate on a
network — observing, crafting, simulating, and building — not just describe
it abstractly.

All demos in L21–L22 require Linux. A VirtualBox-based Linux VM is the standard
environment for this unit. See `notes/topic11_tools/vm_setup_howto.md` for the
installation and configuration guide.

---

## Lecture Schedule

| Lecture | Date | Theme | Directory |
|---------|------|-------|-----------|
| L21 | Tue Apr 14 | See the network | `topic11_tools/` |
| L22 | Tue Apr 21 | Touch the network | `topic11_tools/` |
| L23 | Thu Apr 23 | Application layer | `topic12_applications/` |
| L24 | Tue Apr 28 | Cryptography + security | `topic13_security/` |
| L25 | Thu Apr 30 | Project demo day | — |

---

## L21 (Tue Apr 14) — See the Network

### Theme

CLI tools first, then Python-based analysis. Students have just taken Midterm 2;
this lecture is engaging and tangible — everything connects to something they
already know. The payoff line: *Wireshark shows you one conversation; pyshark
lets you ask questions about a thousand of them.*

### Session 1 — Linux Networking CLI

- `ping` and `traceroute` / `tracepath`: ICMP in action; TTL behavior; how
  filtering affects results in the real world
- `ip addr`, `ip route`, `ip neigh`: interfaces, routing table, ARP cache —
  students have seen all these concepts; now they can touch them
- `ss -tipm`: active TCP connections with kernel-level detail (cwnd, ssthresh,
  RTT) — connects directly to L19–L20 congestion control material
- `dig` / `nslookup`: DNS queries live; recursive vs. authoritative; TTLs;
  sets up L23 application layer content
- `tcpdump`: quick CLI capture; filter syntax; writing to pcap for later
  analysis
- `iperf3`: measure throughput between two hosts; watch `ss -ti` while it runs
  to see cwnd ramp up

### Session 2 — pyshark: Programmatic Packet Analysis

- What pyshark is: a Python wrapper around tshark (Wireshark's CLI backend);
  lets you treat a capture as a dataset
- Load a pcap, iterate over packets, extract fields by layer and name
- Worked examples:
  - Extract all DNS query names from a capture
  - Plot TCP RTT estimates over time from a long-running connection
  - Identify retransmissions and compute loss rate
- Wireshark GUI in parallel: use the GUI to orient, then show the same analysis
  in Python — students see the connection between visual and programmatic
  inspection

### Python Libraries

| Library | Purpose |
|---------|---------|
| `pyshark` | Programmatic pcap / live capture analysis (tshark wrapper) |
| `matplotlib` | Plotting extracted metrics |

### Demo Requirements

- tshark installed in the Linux VM (comes with Wireshark package)
- A pcap of a TCP connection with a visible handshake, data transfer, and FIN
  (reuse the L19 HTTP/1.1 capture if available)
- iperf3 available in the VM

---

## L22 (Tue Apr 21) — Touch the Network

### Theme

Three tools, one narrative arc: craft a single packet → own the topology →
build an application. Students move from passive observer to active participant
at every layer. Socket programming is the capstone — at that point students
can both create traffic and capture and analyze it.

### Session 1 — Scapy and Mininet

**Scapy** — packet crafting and sending in Python:
- Install and basic structure: `IP()`, `TCP()`, `ICMP()`, `/` operator for
  layer stacking
- Craft and send an ICMP echo request; inspect the reply — show every field
  they learned in L17
- Craft a TCP SYN; observe the RST (no server listening); send to a real server
  and watch the handshake
- Implement a minimal traceroute in ~10 lines: loop over TTL, send ICMP, catch
  TimeExceeded replies
- Sniff mode: `sniff()` with filters — capture your own traffic in Scapy,
  cross-check against pyshark

**Mininet (Python API)**:
- What Mininet is: Linux network namespaces + virtual Ethernet pairs; a real
  kernel network stack, not a simulation
- `Mininet()` Python API: add hosts, switches, links with explicit bandwidth /
  delay / loss parameters
- Run `iperf3` between two emulated hosts across a bottleneck link; adjust loss
  rate; watch TCP back off
- Simple topology experiment: linear chain of routers; run traceroute; observe
  RTT increase with each hop

### Session 2 — Socket Programming

The interface between application code and everything below it:
- The socket API: `socket()`, `bind()`, `listen()`, `accept()`, `connect()`,
  `send()`, `recv()` — concept flow before code
- **Demo 1**: minimal TCP echo server + client in Python (~25 lines each); run
  inside Mininet; attach pyshark to capture the exchange
- **Demo 2**: UDP version — show the asymmetry (no connect, no stream, no
  guaranteed order); implement a simple request/reply protocol
- `setsockopt`: `SO_REUSEADDR`, `TCP_NODELAY` — why they exist and when you
  need them
- The full loop: write a socket app → capture with pyshark → inspect headers
  in Scapy → "you now own the full stack"

### Python Libraries

| Library | Purpose |
|---------|---------|
| `scapy` | Packet crafting, sending, sniffing |
| `mininet` | Network topology emulation (Python API) |
| `socket` | Standard library; TCP/UDP client-server |
| `pyshark` | Capture your own socket traffic and inspect it |

### Demo Requirements

- Scapy installed in the Linux VM (requires root for raw socket operations)
- Mininet installed and working in the VM (requires Linux; uses network
  namespaces)
- All demos run as root or with sudo inside the VM

---

## L23 (Thu Apr 23) — Application Layer

*Plan to be written in `notes/topic12_applications/`.*

### High-level outline

- DNS as a distributed database: resolution chain, caching, TTLs; `dig` deep
  dive (already seeded in L21)
- HTTP/1.1: request/response model, persistent connections, HOL blocking;
  frame it as "what you'd build from sockets"
- HTTP/2: multiplexing and header compression; solves application-layer HOL
  blocking but not TCP HOL blocking
- HTTP/3 / QUIC: moves to UDP; eliminates TCP HOL blocking; connects back to
  L18 (why QUIC exists) and L20 (what TCP congestion control QUIC replaces)
- Bridge to L24: plaintext HTTP is a threat model waiting to be exploited;
  HTTPS is the answer — but what is HTTPS?

---

## L24 (Tue Apr 28) — Cryptography and Security

*Plan to be written in `notes/topic13_security/`.*

### High-level outline

**Threat model first (Alice/Bob/Trudy frame)**:
- What can Trudy do? Eavesdrop, modify in transit, replay, impersonate
- Build up requirements from attacks: confidentiality → integrity →
  authentication → non-repudiation
- This frame is used throughout; students heading into a cybersecurity course
  will have the vocabulary

**Symmetric cryptography**:
- Shared secret, AES as a black box, cipher modes (ECB vs. GCM briefly)
- Key distribution problem: how do Alice and Bob agree on a key if Trudy is
  watching?

**Asymmetric cryptography**:
- Public/private key pairs — the core insight
- RSA conceptually (one-way functions, no number theory required)
- Diffie-Hellman key exchange: the elegant solution to the distribution problem

**Integrity and authentication**:
- Hash functions: SHA-256 as a one-way function; properties (collision
  resistance, preimage resistance)
- MACs (HMAC): integrity + authentication with a shared key
- Digital signatures: sign with private key, verify with public; connects
  to the impersonation threat

**PKI and certificates**:
- The trust problem: how does your browser know it's talking to the real bank?
- Certificate authorities, the chain of trust, root stores
- Brief mention of certificate pinning and recent CA compromises as motivation

**TLS as the integration**:
- TLS handshake: asymmetric crypto to agree on a session key, symmetric from
  there; certificate verification
- `openssl s_client -connect hostname:443` — see a real TLS handshake live;
  read the certificate chain

---

## L25 (Thu Apr 30) — Project Demo Day

No lecture content. Students present their projects.

Project assignment (to be issued ~Apr 17, shortly after Midterm 2): details TBD.
Suggested scope: a working networked application in Python using the socket API,
with a brief write-up of the protocol design. Possible extensions: Mininet
topology, Scapy-based analysis, or a Wireshark/pyshark measurement component.

---

## Linux VM Requirements

All L21–L22 demos require Linux. The recommended environment is a VirtualBox VM
running Ubuntu 24.04 LTS. For the full installation and tool configuration guide,
see `notes/topic11_tools/vm_setup_howto.md`.

### Tool inventory

| Tool | Category | Package / install |
|------|----------|-------------------|
| `ping`, `traceroute`, `ip`, `ss`, `dig` | CLI | `iproute2`, `iputils-ping`, `dnsutils` |
| `tcpdump` | CLI capture | `tcpdump` |
| `iperf3` | Throughput | `iperf3` |
| `nmap` | Discovery | `nmap` |
| `netcat` (`nc`) | Raw connections | `netcat-openbsd` |
| `openssl` | Crypto / TLS | `openssl` |
| Wireshark / tshark | GUI + CLI capture | `wireshark` |
| Python 3 | Scripting | `python3`, `python3-pip` |
| pyshark | Programmatic pcap | `pip install pyshark` |
| Scapy | Packet crafting | `pip install scapy` |
| Mininet | Network emulation | install from source or `pip install mininet` |
| `curl`, `wget` | HTTP clients | `curl`, `wget` |
| marimo | Notebooks (optional) | `pip install marimo` |

