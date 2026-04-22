# EC 441 - Introduction to Computer Networking

**Spring 2026**
**Boston University**
**Department of Electrical and Computer Engineering**

---

## Course Materials

This repository contains lecture notes, slides, and Python scripts for EC 441.

### Lecture 01 - Introduction to Computer Networking

**Python Scripts:**
- [lecture_01_intro.py](lecture01/lecture_01_intro.py) - Interactive introduction to networking concepts

---

### Lecture 02 - Information Theory and Networking

**Lecture Notes:**
- [lecture_02_notes.pdf](lecture02/lecture_02_notes.pdf) - Detailed notes on information theory
- [lecture_02_slides.pdf](lecture02/lecture_02_slides.pdf) - Presentation slides

**Python Scripts:**
- [lecture_02_exploration.py](lecture02/lecture_02_exploration.py) - Interactive exploration of information concepts
- [plot_entropy.py](lecture02/plot_entropy.py) - Entropy visualization tool

---

### Lecture 03 - Physical Layer: Guided Media and Digital Signaling

**Lecture Notes:**
- [lecture_03_notes.pdf](lecture03/lecture_03_notes.pdf) - Detailed notes on physical transmission media and signaling
- [lecture_03_slides.pdf](lecture03/lecture_03_slides.pdf) - Presentation slides

**Python Scripts:**
- [lecture_03_exploration.py](lecture03/lecture_03_exploration.py) - Interactive exploration of physical layer concepts

---

### Lecture 04 - Wireless Communication and Networking

**Lecture Notes:**
- [lecture_04_notes.pdf](lecture04/lecture_04_notes.pdf) - Detailed notes on wireless communication principles
- [lecture_04_slides.pdf](lecture04/lecture_04_slides.pdf) - Presentation slides

**Python Scripts:**
- [lecture_04_exploration.py](lecture04/lecture_04_exploration.py) - Interactive exploration of wireless concepts
- [plot_spectrum_allocation.py](lecture04/plot_spectrum_allocation.py) - Visualize frequency spectrum allocation
- [plot_path_loss.py](lecture04/plot_path_loss.py) - Path loss model comparisons
- [plot_link_budget.py](lecture04/plot_link_budget.py) - Link budget analysis tool
- [plot_qam_constellations.py](lecture04/plot_qam_constellations.py) - QAM modulation visualization
- [plot_cellular_reuse.py](lecture04/plot_cellular_reuse.py) - Cellular frequency reuse patterns
- [plot_wifi_rates.py](lecture04/plot_wifi_rates.py) - WiFi data rate analysis

---

### Lecture 05 - Error Control Coding

**Lecture Notes:**
- [lecture_05_notes.pdf](lecture05/lecture_05_notes.pdf) - Detailed notes on block codes, Hamming distance, and error control
- [lecture_05_slides.pdf](lecture05/lecture_05_slides.pdf) - Presentation slides

**Python Scripts:**
- [lecture_05_06_exploration.py](lecture05/lecture_05_06_exploration.py) - Interactive exploration of error control coding and CRC (covers Lectures 05 & 06)
- [plot_hamming_distance.py](lecture05/plot_hamming_distance.py) - Hamming distance and error control sphere visualization

---

### Lecture 06 - CRC and Error Detection

**Lecture Notes:**
- [lecture_06_notes.pdf](lecture06/lecture_06_notes.pdf) - Detailed notes on CRC encoding, decoding, and performance
- [lecture_06_slides.pdf](lecture06/lecture_06_slides.pdf) - Presentation slides

**Python Scripts:**
- [plot_ber_comparison.py](lecture06/plot_ber_comparison.py) - BER comparison of error control methods
- [plot_crc_performance.py](lecture06/plot_crc_performance.py) - CRC error detection capability visualization

---

### Lecture 07 - Multiple Access Protocols

**Lecture Notes:**
- [lecture_07_notes.pdf](lecture07/lecture_07_notes.pdf) - Detailed notes on MAC protocols: channel partitioning, ALOHA, CSMA/CD, and Ethernet
- [lecture_07_slides.pdf](lecture07/lecture_07_slides.pdf) - Presentation slides

**Python Scripts:**
- [lecture_07_exploration.py](lecture07/lecture_07_exploration.py) - Interactive exploration of MAC protocol concepts
- [plot_csma_collision.py](lecture07/plot_csma_collision.py) - CSMA collision space-time diagram visualization
- [plot_hidden_terminal.py](lecture07/plot_hidden_terminal.py) - Hidden terminal problem visualization

### Lecture 08 - Ethernet: Addressing, Switching, and ARP

**Lecture Notes:**
- [lecture_08_notes.pdf](lecture08/lecture_08_notes.pdf) - Detailed notes on Ethernet frame structure, MAC addressing, ARP, switching, and physical layer encoding
- [lecture_08_slides.pdf](lecture08/lecture_08_slides.pdf) - Presentation slides

**Python Scripts:**
- [lecture_08_exploration.py](lecture08/lecture_08_exploration.py) - Interactive exploration of Ethernet concepts: frame anatomy, MAC address decoding, ARP exchange simulation, switch self-learning, and technology timeline

---

## Midterm 1 Review Materials

The exam covers Lectures 1--8 (through Ethernet/802.3). Format: closed book with an instructor-provided reference sheet.

- [review_slides.pdf](midterm1/review_slides.pdf) - One-slide-per-topic summary of all exam topics
- [review_problems.pdf](midterm1/review_problems.pdf) - Practice problems covering all topics
- [review_problems_solutions.pdf](midterm1/review_problems_solutions.pdf) - Worked solutions to the practice problems
- [reference_sheet.pdf](midterm1/reference_sheet.pdf) - Instructor-provided reference sheet (provided during the exam)
- [midterm_one_exam.pdf](midterm1/midterm_one_exam.pdf) - Midterm 1 exam
- [midterm_one_solutions.pdf](midterm1/midterm_one_solutions.pdf) - Midterm 1 solutions
- [midterm_one_histogram.png](midterm1/midterm_one_histogram.png) - Midterm 1 score distribution and per-question statistics

---

## Midterm 2 Material

### Lecture 13 - The Network Layer: Forwarding and Routing

**Lecture Notes:**
- [lecture_13_notes.pdf](lecture13/lecture_13_notes.pdf) - Detailed notes on the network layer, IP addressing, forwarding tables, longest prefix match, and routing overview
- [lecture_13_slides.pdf](lecture13/lecture_13_slides.pdf) - Presentation slides

**Python Scripts:**
- [lecture_13_exploration.py](lecture13/lecture_13_exploration.py) - Interactive exploration of network layer concepts: the narrow waist of the Internet, routing table inspection, longest prefix match visualizer, traceroute explorer, and TTL countdown simulation

---

### Lecture 14 — IP Addressing, CIDR, and Subnetting

**Lecture Notes:**
- [lecture_14_slides.pdf](lecture14/lecture_14_slides.pdf) — Presentation slides
- [lecture_14_notes.pdf](lecture14/lecture_14_notes.pdf) — Detailed notes

**Python Scripts:**
- [lecture_14_exploration.py](lecture14/lecture_14_exploration.py) — Interactive Marimo notebook (run with `marimo run lecture_14_exploration.py`)
- [demo_ipaddress_l14.py](lecture14/demo_ipaddress_l14.py) — Standalone script: subnet arithmetic, membership checks, special address classification (run with `python demo_ipaddress_l14.py`)

---

### Lecture 15 — Routing: Link State and Dijkstra's Algorithm

**Lecture Notes:**
- [lecture_15_slides.pdf](lecture15/lecture_15_slides.pdf) — Presentation slides
- [lecture_15_notes.pdf](lecture15/lecture_15_notes.pdf) — Detailed notes

**Python Scripts:**
- [lecture_15_exploration.py](lecture15/lecture_15_exploration.py) — Interactive Marimo notebook: graph builder, Dijkstra step-by-step visualizer, SPT visualization, link failure simulator, OSPF cost calculator (run with `marimo run lecture_15_exploration.py`)
- [demo_dijkstra_l15.py](lecture15/demo_dijkstra_l15.py) — Standalone Dijkstra implementation with step-by-step trace, forwarding table derivation, and link-failure demo (run with `python demo_dijkstra_l15.py`)

---

### Lecture 16 — Routing: Distance Vector, Bellman-Ford, and BGP Introduction

**Lecture Notes:**
- [lecture_16_slides.pdf](lecture16/lecture_16_slides.pdf) — Presentation slides
- [lecture_16_notes.pdf](lecture16/lecture_16_notes.pdf) — Detailed notes

**Python Scripts:**
- [lecture_16_exploration.py](lecture16/lecture_16_exploration.py) — Interactive Marimo notebook: DV convergence visualizer, count-to-infinity simulator, split horizon/poisoned reverse comparison, LS vs. DV side-by-side (run with `marimo run lecture_16_exploration.py`)
- [demo_bellmanford_l16.py](lecture16/demo_bellmanford_l16.py) — Standalone distance-vector implementation with round-by-round convergence trace, count-to-infinity demo, and split horizon comparison (run with `python demo_bellmanford_l16.py`)

---

### Lecture 17 — IPv4, IPv6, NAT, and ICMP

**Lecture Notes:**
- [lecture_17_slides.pdf](lecture17/lecture_17_slides.pdf) — Presentation slides
- [lecture_17_notes.pdf](lecture17/lecture_17_notes.pdf) — Detailed notes

**Python Scripts:**
- [lecture_17_exploration.py](lecture17/lecture_17_exploration.py) — Interactive Marimo notebook: IPv4 header explorer, ICMP message type reference, fragmentation calculator, NAT translation simulator, IPv6 address tool, IPv4 vs. IPv6 comparison (run with `marimo run lecture_17_exploration.py`)
- [demo_protocols_l17.py](lecture17/demo_protocols_l17.py) — Standalone script: IPv4/IPv6 header parsing, NAT translation demo, ICMP message types (run with `python demo_protocols_l17.py`)

### Lecture 18 — Transport Layer, UDP, and Reliable Data Transfer

**Lecture Notes:**
- [lecture_18_slides.pdf](lecture18/lecture_18_slides.pdf) — Presentation slides
- [lecture_18_notes.pdf](lecture18/lecture_18_notes.pdf) — Detailed notes

**Python Scripts:**
- [lecture_18_exploration.py](lecture18/lecture_18_exploration.py) — Interactive Marimo notebook: transport layer multiplexing, UDP segment anatomy, stop-and-wait vs. pipelined throughput, sliding window visualizer (run with `marimo run lecture_18_exploration.py`)
- [demo_rdt_throughput_l18.py](lecture18/demo_rdt_throughput_l18.py) — Standalone script: RDT protocol throughput comparison, stop-and-wait vs. Go-Back-N vs. Selective Repeat (run with `python demo_rdt_throughput_l18.py`)

---

### Lecture 19 — TCP Part 1: Connections, Sequencing, and Flow Control

**Lecture Notes:**
- [lecture_19_slides.pdf](lecture19/lecture_19_slides.pdf) — Presentation slides
- [lecture_19_notes.pdf](lecture19/lecture_19_notes.pdf) — Detailed notes

**Python Scripts:**
- [lecture_19_exploration.py](lecture19/lecture_19_exploration.py) — Interactive Marimo notebook: TCP 3-way handshake, RTT estimation (EWMA/RTTVAR/RTO), sequence/ACK number mechanics, flow control and receive window (run with `marimo run lecture_19_exploration.py`)
- [demo_tcp_l19.py](lecture19/demo_tcp_l19.py) — Standalone script: TCP RTT estimator (RFC 6298), 3-way handshake ISN arithmetic, sequence/ACK number trace (run with `python demo_tcp_l19.py`)

---

### Lecture 20 — TCP Part 2: Congestion Control and the Modern Picture

**Lecture Notes:**
- [lecture_20_slides.pdf](lecture20/lecture_20_slides.pdf) — Presentation slides
- [lecture_20_notes.pdf](lecture20/lecture_20_notes.pdf) — Detailed notes

**Python Scripts:**
- [lecture_20_exploration.py](lecture20/lecture_20_exploration.py) — Interactive Marimo notebook: TCP congestion control simulator (cwnd/ssthresh trace through slow start, congestion avoidance, fast recovery, timeout), TCP throughput formula explorer (run with `marimo run lecture_20_exploration.py`)
- [demo_tcp_congestion_l20.py](lecture20/demo_tcp_congestion_l20.py) — Standalone script: TCP congestion control simulator, cwnd/ssthresh evolution through slow start, congestion avoidance, fast recovery, and timeout (run with `python demo_tcp_congestion_l20.py`)

---

## Spring 2026 Midterm 2

- [midterm_two_exam_gradescope_solutions.pdf](midterm2/midterm_two_exam_gradescope_solutions.pdf) — Worked solutions to this semester's Midterm 2 (Gradescope version)
- [midterm_two_histogram.png](midterm2/midterm_two_histogram.png) — Score distribution
- [midterm_two_per_question.png](midterm2/midterm_two_per_question.png) — Per-question statistics

---

## Midterm 2 Practice Exams

The following are practice exams from previous semesters. Topics vary somewhat year to year, but all cover the network layer and transport layer/TCP. Use these to practice problem-solving — the format is similar to this semester's exam (closed book, no calculator, 90 minutes).

**Spring 2022**

- [practice_exam_spring2022.pdf](midterm2/practice_exam_spring2022.pdf) — Spring 2022 Midterm 2
- [practice_exam_spring2022_solutions.pdf](midterm2/practice_exam_spring2022_solutions.pdf) — Solutions

**Spring 2023**

- [practice_exam_spring2023.pdf](midterm2/practice_exam_spring2023.pdf) — Spring 2023 Midterm 2
- [practice_exam_spring2023_solutions.pdf](midterm2/practice_exam_spring2023_solutions.pdf) — Solutions

**Spring 2025**

- [practice_exam_spring2025.pdf](midterm2/practice_exam_spring2025.pdf) — Spring 2025 Midterm 2
- [practice_exam_spring2025_solutions.pdf](midterm2/practice_exam_spring2025_solutions.pdf) — Solutions

> **Spring 2025 exam format (historical reference):** 90 minutes, closed book, no calculator. Teams of two allowed (different partner than Midterm 1), one double-sided page of notes per team. Four questions of 25 pts each: subnets/CIDR, routing (distance vector + link state), TCP/tshark trace analysis, and error control coding. *Note: the Spring 2025 exam included a dedicated error coding question; this semester's MT2 does not, though minimum-distance ideas arise in the context of checksums.*

---

## Post-Midterm 2: Project and Supplemental Material

> **Note:** Lectures 21 and beyond are not covered on Midterm 2.
> These materials support the course project and broaden your practical skills.

### Lecture 21 — See the Network: CLI Tools, Wireshark, and pyshark

**Lecture Notes:**
- [lecture_21_slides.pdf](lecture21/lecture_21_slides.pdf) — Presentation slides
- [lecture_21_notes.pdf](lecture21/lecture_21_notes.pdf) — Detailed notes

**Python Scripts:**
- [demo_pyshark_iterate_l21.py](lecture21/demo_pyshark_iterate_l21.py) — Load a pcap and print the highest-layer protocol and frame length for every packet (run with `python demo_pyshark_iterate_l21.py capture.pcap`)
- [demo_pyshark_inspect_l21.py](lecture21/demo_pyshark_inspect_l21.py) — Inspect a single packet: layers, source IP, TTL, transport protocol (run with `python demo_pyshark_inspect_l21.py capture.pcap`)
- [demo_pyshark_dns_l21.py](lecture21/demo_pyshark_dns_l21.py) — Extract and print all unique DNS query names from a capture (run with `python demo_pyshark_dns_l21.py capture.pcap`)
- [demo_pyshark_rtt_l21.py](lecture21/demo_pyshark_rtt_l21.py) — Plot TCP ACK RTT over time from a capture, saves `rtt_plot.png` (run with `python demo_pyshark_rtt_l21.py capture.pcap`)

---

### Lecture 22 — Touch the Network: Scapy, Mininet, and Sockets

**Lecture Notes:**
- [lecture_22_slides.pdf](lecture22/lecture_22_slides.pdf) — Presentation slides
- [lecture_22_notes.pdf](lecture22/lecture_22_notes.pdf) — Detailed notes

**Python Scripts (Scapy — raw sockets, run as `sudo python3 ...` in the ec441 VM):**
- [demo_scapy_build_l22.py](lecture22/demo_scapy_build_l22.py) — Build a packet byte-by-byte and inspect IP header defaults
- [demo_scapy_icmp_l22.py](lecture22/demo_scapy_icmp_l22.py) — Craft and send an ICMP Echo Request; inspect the reply
- [demo_scapy_syn_l22.py](lecture22/demo_scapy_syn_l22.py) — TCP SYN probe against open and closed ports on scanme.nmap.org
- [demo_scapy_traceroute_l22.py](lecture22/demo_scapy_traceroute_l22.py) — Minimal traceroute via TTL-stepped ICMP (run with an optional destination argument)
- [demo_scapy_sniff_l22.py](lecture22/demo_scapy_sniff_l22.py) — Scapy sniff mode; cross-check with pyshark

**Python Scripts (Mininet — also requires Linux + sudo):**
- [demo_mininet_bottleneck_l22.py](lecture22/demo_mininet_bottleneck_l22.py) — Two hosts across a 10 Mb/s / 20 ms / 1% loss bottleneck; iperf3 + `ss -tipm`

**Python Scripts (sockets — any Linux/macOS):**
- [demo_tcp_echo_server_l22.py](lecture22/demo_tcp_echo_server_l22.py) — Minimal TCP echo server
- [demo_tcp_echo_client_l22.py](lecture22/demo_tcp_echo_client_l22.py) — Minimal TCP echo client
- [demo_udp_echo_server_l22.py](lecture22/demo_udp_echo_server_l22.py) — Minimal UDP echo server
- [demo_udp_echo_client_l22.py](lecture22/demo_udp_echo_client_l22.py) — Minimal UDP echo client

---

### Lecture 23 — Application Layer: Design Patterns, DNS, HTTP, and QUIC

**Lecture Notes:**
- [lecture_23_slides.pdf](lecture23/lecture_23_slides.pdf) — Presentation slides
- [lecture_23_notes.pdf](lecture23/lecture_23_notes.pdf) — Detailed notes

**Demo Scripts:**
- [demo_dig_trace_l23.sh](lecture23/demo_dig_trace_l23.sh) — Walk through DNS resolution with `dig`: record types, `+trace`, reverse lookup, DoH (run with `bash demo_dig_trace_l23.sh`)
- [demo_curl_versions_l23.sh](lecture23/demo_curl_versions_l23.sh) — HTTP/1.1 vs HTTP/2 vs HTTP/3 with `curl -v` (run with `bash demo_curl_versions_l23.sh`; needs a curl with HTTP/3 support, e.g. `brew install curl`)
- [demo_http_server_l23.py](lecture23/demo_http_server_l23.py) — Trivial HTTP/1.1 server using Python's stdlib `http.server` — shows that HTTP is buildable on the socket API from L22 (run with `python3 demo_http_server_l23.py`)

---

### Lecture 24 — Cryptography and Security

**Lecture Notes:**
- [lecture_24_slides.pdf](lecture24/lecture_24_slides.pdf) — Presentation slides
- [lecture_24_notes.pdf](lecture24/lecture_24_notes.pdf) — Detailed notes

**Demo Scripts:**
- [demo_rsa_math_l24.py](lecture24/demo_rsa_math_l24.py) — Toy RSA (p=11, q=13, e=7) end-to-end: key generation, encrypt/decrypt, sign/verify — stdlib only (run with `python3 demo_rsa_math_l24.py`)
- [demo_hash_l24.py](lecture24/demo_hash_l24.py) — SHA-256 properties: fixed output size, avalanche effect, a toy commitment scheme — stdlib only (run with `python3 demo_hash_l24.py`)
- [demo_aes_gcm_l24.py](lecture24/demo_aes_gcm_l24.py) — AES-GCM authenticated encryption: round-trip, tampered ciphertext and tampered AAD both fail (requires `pip install cryptography`)
- [demo_openssl_client_l24.sh](lecture24/demo_openssl_client_l24.sh) — Inspect real TLS cert chains with `openssl s_client` (run with `bash demo_openssl_client_l24.sh [host] [port]`)

---

## Final Project

Demo day is **Thursday, April 30, 2026**. See the assignment for artifact types, format, partner / team rules, and alternate dates for seniors.

- [final_project.md](final_project.md) — Final project assignment

---

## Assignments

- [assignments.md](assignments.md) - Assignment requirements and expectations (Markdown)
- [assignments.html](assignments.html) - Assignment requirements and expectations (HTML)
- [assignments.pdf](assignments.pdf) - Assignment requirements and expectations (PDF)

*This is a draft -- feedback welcome!*

---

## Tools and Setup Guides

### Setting Up Your Environment

- [Git Setup Guide](tools/git_setup_guide.md) - Install Git and keep your course materials up-to-date
- [Marimo Setup with uv](tools/marimo_setup_guide.md) - Complete guide for installing Marimo notebooks using uv

### Linux VM (Required for L21–L22)

- [VM Setup Guide](tools/vm_setup_howto.md) - Install Multipass and provision the ec441 Ubuntu VM (macOS, Windows, Linux)
- [vm_setup_howto.pdf](tools/vm_setup_howto.pdf) - PDF version of the VM setup guide
- [ec441_setup.yaml](tools/ec441_setup.yaml) - Cloud-init provisioning script (download this before running `multipass launch`)

### Course Plan

- [end_of_semester_plan.md](end_of_semester_plan.md) - Overview of Lectures 21–25: themes, tools, and what to expect

---

## Using the Materials

### Python Scripts

All Python scripts are interactive [Marimo](https://marimo.io/) notebooks. To run them:

1. Install Marimo:
   ```bash
   pip install marimo
   ```

2. Run a notebook:
   ```bash
   marimo edit lecture_01_intro.py
   ```

3. Your browser will open with an interactive notebook interface.

---

## About This Course

EC 441 provides a comprehensive introduction to computer networking, covering fundamental concepts, protocols, and practical applications.

**Last Updated:** April 21, 2026 (MT2 solutions posted)
