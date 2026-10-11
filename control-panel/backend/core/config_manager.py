#!/usr/bin/env python3
"""
Control Panel Backend - Configuration Manager
Handles configuration storage and retrieval
"""

import json
from pathlib import Path
from typing import Dict, Any, Optional
from dataclasses import dataclass, asdict
import threading


@dataclass
class AppConfig:
    """Application configuration"""
    device_ip: str = "192.168.1.25"
    device_port: int = 5555
    laptop_ip: str = "192.168.1.50"
    laptop_user: str = "user"
    laptop_password: str = ""
    log_dir: str = None
    theme: str = "dark"
    auto_connect: bool = True
    monitor_interval: int = 10
    max_log_size: int = 100  # MB
    
    def __post_init__(self):
        if self.log_dir is None:
            self.log_dir = str(Path.home() / ".lab-control" / "logs")


class ConfigManager:
    """Manages application configuration"""
    
    def __init__(self):
        self.config_dir = Path.home() / ".lab-control"
        self.config_file = self.config_dir / "config.json"
        self.config_dir.mkdir(parents=True, exist_ok=True)
        self.config = AppConfig()
        self.lock = threading.Lock()
        self.load()
    
    def load(self) -> AppConfig:
        """Load configuration from disk"""
        try:
            if self.config_file.exists():
                with open(self.config_file, "r") as f:
                    data = json.load(f)
                    self.config = AppConfig(**data)
        except Exception as e:
            print(f"Error loading config: {e}")
        
        return self.config
    
    def save(self) -> bool:
        """Save configuration to disk"""
        try:
            with self.lock:
                with open(self.config_file, "w") as f:
                    json.dump(asdict(self.config), f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving config: {e}")
            return False
    
    def update(self, **kwargs) -> bool:
        """Update configuration"""
        try:
            for key, value in kwargs.items():
                if hasattr(self.config, key):
                    setattr(self.config, key, value)
            return self.save()
        except Exception as e:
            print(f"Error updating config: {e}")
            return False
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value"""
        return getattr(self.config, key, default)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert config to dictionary"""
        return asdict(self.config)
