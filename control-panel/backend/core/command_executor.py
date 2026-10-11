#!/usr/bin/env python3
"""
Control Panel Backend - Command Executor
Handles all command execution with proper error handling and logging
"""

import subprocess
import threading
import queue
from typing import Callable, Optional, Dict, Any
from dataclasses import dataclass
from enum import Enum
from datetime import datetime
import json


class CommandStatus(Enum):
    """Command execution status"""
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    TIMEOUT = "timeout"


@dataclass
class CommandResult:
    """Result of command execution"""
    status: CommandStatus
    stdout: str
    stderr: str
    return_code: int
    duration: float
    executed_at: datetime
    
    def to_dict(self) -> dict:
        return {
            "status": self.status.value,
            "stdout": self.stdout,
            "stderr": self.stderr,
            "return_code": self.return_code,
            "duration": self.duration,
            "executed_at": self.executed_at.isoformat()
        }


class CommandExecutor:
    """Executes system commands safely with callbacks and logging"""
    
    def __init__(self, max_timeout: int = 60):
        self.max_timeout = max_timeout
        self.command_queue: queue.Queue = queue.Queue()
        self.result_callbacks = []
        self._running = False
        self._thread_pool = []
    
    def register_callback(self, callback: Callable[[CommandResult], None]):
        """Register callback for command results"""
        self.result_callbacks.append(callback)
    
    def execute_async(self, cmd: list, description: str = "") -> str:
        """
        Execute command asynchronously
        Returns command ID
        """
        import uuid
        cmd_id = str(uuid.uuid4())
        
        thread = threading.Thread(
            target=self._execute_internal,
            args=(cmd_id, cmd, description),
            daemon=True
        )
        thread.start()
        
        return cmd_id
    
    def execute_sync(self, cmd: list, timeout: Optional[int] = None) -> CommandResult:
        """
        Execute command synchronously
        Blocks until completion
        """
        timeout = timeout or self.max_timeout
        start_time = datetime.now()
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            
            duration = (datetime.now() - start_time).total_seconds()
            
            return CommandResult(
                status=CommandStatus.SUCCESS if result.returncode == 0 else CommandStatus.FAILED,
                stdout=result.stdout,
                stderr=result.stderr,
                return_code=result.returncode,
                duration=duration,
                executed_at=start_time
            )
            
        except subprocess.TimeoutExpired:
            duration = (datetime.now() - start_time).total_seconds()
            return CommandResult(
                status=CommandStatus.TIMEOUT,
                stdout="",
                stderr="Command timeout exceeded",
                return_code=-1,
                duration=duration,
                executed_at=start_time
            )
        
        except Exception as e:
            duration = (datetime.now() - start_time).total_seconds()
            return CommandResult(
                status=CommandStatus.FAILED,
                stdout="",
                stderr=str(e),
                return_code=-1,
                duration=duration,
                executed_at=start_time
            )
    
    def _execute_internal(self, cmd_id: str, cmd: list, description: str):
        """Internal method for async execution"""
        result = self.execute_sync(cmd)
        
        # Notify all callbacks
        for callback in self.result_callbacks:
            try:
                callback({
                    "id": cmd_id,
                    "description": description,
                    **result.to_dict()
                })
            except:
                pass
