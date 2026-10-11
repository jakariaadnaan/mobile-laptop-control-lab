#!/usr/bin/env python3
"""
Control Panel Backend - Monitor
Continuous monitoring of devices and system state
"""

import threading
import time
from typing import Callable, Dict, Any, List
from datetime import datetime
from dataclasses import dataclass
from enum import Enum


class MonitorEventType(Enum):
    """Types of monitoring events"""
    DEVICE_ONLINE = "device_online"
    DEVICE_OFFLINE = "device_offline"
    PERFORMANCE_ALERT = "performance_alert"
    CONNECTION_LOST = "connection_lost"
    COMMAND_EXECUTED = "command_executed"
    ERROR_OCCURRED = "error_occurred"


@dataclass
class MonitorEvent:
    """Monitoring event data"""
    event_type: MonitorEventType
    device_id: str
    timestamp: datetime
    data: Dict[str, Any]
    
    def to_dict(self) -> dict:
        return {
            "event_type": self.event_type.value,
            "device_id": self.device_id,
            "timestamp": self.timestamp.isoformat(),
            "data": self.data
        }


class MonitorService:
    """Continuous monitoring service for devices"""
    
    def __init__(self, interval: int = 10):
        self.interval = interval  # seconds
        self.is_monitoring = False
        self._thread = None
        self._callbacks: List[Callable] = []
        self._last_states: Dict[str, Any] = {}
    
    def register_callback(self, callback: Callable[[MonitorEvent], None]):
        """Register callback for monitor events"""
        self._callbacks.append(callback)
    
    def start(self):
        """Start continuous monitoring"""
        if self.is_monitoring:
            return
        
        self.is_monitoring = True
        self._thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self._thread.start()
    
    def stop(self):
        """Stop continuous monitoring"""
        self.is_monitoring = False
        if self._thread:
            self._thread.join(timeout=5)
    
    def _monitor_loop(self):
        """Main monitoring loop"""
        while self.is_monitoring:
            try:
                self._check_device_status()
                self._check_system_health()
                time.sleep(self.interval)
            except Exception as e:
                self._emit_event(MonitorEventType.ERROR_OCCURRED, "", {"error": str(e)})
    
    def _check_device_status(self):
        """Check connected devices status"""
        import subprocess
        
        try:
            result = subprocess.run(
                ["adb", "devices"],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            devices = {}
            for line in result.stdout.split("\n")[1:]:
                if not line.strip():
                    continue
                parts = line.split()
                if len(parts) >= 2:
                    devices[parts[0]] = parts[1]
            
            # Detect changes
            for device_id, status in devices.items():
                if device_id not in self._last_states:
                    self._emit_event(MonitorEventType.DEVICE_ONLINE, device_id, {"status": status})
                elif self._last_states[device_id] != status:
                    event_type = MonitorEventType.DEVICE_ONLINE if status == "device" else MonitorEventType.DEVICE_OFFLINE
                    self._emit_event(event_type, device_id, {"status": status})
            
            # Detect disconnections
            for device_id in list(self._last_states.keys()):
                if device_id not in devices:
                    self._emit_event(MonitorEventType.DEVICE_OFFLINE, device_id, {})
            
            self._last_states = devices
            
        except Exception as e:
            self._emit_event(MonitorEventType.ERROR_OCCURRED, "", {"error": str(e)})
    
    def _check_system_health(self):
        """Check overall system health"""
        import psutil
        
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            
            if cpu_percent > 80:
                self._emit_event(MonitorEventType.PERFORMANCE_ALERT, "", {
                    "metric": "cpu",
                    "value": cpu_percent,
                    "threshold": 80
                })
            
            if memory.percent > 85:
                self._emit_event(MonitorEventType.PERFORMANCE_ALERT, "", {
                    "metric": "memory",
                    "value": memory.percent,
                    "threshold": 85
                })
        except:
            pass
    
    def _emit_event(self, event_type: MonitorEventType, device_id: str, data: Dict[str, Any]):
        """Emit monitoring event to all callbacks"""
        event = MonitorEvent(
            event_type=event_type,
            device_id=device_id,
            timestamp=datetime.now(),
            data=data
        )
        
        for callback in self._callbacks:
            try:
                callback(event)
            except:
                pass
