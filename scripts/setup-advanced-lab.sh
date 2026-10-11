#!/usr/bin/env bash
set -euo pipefail

OS_NAME="$(uname -s)"

echo "[INFO] Setting up advanced mobile-laptop control lab..."

if [[ "$OS_NAME" == "Linux" ]]; then
  if command -v apt-get >/dev/null 2>&1; then
    echo "[INFO] Detected Debian/Ubuntu-based Linux. Installing required packages..."
    sudo apt-get update
    sudo apt-get install -y adb scrcpy openssh-server net-tools python3 python3-pip
  elif command -v dnf >/dev/null 2>&1; then
    echo "[INFO] Detected Fedora/RHEL-based Linux. Installing required packages..."
    sudo dnf install -y android-tools scrcpy openssh-server net-tools python3 python3-pip
  elif command -v pacman >/dev/null 2>&1; then
    echo "[INFO] Detected Arch Linux. Installing required packages..."
    sudo pacman -S --noconfirm adb scrcpy openssh python net-tools
  else
    echo "[ERROR] Unsupported Linux distribution. Please install adb, scrcpy, openssh-server, and python3 manually."
    exit 1
  fi
else
  echo "[ERROR] This setup script is intended for Linux hosts."
  exit 1
fi

if ! command -v adb >/dev/null 2>&1; then
  echo "[ERROR] adb was not installed correctly."
  exit 1
fi

if ! command -v sshd >/dev/null 2>&1; then
  echo "[WARN] sshd not found. Attempting to enable openssh-server..."
fi

sudo systemctl enable --now ssh 2>/dev/null || true

mkdir -p "$HOME/.lab-control" "$HOME/.lab-control/logs"

cat > "$HOME/.lab-control/README.txt" <<'EOF'
Advanced Mobile-Laptop Control Lab Setup
=====================================

This directory stores local lab notes and logs.

Suggested commands:
  adb devices
  adb tcpip 5555
  adb connect 192.168.1.25:5555
  scrcpy
  ssh user@192.168.1.50
EOF

echo "[INFO] Setup complete."
echo ""
echo "Next steps:"
echo "  1. Enable Developer Options and USB debugging on your Android device"
echo "  2. Connect via USB or Wi-Fi debugging"
echo "  3. Run: adb devices"
echo "  4. Run: scrcpy"
echo "  5. For remote shell: ssh user@<laptop-host>"
echo ""
echo "Useful commands:"
echo "  adb tcpip 5555"
echo "  adb connect 192.168.1.25:5555"
echo "  adb shell getprop ro.product.model"
echo "  adb logcat -d > ~/device-log.txt"
