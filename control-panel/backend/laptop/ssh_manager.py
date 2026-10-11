#!/usr/bin/env python3
"""
Control Panel Backend - SSH Manager
Handles SSH connections and remote execution
"""

import subprocess
from typing import Tuple, Optional, Dict, Any
from dataclasses import dataclass
from enum import Enum
import threading


class ConnectionStatus(Enum):
    """SSH connection status"""
    CONNECTED = "connected"
    DISCONNECTED = "disconnected"
    CONNECTING = "connecting"
    ERROR = "error"


@dataclass
class SSHConfig:
    """SSH configuration"""
    host: str
    user: str
    port: int = 22
    password: Optional[str] = None
    key_file: Optional[str] = None
    use_key_auth: bool = True


class SSHManager:
    """Manages SSH connections and remote operations"""
    
    def __init__(self, config: SSHConfig):
        self.config = config
        self.status = ConnectionStatus.DISCONNECTED
        self._callbacks = []
    
    def register_callback(self, callback):
        """Register callback for connection events"""
        self._callbacks.append(callback)
    
    def test_connection(self) -> bool:
        """
        Test SSH connection
        """
        try:
            cmd = self._build_ssh_cmd(["echo", "test"])
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=10
            )
            
            success = result.returncode == 0
            self._set_status(ConnectionStatus.CONNECTED if success else ConnectionStatus.ERROR)
            return success
            
        except Exception as e:
            self._set_status(ConnectionStatus.ERROR)
            return False
    
    def execute_remote(self, command: str) -> Tuple[str, str, int]:
        """
        Execute command on remote host
        Returns: (stdout, stderr, return_code)
        """
        try:
            cmd = self._build_ssh_cmd([command])
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30
            )
            return result.stdout, result.stderr, result.returncode
        except Exception as e:
            return "", str(e), -1
    
    def get_remote_file(self, remote_path: str, local_path: str) -> bool:
        """
        Download file from remote host (SFTP)
        """
        try:
            cmd = [
                "scp",
                f"{self.config.user}@{self.config.host}:{remote_path}",
                local_path
            ]
            
            result = subprocess.run(cmd, capture_output=True, timeout=30)
            return result.returncode == 0
        except:
            return False
    
    def put_remote_file(self, local_path: str, remote_path: str) -> bool:
        """
        Upload file to remote host (SFTP)
        """
        try:
            cmd = [
                "scp",
                local_path,
                f"{self.config.user}@{self.config.host}:{remote_path}"
            ]
            
            result = subprocess.run(cmd, capture_output=True, timeout=30)
            return result.returncode == 0
        except:
            return False
    
    def _build_ssh_cmd(self, remote_cmd: list) -> list:
        """
        Build SSH command
        """
        cmd = ["ssh"]
        
        if self.config.use_key_auth and self.config.key_file:
            cmd.extend(["-i", self.config.key_file])
        
        if self.config.port != 22:
            cmd.extend(["-p", str(self.config.port)])
        
        cmd.append(f"{self.config.user}@{self.config.host}")
        cmd.extend(remote_cmd)
        
        return cmd
    
    def _set_status(self, status: ConnectionStatus):
        """Set connection status and notify callbacks"""
        self.status = status
        for callback in self._callbacks:
            try:
                callback({"status": status.value})
            except:
                pass
