
Assignments
===========

*EC 441 -- Intro to Computer Networking, Spring 2026*

## Overview

Each student will maintain a personal git repository documenting their ongoing engagement with the course material. You are encouraged and expected to use generative AI tools in this work.

Each week, your assignment is to engage with the material and produce an artifact of that engagement. Your repository should grow over the semester into a portfolio that demonstrates breadth, accuracy, and thoughtful understanding of networking concepts.

**Share your repo with me** by adding my GitHub account: **jbcarruthers**.


## What to Submit

Each artifact should be one of the following types:

- **Problem**: A homework- or exam-style problem with a worked solution
- **Lab**: A tool- or code-based exploration (e.g., using Wireshark, traceroute, Mininet, or socket programming)
- **Report**: A review, explanation, critique, or tutorial on a networking topic

Other examples of acceptable artifacts include:

- Infographic images with annotations (like a lecture slide)
- Gradescope-format problems
- Review or critique of course notes or code
- A "how-to" guide for a networking tool
- A proposed problem set with solutions


## Schedule and Deadlines

- Assignments begin the week of January 26.
- **Final deadline: May 5, 2026.**
- There are 11 available weeks. You must submit work in at least **10 of 11 weeks**. One week may be skipped without penalty.
- A gap of **8 or more days** between commits will count as a missed week. The relevant timestamp is the **commit date**.
- Push your work regularly. While commit dates are used for tracking, frequent pushes ensure you receive timely feedback.


## Breadth Requirements

Your portfolio must collectively satisfy all of the following:

1. **Topics**: Cover at least **8 different topics** from the course. The course topics are:

   - Information: sources, representation
   - Physical layer: media, propagation, signals, noise, data rates
   - Link layer: frames, error control, CRC
   - Multiple access: ALOHA, CSMA
   - Ethernet: addressing, switching, ARP
   - Wireless networks: 802.11
   - Reliable data transfer: Stop-and-Wait, sliding window (GBN, SR)
   - Network layer: forwarding, routing, IP addressing, CIDR, subnetting
   - Routing: Link State (Dijkstra), Distance Vector
   - Autonomous systems, BGP
   - IPv4, IPv6, DHCP, NAT
   - TCP: sequencing, connection management, congestion/flow control
   - Tools: ping, traceroute, Wireshark, Mininet, sockets
   - Applications: client/server, P2P
   - Web: HTTP, HTML
   - Security: cryptography, protocols

2. **Layers**: Cover all **5 network stack layers** (physical, data link, network, transport, and application).

3. **Types**: Include at least **one lab**, **one problem**, and **one report**.


## Final Project

One of your submissions will serve as your **final project**, worth double the points of a regular assignment. This should be a more substantial piece of work -- deeper analysis, a more ambitious lab, or a comprehensive report. Identify it clearly in your repository (e.g., in a `final_project/` folder or noted in your README).


## Grading

Assignments account for **40 points** of your course grade, broken down as follows:

| Component | Points |
|---|---|
| Weekly assignments (best 8 of 10, 4 pts each) | 32 |
| Final project | 8 |
| **Total** | **40** |

**Breadth penalty**: Failing to meet the breadth requirements (8 topics, all 5 layers, all 3 types) will result in a deduction of up to **10 points**.

Each weekly submission is scored **0--4** (the final project is scored **0--8**) based on:

- **Relevance**: Is it related to the course material?
- **Accuracy**: Is it factually correct?
- **Engagement**: Does it reflect thoughtful engagement with the topic, beyond surface-level prompting?


## Generative AI Usage

You are expected to use generative AI tools. Good prompts demonstrate understanding of the material -- the goal is engagement, not just output.

Include a **README** in your repository that describes your generative AI tool usage: what model(s) and platform(s) you used. This can start as "I plan to use..." and evolve into "I actually used..." as the semester progresses.


## Collaboration

You may collaborate with classmates on ideas, strategies, and approaches. However, **each student must submit their own original work**. Identical or substantially similar submissions are not acceptable.


## Acceptable Formats

**Source formats** (what you write):

- Markdown
- Python
- LaTeX
- Plain text
- Marimo or Jupyter notebooks

**Output formats** (final rendered formats):

- Documents: text, PDF, HTML
- Images: PNG
- Video: MP4

You may organize your repository however you see fit (by week, by topic, etc.). As a good practice, include alt text for images and ensure PDFs are readable.


## Example Repository Structure

Below is one possible way to organize your repo. You are free to use any structure that works for you.

```
ec441-assignments/
    README.md                  # GenAI usage, repo overview
    week01-physical-layer/
        signal_analysis.py
        signal_analysis.pdf
    week02-error-control/
        crc_problems.md
    week03-ethernet/
        wireshark_lab/
            capture.png
            report.md
    ...
    final_project/
        tcp_congestion_analysis.py
        report.pdf
```
