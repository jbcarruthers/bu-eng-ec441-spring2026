# EC 441 Final Project — Demo Day
## Thursday, April 30, 2026

This replaces a traditional final exam. Your goal is simple:

> **Show me and each other your mastery of computer networking — either
> generally (an integration of what we've covered) or a particular topic
> (going deep on one area).**

The format is a live demo of an *artifact* you bring on your laptop.

---

## What to produce

An **artifact** — something you can show to people standing next to your
laptop. Examples, not a closed list:

- **Slides** — a clear, well-structured walk-through of a topic. Think
  conference talk, not term paper.
- **Software** — a working piece of code: a custom protocol, a
  measurement tool, a small simulator, a Scapy-based scanner, a socket
  chat app, a BitTorrent-style file splitter. It does not need to be
  production quality; it needs to work and reflect real understanding.
- **Simulation or analysis** — a Mininet experiment that shows a
  specific behavior, a pcap analysis of an app you use, a congestion
  control visualization, a Marimo / Jupyter notebook with findings.
- **Something else** — if you have an idea that doesn't fit these
  categories but demonstrates mastery, bring it. Come talk to me if
  you're unsure whether it counts.

The bar: **you can walk someone through it in 3–5 minutes and answer
good questions about it for another 5.**

---

## Demo day format — poster session, not presentations

The classroom has **nine circular tables**. We'll run demo day like a
poster session at a conference:

- You (or you + your partner) are stationed at a table with your laptop.
- Others walk around, stop at whatever interests them, hear your demo,
  ask questions.
- **Multiple demos run simultaneously** throughout the 80-minute block
  — not sequential presentations to the whole class.
- Everyone both demos and reviews peers. You will see many of your
  classmates' projects in the same session.

You do not need a poster board. Your laptop screen is the poster.

---

## Partners and teams

Working with a partner is fine. Teams of three are also fine if you
have a reason. My expectations scale with team size — a pair should
produce something with noticeably more depth or breadth than a solo
project; a team of three more than a pair. If you want to team up,
just let me know who's on the team.

---

## Peer review

I'll design a mechanism for you to review each other's projects during
the session. Details will come out before demo day. Plan on giving
structured feedback on several peers' work, and on receiving the same.

---

## Alternate dates

Senior capstone day is **Friday May 1**. If you're a senior with a
capstone deadline around that time — or if you have any other
scheduling conflict — email me (**jbc@bu.edu**) with your constraints
and we'll arrange a private demo either earlier or later in the week.

No formal justification required. Just email.

---

## Topic ideas

A non-exhaustive starting list, organized by where it lives in the
course. You are not limited to these; come with your own if you have
one.

**Physical and link layer (L3–L9).**
- A Python simulation of a line code (Manchester, 4B5B, NRZ-I) with
  BER curves under noise.
- CSMA/CA simulator: show how collision probability and throughput
  behave vs. load and number of stations.
- WiFi performance under interference: measure and analyze.

**Network layer (L13–L17).**
- Mininet topology that exposes a specific routing behavior (convergence
  time, a BGP-style path change, NAT traversal).
- IPv4 / IPv6 / NAT comparison: run real traffic and compare.

**Transport and congestion control (L18–L20).**
- CUBIC vs BBR vs Reno under the same Mininet bottleneck — measure and
  plot.
- RTT estimator visualization: EWMA / RTTVAR / RTO under variable delay.
- A hand-rolled reliable transport on top of UDP with retransmissions
  and a sliding window.

**Tools and application layer (L21–L23).**
- Analyze a real app's traffic (Zoom, Slack, a game) with pyshark; write
  up what you found.
- HTTP/1.1 vs HTTP/2 vs HTTP/3 performance comparison on a page with
  many sub-resources.
- A socket-based chat or file-transfer app with a protocol you designed.
- A BitTorrent-style chunk-and-hash file distributor (pair / team scope).

**Security (L24).**
- Implement textbook RSA from scratch with small primes and step
  through sign / verify.
- Walk through a real TLS handshake packet by packet, naming every
  primitive.
- Build a Diffie–Hellman demo that shows the shared secret emerging
  between two scripts.

---

## Grading

Scoring considers:

- **Clarity.** Can you explain what you built and why, at a
  conversational level, to a peer?
- **Depth.** Does the artifact reflect real understanding — not just a
  pretty wrapper?
- **Craft.** Is it polished enough that the demo works and the story
  lands?
- **Peer review.** How your classmates rate and respond to your demo.

I'm not looking for production-grade software or flawless slides. I am
looking for evidence that you get it, and can help someone else get it.

---

## Quick checklist

- [ ] Build the artifact. Test that your demo works on *your* laptop
      without internet if possible — don't count on the classroom WiFi.
- [ ] Prepare a 3–5 minute walk-through you can deliver repeatedly.
- [ ] Show up Thursday April 30 with your laptop and a table-side pitch.

Email me (**jbc@bu.edu**) with questions, topic ideas you want to
sanity-check, team composition, or scheduling constraints.
