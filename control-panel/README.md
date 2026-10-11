# Control Panel - GUI Application

This is the main application for the Mobile-Laptop Control Lab. A professional desktop GUI for managing Android devices and remote laptops without any coding.

## Files

- **app.py** - Main GUI application (start here)
- **start-panel.sh** - Automated launcher script
- **requirements.txt** - Python dependencies
- **README.md** - This file

## Quick Launch

### Option 1: Using launcher script (Recommended)

```bash
bash start-panel.sh
```

### Option 2: Direct Python

```bash
python3 app.py
```

## Features

### 📱 Android Device Management
- Connect devices via USB or Wi-Fi
- Check connected devices
- Get device information
- Mirror screen (scrcpy)
- Capture screenshots
- View logs (logcat)
- Reboot devices
- List installed apps

### 💻 Laptop Remote Access
- SSH terminal connection
- SFTP file transfer
- VNC remote desktop
- Port forwarding
- Network testing (ping)

### 📊 Monitoring & Logging
- Real-time device monitoring
- Automatic log capture
- Log viewer and explorer
- Environment checks
- Network status

### ⚙️ Configuration
- Save device IP addresses
- Save laptop credentials
- Persistent configuration
- Easy reconfiguration

## System Requirements

- Python 3.6+
- Tkinter (usually included with Python)
- Linux/macOS/Windows with display server
- ADB and scrcpy installed (automated by setup script)
- SSH access to laptop

## Getting Started

1. Run setup: `bash scripts/setup-advanced-lab.sh`
2. Launch panel: `bash control-panel/start-panel.sh`
3. Configure devices: **Device Configuration Tab**
4. Connect Android: **Android Controls Tab**
5. Mirror screen: **Android Controls → Mirror Screen**
6. Access laptop: **Laptop Access Tab**

## Documentation

- **GUI-TUTORIAL.md** - Complete user guide
- **QUICK-START.md** - 5-minute setup guide
- **advanced-lab.md** - Technical architecture

## Troubleshooting

See the green console output at the bottom of the window for detailed error messages and command output.

### Common Issues

**"Permission denied" on start-panel.sh**
```bash
chmod +x start-panel.sh
bash start-panel.sh
```

**"ModuleNotFoundError" for tkinter**
```bash
# Ubuntu/Debian
sudo apt install python3-tk

# Fedora
sudo dnf install python3-tkinter

# macOS
brew install python-tk
```

**Application won't start**
```bash
# Try direct launch
python3 app.py

# Check console output for errors
```

## Architecture

The app is built with:
- **Tkinter** - GUI framework
- **threading** - Background command execution
- **subprocess** - Command execution
- **pathlib** - File operations
- **json** - Configuration management

No external frameworks required beyond Python standard library!

## Performance

- Lightweight: ~20KB app.py
- Fast startup: <2 seconds
- Non-blocking UI: Commands run in background threads
- Efficient logging: Disk-based persistence

## Security

- All commands logged for audit trail
- Local network only (configurable)
- SSH key support for secure connections
- No credentials stored in code
- Firewall-friendly

## Future Enhancements

- [ ] Web-based interface for remote access
- [ ] Notification system (device connected/disconnected)
- [ ] Advanced automation workflows
- [ ] Custom command execution
- [ ] Device grouping and batch operations
- [ ] Performance metrics dashboard
- [ ] Integration with CI/CD pipelines

## Contributing

Feel free to extend this control panel!

## License

Open source - educational use

---

**Start your lab journey:** `bash start-panel.sh` 🚀
