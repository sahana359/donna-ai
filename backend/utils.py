"""
Utility functions for Donna AI Backend
"""
import sys

# Force unbuffered output for instant logs
sys.stdout.reconfigure(line_buffering=True) if hasattr(sys.stdout, 'reconfigure') else None


def log(msg: str):
    """Print and flush immediately for logging."""
    print(msg, flush=True)
