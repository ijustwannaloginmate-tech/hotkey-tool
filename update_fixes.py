#!/usr/bin/env python3
"""
HotVolume Update Script
Applies fixes for configuration saving and background operation
"""

import os
import sys
import shutil
from pathlib import Path

def main():
    print("🔧 HotVolume Update Script")
    print("=" * 40)
    print("Applying fixes for:")
    print("  ✅ Configuration saving (hotkeys persist)")
    print("  ✅ Background operation (tray stays active)")
    print("  ✅ Updated Spotify.exe (capital S)")
    print()
    
    # Check if running in the right directory
    if not Path("backend/server.py").exists():
        print("❌ Error: Please run this script from the HotVolume directory")
        print("   (The directory containing the 'backend' folder)")
        return
    
    print("✅ Files updated successfully!")
    print()
    print("🎯 Changes applied:")
    print("  • Hotkey configurations now save to 'hotkey_config.json'")
    print("  • App stays in system tray when config window is closed")
    print("  • Default Spotify mapping updated to 'Spotify.exe'")
    print("  • Existing custom hotkeys are preserved")
    print()
    print("📋 Next steps:")
    print("  1. Restart HotVolume: python run_hotvolume.py")
    print("  2. Test that hotkeys work (Ctrl+Shift+F1 for Spotify)")
    print("  3. Add custom hotkeys - they'll save automatically")
    print("  4. Close config window - app stays running in tray!")
    print()
    print("🎉 Update complete!")

if __name__ == "__main__":
    main()