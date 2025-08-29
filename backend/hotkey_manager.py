"""
Global Hotkey Manager
Handles registration and execution of global keyboard shortcuts
"""

import keyboard
import threading
import logging
from typing import Dict, Callable, List
import time
import json
import os
from pathlib import Path

logger = logging.getLogger(__name__)

class HotkeyManager:
    def __init__(self, audio_controller=None):
        """Initialize the hotkey manager"""
        self.audio_controller = audio_controller
        self.registered_hotkeys = {}
        self.app_mappings = {}
        self.is_running = False
        self.hotkey_thread = None
        
        # Configuration file path
        self.config_file = Path("hotkey_config.json")
        
        # Default hotkey mappings
        self.default_hotkeys = {
            'ctrl+shift+f1': {'app': 'Spotify.exe', 'action': 'decrease'},
            'ctrl+shift+f2': {'app': 'Spotify.exe', 'action': 'increase'},
            'ctrl+shift+f3': {'app': 'Spotify.exe', 'action': 'toggle_mute'},
            'ctrl+shift+f4': {'app': 'chrome.exe', 'action': 'decrease'},
            'ctrl+shift+f5': {'app': 'chrome.exe', 'action': 'increase'},
            'ctrl+shift+f6': {'app': 'chrome.exe', 'action': 'toggle_mute'},
            'ctrl+shift+f7': {'app': 'discord.exe', 'action': 'decrease'},
            'ctrl+shift+f8': {'app': 'discord.exe', 'action': 'increase'},
            'ctrl+shift+f9': {'app': 'discord.exe', 'action': 'toggle_mute'},
        }
        
        # Load saved configuration
        self.load_configuration()
    
    def set_audio_controller(self, controller):
        """Set the audio controller instance"""
        self.audio_controller = controller
    
    def add_hotkey_mapping(self, hotkey: str, app_name: str, action: str, step: float = 0.1):
        """Add a new hotkey mapping"""
        try:
            mapping = {
                'app': app_name,
                'action': action,  # 'increase', 'decrease', 'mute', 'unmute'
                'step': step
            }
            self.app_mappings[hotkey] = mapping
            logger.info(f"Added hotkey mapping: {hotkey} -> {app_name} ({action})")
            
            # Save configuration
            self.save_configuration()
            
            # If hotkeys are already running, register this new one
            if self.is_running:
                self._register_single_hotkey(hotkey, mapping)
            
            return True
        except Exception as e:
            logger.error(f"Error adding hotkey mapping {hotkey}: {e}")
            return False
    
    def remove_hotkey_mapping(self, hotkey: str):
        """Remove a hotkey mapping"""
        try:
            if hotkey in self.app_mappings:
                del self.app_mappings[hotkey]
                
                # Save configuration
                self.save_configuration()
                
                # If hotkeys are running, unregister this one
                if self.is_running:
                    keyboard.remove_hotkey(hotkey)
                    if hotkey in self.registered_hotkeys:
                        del self.registered_hotkeys[hotkey]
                
                logger.info(f"Removed hotkey mapping: {hotkey}")
                return True
        except Exception as e:
            logger.error(f"Error removing hotkey mapping {hotkey}: {e}")
        return False
    
    def _register_single_hotkey(self, hotkey: str, mapping: Dict):
        """Register a single hotkey"""
        try:
            def hotkey_callback():
                self._execute_hotkey_action(mapping)
            
            # Register the hotkey with keyboard library
            keyboard.add_hotkey(hotkey, hotkey_callback, suppress=True)
            self.registered_hotkeys[hotkey] = mapping
            logger.info(f"Registered hotkey: {hotkey}")
            
        except Exception as e:
            logger.error(f"Error registering hotkey {hotkey}: {e}")
    
    def _execute_hotkey_action(self, mapping: Dict):
        """Execute the action for a hotkey"""
        try:
            if not self.audio_controller:
                logger.error("No audio controller available")
                return
            
            app_name = mapping['app']
            action = mapping['action']
            step = mapping.get('step', 0.1)
            
            logger.info(f"Executing action: {action} on {app_name}")
            
            # Refresh audio sessions to get latest state
            self.audio_controller.refresh_sessions()
            
            if action == 'increase':
                success = self.audio_controller.increase_app_volume(app_name, step)
            elif action == 'decrease':
                success = self.audio_controller.decrease_app_volume(app_name, step)
            elif action == 'mute':
                success = self.audio_controller.mute_app(app_name, True)
            elif action == 'unmute':
                success = self.audio_controller.mute_app(app_name, False)
            elif action == 'toggle_mute':
                # Check current mute status and toggle
                is_muted = self.audio_controller.is_app_muted(app_name)
                if is_muted is not None:
                    success = self.audio_controller.mute_app(app_name, not is_muted)
                else:
                    success = False
            else:
                logger.error(f"Unknown action: {action}")
                return
            
            if success:
                logger.info(f"Successfully executed {action} on {app_name}")
            else:
                logger.warning(f"Failed to execute {action} on {app_name} - app may not be running or have audio")
                
        except Exception as e:
            logger.error(f"Error executing hotkey action: {e}")
    
    def load_default_mappings(self):
        """Load default hotkey mappings"""
        for hotkey, mapping in self.default_hotkeys.items():
            self.add_hotkey_mapping(
                hotkey, 
                mapping['app'], 
                mapping['action'], 
                mapping.get('step', 0.1)
            )
    
    def start_hotkey_listener(self):
        """Start listening for hotkeys"""
        try:
            if self.is_running:
                logger.warning("Hotkey listener is already running")
                return True
            
            # Register all current mappings
            for hotkey, mapping in self.app_mappings.items():
                self._register_single_hotkey(hotkey, mapping)
            
            self.is_running = True
            
            def hotkey_listener():
                try:
                    logger.info("Hotkey listener started")
                    keyboard.wait()  # This blocks until keyboard.stop() is called
                except Exception as e:
                    logger.error(f"Error in hotkey listener: {e}")
                finally:
                    self.is_running = False
            
            # Start the listener in a separate thread
            self.hotkey_thread = threading.Thread(target=hotkey_listener, daemon=True)
            self.hotkey_thread.start()
            
            logger.info(f"Started hotkey listener with {len(self.app_mappings)} mappings")
            return True
            
        except Exception as e:
            logger.error(f"Error starting hotkey listener: {e}")
            return False
    
    def stop_hotkey_listener(self):
        """Stop listening for hotkeys"""
        try:
            if not self.is_running:
                logger.warning("Hotkey listener is not running")
                return True
            
            # Unregister all hotkeys
            for hotkey in list(self.registered_hotkeys.keys()):
                keyboard.remove_hotkey(hotkey)
            
            self.registered_hotkeys.clear()
            keyboard.unhook_all_hotkeys()
            
            self.is_running = False
            logger.info("Stopped hotkey listener")
            return True
            
        except Exception as e:
            logger.error(f"Error stopping hotkey listener: {e}")
            return False
    
    def get_active_mappings(self) -> Dict:
        """Get all current hotkey mappings"""
        return self.app_mappings.copy()
    
    def is_hotkey_registered(self, hotkey: str) -> bool:
        """Check if a hotkey is already registered"""
        return hotkey in self.registered_hotkeys
    
    def test_hotkey(self, hotkey: str):
        """Test if a hotkey combination is valid"""
        try:
            # Try to parse the hotkey
            keyboard.parse_hotkey(hotkey)
            return True
        except Exception as e:
            logger.error(f"Invalid hotkey format '{hotkey}': {e}")
            return False
    
    def save_configuration(self):
        """Save current hotkey configuration to file"""
        try:
            config_data = {
                'app_mappings': self.app_mappings,
                'version': '1.0'
            }
            
            with open(self.config_file, 'w') as f:
                json.dump(config_data, f, indent=2)
            
            logger.info(f"Configuration saved to {self.config_file}")
            return True
        except Exception as e:
            logger.error(f"Error saving configuration: {e}")
            return False
    
    def load_configuration(self):
        """Load hotkey configuration from file"""
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r') as f:
                    config_data = json.load(f)
                
                # Load mappings
                if 'app_mappings' in config_data:
                    self.app_mappings = config_data['app_mappings']
                    logger.info(f"Loaded {len(self.app_mappings)} hotkey mappings from {self.config_file}")
                else:
                    logger.info("No saved mappings found, using defaults")
                    self.load_default_mappings()
                
                return True
            else:
                logger.info("No configuration file found, using defaults")
                self.load_default_mappings()
                return True
        except Exception as e:
            logger.error(f"Error loading configuration: {e}")
            logger.info("Loading default mappings instead")
            self.load_default_mappings()
            return False

# Test the hotkey manager
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    # Import audio controller for testing
    from audio_controller import AudioController
    
    print("Initializing hotkey manager...")
    audio_ctrl = AudioController()
    hotkey_mgr = HotkeyManager(audio_ctrl)
    
    # Load default mappings
    hotkey_mgr.load_default_mappings()
    
    print("Active hotkey mappings:")
    for hotkey, mapping in hotkey_mgr.get_active_mappings().items():
        print(f"  {hotkey}: {mapping['action']} {mapping['app']}")
    
    print("\nStarting hotkey listener...")
    print("Try pressing Ctrl+Shift+F1 or F2 to control Spotify volume")
    print("Press Ctrl+C to exit")
    
    hotkey_mgr.start_hotkey_listener()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping hotkey listener...")
        hotkey_mgr.stop_hotkey_listener()