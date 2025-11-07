"""Backend auto-start manager for hybrid architecture.

This module provides automatic backend management for cloud features
while maintaining offline-first operation for core functionality.
"""

from __future__ import annotations

import atexit
import logging
import os
import socket
import subprocess
import sys
import time
from pathlib import Path
from typing import Optional

LOG = logging.getLogger(__name__)


class BackendManager:
    """Manages optional backend service for cloud features."""
    
    def __init__(self, port: int = 8001, auto_start: bool = True):
        """Initialize backend manager.
        
        Args:
            port: Port to run backend on
            auto_start: Whether to automatically start backend
        """
        self.port = port
        self.auto_start = auto_start
        self.process: Optional[subprocess.Popen] = None
        self._available = False
        self._startup_attempts = 0
        self._max_startup_attempts = 3
        
        # Register cleanup on exit
        atexit.register(self.shutdown)
    
    def is_port_available(self, port: int) -> bool:
        """Check if a port is available for use.
        
        Args:
            port: Port number to check
            
        Returns:
            True if port is available, False otherwise
        """
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(1)
                result = sock.connect_ex(('localhost', port))
                return result != 0  # Port is available if connection fails
        except Exception:
            return True  # Assume available if we can't check
    
    def find_backend_executable(self) -> Optional[str]:
        """Find the backend executable or script.
        
        Returns:
            Path to backend executable or None if not found
        """
        # Look for backend in common locations
        possible_paths = [
            # Development setup
            "backend/main.py",
            "../backend/main.py", 
            "backend/app/main.py",
            "../backend/app/main.py",
            # Packaged setup
            "backend/backend.exe",
            "backend/backend",
            # Virtual environment
            ".venv/Scripts/uvicorn.exe",
            ".venv/bin/uvicorn",
            "venv/Scripts/uvicorn.exe", 
            "venv/bin/uvicorn",
        ]
        
        for path in possible_paths:
            full_path = Path(path)
            if full_path.exists():
                LOG.debug(f"Found backend at: {full_path}")
                return str(full_path)
        
        # Try to find uvicorn in PATH
        try:
            result = subprocess.run(
                ["which", "uvicorn"] if sys.platform != "win32" else ["where", "uvicorn"],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0 and result.stdout.strip():
                LOG.debug(f"Found uvicorn in PATH: {result.stdout.strip()}")
                return "uvicorn"
        except Exception:
            pass
        
        LOG.warning("Backend executable not found")
        return None
    
    def start(self) -> bool:
        """Start backend as subprocess (non-blocking).
        
        Returns:
            True if backend is available (started or already running), False for offline mode
        """
        if not self.auto_start:
            LOG.debug("Auto-start disabled, checking if backend is already running")
            return self.is_available()
        
        # Check if already running
        if self.process and self.process.poll() is None:
            if self.is_available():
                LOG.debug("Backend process already running and healthy")
                return True
            else:
                LOG.warning("Backend process running but not responding, restarting")
                self.shutdown()
        
        # Check if port is available
        if not self.is_port_available(self.port):
            LOG.info(f"Port {self.port} is already in use, checking if it's our backend")
            if self.is_available():
                LOG.info("Backend already running on port, using existing instance")
                return True
            else:
                LOG.error(f"Port {self.port} is occupied by another service")
                return False
        
        # Find backend executable
        backend_path = self.find_backend_executable()
        if not backend_path:
            LOG.warning("Backend executable not found, running in offline mode")
            return False
        
        # Increment startup attempts
        self._startup_attempts += 1
        if self._startup_attempts > self._max_startup_attempts:
            LOG.error(f"Max startup attempts ({self._max_startup_attempts}) exceeded")
            return False
        
        try:
            LOG.info(f"Starting backend on port {self.port} (attempt {self._startup_attempts})")
            
            # Prepare command
            if backend_path.endswith('.py'):
                # Python script - use uvicorn
                cmd = [
                    sys.executable, "-m", "uvicorn",
                    "backend.app.main:app",
                    "--host", "127.0.0.1",
                    "--port", str(self.port),
                    "--log-level", "warning"
                ]
                cwd = None
            elif backend_path == "uvicorn":
                # Uvicorn in PATH
                cmd = [
                    "uvicorn",
                    "backend.app.main:app", 
                    "--host", "127.0.0.1",
                    "--port", str(self.port),
                    "--log-level", "warning"
                ]
                cwd = None
            else:
                # Executable
                cmd = [backend_path, "--port", str(self.port)]
                cwd = None
            
            # Start process
            self.process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                cwd=cwd,
                # Prevent process from inheriting parent's console on Windows
                creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0
            )
            
            LOG.info(f"Backend process started with PID {self.process.pid}")
            
            # Wait for backend to become available
            max_wait = 10  # seconds
            wait_interval = 0.5
            waited = 0
            
            while waited < max_wait:
                if self.is_available():
                    LOG.info(f"Backend started successfully after {waited:.1f}s")
                    self._available = True
                    return True
                
                # Check if process died
                if self.process.poll() is not None:
                    stdout, stderr = self.process.communicate()
                    LOG.error(f"Backend process died during startup:")
                    LOG.error(f"stdout: {stdout.decode()}")
                    LOG.error(f"stderr: {stderr.decode()}")
                    return False
                
                time.sleep(wait_interval)
                waited += wait_interval
            
            LOG.warning(f"Backend did not become available within {max_wait}s")
            return False
            
        except Exception as e:
            LOG.error(f"Failed to start backend: {e}")
            return False
    
    def is_available(self) -> bool:
        """Check if backend is currently available.
        
        Returns:
            True if backend is responding to health checks
        """
        try:
            import requests
            
            url = f"http://127.0.0.1:{self.port}/health"
            response = requests.get(url, timeout=2)
            
            if response.status_code == 200:
                self._available = True
                return True
            else:
                self._available = False
                return False
                
        except Exception:
            self._available = False
            return False
    
    def shutdown(self) -> None:
        """Gracefully shutdown backend process."""
        if self.process:
            try:
                LOG.info("Shutting down backend process")
                
                # Try graceful termination first
                self.process.terminate()
                
                # Wait for graceful shutdown
                try:
                    self.process.wait(timeout=5)
                    LOG.info("Backend shut down gracefully")
                except subprocess.TimeoutExpired:
                    # Force kill if graceful shutdown fails
                    LOG.warning("Backend did not shut down gracefully, forcing termination")
                    self.process.kill()
                    self.process.wait()
                    
            except Exception as e:
                LOG.error(f"Error shutting down backend: {e}")
            finally:
                self.process = None
                self._available = False
    
    def restart(self) -> bool:
        """Restart the backend process.
        
        Returns:
            True if restart successful, False otherwise
        """
        LOG.info("Restarting backend")
        self.shutdown()
        time.sleep(1)  # Brief pause
        return self.start()
    
    def get_status(self) -> dict:
        """Get current backend status information.
        
        Returns:
            Dictionary with status information
        """
        return {
            "available": self._available,
            "process_running": self.process is not None and self.process.poll() is None,
            "port": self.port,
            "auto_start": self.auto_start,
            "startup_attempts": self._startup_attempts,
            "pid": self.process.pid if self.process else None
        }


def ensure_backend_available(backend_manager: BackendManager) -> str:
    """Ensure backend is available and return status.
    
    Args:
        backend_manager: BackendManager instance
        
    Returns:
        Status string: "online", "offline", or "starting"
    """
    if backend_manager.is_available():
        return "online"
    
    if backend_manager.auto_start:
        if backend_manager.start():
            return "online"
        else:
            return "offline"
    else:
        return "offline"