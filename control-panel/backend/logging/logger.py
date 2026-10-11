#!/usr/bin/env python3
"""
Control Panel Backend - Logger
Comprehensive logging system with database storage
"""

import logging
import sqlite3
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional
from enum import Enum
import json


class LogLevel(Enum):
    """Log levels"""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class LogEntry:
    """Log entry data"""
    def __init__(self, timestamp: datetime, level: LogLevel, category: str, message: str, data: Dict = None):
        self.timestamp = timestamp
        self.level = level
        self.category = category
        self.message = message
        self.data = data or {}
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "timestamp": self.timestamp.isoformat(),
            "level": self.level.value,
            "category": self.category,
            "message": self.message,
            "data": self.data
        }


class LoggerService:
    """Professional logging service with database backend"""
    
    def __init__(self, log_dir: str):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.db_path = self.log_dir / "logs.db"
        self._init_database()
    
    def _init_database(self):
        """Initialize SQLite database for logs"""
        try:
            conn = sqlite3.connect(str(self.db_path))
            cursor = conn.cursor()
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    level TEXT NOT NULL,
                    category TEXT NOT NULL,
                    message TEXT NOT NULL,
                    data TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_timestamp ON logs(timestamp)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_level ON logs(level)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_category ON logs(category)")
            
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Error initializing database: {e}")
    
    def log(self, level: LogLevel, category: str, message: str, data: Dict = None):
        """Log a message"""
        entry = LogEntry(datetime.now(), level, category, message, data)
        self._save_to_database(entry)
    
    def _save_to_database(self, entry: LogEntry):
        """Save log entry to database"""
        try:
            conn = sqlite3.connect(str(self.db_path))
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO logs (timestamp, level, category, message, data)
                VALUES (?, ?, ?, ?, ?)
            """, (
                entry.timestamp.isoformat(),
                entry.level.value,
                entry.category,
                entry.message,
                json.dumps(entry.data)
            ))
            
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Error saving log: {e}")
    
    def get_logs(self, level: Optional[LogLevel] = None, category: Optional[str] = None, 
                 limit: int = 100) -> List[Dict[str, Any]]:
        """Retrieve logs with filtering"""
        try:
            conn = sqlite3.connect(str(self.db_path))
            cursor = conn.cursor()
            
            query = "SELECT * FROM logs WHERE 1=1"
            params = []
            
            if level:
                query += " AND level = ?"
                params.append(level.value)
            
            if category:
                query += " AND category = ?"
                params.append(category)
            
            query += " ORDER BY timestamp DESC LIMIT ?"
            params.append(limit)
            
            cursor.execute(query, params)
            columns = [desc[0] for desc in cursor.description]
            logs = [dict(zip(columns, row)) for row in cursor.fetchall()]
            
            conn.close()
            return logs
        except Exception as e:
            print(f"Error retrieving logs: {e}")
            return []
    
    def export_logs(self, output_path: str, format: str = "json"):
        """Export logs to file"""
        try:
            logs = self.get_logs(limit=10000)
            
            if format == "json":
                with open(output_path, "w") as f:
                    json.dump(logs, f, indent=2)
            elif format == "csv":
                import csv
                with open(output_path, "w", newline="") as f:
                    writer = csv.DictWriter(f, fieldnames=logs[0].keys())
                    writer.writeheader()
                    writer.writerows(logs)
        except Exception as e:
            print(f"Error exporting logs: {e}")
