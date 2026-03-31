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

**Last Updated:** March 31, 2026
