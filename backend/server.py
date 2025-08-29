"""
HotVolume - Application Volume Controller
Main application that provides system-wide volume control for individual applications using hotkeys
"""

import logging
import threading
import time
import sys
import os
from pathlib import Path

# Import our custom modules
from audio_controller import AudioController
from hotkey_manager import HotkeyManager
from app_detector import AppDetector
from tray_interface import TrayInterface
from config_gui import ConfigGUI

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('hotvolume.log')
    ]
)
logger = logging.getLogger(__name__)

class HotVolumeApp:
    def __init__(self):
        """Initialize the HotVolume application"""
        logger.info("Initializing HotVolume application...")
        
        # Initialize core components
        self.audio_controller = AudioController()
        self.app_detector = AppDetector()
        self.hotkey_manager = HotkeyManager(self.audio_controller)
        self.config_gui = None
        self.tray_interface = None
        
        self.running = False
    
    def setup_default_hotkeys(self):
        """Set up default hotkey mappings"""
        logger.info("Setting up default hotkeys...")
        
        # Don't overwrite existing saved configurations
        if not self.hotkey_manager.app_mappings:
            default_mappings = [
                # Spotify controls (updated to use capital S)
                ('ctrl+shift+f1', 'Spotify.exe', 'decrease', 0.1),
                ('ctrl+shift+f2', 'Spotify.exe', 'increase', 0.1),
                ('ctrl+shift+f3', 'Spotify.exe', 'toggle_mute', 0.1),
                
                # Chrome/Browser controls
                ('ctrl+shift+f4', 'chrome.exe', 'decrease', 0.1),
                ('ctrl+shift+f5', 'chrome.exe', 'increase', 0.1),
                ('ctrl+shift+f6', 'chrome.exe', 'toggle_mute', 0.1),
                
                # Discord controls
                ('ctrl+shift+f7', 'discord.exe', 'decrease', 0.1),
                ('ctrl+shift+f8', 'discord.exe', 'increase', 0.1),
                ('ctrl+shift+f9', 'discord.exe', 'toggle_mute', 0.1),
            ]
            
            for hotkey, app, action, step in default_mappings:
                success = self.hotkey_manager.add_hotkey_mapping(hotkey, app, action, step)
                if success:
                    logger.info(f"Added default hotkey: {hotkey} -> {app} ({action})")
        else:
            logger.info("Using existing saved hotkey configuration")
    
    def config_callback(self):
        """Callback to open configuration GUI"""
        if not self.config_gui:
            self.config_gui = ConfigGUI(
                self.audio_controller,
                self.hotkey_manager,
                self.app_detector
            )
        
        self.config_gui.show()
    
    def start(self):
        """Start the HotVolume application"""
        try:
            logger.info("Starting HotVolume application...")
            
            # Set up default hotkeys
            self.setup_default_hotkeys()
            
            # Start hotkey listener
            logger.info("Starting hotkey listener...")
            if not self.hotkey_manager.start_hotkey_listener():
                logger.error("Failed to start hotkey listener")
                return False
            
            # Initialize tray interface
            logger.info("Initializing system tray interface...")
            self.tray_interface = TrayInterface(
                self.audio_controller,
                self.hotkey_manager,
                self.config_callback
            )
            
            self.running = True
            
            # Show initial information
            logger.info("HotVolume is now running!")
            logger.info("Available hotkeys:")
            for hotkey, mapping in self.hotkey_manager.get_active_mappings().items():
                logger.info(f"  {hotkey}: {mapping['action']} {mapping['app']}")
            
            # Start tray interface (this will block)
            logger.info("Starting system tray interface...")
            self.tray_interface.start()
            
        except KeyboardInterrupt:
            logger.info("Received keyboard interrupt")
        except Exception as e:
            logger.error(f"Error starting application: {e}")
        finally:
            self.stop()
        
        return True
    
    def stop(self):
        """Stop the HotVolume application"""
        logger.info("Stopping HotVolume application...")
        
        self.running = False
        
        # Stop hotkey listener
        if self.hotkey_manager:
            self.hotkey_manager.stop_hotkey_listener()
        
        # Stop tray interface
        if self.tray_interface:
            self.tray_interface.stop()
        
        # Close config GUI
        if self.config_gui and self.config_gui.window_open:
            self.config_gui.on_closing()
        
        logger.info("HotVolume application stopped")
    
    def test_functionality(self):
        """Test the core functionality"""
        logger.info("Testing HotVolume functionality...")
        
        # Test audio controller
        logger.info("Testing audio controller...")
        apps = self.audio_controller.get_available_apps()
        logger.info(f"Found {len(apps)} applications with audio sessions:")
        for app in apps:
            volume = self.audio_controller.get_app_volume(app)
            logger.info(f"  {app}: Volume = {volume}")
        
        # Test app detector
        logger.info("Testing app detector...")
        audio_apps = self.app_detector.get_audio_capable_apps()
        logger.info(f"Found {len(audio_apps)} audio-capable applications")
        
        # Test hotkey manager
        logger.info("Testing hotkey manager...")
        test_hotkey = "ctrl+shift+t"
        if self.hotkey_manager.test_hotkey(test_hotkey):
            logger.info(f"Hotkey format '{test_hotkey}' is valid")
        
        return True

def main():
    """Main entry point"""
    logger.info("=" * 60)
    logger.info("HotVolume - Application Volume Controller v1.0")
    logger.info("=" * 60)
    
    # Check if running on Windows
    if os.name != 'nt':
        logger.error("This application is designed for Windows only")
        sys.exit(1)
    
    # Create and start the application
    app = HotVolumeApp()
    
    # Handle command line arguments
    if len(sys.argv) > 1:
        if sys.argv[1] == '--test':
            app.test_functionality()
            return
        elif sys.argv[1] == '--config':
            app.config_callback()
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                pass
            return
    
    # Normal startup
    try:
        app.start()
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
