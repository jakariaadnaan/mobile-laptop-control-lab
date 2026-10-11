#!/usr/bin/env python3
"""Advanced Mobile-Laptop Control Lab - Professional GUI Dashboard.

This version adds laptop access, monitoring, and a polished user workflow while
keeping the app stable and usable for non-developers.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import threading
import time
from datetime import datetime
from pathlib import Path
from tkinter import messagebox, ttk
import tkinter as tk

BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from backend.core.command_executor import CommandExecutor
from backend.core.config_manager import ConfigManager
from backend.core.device_manager import DeviceManager
from backend.logging.logger import LoggerService


class AppLogger:
    def __init__(self, log_dir: Path):
        self.log_dir = log_dir
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.logger = LoggerService(str(log_dir))

    def info(self, message: str, category: str = "app"):
        self.logger.log("INFO", category, message)

    def error(self, message: str, category: str = "app"):
        self.logger.log("ERROR", category, message)


class ProfessionalControlApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Advanced Mobile-Laptop Control Lab")
        self.root.geometry("1200x780")
        self.root.minsize(1000, 650)
        self.root.configure(bg="#101418")

        self.config = ConfigManager()
        self.device_manager = DeviceManager()
        self.executor = CommandExecutor(max_timeout=35)
        self.log_dir = Path(self.config.get("log_dir", str(Path.home() / ".lab-control" / "logs")))
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.app_logger = AppLogger(self.log_dir)

        self.device_ip = tk.StringVar(value=self.config.get("device_ip", "192.168.1.25"))
        self.device_port = tk.StringVar(value=str(self.config.get("device_port", 5555)))
        self.laptop_ip = tk.StringVar(value=self.config.get("laptop_ip", "192.168.1.50"))
        self.laptop_user = tk.StringVar(value=self.config.get("laptop_user", "user"))

        self.console_lock = threading.Lock()
        self.monitor_active = False
        self.monitor_thread = None

        self._build_ui()
        self._log("System initialized")
        self._refresh_device_table()

    def _build_ui(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TFrame", background="#101418")
        style.configure("TLabel", background="#101418", foreground="#dfeaf4")
        style.configure("TButton", background="#1d2a35", foreground="#ffffff")
        style.configure("TLabelframe", background="#101418")
        style.configure("TLabelframe.Label", background="#101418", foreground="#8be9fd")
        style.configure("Treeview", background="#0d1117", foreground="#dfeaf4", fieldbackground="#0d1117")
        style.configure("Treeview.Heading", background="#1d2a35", foreground="#f2f2f2")

        top = ttk.Frame(self.root, padding=(18, 18, 18, 8))
        top.pack(fill="x")

        ttk.Label(top, text="ADVANCED MOBILE-LAPTOP CONTROL LAB", font=("Arial", 18, "bold")).pack(side="left")

        self.status_var = tk.StringVar(value="System ready")
        ttk.Label(top, textvariable=self.status_var, foreground="#7ef29a").pack(side="right")

        main = ttk.Frame(self.root)
        main.pack(fill="both", expand=True, padx=(18, 18), pady=(0, 18))

        left = ttk.Frame(main)
        left.pack(side="left", fill="y", padx=(0, 12))

        notebook = ttk.Notebook(left)
        notebook.pack(fill="both", expand=True)

        self._build_dashboard_tab(notebook)
        self._build_android_tab(notebook)
        self._build_laptop_tab(notebook)
        self._build_monitor_tab(notebook)
        self._build_security_tab(notebook)

        right = ttk.Frame(main)
        right.pack(side="left", fill="both", expand=True)

        ttk.Label(right, text="Live Console", font=("Arial", 11, "bold")).pack(anchor="w", pady=(0, 6))

        console_frame = ttk.Frame(right)
        console_frame.pack(fill="both", expand=True)

        self.console = tk.Text(
            console_frame,
            bg="#0b0f13",
            fg="#7ef29a",
            font=("Consolas", 10),
            wrap="word",
            insertbackground="#7ef29a",
        )
        self.console.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(console_frame, command=self.console.yview)
        scrollbar.pack(side="right", fill="y")
        self.console.configure(yscrollcommand=scrollbar.set)

        status_bar = ttk.Frame(self.root)
        status_bar.pack(fill="x", padx=18, pady=(0, 14))

        ttk.Label(status_bar, text="Connected devices: ").pack(side="left")
        self.device_count_var = tk.StringVar(value="0")
        ttk.Label(status_bar, textvariable=self.device_count_var, foreground="#7ef29a").pack(side="left")

        ttk.Label(status_bar, text="  |  Monitoring: ").pack(side="left")
        self.monitor_status_var = tk.StringVar(value="OFF")
        ttk.Label(status_bar, textvariable=self.monitor_status_var, foreground="#ffd166").pack(side="left")

    def _build_dashboard_tab(self, parent):
        frame = ttk.Frame(parent)
        parent.add(frame, text="Dashboard")

        quick = ttk.LabelFrame(frame, text="Quick Commands", padding=(12, 8, 12, 8))
        quick.pack(fill="x", padx=10, pady=10)

        ttk.Button(quick, text="Scan Devices", command=self.scan_devices).pack(fill="x", pady=3)
        ttk.Button(quick, text="Check Environment", command=self.check_environment).pack(fill="x", pady=3)
        ttk.Button(quick, text="Auto Setup", command=self.auto_setup).pack(fill="x", pady=3)

        devices = ttk.LabelFrame(frame, text="Connected Device List", padding=(12, 8, 12, 8))
        devices.pack(fill="both", expand=True, padx=10, pady=10)

        cols = ("name", "model", "version", "status")
        self.device_tree = ttk.Treeview(devices, columns=cols, show="headings", height=12)
        self.device_tree.heading("name", text="Name")
        self.device_tree.heading("model", text="Model")
        self.device_tree.heading("version", text="Version")
        self.device_tree.heading("status", text="Status")
        self.device_tree.column("name", width=120)
        self.device_tree.column("model", width=140)
        self.device_tree.column("version", width=120)
        self.device_tree.column("status", width=100)
        self.device_tree.pack(fill="both", expand=True)

    def _build_android_tab(self, parent):
        frame = ttk.Frame(parent)
        parent.add(frame, text="Android")

        conn = ttk.LabelFrame(frame, text="Connection", padding=(12, 8, 12, 8))
        conn.pack(fill="x", padx=10, pady=10)

        ttk.Label(conn, text="Device IP:").grid(row=0, column=0, sticky="w", padx=(0, 8), pady=4)
        ttk.Entry(conn, textvariable=self.device_ip, width=28).grid(row=0, column=1, sticky="ew", pady=4)
        ttk.Label(conn, text="Port:").grid(row=1, column=0, sticky="w", padx=(0, 8), pady=4)
        ttk.Entry(conn, textvariable=self.device_port, width=28).grid(row=1, column=1, sticky="ew", pady=4)
        conn.columnconfigure(1, weight=1)

        actions = [
            ("Check Devices", self.scan_devices),
            ("Connect via IP", self.connect_wireless),
            ("Disconnect All", self.disconnect_all),
            ("Restart ADB", self.restart_adb),
            ("Get Device Info", self.get_device_info),
            ("Mirror Screen", self.start_mirror),
            ("Capture Screenshot", self.capture_screenshot),
            ("View Logcat", self.view_logcat),
            ("Reboot Device", self.reboot_device),
            ("List Packages", self.list_packages),
        ]

        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill="x", padx=10, pady=(0, 10))
        for text, callback in actions:
            ttk.Button(btn_frame, text=text, command=callback).pack(fill="x", pady=3)

    def _build_laptop_tab(self, parent):
        frame = ttk.Frame(parent)
        parent.add(frame, text="Laptop")

        config = ttk.LabelFrame(frame, text="Laptop Access", padding=(12, 8, 12, 8))
        config.pack(fill="x", padx=10, pady=10)

        ttk.Label(config, text="Laptop IP:").grid(row=0, column=0, sticky="w", padx=(0, 8), pady=4)
        ttk.Entry(config, textvariable=self.laptop_ip, width=28).grid(row=0, column=1, sticky="ew", pady=4)
        ttk.Label(config, text="Username:").grid(row=1, column=0, sticky="w", padx=(0, 8), pady=4)
        ttk.Entry(config, textvariable=self.laptop_user, width=28).grid(row=1, column=1, sticky="ew", pady=4)
        config.columnconfigure(1, weight=1)

        actions = [
            ("SSH Terminal", self.launch_ssh),
            ("SFTP", self.launch_sftp),
            ("Ping Host", self.ping_host),
            ("VNC Viewer", self.open_vnc),
            ("SSH Forwarding", self.show_ssh_forward),
            ("X11VNC Guide", self.show_vnc_guide),
        ]

        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill="x", padx=10, pady=(0, 10))
        for text, callback in actions:
            ttk.Button(btn_frame, text=text, command=callback).pack(fill="x", pady=3)

    def _build_monitor_tab(self, parent):
        frame = ttk.Frame(parent)
        parent.add(frame, text="Monitoring")

        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill="x", padx=10, pady=10)
        ttk.Button(btn_frame, text="Start Monitoring", command=self.start_monitoring).pack(fill="x", pady=3)
        ttk.Button(btn_frame, text="Stop Monitoring", command=self.stop_monitoring).pack(fill="x", pady=3)
        ttk.Button(btn_frame, text="Open Log Folder", command=self.open_log_folder).pack(fill="x", pady=3)
        ttk.Button(btn_frame, text="View Latest Log", command=self.view_latest_log).pack(fill="x", pady=3)

    def _build_security_tab(self, parent):
        frame = ttk.Frame(parent)
        parent.add(frame, text="Security")

        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill="x", padx=10, pady=10)
        ttk.Button(btn_frame, text="Save Config", command=self.save_config).pack(fill="x", pady=3)
        ttk.Button(btn_frame, text="Generate SSH Keys", command=self.generate_ssh_keys).pack(fill="x", pady=3)
        ttk.Button(btn_frame, text="Firewall Rules", command=self.show_firewall_guide).pack(fill="x", pady=3)
        ttk.Button(btn_frame, text="Environment Check", command=self.check_environment).pack(fill="x", pady=3)

    def _log(self, message: str, level: str = "INFO"):
        with self.console_lock:
            ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.console.insert("end", f"[{ts}] {level}: {message}\n")
            self.console.see("end")
            self.root.update_idletasks()
        self.app_logger.logger.log(level, "ui", message)

    def _refresh_device_table(self):
        for row in self.device_tree.get_children():
            self.device_tree.delete(row)

        try:
            devices = self.device_manager.scan_devices()
            self.device_count_var.set(str(len(devices)))
            for device in devices:
                self.device_tree.insert("", "end", values=(device.name, device.model, device.version, device.status.value))
        except Exception as exc:
            self._log(f"Device scan error: {exc}", "ERROR")

    def save_config(self):
        config = {
            "device_ip": self.device_ip.get(),
            "device_port": int(self.device_port.get() or 5555),
            "laptop_ip": self.laptop_ip.get(),
            "laptop_user": self.laptop_user.get(),
            "log_dir": str(self.log_dir),
        }
        self.config.update(**config)
        self._log("Configuration saved")
        messagebox.showinfo("Saved", "Settings saved successfully.")

    def scan_devices(self):
        self._log("Scanning Android devices...")
        self._refresh_device_table()

    def connect_wireless(self):
        ip = self.device_ip.get().strip()
        port = int(self.device_port.get() or 5555)
        self._log(f"Connecting to Android device at {ip}:{port}...")
        ok = self.device_manager.connect_wireless(ip, port)
        if ok:
            self._log("Wireless ADB connection successful", "SUCCESS")
        else:
            self._log("Wireless ADB connection failed", "ERROR")

    def disconnect_all(self):
        self._log("Disconnecting all ADB devices...")
        try:
            result = subprocess.run(["adb", "disconnect"], capture_output=True, text=True, timeout=15)
            if result.returncode == 0:
                self._log("ADB disconnected", "SUCCESS")
            else:
                self._log(result.stderr or result.stdout, "ERROR")
        except Exception as exc:
            self._log(f"ADB disconnect failed: {exc}", "ERROR")

    def restart_adb(self):
        self._log("Restarting ADB server...")
        try:
            subprocess.run(["adb", "kill-server"], check=False, capture_output=True, text=True)
            result = subprocess.run(["adb", "start-server"], capture_output=True, text=True, timeout=15)
            if result.returncode == 0:
                self._log("ADB server restarted", "SUCCESS")
            else:
                self._log(result.stderr or result.stdout, "ERROR")
        except Exception as exc:
            self._log(f"ADB restart failed: {exc}", "ERROR")

    def get_device_info(self):
        target = f"{self.device_ip.get()}:{self.device_port.get() or 5555}"
        self._log(f"Collecting info for {target}...")
        info = self.device_manager.get_device_info(target)
        if info:
            self._log(json.dumps(info, indent=2))
        else:
            self._log("Unable to fetch device info", "ERROR")

    def start_mirror(self):
        target = f"{self.device_ip.get()}:{self.device_port.get() or 5555}"
        self._log(f"Starting screen mirroring for {target}...")
        ok = self.device_manager.start_mirroring(target)
        if ok:
            self._log("Mirroring launched", "SUCCESS")
        else:
            self._log("Mirroring failed", "ERROR")

    def capture_screenshot(self):
        target = f"{self.device_ip.get()}:{self.device_port.get() or 5555}"
        output = self.log_dir / f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        self._log(f"Capturing screenshot to {output}...")
        ok = self.device_manager.capture_screenshot(target, str(output))
        if ok:
            self._log(f"Screenshot saved: {output}", "SUCCESS")
        else:
            self._log("Capture screenshot failed", "ERROR")

    def view_logcat(self):
        target = f"{self.device_ip.get()}:{self.device_port.get() or 5555}"
        self._log(f"Retrieving logcat for {target}...")
        output = self.device_manager.get_logcat(target, 150)
        if output:
            self._log(output)
        else:
            self._log("No logcat output returned", "ERROR")

    def reboot_device(self):
        if messagebox.askyesno("Reboot Android device", "Reboot the connected Android device?"):
            target = f"{self.device_ip.get()}:{self.device_port.get() or 5555}"
            self._log(f"Rebooting {target}...")
            ok = self.device_manager.reboot_device(target)
            if ok:
                self._log("Reboot command sent", "SUCCESS")
            else:
                self._log("Reboot failed", "ERROR")

    def list_packages(self):
        target = f"{self.device_ip.get()}:{self.device_port.get() or 5555}"
        packages = self.device_manager.list_packages(target)
        if packages:
            self._log("Installed packages:\n" + "\n".join(packages[:60]))
        else:
            self._log("No packages returned", "ERROR")

    def launch_ssh(self):
        user_host = f"{self.laptop_user.get()}@{self.laptop_ip.get()}"
        self._log(f"Opening SSH: ssh {user_host}")
        try:
            if os.name == "nt":
                os.system(f"start cmd /k ssh {user_host}")
            else:
                os.system(f"xterm -e 'ssh {user_host}' >/dev/null 2>&1 &")
        except Exception as exc:
            self._log(f"SSH launch failed: {exc}", "ERROR")

    def launch_sftp(self):
        user_host = f"{self.laptop_user.get()}@{self.laptop_ip.get()}"
        self._log(f"Opening SFTP: sftp {user_host}")
        try:
            if os.name == "nt":
                os.system(f"start cmd /k sftp {user_host}")
            else:
                os.system(f"xterm -e 'sftp {user_host}' >/dev/null 2>&1 &")
        except Exception as exc:
            self._log(f"SFTP launch failed: {exc}", "ERROR")

    def ping_host(self):
        ip = self.laptop_ip.get().strip()
        self._log(f"Pinging {ip}...")
        try:
            result = subprocess.run(["ping", "-c", "4", ip], capture_output=True, text=True, timeout=15)
            output = result.stdout + result.stderr
            self._log(output or "Ping completed")
        except Exception as exc:
            self._log(f"Ping failed: {exc}", "ERROR")

    def open_vnc(self):
        host = self.laptop_ip.get().strip()
        self._log(f"VNC target: {host}:5901")
        messagebox.showinfo("VNC", f"Open VNC Viewer and connect to:\n{host}:5901")

    def show_vnc_guide(self):
        text = """X11VNC Setup Guide:\n\n1. sudo apt install x11vnc\n2. x11vnc -display :0 -listen localhost\n3. Connect with VNC Viewer to <ip>:5901\n"""
        messagebox.showinfo("X11VNC Guide", text)

    def show_ssh_forward(self):
        text = """SSH port forwarding example:\n\nssh -L 5901:localhost:5901 user@192.168.1.50\n"""
        messagebox.showinfo("SSH Forwarding", text)

    def start_monitoring(self):
        if self.monitor_active:
            self._log("Monitoring is already active")
            return

        self.monitor_active = True
        self.monitor_status_var.set("ON")
        self.status_var.set("Monitoring active")
        self._log("Monitoring started")

        def worker():
            while self.monitor_active:
                try:
                    result = subprocess.run(["adb", "devices"], capture_output=True, text=True, timeout=10)
                    if result.returncode == 0:
                        lines = [ln for ln in result.stdout.splitlines() if "List of attached" not in ln and ln.strip()]
                        if lines:
                            self._log(" | ".join(lines[-3:]))
                    time.sleep(10)
                except Exception as exc:
                    self._log(f"Monitor error: {exc}", "ERROR")
                    time.sleep(10)

        self.monitor_thread = threading.Thread(target=worker, daemon=True)
        self.monitor_thread.start()

    def stop_monitoring(self):
        self.monitor_active = False
        self.monitor_status_var.set("OFF")
        self.status_var.set("Monitoring stopped")
        self._log("Monitoring stopped")

    def open_log_folder(self):
        self._log(f"Opening log folder: {self.log_dir}")
        try:
            if os.name == "nt":
                os.startfile(str(self.log_dir))
            else:
                os.system(f"xdg-open '{self.log_dir}' >/dev/null 2>&1 &")
        except Exception as exc:
            self._log(f"Could not open log folder: {exc}", "ERROR")

    def view_latest_log(self):
        logs = sorted(self.log_dir.glob("*.log"), reverse=True)
        if not logs:
            self._log("No logs found yet")
            return
        latest = logs[0]
        try:
            with latest.open("r", encoding="utf-8") as fh:
                content = fh.read()[-1500:]
            self._log(f"Latest log: {latest.name}\n{content}")
        except Exception as exc:
            self._log(f"Could not read log: {exc}", "ERROR")

    def generate_ssh_keys(self):
        ssh_dir = Path.home() / ".ssh"
        ssh_dir.mkdir(exist_ok=True)
        key_path = ssh_dir / "id_rsa"
        if key_path.exists():
            self._log("SSH key already exists")
            return
        self._log("Generating SSH key pair...")
        result = subprocess.run(["ssh-keygen", "-t", "rsa", "-b", "4096", "-f", str(key_path), "-N", ""], capture_output=True, text=True)
        if result.returncode == 0:
            self._log("SSH key generated successfully", "SUCCESS")
        else:
            self._log(result.stderr or result.stdout, "ERROR")

    def show_firewall_guide(self):
        text = """Firewall rules example:\n\nufw allow 22\nufw allow 5901\nufw allow 5555\nufw enable\n"""
        messagebox.showinfo("Firewall", text)

    def check_environment(self):
        tools = ["adb", "scrcpy", "ssh", "python3", "git"]
        for tool in tools:
            result = subprocess.run(["which", tool], capture_output=True, text=True)
            if result.returncode == 0:
                self._log(f"{tool}: OK")
            else:
                self._log(f"{tool}: MISSING", "ERROR")

    def auto_setup(self):
        self._log("Running setup script...")
        result = subprocess.run(["bash", "scripts/setup-advanced-lab.sh"], capture_output=True, text=True)
        if result.returncode == 0:
            self._log("Auto setup completed", "SUCCESS")
            self._log(result.stdout)
        else:
            self._log(result.stderr or result.stdout, "ERROR")


def main():
    root = tk.Tk()
    app = ProfessionalControlApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
