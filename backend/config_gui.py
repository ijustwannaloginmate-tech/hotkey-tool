"""
Configuration GUI
Provides a graphical interface for configuring hotkeys and application mappings
"""

import tkinter as tk
from tkinter import ttk, messagebox
import logging
from typing import Dict, List
import threading

logger = logging.getLogger(__name__)

class ConfigGUI:
    def __init__(self, audio_controller=None, hotkey_manager=None, app_detector=None):
        """Initialize the configuration GUI"""
        self.audio_controller = audio_controller
        self.hotkey_manager = hotkey_manager
        self.app_detector = app_detector
        
        self.root = None
        self.hotkey_listbox = None
        self.app_combo = None
        self.action_combo = None
        self.hotkey_entry = None
        self.step_var = None
        
        self.window_open = False
    
    def create_window(self):
        """Create the main configuration window"""
        if self.window_open:
            logger.warning("Configuration window is already open")
            return
        
        self.root = tk.Tk()
        self.root.title("HotVolume Configuration")
        self.root.geometry("700x500")
        self.root.resizable(True, True)
        
        # Set window icon (if we had an icon file)
        try:
            # self.root.iconbitmap("icon.ico")
            pass
        except:
            pass
        
        self.window_open = True
        
        # Handle window close
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Create the UI elements
        self.create_widgets()
        self.refresh_data()
    
    def create_widgets(self):
        """Create all GUI widgets"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="HotVolume Configuration", font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Current hotkeys section
        hotkey_frame = ttk.LabelFrame(main_frame, text="Current Hotkey Mappings", padding="10")
        hotkey_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 20))
        hotkey_frame.columnconfigure(0, weight=1)
        hotkey_frame.rowconfigure(0, weight=1)
        
        # Hotkey listbox with scrollbar
        listbox_frame = ttk.Frame(hotkey_frame)
        listbox_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        listbox_frame.columnconfigure(0, weight=1)
        listbox_frame.rowconfigure(0, weight=1)
        
        self.hotkey_listbox = tk.Listbox(listbox_frame, height=8)
        self.hotkey_listbox.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        scrollbar = ttk.Scrollbar(listbox_frame, orient=tk.VERTICAL, command=self.hotkey_listbox.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.hotkey_listbox.configure(yscrollcommand=scrollbar.set)
        
        # Buttons for hotkey management
        button_frame = ttk.Frame(hotkey_frame)
        button_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(10, 0))
        
        ttk.Button(button_frame, text="Remove Selected", command=self.remove_hotkey).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="Refresh", command=self.refresh_hotkeys).pack(side=tk.LEFT)
        
        # Add new hotkey section
        add_frame = ttk.LabelFrame(main_frame, text="Add New Hotkey", padding="10")
        add_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 20))
        add_frame.columnconfigure(1, weight=1)
        
        # Hotkey input
        ttk.Label(add_frame, text="Hotkey:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        self.hotkey_entry = ttk.Entry(add_frame, width=30)
        self.hotkey_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 10))
        ttk.Label(add_frame, text="(e.g., ctrl+shift+f1)").grid(row=0, column=2, sticky=tk.W)
        
        # Application selection
        ttk.Label(add_frame, text="Application:").grid(row=1, column=0, sticky=tk.W, padx=(0, 10), pady=(10, 0))
        self.app_combo = ttk.Combobox(add_frame, width=40, state="readonly")
        self.app_combo.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(0, 10), pady=(10, 0))
        
        # Action selection
        ttk.Label(add_frame, text="Action:").grid(row=2, column=0, sticky=tk.W, padx=(0, 10), pady=(10, 0))
        self.action_combo = ttk.Combobox(add_frame, values=["increase", "decrease", "mute", "unmute", "toggle_mute"], state="readonly")
        self.action_combo.grid(row=2, column=1, sticky=(tk.W, tk.E), padx=(0, 10), pady=(10, 0))
        self.action_combo.set("increase")
        
        # Step size
        ttk.Label(add_frame, text="Step Size:").grid(row=3, column=0, sticky=tk.W, padx=(0, 10), pady=(10, 0))
        self.step_var = tk.DoubleVar(value=0.1)
        step_spinbox = ttk.Spinbox(add_frame, from_=0.01, to=1.0, increment=0.01, textvariable=self.step_var, width=10)
        step_spinbox.grid(row=3, column=1, sticky=tk.W, padx=(0, 10), pady=(10, 0))
        
        # Add button
        ttk.Button(add_frame, text="Add Hotkey", command=self.add_hotkey).grid(row=4, column=0, columnspan=2, pady=(15, 0))
        
        # Control buttons
        control_frame = ttk.Frame(main_frame)
        control_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E))
        
        ttk.Button(control_frame, text="Start Hotkeys", command=self.start_hotkeys).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(control_frame, text="Stop Hotkeys", command=self.stop_hotkeys).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(control_frame, text="Test Hotkey", command=self.test_hotkey).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(control_frame, text="Close", command=self.on_closing).pack(side=tk.RIGHT)
    
    def refresh_data(self):
        """Refresh all data in the GUI"""
        self.refresh_hotkeys()
        self.refresh_applications()
    
    def refresh_hotkeys(self):
        """Refresh the hotkey listbox"""
        if not self.hotkey_listbox or not self.hotkey_manager:
            return
        
        try:
            self.hotkey_listbox.delete(0, tk.END)
            
            mappings = self.hotkey_manager.get_active_mappings()
            for hotkey, mapping in mappings.items():
                display_text = f"{hotkey} → {mapping['app']} ({mapping['action']})"
                if mapping.get('step'):
                    display_text += f" [step: {mapping['step']:.2f}]"
                self.hotkey_listbox.insert(tk.END, display_text)
                
        except Exception as e:
            logger.error(f"Error refreshing hotkeys: {e}")
    
    def refresh_applications(self):
        """Refresh the application combobox"""
        if not self.app_combo:
            return
        
        try:
            apps = []
            
            # Get applications from audio controller
            if self.audio_controller:
                audio_apps = self.audio_controller.get_available_apps()
                apps.extend(audio_apps)
            
            # Get applications from app detector
            if self.app_detector:
                detected_apps = self.app_detector.get_audio_capable_apps()
                for app in detected_apps:
                    if app['name'] not in apps:
                        apps.append(app['name'])
            
            # Add common applications even if not currently running
            common_apps = ['spotify.exe', 'chrome.exe', 'firefox.exe', 'discord.exe', 'steam.exe', 'vlc.exe']
            for app in common_apps:
                if app not in apps:
                    apps.append(app)
            
            apps.sort()
            self.app_combo['values'] = apps
            
            if apps and not self.app_combo.get():
                self.app_combo.set(apps[0])
                
        except Exception as e:
            logger.error(f"Error refreshing applications: {e}")
    
    def add_hotkey(self):
        """Add a new hotkey mapping"""
        try:
            hotkey = self.hotkey_entry.get().strip()
            app = self.app_combo.get()
            action = self.action_combo.get()
            step = self.step_var.get()
            
            if not hotkey:
                messagebox.showerror("Error", "Please enter a hotkey combination")
                return
            
            if not app:
                messagebox.showerror("Error", "Please select an application")
                return
            
            if not action:
                messagebox.showerror("Error", "Please select an action")
                return
            
            # Test if hotkey format is valid
            if self.hotkey_manager and not self.hotkey_manager.test_hotkey(hotkey):
                messagebox.showerror("Error", "Invalid hotkey format")
                return
            
            # Add the hotkey mapping
            if self.hotkey_manager:
                success = self.hotkey_manager.add_hotkey_mapping(hotkey, app, action, step)
                if success:
                    self.refresh_hotkeys()
                    self.hotkey_entry.delete(0, tk.END)
                    messagebox.showinfo("Success", f"Added hotkey: {hotkey}")
                else:
                    messagebox.showerror("Error", "Failed to add hotkey mapping")
            
        except Exception as e:
            logger.error(f"Error adding hotkey: {e}")
            messagebox.showerror("Error", f"Failed to add hotkey: {str(e)}")
    
    def remove_hotkey(self):
        """Remove the selected hotkey mapping"""
        try:
            selection = self.hotkey_listbox.curselection()
            if not selection:
                messagebox.showwarning("Warning", "Please select a hotkey to remove")
                return
            
            # Get the hotkey from the selected text
            selected_text = self.hotkey_listbox.get(selection[0])
            hotkey = selected_text.split(" →")[0]
            
            if self.hotkey_manager:
                success = self.hotkey_manager.remove_hotkey_mapping(hotkey)
                if success:
                    self.refresh_hotkeys()
                    messagebox.showinfo("Success", f"Removed hotkey: {hotkey}")
                else:
                    messagebox.showerror("Error", "Failed to remove hotkey mapping")
            
        except Exception as e:
            logger.error(f"Error removing hotkey: {e}")
            messagebox.showerror("Error", f"Failed to remove hotkey: {str(e)}")
    
    def start_hotkeys(self):
        """Start the hotkey listener"""
        if self.hotkey_manager:
            success = self.hotkey_manager.start_hotkey_listener()
            if success:
                messagebox.showinfo("Success", "Hotkey listener started")
            else:
                messagebox.showerror("Error", "Failed to start hotkey listener")
    
    def stop_hotkeys(self):
        """Stop the hotkey listener"""
        if self.hotkey_manager:
            success = self.hotkey_manager.stop_hotkey_listener()
            if success:
                messagebox.showinfo("Success", "Hotkey listener stopped")
            else:
                messagebox.showerror("Error", "Failed to stop hotkey listener")
    
    def test_hotkey(self):
        """Test if a hotkey format is valid"""
        hotkey = self.hotkey_entry.get().strip()
        if not hotkey:
            messagebox.showwarning("Warning", "Please enter a hotkey to test")
            return
        
        if self.hotkey_manager:
            if self.hotkey_manager.test_hotkey(hotkey):
                messagebox.showinfo("Success", f"Hotkey format '{hotkey}' is valid")
            else:
                messagebox.showerror("Error", f"Invalid hotkey format: '{hotkey}'")
    
    def on_closing(self):
        """Handle window closing"""
        try:
            self.window_open = False
            if self.root:
                self.root.withdraw()  # Hide instead of destroy
                logger.info("Configuration window hidden")
        except Exception as e:
            logger.error(f"Error hiding configuration window: {e}")
    
    def show(self):
        """Show the configuration window"""
        def run_gui():
            if not self.root:
                self.create_window()
            else:
                # Refresh data and show existing window
                self.refresh_data()
                self.root.deiconify()  # Show the window
                self.root.lift()
                self.root.attributes('-topmost', True)
                self.root.attributes('-topmost', False)
            
            if self.root:
                self.root.mainloop()
        
        if not self.window_open:
            self.window_open = True
            gui_thread = threading.Thread(target=run_gui, daemon=True)
            gui_thread.start()
        else:
            # Bring existing window to front
            if self.root:
                self.root.deiconify()
                self.root.lift()
                self.root.attributes('-topmost', True)
                self.root.attributes('-topmost', False)

# Test the configuration GUI
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    from audio_controller import AudioController
    from hotkey_manager import HotkeyManager
    from app_detector import AppDetector
    
    # Initialize components
    audio_ctrl = AudioController()
    hotkey_mgr = HotkeyManager(audio_ctrl)
    app_detect = AppDetector()
    
    # Load default mappings
    hotkey_mgr.load_default_mappings()
    
    # Create and show GUI
    config_gui = ConfigGUI(audio_ctrl, hotkey_mgr, app_detect)
    config_gui.show()
    
    # Keep the main thread alive
    import time
    try:
        while config_gui.window_open:
            time.sleep(1)
    except KeyboardInterrupt:
        pass