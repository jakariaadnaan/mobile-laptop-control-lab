#!/usr/bin/env python3
"""
Control Panel Backend - Device Manager
Handles all device communication and management
"""

import subprocess
import json
import time
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum
from datetime import datetime
import threading


class DeviceStatus(Enum):
    """Device status enumeration"""
    ONLINE = "online"
    OFFLINE = "offline"
    UNAUTHORIZED = "unauthorized"
    UNKNOWN = "unknown"


@dataclass
class Device:
    """Device information container"""
    id: str
    status: DeviceStatus
    name: str
    model: str
    version: str
    adb_port: int
    last_seen: datetime
    
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "status": self.status.value,
            "name": self.name,
            "model": self.model,
            "version": self.version,
            "adb_port": self.adb_port,
            "last_seen": self.last_seen.isoformat()
        }


class DeviceManager:
    """Manages all device operations - ADB, connection, control"""
    
    def __init__(self):
        self.devices: Dict[str, Device] = {}
        self.lock = threading.Lock()
        self._command_callbacks = []
    
    def register_callback(self, callback):
        """Register callback for device events"""
        self._command_callbacks.append(callback)
    
    def _notify(self, event_type: str, data: dict):
        """Notify all registered callbacks"""
        for callback in self._command_callbacks:
            try:
                callback({"type": event_type, "data": data})
            except:
                pass
    
    def scan_devices(self) -> List[Device]:
        """
        Scan for all connected Android devices
        Returns list of discovered devices
        """
        try:
            result = subprocess.run(
                ["adb", "devices", "-l"],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            devices = []
            for line in result.stdout.split("\n")[1:]:
                if not line.strip() or "List of attached" in line:
                    continue
                
                parts = line.split()
                if len(parts) < 2:
                    continue
                
                device_id = parts[0]
                status = DeviceStatus(parts[1])
                
                device = Device(
                    id=device_id,
                    status=status,
                    name=self._extract_property(device_id, "model") or "Unknown",
                    model=self._extract_property(device_id, "ro.product.model") or "N/A",
                    version=self._extract_property(device_id, "ro.build.version.release") or "N/A",
                    adb_port=5555,
                    last_seen=datetime.now()
                )
                
                with self.lock:
                    self.devices[device_id] = device
                    devices.append(device)
            
            self._notify("devices_scanned", {"count": len(devices)})
            return devices
            
        except Exception as e:
            self._notify("error", {"message": f"Scan failed: {str(e)}"})
            return []
    
    def connect_wireless(self, ip: str, port: int = 5555) -> bool:
        """
        Connect to Android device via IP (wireless debugging)
        """
        try:
            target = f"{ip}:{port}"
            result = subprocess.run(
                ["adb", "connect", target],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            success = result.returncode == 0
            self._notify("wireless_connect", {"target": target, "success": success})
            return success
            
        except Exception as e:
            self._notify("error", {"message": f"Connect failed: {str(e)}"})
            return False
    
    def disconnect_device(self, device_id: str) -> bool:
        """
        Disconnect a device
        """
        try:
            result = subprocess.run(
                ["adb", "disconnect", device_id],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            success = result.returncode == 0
            if success:
                with self.lock:
                    if device_id in self.devices:
                        del self.devices[device_id]
            
            self._notify("device_disconnected", {"device": device_id, "success": success})
            return success
            
        except Exception as e:
            self._notify("error", {"message": f"Disconnect failed: {str(e)}"})
            return False
    
    def get_device_info(self, device_id: str) -> Dict:
        """
        Get detailed device information
        """
        try:
            properties = {
                "model": "ro.product.model",
                "brand": "ro.product.brand",
                "android_version": "ro.build.version.release",
                "sdk_version": "ro.build.version.sdk",
                "cpu_abi": "ro.product.cpu.abi",
                "serial": "ro.serialno",
                "build_id": "ro.build.id",
                "fingerprint": "ro.build.fingerprint"
            }
            
            info = {"device_id": device_id}
            
            for key, prop in properties.items():
                value = self._execute_shell(device_id, ["getprop", prop])
                info[key] = value or "N/A"
            
            self._notify("device_info_retrieved", info)
            return info
            
        except Exception as e:
            self._notify("error", {"message": f"Get info failed: {str(e)}"})
            return {}
    
    def _extract_property(self, device_id: str, prop: str) -> Optional[str]:
        """
        Extract a single device property
        """
        try:
            result = subprocess.run(
                ["adb", "-s", device_id, "shell", "getprop", prop],
                capture_output=True,
                text=True,
                timeout=5
            )
            return result.stdout.strip() if result.returncode == 0 else None
        except:
            return None
    
    def _execute_shell(self, device_id: str, cmd: List[str]) -> Optional[str]:
        """
        Execute shell command on device
        """
        try:
            result = subprocess.run(
                ["adb", "-s", device_id, "shell"] + cmd,
                capture_output=True,
                text=True,
                timeout=10
            )
            return result.stdout.strip() if result.returncode == 0 else None
        except:
            return None
    
    def capture_screenshot(self, device_id: str, output_path: str) -> bool:
        """
        Capture screenshot from device
        """
        try:
            result = subprocess.run(
                ["adb", "-s", device_id, "exec-out", "screencap", "-p"],
                capture_output=True,
                timeout=10
            )
            
            if result.returncode == 0:
                with open(output_path, "wb") as f:
                    f.write(result.stdout)
                self._notify("screenshot_captured", {"path": output_path})
                return True
            return False
            
        except Exception as e:
            self._notify("error", {"message": f"Screenshot failed: {str(e)}"})
            return False
    
    def get_logcat(self, device_id: str, lines: int = 100) -> str:
        """
        Get device logcat
        """
        try:
            result = subprocess.run(
                ["adb", "-s", device_id, "logcat", "-d", f"*:{lines}"],
                capture_output=True,
                text=True,
                timeout=10
            )
            return result.stdout if result.returncode == 0 else ""
        except Exception as e:
            self._notify("error", {"message": f"Logcat failed: {str(e)}"})
            return ""
    
    def reboot_device(self, device_id: str) -> bool:
        """
        Reboot the device
        """
        try:
            result = subprocess.run(
                ["adb", "-s", device_id, "reboot"],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            success = result.returncode == 0
            self._notify("device_rebooted", {"device": device_id, "success": success})
            return success
            
        except Exception as e:
            self._notify("error", {"message": f"Reboot failed: {str(e)}"})
            return False
    
    def list_packages(self, device_id: str) -> List[str]:
        """
        List installed packages on device
        """
        try:
            result = subprocess.run(
                ["adb", "-s", device_id, "shell", "pm", "list", "packages"],
                capture_output=True,
                text=True,
                timeout=15
            )
            
            if result.returncode == 0:
                packages = [line.replace("package:", "") for line in result.stdout.split("\n") if line]
                self._notify("packages_listed", {"count": len(packages)})
                return packages
            return []
            
        except Exception as e:
            self._notify("error", {"message": f"List packages failed: {str(e)}"})
            return []
    
    def get_device_storage(self, device_id: str) -> Dict:
        """
        Get device storage information
        """
        try:
            result = subprocess.run(
                ["adb", "-s", device_id, "shell", "df"],
                capture_output=True,
                text=True,
                timeout=10
            )
            return {"output": result.stdout if result.returncode == 0 else ""}
        except Exception as e:
            return {"error": str(e)}
    
    def start_mirroring(self, device_id: str) -> bool:
        """
        Start screen mirroring with scrcpy
        """
        try:
            subprocess.Popen(
                ["scrcpy", "-s", device_id],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            self._notify("mirroring_started", {"device": device_id})
            return True
        except Exception as e:
            self._notify("error", {"message": f"Mirroring failed: {str(e)}"})
            return False
