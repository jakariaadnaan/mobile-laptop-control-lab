# GUI Control Panel - Complete Tutorial

## Overview

The Advanced Mobile-Laptop Control Lab GUI is a powerful desktop application that allows you to manage and control Android devices and laptops without writing any code. Just click buttons!

## Installation & Launch

### Quick Start

```bash
cd mobile-laptop-control-lab/control-panel
bash start-panel.sh
```

Or directly:

```bash
python3 control-panel/app.py
```

## GUI Layout

The app has 4 main tabs:

### 1️⃣ **Device Configuration**

Set up your Android device and Laptop IP addresses.

**What you need:**
- Android Device IP: `192.168.1.25` (or your device's actual IP)
- Port: `5555` (ADB wireless port)
- Laptop IP: `192.168.1.50` (or your laptop's actual IP)
- Username: `user` (your username)

**Buttons:**
- 💾 **Save Configuration** - Saves your settings
- 🔄 **Refresh** - Reloads settings

### 2️⃣ **Android Controls**

#### Device Status
- ✅ **Check Connected Devices** - Lists all connected Android devices
- 📊 **Get Device Info** - Displays model, Android version, serial number
- 🔄 **Restart adb Server** - Restarts the Android Debug Bridge

#### Wireless Connection
- 📡 **Connect via IP (Wi-Fi)** - Connects to your Android device over Wi-Fi
- 🔌 **Disconnect Device** - Disconnects the device

#### Screen & Control
- 🎬 **Mirror Screen (scrcpy)** - Opens live screen mirroring
- 📸 **Capture Screenshot** - Captures and saves a screenshot

#### Advanced Commands
- 📋 **View Logcat (Logs)** - Shows device system logs
- 🔄 **Reboot Device** - Restarts the Android device
- 📝 **List Installed Apps** - Lists all installed applications

### 3️⃣ **Laptop Access**

#### SSH Remote Access
- 🖥️ **SSH Terminal Connection** - Opens terminal to your laptop
- 📁 **SSH File Transfer (SFTP)** - Transfer files between devices
- 🔐 **SSH Key Setup Guide** - Shows how to set up secure SSH keys

#### VNC Remote Desktop
- 🖱️ **VNC Viewer Connection** - Remote desktop access
- 📺 **X11VNC Server Setup** - Configure VNC on your laptop

#### Network & Tunneling
- 🌐 **Ping Laptop Host** - Test network connectivity
- 🔒 **SSH Port Forwarding** - Set up secure tunnels

### 4️⃣ **Monitoring & Logs**

#### Device Monitoring
- 📊 **Run Device Monitor** - Start continuous monitoring
- ⏸️ **Stop Monitoring** - Stop the monitoring process

#### Logs & Reports
- 📂 **Open Log Folder** - Browse all saved logs
- 📄 **View Latest Log** - Display the most recent log
- 🗑️ **Clear Old Logs** - Delete old log files

#### System Information
- 💻 **Network Status** - View current network configuration
- 🔧 **Environment Check** - Verify all required tools are installed

## Console Output

All commands and their output are displayed in the green console at the bottom. This console also:
- Shows real-time progress
- Displays errors with ❌ indicators
- Logs successful operations with ✅
- Saves everything to disk

## Step-by-Step Example Workflow

### Setup Phase (First Time)

1. **Open Configuration Tab**
   - Enter your Android device's IP address
   - Enter your laptop's IP address
   - Enter your username
   - Click 💾 Save Configuration

2. **Check Environment**
   - Go to Monitoring & Logs tab
   - Click 🔧 Environment Check
   - Verify all tools are installed (✅ for each)

### Daily Usage

#### Monitor Android Device

1. Go to **Android Controls** tab
2. Click ✅ **Check Connected Devices**
3. Click 📊 **Get Device Info**
4. Click 🎬 **Mirror Screen** to see device display
5. Use your mouse and keyboard to control the device!

#### Access Laptop Remotely

1. Go to **Laptop Access** tab
2. Click 🖥️ **SSH Terminal Connection** OR
3. Click 🖱️ **VNC Viewer Connection** for full desktop

#### Monitor Everything

1. Go to **Monitoring & Logs** tab
2. Click 📊 **Run Device Monitor** (runs in background)
3. Click 📄 **View Latest Log** to check status
4. Click 📂 **Open Log Folder** to browse all logs

## Console Commands Explained

When you click a button, the app runs commands in the background:

```bash
# Example outputs you'll see:

▶ Checking connected devices...
============================================================
List of attached devices
192.168.1.25:5555 device

✅ Command completed successfully

▶ Starting screen mirror...
============================================================
(scrcpy opens in a separate window)

✅ Command completed successfully
```

## Troubleshooting

### "Device not found" error

1. Ensure Android device has USB Debugging enabled
2. Device must be on same Wi-Fi network
3. Try: 📡 **Connect via IP (Wi-Fi)**
4. Run: ✅ **Check Connected Devices**

### "SSH Connection Refused"

1. Check laptop is running SSH server
2. Verify correct IP address in Configuration
3. Ensure both devices are on same network
4. Try: 🌐 **Ping Laptop Host**

### Logs not saving

1. Check folder permissions: `~/.lab-control/logs/`
2. Ensure disk has free space
3. Try: 📂 **Open Log Folder**

## Advanced Features

### Automated Monitoring

The control panel can run continuous monitoring:

1. Click 📊 **Run Device Monitor** (doesn't block UI)
2. Device status is checked every 30 seconds
3. Logs are saved automatically
4. Click ⏸️ **Stop Monitoring** when done

### Log Analysis

All logs are saved in: `~/.lab-control/logs/`

Format:
- Timestamp included in each log entry
- Separate file for each day
- All commands and outputs recorded

### Configuration Persistence

Your settings are saved automatically:
- Location: `~/.lab-control/config.json`
- IP addresses, usernames, ports all saved
- Settings load automatically on app restart

## Power User Tips

1. **Batch Operations**
   - Set up device
   - Enable continuous monitoring
   - Mirror screen
   - Open SSH terminal
   - All working simultaneously!

2. **Screenshots & Logs**
   - Automated capture every time you click
   - Historical logs for debugging
   - Export to CSV/JSON if needed

3. **Network Optimization**
   - SSH Port Forwarding for secure tunnels
   - VNC for low-bandwidth environments
   - ADB over Wi-Fi for mobility

4. **Security**
   - Use SSH keys (recommended in guide)
   - Firewall rules limit access
   - Local network only (no public exposure)
   - Audit logs for tracking

## Summary

You now have a professional-grade control system:

✅ No coding required - just click buttons  
✅ Control Android devices in real-time  
✅ Remote access to laptops  
✅ Automatic monitoring and logging  
✅ Production-ready architecture  
✅ Extensible for future features  

Enjoy your advanced lab! 🚀
