# Mobile-Laptop Control Lab

A secure, advanced lab for learning how to control and monitor mobile and laptop devices in a local network environment.

This repository demonstrates a practical architecture for:

- Android device access via ADB + scrcpy
- Laptop desktop access via VNC / SSH / remote desktop
- Secure local networking using SSH or WireGuard
- Monitoring and automation flows for remote testing
- Safe lab practices for educational and controlled environments

## Lab Objective

Build a lab that allows a laptop to act as the control plane for a mobile device and another laptop or workstation inside the same trusted network. The lab does not aim to bypass security controls or operate outside authorized boundaries.

## Architecture Overview

```text
+----------------------+      +------------------------------------+
| Android device      |<---->| Laptop A (Control Host)            |
| - adb enabled       |      | - SSH server                       |
| - wireless debug    |      | - VNC / x11vnc / NoMachine         |
| - scrcpy            |      | - adb client                       |
+----------------------+      | - automation scripts               |
         ^                     +------------------------------------+
         |                               |
         |                               | secure local tunnel / VPN
         |                               v
+----------------------+      +------------------------------------+
| Android Emulator    |      | Laptop B / Remote Workstation      |
| - Android Studio    |      | - remote desktop access            |
| - ADB               |      | - monitoring                      |
+----------------------+      +------------------------------------+
```

## Included Components

- Device discovery and connectivity checks
- ADB-based mobile command automation
- Screen mirroring with scrcpy
- Remote desktop access for laptop flows
- LAN-based secure control channel
- Logging and monitoring scripts

## Repository Structure

```text
.
├── README.md
├── docs/
│   └── advanced-lab.md
├── scripts/
│   ├── setup-advanced-lab.sh
│   └── adb-monitor.py
├── .gitignore
└── lab-notes/
    └── README.md
```

## Quick Start

1. Read the advanced lab guide:
   - `docs/advanced-lab.md`
2. Prepare your devices:
   - Android device or emulator with ADB enabled
   - Linux laptop with SSH and desktop tools
3. Run setup script:
   - `bash scripts/setup-advanced-lab.sh`
4. Verify connectivity:
   - `adb devices`
   - `ssh user@laptop-host`
5. Mirror the Android screen:
   - `scrcpy`

## Safe Usage

This lab is intended for:

- teaching
- controlled network testing
- authorized device management
- local lab experimentation

Do not use this setup for unauthorized device access, bypassing user consent, or production environments without approval.

## Learning Goals

- Understand ADB connectivity and device control
- Learn secure remote access patterns
- Build a local control plane between mobile and laptop devices
- Practice automation for monitoring, logs, and remote command execution
- Explore desktop remoting and network tunneling

## Recommended Lab Mode

Use this lab on:

- your own Android device with developer options enabled
- local trusted Wi-Fi
- controlled LAN/VPN environment
- test systems only

## Next Steps

Open the advanced lab guide for a full walkthrough with commands, diagrams, and practical tasks.

---

This project is intentionally designed as a learning lab and not a production remote-control platform.
