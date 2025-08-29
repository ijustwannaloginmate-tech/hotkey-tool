#!/usr/bin/env python3
"""
HotVolume Launcher
Simple launcher script for the HotVolume application
"""

import sys
import os
from pathlib import Path

# Add the backend directory to the Python path
backend_dir = Path(__file__).parent / 'backend'
sys.path.insert(0, str(backend_dir))

try:
    from server import main
    main()
except ImportError as e:
    print(f"Error importing modules: {e}")
    print("Make sure all dependencies are installed:")
    print("pip install -r backend/requirements.txt")
    sys.exit(1)
except Exception as e:
    print(f"Error starting HotVolume: {e}")
    sys.exit(1)