"""
System Tray Interface
Provides a system tray icon and menu for the volume control application
"""

import pystray
from PIL import Image, ImageDraw
import threading
import logging
from pathlib import Path
import base64
import io

logger = logging.getLogger(__name__)

class TrayInterface:
    def __init__(self, audio_controller=None, hotkey_manager=None, config_callback=None):
        """Initialize the system tray interface"""
        self.audio_controller = audio_controller
        self.hotkey_manager = hotkey_manager
        self.config_callback = config_callback
        self.icon = None
        self.is_running = False
    
    def create_icon_image(self):
        """Create a simple icon image for the system tray"""
        # Create a 64x64 image with a volume icon
        width = 64
        height = 64
        image = Image.new('RGB', (width, height), color='black')
        draw = ImageDraw.Draw(image)
        
        # Draw a simple speaker icon
        # Speaker body
        draw.rectangle([10, 20, 25, 44], fill='white')
        # Speaker cone
        draw.polygon([(25, 20), (40, 15), (40, 49), (25, 44)], fill='white')
        # Sound waves
        draw.arc([45, 18, 55, 28], 0, 180, fill='white', width=2)
        draw.arc([48, 25, 58, 35], 0, 180, fill='white', width=2)
        draw.arc([51, 32, 61, 42], 0, 180, fill='white', width=2)
        
        return image
    
    def get_menu_items(self):
        """Generate menu items for the tray icon"""
        menu_items = []
        
        # Quick volume controls for common apps
        if self.audio_controller:
            apps = self.audio_controller.get_available_apps()
            if apps:
                menu_items.append(pystray.MenuItem("Quick Controls", None, enabled=False))
                
                for app in apps[:5]:  # Show first 5 apps
                    app_menu = pystray.Menu(
                        pystray.MenuItem(f"Volume Up", lambda _, app=app: self.quick_volume_up(app)),
                        pystray.MenuItem(f"Volume Down", lambda _, app=app: self.quick_volume_down(app)),
                        pystray.MenuItem(f"Mute", lambda _, app=app: self.quick_mute_toggle(app))
                    )
                    menu_items.append(pystray.MenuItem(app, app_menu))
                
                menu_items.append(pystray.MenuItem("", None))  # Separator
        
        # Configuration and status
        menu_items.extend([
            pystray.MenuItem("Configure Hotkeys", self.open_config),
            pystray.MenuItem("Refresh Apps", self.refresh_apps),
            pystray.MenuItem("", None),  # Separator
        ])
        
        # Hotkey status
        if self.hotkey_manager:
            if self.hotkey_manager.is_running:
                menu_items.append(pystray.MenuItem("Hotkeys: Active ✓", self.toggle_hotkeys))
            else:
                menu_items.append(pystray.MenuItem("Hotkeys: Inactive ✗", self.toggle_hotkeys))
        
        menu_items.extend([
            pystray.MenuItem("", None),  # Separator
            pystray.MenuItem("About", self.show_about),
            pystray.MenuItem("Exit", self.quit_app)
        ])
        
        return menu_items
    
    def quick_volume_up(self, app_name):
        """Quick volume up for an app"""
        if self.audio_controller:
            success = self.audio_controller.increase_app_volume(app_name, 0.1)
            logger.info(f"Volume up for {app_name}: {'Success' if success else 'Failed'}")
    
    def quick_volume_down(self, app_name):
        """Quick volume down for an app"""
        if self.audio_controller:
            success = self.audio_controller.decrease_app_volume(app_name, 0.1)
            logger.info(f"Volume down for {app_name}: {'Success' if success else 'Failed'}")
    
    def quick_mute_toggle(self, app_name):
        """Toggle mute for an app"""
        if self.audio_controller:
            is_muted = self.audio_controller.is_app_muted(app_name)
            if is_muted is not None:
                success = self.audio_controller.mute_app(app_name, not is_muted)
                logger.info(f"Toggle mute for {app_name}: {'Success' if success else 'Failed'}")
    
    def refresh_apps(self, icon=None, item=None):
        """Refresh the list of available applications"""
        if self.audio_controller:
            self.audio_controller.refresh_sessions()
            # Update the menu
            self.update_menu()
            logger.info("Refreshed application list")
    
    def open_config(self, icon=None, item=None):
        """Open the configuration window"""
        try:
            if self.config_callback:
                # Run config in a separate thread to avoid blocking the tray
                config_thread = threading.Thread(target=self.config_callback, daemon=True)
                config_thread.start()
            else:
                logger.info("Configuration window requested but no callback provided")
        except Exception as e:
            logger.error(f"Error opening configuration: {e}")
    
    def toggle_hotkeys(self, icon=None, item=None):
        """Toggle hotkey listening on/off"""
        if self.hotkey_manager:
            if self.hotkey_manager.is_running:
                self.hotkey_manager.stop_hotkey_listener()
            else:
                self.hotkey_manager.start_hotkey_listener()
            
            # Update the menu
            self.update_menu()
    
    def show_about(self, icon=None, item=None):
        """Show about information"""
        logger.info("HotVolume - Application Volume Controller v1.1")
        # In a full implementation, you might show a message box here
    
    def quit_app(self, icon=None, item=None):
        """Quit the application"""
        logger.info("Quitting application...")
        self.stop()
    
    def update_menu(self):
        """Update the tray menu"""
        if self.icon:
            menu_items = self.get_menu_items()
            self.icon.menu = pystray.Menu(*menu_items)
            self.icon.update_menu()
    
    def start(self):
        """Start the system tray interface"""
        try:
            if self.is_running:
                logger.warning("Tray interface is already running")
                return
            
            # Create the icon image
            icon_image = self.create_icon_image()
            
            # Create menu items
            menu_items = self.get_menu_items()
            menu = pystray.Menu(*menu_items)
            
            # Create the system tray icon
            self.icon = pystray.Icon(
                "HotVolume",
                icon_image,
                "HotVolume - Application Volume Controller v1.1",
                menu
            )
            
            self.is_running = True
            logger.info("Starting system tray interface...")
            
            # This will block until the icon is stopped
            self.icon.run()
            
        except Exception as e:
            logger.error(f"Error starting tray interface: {e}")
            self.is_running = False
    
    def stop(self):
        """Stop the system tray interface"""
        try:
            if self.icon:
                self.icon.stop()
            self.is_running = False
            logger.info("Stopped system tray interface")
        except Exception as e:
            logger.error(f"Error stopping tray interface: {e}")
    
    def run_in_thread(self):
        """Run the tray interface in a separate thread"""
        tray_thread = threading.Thread(target=self.start, daemon=False)
        tray_thread.start()
        return tray_thread

# Test the tray interface
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    from audio_controller import AudioController
    from hotkey_manager import HotkeyManager
    
    # Initialize components
    audio_ctrl = AudioController()
    hotkey_mgr = HotkeyManager(audio_ctrl)
    
    def config_callback():
        print("Configuration window would open here")
    
    # Create and start tray interface
    tray = TrayInterface(audio_ctrl, hotkey_mgr, config_callback)
    
    print("Starting system tray interface...")
    print("Right-click the tray icon to access controls")
    print("Press Ctrl+C to exit")
    
    try:
        tray.start()
    except KeyboardInterrupt:
        print("\nShutting down...")
        tray.stop()