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
| A7 | Secure Network Application Development Using TCP | [`CS-BTC25-39_PARINITA_DEVI_ASSIGNMENT7`](./CS-BTC25-39_PARINITA_DEVI_ASSIGNMENT7) | Extends the Assignment 6 GUI chat application with practical security mechanisms — username/password authentication, SHA-256 password hashing, duplicate login prevention, input validation, failed-login lockout, session timeout, secure logging, and Wireshark-based authentication verification. |
| A8 | Application Optimization, Scalability and Reliability | [`CS-BTC25-39_PARINITA_DEVI_ASSIGNMENT8`](./CS-BTC25-39_PARINITA_DEVI_ASSIGNMENT8) | Builds on Assignment 7 to improve scalability, reliability, and maintainability — automatic disconnect detection, reconnection and graceful shutdown, support for 10+ concurrent clients, externalized configuration via `config.json`, before/after performance evaluation (delay, throughput, CPU, memory), and Wireshark verification. |

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
7. **A7 – Secure Application** extends the GUI chat application with authentication, secure password storage, and other application-level security mechanisms.
8. **A8 – Optimization & Scalability** builds on A7 to improve scalability, reliability, and resource management, backed by measured performance evaluation.

---

## Tech Stack

- **Language:** Python / C (as applicable per assignment)
- **Concepts:** Socket Programming, TCP/UDP Protocols, Raw Sockets, Multithreading, Client-Server Architecture, GUI Development, Application Security (Authentication, Password Hashing, Session Management), Performance Optimization & Scalability
- **Tools:** Wireshark (packet analysis), Mininet (network emulation/testing), hashlib (SHA-256 password hashing)

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
