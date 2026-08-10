# Computer Networks — Internship Assignments

**Name:** Parinita Devi
**Roll No.:** CS-BTC25-39
**Internship:** ISEA Phase III, Tezpur University

This repository contains a series of socket programming assignments completed during the ISEA Phase III internship at Tezpur University. Each assignment builds progressively on core networking concepts — from basic UDP communication to a full-fledged GUI-based TCP chat application.

---

## Repository Structure

| # | Assignment | Folder | Description |
|---|------------|--------|--------------|
| A1 | Reliable UDP | [`CS-BTC25-39_PARINITA_DEVI_UDP_ASSIGNMENT`](./CS-BTC25-39_PARINITA_DEVI_UDP_ASSIGNMENT) | Implementation of a reliable data transfer mechanism over UDP, incorporating acknowledgments and retransmission to compensate for UDP's connectionless, unreliable nature. |
| A2 | TCP Connection | [`CS-BTC25-39_PARINITA_DEVI_TCP_ASSIGNMENT`](./CS-BTC25-39_PARINITA_DEVI_TCP_ASSIGNMENT) | Basic client-server communication using TCP sockets, demonstrating connection establishment, data exchange, and graceful termination. |
| A3 | Raw Sockets | [`CS-BTC25-39_PARINITA_DEVI_RAW_SOCKET_ASSIGNMENT`](./CS-BTC25-39_PARINITA_DEVI_RAW_SOCKET_ASSIGNMENT) | Low-level packet crafting and analysis using raw sockets, providing direct access to network-layer headers and protocol fields. |
| A4 | Multi-Client TCP Chat | [`CS-BTC25-39_PARINITA_DEVI_CHATSERVER`](./CS-BTC25-39_PARINITA_DEVI_CHATSERVER) | A TCP-based chat server capable of handling multiple simultaneous client connections using multithreading/multiplexing. |
| A5 | Advanced TCP Chat | [`CS-BTC25-39_PARINITA_DEVI_ASSIGNMENT5`](./CS-BTC25-39_PARINITA_DEVI_ASSIGNMENT5) | An enhanced version of the chat application with additional features such as improved concurrency handling, message broadcasting, and client management. |
| A6 | GUI TCP Chat | [`CS-BTC25-39_PARINITA_DEVI_ASSIGNMENT6`](./CS-BTC25-39_PARINITA_DEVI_ASSIGNMENT6) | A graphical user interface built on top of the TCP chat application, providing an intuitive front-end for real-time messaging. |

---

## Overview

Each assignment folder is self-contained and includes:
- Source code for the client and server components
- Sample outputs / screenshots (where applicable)

The assignments follow a logical progression:

1. **A1 – UDP** introduces unreliable, connectionless communication and the challenges of building reliability on top of it.
2. **A2 – TCP** covers reliable, connection-oriented communication as a contrast to UDP.
3. **A3 – Raw Sockets** dives into low-level packet construction and header manipulation, bypassing the standard transport-layer abstractions.
4. **A4 – Multi-Client Chat** applies TCP concepts to build a functional multi-user chat server.
5. **A5 – Advanced Chat** refines the chat server with better concurrency and feature handling.
6. **A6 – GUI Chat** completes the series by wrapping the chat client in a graphical interface for a more user-friendly experience.

---

## Tech Stack

- **Language:** Python / C (as applicable per assignment)
- **Concepts:** Socket Programming, TCP/UDP Protocols, Raw Sockets, Multithreading, Client-Server Architecture, GUI Development
- **Tools:** Wireshark (for packet analysis, where applicable)

---

## How to Run

Navigate into the specific assignment folder and run the server and client scripts. In general:

```bash
# Run the server first
python server.py

# Then run the client in a separate terminal
python client.py
```

---

## Acknowledgement

These assignments were completed as part of the **ISEA Phase III Internship Program** at **Tezpur University**, under the guidance of the respective faculty/mentors, with the objective of building a strong foundation in computer networks and socket programming.

---

## Author

**Parinita Devi**
CS-BTC25-39
