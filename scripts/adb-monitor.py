#!/usr/bin/env python3
import argparse
import subprocess
import sys
from pathlib import Path


def run(cmd):
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"[ERROR] Command failed: {' '.join(cmd)}")
        if result.stderr:
            print(result.stderr.strip())
        return None
    return result.stdout.strip()


def main():
    parser = argparse.ArgumentParser(description="Advanced mobile/laptop connectivity checker")
    parser.add_argument("--device", default="", help="ADB device target, e.g. 192.168.1.25:5555")
    args = parser.parse_args()

    target = args.device.strip()

    print("[INFO] Checking Android device connectivity...")
    devices = run(["adb", "devices"])
    if devices is None:
        sys.exit(1)
    print(devices)

    if target:
        print(f"[INFO] Querying target: {target}")
        model = run(["adb", "-s", target, "shell", "getprop", "ro.product.model"]) or "unknown"
        version = run(["adb", "-s", target, "shell", "getprop", "ro.build.version.release"]) or "unknown"
        print(f"Model: {model}")
        print(f"Android Version: {version}")

    log_dir = Path.home() / ".lab-control" / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / "device-check.log"
    with log_file.open("a", encoding="utf-8") as fh:
        fh.write(f"ADB connectivity check at target={target or 'default'}\n")
        fh.write((devices or "") + "\n")

    print(f"[INFO] Logs saved to {log_file}")


if __name__ == "__main__":
    main()
