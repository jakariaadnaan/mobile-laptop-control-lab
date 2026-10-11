# Advanced Mobile-Laptop Control Lab

This document describes a practical advanced lab for controlling and monitoring a mobile device and a laptop over a trusted local network. The lab focuses on education, safety, and controlled access patterns.

## Goals

- Connect a mobile phone and a laptop in a lab environment
- Use Android Debug Bridge (ADB) for device communication
- Mirror the phone screen using scrcpy
- Access the laptop remotely using SSH or VNC
- Establish a secure, controlled control plane
- Capture logs and automate repeated checks

## Threat Model and Safety

This lab is designed strictly for:

- authorized devices
- local network testing
- educational practice
- controlled home or office lab use

It should not be used for unauthorized access or any activity that violates device ownership, network policy, or legal requirements.

## Topology

```text
[Android Phone]
    |
    | ADB / USB or Wi-Fi debugging
    v
[Laptop Host]
    |
    +-- SSH server
    +-- VNC / x11vnc / NoMachine
    +-- adb client
    +-- automation scripts
    |
    +-- Secure LAN or VPN tunnel
    |
    v
[Remote Workstation / Second Laptop]
```

## Components

### 1. Android Access

ADB (Android Debug Bridge) is the main control layer for Android devices.

Typical actions:

- `adb devices`
- `adb shell`
- `adb install app.apk`
- `adb logcat`
- `adb reboot`

### 2. Screen Mirroring

The tool `scrcpy` allows live screen sharing and optional control of the Android screen from a laptop.

Example usage:

```bash
scrcpy
scrcpy --max-fps 60
scrcpy --bit-rate 8M
```

### 3. Laptop Remote Access

A laptop can be controlled using:

- SSH for terminal access
- VNC for graphical desktop access
- NoMachine or XRDP for richer remote GUI workflows

Example:

```bash
ssh user@192.168.1.50
```

### 4. Secure Network Layer

For a more advanced lab, use:

- WireGuard for peer-to-peer VPN
- SSH port forwarding
- local trusted Wi-Fi only
- firewall rules for restricted access

### 5. Monitoring and Automation

Python scripts can be used to:

- verify device connectivity
- collect logs
- detect offline devices
- snapshot state

## Lab Environment Requirements

You need:

- 1 Android phone or emulator
- 1 Linux laptop or workstation
- optional second laptop or VM for remote access testing
- local Wi-Fi or LAN
- USB cable for initial pairing if needed

## Setup Steps

### Step 1: Prepare the Android device

Enable developer options and USB debugging.

For wireless debugging:

```bash
adb tcpip 5555
adb connect 192.168.1.25:5555
```

Check status:

```bash
adb devices
```

### Step 2: Install ADB and scrcpy on the control laptop

Ubuntu/Debian example:

```bash
sudo apt update
sudo apt install -y adb scrcpy openssh-server
```

### Step 3: Verify control connection

```bash
adb devices
adb shell getprop ro.product.model
```

### Step 4: Mirror the Android display

```bash
scrcpy
```

### Step 5: Enable secure laptop access

```bash
sudo systemctl enable --now ssh
sudo systemctl status ssh
```

### Step 6: Create remote access path

Use SSH or WireGuard for a controlled request/response flow.

Example socket channel:

```bash
ssh -L 5901:localhost:5901 user@192.168.1.50
```

### Step 7: Add monitoring

Run a simple monitoring routine:

```bash
python3 scripts/adb-monitor.py --device 192.168.1.25:5555
```

## Example Tasks

### Task 1: Confirm device online

```bash
adb devices
```

### Task 2: Read device state

```bash
adb shell getprop ro.product.model
adb shell getprop ro.build.version.release
```

### Task 3: Capture log output

```bash
adb logcat -d > device-log.txt
```

### Task 4: Mirror screen and interact

```bash
scrcpy
```

### Task 5: Remote into a workstation

```bash
ssh user@192.168.1.50
```

## Advanced Enhancements

Possible extensions for a stronger lab:

- WireGuard mesh for secure tunneling
- automation with Python and cron
- event logging to CSV/JSON
- remote command dispatch from the laptop to Android
- storing screenshots and logs in a lab directory
- using Android emulator instances for isolated testing

## Example Lab Flow

1. Android connects to laptop over USB or Wi-Fi debugging
2. ADB establishes a trusted channel
3. Control laptop performs commands and captures logs
4. scrcpy mirrors the phone screen for visual monitoring
5. SSH/VNC allows remote access to the control laptop
6. Logs are saved to a lab folder for review

## Notes

- Use only local or approved network ranges
- Disable public exposure for any lab service
- Use SSH keys rather than passwords whenever possible
- Restrict firewall rules to known addresses
- Validate device ownership before running tests

## Summary

This lab demonstrates a realistic advanced setup for controlled mobile and laptop interaction in a local environment. It is best suited for teaching, training, and authorized technical exploration in a lab context.
