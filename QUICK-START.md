# Quick Start - 5 Minutes to Working Lab

## Step 1: Clone Repository

```bash
git clone https://github.com/jakariaadnaan/mobile-laptop-control-lab.git
cd mobile-laptop-control-lab
```

## Step 2: Run Initial Setup

```bash
bash scripts/setup-advanced-lab.sh
```

This installs:
- Android Debug Bridge (adb)
- Screen mirror tool (scrcpy)
- SSH server
- Python 3

## Step 3: Launch Control Panel

```bash
bash control-panel/start-panel.sh
```

A beautiful GUI window opens! 🎉

## Step 4: Configure Your Devices

1. **Device Configuration Tab**
   - Enter your Android device IP: `192.168.1.25`
   - Enter your laptop IP: `192.168.1.50`
   - Enter your username: `user`
   - Click 💾 **Save Configuration**

## Step 5: Connect Android Device

1. **Android Controls Tab**
   - Enable Developer Options on your phone
   - Enable USB Debugging
   - Click 📡 **Connect via IP (Wi-Fi)**
   - Click ✅ **Check Connected Devices** (verify connection)

## Step 6: Mirror Your Phone Screen

1. **Android Controls Tab**
   - Click 🎬 **Mirror Screen (scrcpy)**
   - Your phone screen appears in a window
   - Control it with your mouse and keyboard!

## Step 7: Access Your Laptop Remotely

1. **Laptop Access Tab**
   - Click 🖥️ **SSH Terminal Connection** for command line
   - OR Click 🖱️ **VNC Viewer Connection** for full desktop

## Step 8: Monitor Everything

1. **Monitoring & Logs Tab**
   - Click 📊 **Run Device Monitor** (continuous check)
   - Click 📄 **View Latest Log** (see all activity)
   - Click 📂 **Open Log Folder** (browse logs)

## Done! 🎊

You now have:
- ✅ Android device control
- ✅ Laptop remote access
- ✅ Real-time monitoring
- ✅ Complete logging
- ✅ No coding required!

## Next Steps

- Read: `docs/GUI-TUTORIAL.md` for detailed guide
- Read: `docs/advanced-lab.md` for technical details
- Explore all buttons in the control panel
- Set up SSH keys for secure access
- Enable continuous monitoring for production use

## Troubleshooting

**Devices not showing up?**
```bash
# In Android Controls tab, click:
# - 🔄 Restart adb Server
# - 📡 Connect via IP (Wi-Fi)
# - ✅ Check Connected Devices
```

**Can't connect to laptop?**
```bash
# In Laptop Access tab, click:
# - 🌐 Ping Laptop Host
# - 🔐 SSH Key Setup Guide
```

**Need help?**
- See: `docs/GUI-TUTORIAL.md`
- See: `docs/advanced-lab.md`
- Check: Console output (green box at bottom)

---

**You're all set! Enjoy your powerful lab control system!** 🚀
