import marimo

__generated_with = "0.19.4"
app = marimo.App(
    width="medium",
    app_title="EC 441 - Lecture 1: Introduction to Networking",
    layout_file="layouts/lecture_01_intro.slides.json",
    css_file="lecture_styles.css",
)


@app.cell
def _():
    import marimo as mo
    import matplotlib.pyplot as plt
    import numpy as np
    from datetime import datetime
    return mo, np, plt


@app.cell
def _(mo):
    mo.md(r"""
    # EC 441: Introduction to Computer Networking

    ## Lecture 1: About the Course. Communications. Networks. Protocols.

    **Spring 2026**
    Professor Jeff Carruthers
    Boston University
    """)
    return


@app.cell
def _():
    time_processing = 0.1 # thinking tim

    d = 8 # m 
    s = 343 # m/s

    time_prop = d/ s
    print(time_prop)

    R = 20  # bits / second
    L = [3,7,7,5, 3,7,6,7]
    time_transmission = [l/R for l in L]
    print(time_transmission)

    time_queueing = [sum(time_transmission[:i]) for i in range(9)]
    print(time_queueing)
    return


@app.cell
def _(mo):
    mo.md(r"""
    # Introductions

    - history of this course
    - survey: seniors, juniors, LEAP, other?
    - current structure of the course
    - prerequisites, books and resources
    """)
    return


@app.cell
def _(mo):
    header = mo.md(r"""
    # Interactive Exercise: Communication in This Room

    ## How many different ways can you communicate with...
    """)

    question_room = mo.md("### The people at your table?")

    answers_room = mo.accordion({
        "Click to reveal answers": mo.md("""
        - Speaking (voice)
        - Hand signals / sign language
        - Writing on paper
        - Text messages
        - Email
        - Shared document
        - Social media
        - Whiteboard
        """)
    })

    question_neighbors = mo.md("### Your neighbors (next or remote tables)?")

    answers_neighbors = mo.accordion({
        "Click to reveal answers": mo.md("""
        - All of the above, but some are harder!
        - Physical constraints matter
        """)
    })

    mo.vstack([header, question_room, answers_room, question_neighbors, answers_neighbors])
    return


@app.cell
def _(mo):
    mo.md(r"""
    - blinking
    - tapping
    - paper -- pencil paper characters "latin" heirglyphics emoji chinese words !.? end of sentence.
    - talking: voice ( vocal chords lungs brain) air  pressure waves ear neural network brain.
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    # Three Giant Systems for Human Communication

    - **The Internet**
    - **The Postal System**
    - **The Telephone Network**

    ### Question: How do these differ in their design and implementation?
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    # Boston to London: 400 Years of Communication

    How did people communicate between Boston and London in...

    - **1625**: Charlestown (no Boston yet)! But think: ships, months of travel
    - **1725**: Letters by sailing ship (6-8 weeks)
    - **1825**: Faster ships, still weeks
    - **1925**: Telegraph, radio, telephone cables
    - **1975**: Satellite communications, early internet (ARPANET)
    - **2025**: Instantaneous - fiber optics, 5G, undersea cables

    _Reference: [History of telecommunication](https://en.wikipedia.org/wiki/History_of_telecommunication)_
    """)
    return


@app.cell
def _(np, plt):
    # Visualization of communication speed evolution
    years = np.array([1625, 1725, 1825, 1925, 1975, 2025])
    # Time in hours to send a message (log scale for visualization)
    times_hours = np.array([1000, 1000, 800, 1, 0.1, 0.00001])  # approximate

    fig1, ax1 = plt.subplots(figsize=(10, 6))
    ax1.semilogy(years, times_hours, 'o-', linewidth=2, markersize=10, color='#1f77b4')
    ax1.set_xlabel('Year', fontsize=12)
    ax1.set_ylabel('Time to Send Message (hours, log scale)', fontsize=12)
    ax1.set_title('Boston to London: Communication Speed Over Time', fontsize=14, fontweight='bold')
    ax1.grid(True, alpha=0.3)
    ax1.set_xlim(1600, 2050)

    # Annotations
    _annotations = [
        (1725, 1000, 'Sailing ships'),
        (1925, 1, 'Telegraph/Radio'),
        (2025, 0.00001, 'Fiber optics\n(microseconds)')
    ]
    for _year, _time, _label in _annotations:
        ax1.annotate(_label, xy=(_year, _time), xytext=(10, 10),
                   textcoords='offset points', fontsize=9,
                   bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.3))

    plt.tight_layout()
    plt.gca()
    return


@app.cell
def _(mo):
    mo.md(r"""
    # Eight Orders of Magnitude!

    ## What other engineering systems have undergone similar transformations, and how did it change society?

    - one
    - two
    - three
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    # The Evolution of Communication Technology

    Communication methods have evolved alongside technology:

    1. **Oral history, walking** - human messengers
    2. **Tablets, paper** - persistent storage of information
    3. **Ship navigation flags** - visual signaling systems
    4. **Smoke signals** - long-distance visual communication
       _See: [Smoke signal](https://en.wikipedia.org/wiki/Smoke_signal)_
    5. **Printing press** (1440s) - mass distribution
    6. **Telegraph** (1830s-1840s) - electrical signals
    7. **Radio, telephone, television** (late 1800s-1900s)
    8. **The Internet** (1960s-present)

    _Reference: [Timeline of communication technology](https://en.wikipedia.org/wiki/Timeline_of_communication_technology)_
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    # Fundamental Communication Concepts

    When humans communicate, we use **protocols** (rules):

    - **Encoding**: How is information represented?
      - Sound waves (speech)
      - Light patterns (visual signals)
      - Electrical signals (telegraph, phone)
      - Paper symbols (writing systems)

    - **Channel**: What medium carries the signal?
      - Air (sound)
      - Wire (electrical)
      - Fiber optic cable (light)
      - Radio waves (wireless)

    - **Message boundaries**: When does a message start and stop?

    - **Acknowledgements**: "I received your message" (ACK)

    - **Collisions**: What happens when two people talk at once?
    """)
    return


@app.cell
def _(plt):
    # Simple visualization of a communication channel
    fig2, ax2 = plt.subplots(figsize=(10, 4))

    # Draw sender and receiver
    _sender_x, _receiver_x = 1, 9
    _y_pos = 0.5

    # Boxes for sender and receiver
    ax2.add_patch(plt.Rectangle((_sender_x-0.3, _y_pos-0.15), 0.6, 0.3,
                                facecolor='lightblue', edgecolor='black', linewidth=2))
    ax2.add_patch(plt.Rectangle((_receiver_x-0.3, _y_pos-0.15), 0.6, 0.3,
                                facecolor='lightgreen', edgecolor='black', linewidth=2))

    ax2.text(_sender_x, _y_pos, 'Sender', ha='center', va='center', fontweight='bold')
    ax2.text(_receiver_x, _y_pos, 'Receiver', ha='center', va='center', fontweight='bold')

    # Arrow for channel
    ax2.annotate('', xy=(_receiver_x-0.4, _y_pos), xytext=(_sender_x+0.4, _y_pos),
                arrowprops=dict(arrowstyle='->', lw=2, color='red'))
    ax2.text(5, _y_pos+0.2, 'Channel (medium)', ha='center', fontsize=11, color='red')

    # Message
    ax2.text(5, _y_pos-0.25, 'Message: "Hello!"', ha='center', fontsize=10,
            bbox=dict(boxstyle='round,pad=0.4', facecolor='yellow', alpha=0.5))

    ax2.set_xlim(0, 10)
    ax2.set_ylim(0, 1)
    ax2.axis('off')
    ax2.set_title('Basic Communication Model', fontsize=14, fontweight='bold', pad=20)

    plt.tight_layout()
    plt.gca()
    return


@app.cell
def _(mo):
    mo.md(r"""
    # Understanding the Internet: Our Model

    We'll build understanding from the ground up:

    1. **Build local area networks** (LANs)
       - How do computers in one room talk to each other?

    2. **Connect networks together** (internetworking)
       - How do we connect LANs in different buildings? Cities? Countries?

    3. **Design for scale and reliability**
       - How does it work with billions of devices?

    _Reference: [Computer network](https://en.wikipedia.org/wiki/Computer_network)_
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    # Key Networking Questions

    ## How do we establish "links"?
    - Physical cables (copper, fiber)
    - Wireless (radio, infrared, satellite)

    ## Addressing: Location or Person?
    - Should addresses identify a device's location or the device itself?
    - **Uniqueness**: How do we ensure addresses are unique?
    - **Routing**: How do we find a path to the destination?

    ## Network Topology
    - **Discovery**: How do devices find each other?
    - **Structure**: Star, bus, ring, mesh, tree?

    _Reference: [Network topology](https://en.wikipedia.org/wiki/Network_topology)_
    """)
    return


@app.cell
def _(np, plt):
    # Visualization of different network topologies
    _fig3, _axes = plt.subplots(2, 2, figsize=(10, 10))

    def _draw_node(_ax, _x, _y, _label=''):
        _circle = plt.Circle((_x, _y), 0.08, color='lightblue', ec='black', linewidth=2)
        _ax.add_patch(_circle)
        if _label:
            _ax.text(_x, _y, _label, ha='center', va='center', fontweight='bold', fontsize=9)

    def _draw_edge(_ax, _x1, _y1, _x2, _y2):
        _ax.plot([_x1, _x2], [_y1, _y2], 'k-', linewidth=2)

    # Star topology
    _ax = _axes[0, 0]
    _center = (0.5, 0.5)
    _draw_node(_ax, *_center)
    for _i, _angle in enumerate(np.linspace(0, 2*np.pi, 6, endpoint=False)):
        _x = _center[0] + 0.3 * np.cos(_angle)
        _y = _center[1] + 0.3 * np.sin(_angle)
        _draw_edge(_ax, _center[0], _center[1], _x, _y)
        _draw_node(_ax, _x, _y)
    _ax.set_title('Star Topology', fontweight='bold', fontsize=12)
    _ax.set_xlim(0, 1)
    _ax.set_ylim(0, 1)
    _ax.axis('off')
    _ax.set_aspect('equal')

    # Bus topology
    _ax = _axes[0, 1]
    _bus_y = 0.5
    for _i, _x in enumerate(np.linspace(0.2, 0.8, 5)):
        _draw_node(_ax, _x, _bus_y + (0.15 if _i % 2 == 0 else -0.15))
        _ax.plot([_x, _x], [_bus_y, _bus_y + (0.15 if _i % 2 == 0 else -0.15)], 'k-', linewidth=2)
    _ax.plot([0.1, 0.9], [_bus_y, _bus_y], 'k-', linewidth=3)
    _ax.set_title('Bus Topology', fontweight='bold', fontsize=12)
    _ax.set_xlim(0, 1)
    _ax.set_ylim(0, 1)
    _ax.axis('off')
    _ax.set_aspect('equal')

    # Ring topology
    _ax = _axes[1, 0]
    _center = (0.5, 0.5)
    _n_nodes = 6
    _positions = []
    for _i, _angle in enumerate(np.linspace(0, 2*np.pi, _n_nodes, endpoint=False)):
        _x = _center[0] + 0.3 * np.cos(_angle)
        _y = _center[1] + 0.3 * np.sin(_angle)
        _positions.append((_x, _y))
        _draw_node(_ax, _x, _y)
    for _i in range(_n_nodes):
        _x1, _y1 = _positions[_i]
        _x2, _y2 = _positions[(_i+1) % _n_nodes]
        _draw_edge(_ax, _x1, _y1, _x2, _y2)
    _ax.set_title('Ring Topology', fontweight='bold', fontsize=12)
    _ax.set_xlim(0, 1)
    _ax.set_ylim(0, 1)
    _ax.axis('off')
    _ax.set_aspect('equal')

    # Mesh topology
    _ax = _axes[1, 1]
    _positions = [(0.25, 0.75), (0.75, 0.75), (0.25, 0.25), (0.75, 0.25), (0.5, 0.9)]
    for _i in range(len(_positions)):
        for _j in range(_i+1, len(_positions)):
            _draw_edge(_ax, _positions[_i][0], _positions[_i][1],
                     _positions[_j][0], _positions[_j][1])
    for _x, _y in _positions:
        _draw_node(_ax, _x, _y)
    _ax.set_title('Mesh Topology', fontweight='bold', fontsize=12)
    _ax.set_xlim(0, 1)
    _ax.set_ylim(0, 1)
    _ax.axis('off')
    _ax.set_aspect('equal')

    plt.tight_layout()
    plt.gca()
    return


@app.cell
def _(mo):
    mo.md(r"""
    # Performance Metrics: How Good is a Network?

    We measure networks using several key metrics:

    1. **Throughput**: How much data can we send per second?
       - Measured in bits per second (b/s, kb/s, Mb/s, Gb/s)

    2. **Delay (Latency)**: How long does it take for data to arrive?
       - Measured in milliseconds (ms) or microseconds (μs)
       - Components: transmission, propagation, queueing, processing

    3. **Reliability**: How often do messages get through correctly?
       - Packet loss rate, bit error rate

    4. **Security**: Can others read or modify our messages?
       - Confidentiality, integrity, authentication

    _Reference: [Network performance](https://en.wikipedia.org/wiki/Network_performance)_
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    # Topology Evaluation

    ## How do these 4 basic topologies compare?

    - Throughput
    - Delay
    - Reliability
    - Security

    ## How do they scale for large $N$?

    - think $O(f(N))$ "big O"idea
    """)
    return


@app.cell
def _(plt):
    # Visualization of delay components
    _fig4, _ax4 = plt.subplots(figsize=(10, 5))

    _components = ['Transmission\nDelay', 'Propagation\nDelay', 'Queueing\nDelay', 'Processing\nDelay']
    _colors4 = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99']

    # Example values (in milliseconds)
    _delays = [10, 9, 5, 3]

    _left = 0
    for _i, (_component, _delay, _color) in enumerate(zip(_components, _delays, _colors4)):
        _ax4.barh(0, _delay, left=_left, height=0.5, color=_color,
                edgecolor='black', linewidth=2, label=_component)
        _ax4.text(_left + _delay/2, 0, f'{_delay}ms',
                ha='center', va='center', fontweight='bold', fontsize=10)
        _left += _delay

    _ax4.set_ylim(-0.5, 0.5)
    _ax4.set_xlim(0, sum(_delays)*1.1)
    _ax4.set_xlabel('Time (milliseconds)', fontsize=12)
    _ax4.set_title('Components of Network Delay', fontsize=14, fontweight='bold')
    _ax4.set_yticks([])
    _ax4.legend(loc='upper right', fontsize=10)
    _ax4.grid(axis='x', alpha=0.3)

    # Total delay annotation
    _total = sum(_delays)
    _ax4.annotate(f'Total: {_total}ms', xy=(_total, 0), xytext=(_total*0.9, 0.35),
                fontsize=11, fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.5', facecolor='yellow', alpha=0.7))

    plt.tight_layout()
    plt.gca()
    return


@app.cell
def _(mo):
    mo.md(r"""
    # Major Concepts of the Modern Internet

    ## Packets and Store-and-Forward
    - Data is broken into small **packets**
    - Each packet is stored temporarily at routers, then forwarded
    - Like the postal system: letters, sorting facilities, delivery

    _Reference: [Packet switching](https://en.wikipedia.org/wiki/Packet_switching)_

    ## Internetworks
    - The Internet is a "network of networks"
    - Different technologies connected together
    - Need standards for interoperability

    _Reference: [Internetworking](https://en.wikipedia.org/wiki/Internetworking)_
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    # Layers and Protocols

    Complex systems need **organization**. The Internet uses **layers**:

    | Layer | Function | Example Protocols |
    |-------|----------|-------------------|
    | **Application** | User-facing services | HTTP, DNS, SMTP |
    | **Transport** | End-to-end communication | TCP, UDP |
    | **Network** | Routing between networks | IP, ICMP |
    | **Link** | Direct link communication | Ethernet, WiFi |
    | **Physical** | Bits on wire | Cables, radio waves |

    Each layer provides services to the layer above and uses services from the layer below.

    _Reference: [OSI model](https://en.wikipedia.org/wiki/OSI_model), [Internet protocol suite](https://en.wikipedia.org/wiki/Internet_protocol_suite)_
    """)
    return


@app.cell
def _(plt):
    # Visualization of the protocol stack
    _fig5, _ax5 = plt.subplots(figsize=(8, 7))

    _layers = ['Physical', 'Link', 'Network', 'Transport', 'Application']
    _examples = ['Copper/Fiber/Radio', 'Ethernet/WiFi', 'IP', 'TCP/UDP', 'HTTP/DNS/SMTP']
    _colors5 = ['#ff6b6b', '#feca57', '#48dbfb', '#1dd1a1', '#ee5a6f']

    for _i, (_layer, _example, _color) in enumerate(zip(_layers, _examples, _colors5)):
        _y_bottom = _i
        _ax5.add_patch(plt.Rectangle((0, _y_bottom), 6, 0.8,
                                   facecolor=_color, edgecolor='black', linewidth=2))
        _ax5.text(3, _y_bottom + 0.4, f'{_layer}\n({_example})',
                ha='center', va='center', fontweight='bold', fontsize=11)

    # Add arrows showing data flow
    _ax5.annotate('', xy=(6.5, 4.5), xytext=(6.5, 0.3),
                arrowprops=dict(arrowstyle='->', lw=2, color='blue'))
    _ax5.text(7.2, 2.4, 'Data\nFlow\nDown', ha='center', fontsize=10, color='blue', fontweight='bold')

    _ax5.annotate('', xy=(7.5, 0.3), xytext=(7.5, 4.5),
                arrowprops=dict(arrowstyle='->', lw=2, color='green'))
    _ax5.text(8.2, 2.4, 'Data\nFlow\nUp', ha='center', fontsize=10, color='green', fontweight='bold')

    _ax5.set_xlim(-0.5, 9)
    _ax5.set_ylim(-0.2, 5.2)
    _ax5.axis('off')
    _ax5.set_title('Internet Protocol Stack', fontsize=14, fontweight='bold', pad=10)

    plt.tight_layout()
    plt.gca()
    return


@app.cell
def _(mo):
    mo.md(r"""
    # Internet Service Providers (ISPs) and Tiers

    The Internet has a **hierarchical structure**:

    - **Tier 1 ISPs**: Global networks, no paid transit (e.g., Level 3, AT&T)
    - **Tier 2 ISPs**: Regional networks, pay for transit to Tier 1
    - **Tier 3 ISPs**: Local networks, your home ISP

    This structure enables:
    - Scalability (billions of devices)
    - Economic viability (who pays for what?)
    - Resilience (multiple paths)

    _Reference: [Tier 1 network](https://en.wikipedia.org/wiki/Tier_1_network)_
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    # Technology and Economics: A Historical Lesson

    ## AT&T Picturephone
    - **1964**: World's Fair demonstration
    - **1970**: Commercial service launch
    - **1992**: Discontinued
    - Why did it fail? Cost, infrastructure, limited utility

    ## Zoom (2011-present)
    - **2020**: Global pandemic drives adoption
    - Why did it succeed? Cheap bandwidth, existing infrastructure, clear need

    ### Lesson: Technology alone doesn't determine success!

    _Reference: [AT&T Picturephone](https://en.wikipedia.org/wiki/Picturephone)_
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    # Organizing Principles for Complex Systems

    How do we...

    - **Understand** a complex system?
      - Abstraction, layers, modular design

    - **Design** a complex system?
      - Start simple, iterate, test components

    - **Maintain** a complex system?
      - Monitoring, logging, debugging tools

    - **Improve** a complex system?
      - Identify bottlenecks, optimize, add features

    - **Teach** a complex system?
      - Bottom-up (this course!) or top-down
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    # Our Bottom-Up Approach

    In this course, we'll build understanding layer by layer:

    1. **Physical layer**: How are bits transmitted?
    2. **Link layer**: How do directly connected devices communicate?
    3. **Network layer**: How do we route across multiple networks?
    4. **Transport layer**: How do we provide reliable end-to-end service?
    5. **Application layer**: How do we build useful services?

    At each step, we'll ask:
    - What problems need solving?
    - What are possible solutions?
    - What trade-offs exist?
    - How do real systems work?
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    # Course Structure

    - **Lectures**: Concepts, principles, and theory
    - **Labs**: Hands-on with real networking tools
      - Wireshark, ping, traceroute, Python sockets
      - Mininet for network simulation
    - **Assignments**: Problem sets and programming projects
    - **Quizzes and Exams**: Check understanding

    ### Key Tools We'll Use
    - Python (socket programming, simulations)
    - Wireshark (packet analysis)
    - Mininet (network emulation)
    - Wikipedia and open resources
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    # Next Steps

    - Review the syllabus and course schedule
    - Mark your calendars for the midterm dates
    - Set up your development environment
    - Start reading Wikipedia articles on course topics
    - First assignment will be posted soon

    ## Questions?

    ---

    ### Key Wikipedia Resources
    - [Computer network](https://en.wikipedia.org/wiki/Computer_network)
    - [Internet protocol suite](https://en.wikipedia.org/wiki/Internet_protocol_suite)
    - [OSI model](https://en.wikipedia.org/wiki/OSI_model)
    - [History of telecommunication](https://en.wikipedia.org/wiki/History_of_telecommunication)
    """)
    return


if __name__ == "__main__":
    app.run()
