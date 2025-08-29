"""
Windows Audio Session API Controller
Handles volume control for individual applications
"""

import ctypes
from ctypes import wintypes
from comtypes import CLSCTX_ALL, GUID
from pycaw.pycaw import AudioUtilities, AudioSession, ISimpleAudioVolume
import logging

logger = logging.getLogger(__name__)

class AudioController:
    def __init__(self):
        """Initialize the audio controller"""
        self.sessions = {}
        self.refresh_sessions()
    
    def refresh_sessions(self):
        """Refresh the list of available audio sessions"""
        try:
            self.sessions.clear()
            sessions = AudioUtilities.GetAllSessions()
            
            for session in sessions:
                if session.Process and session.Process.name():
                    process_name = session.Process.name()
                    if process_name not in self.sessions:
                        self.sessions[process_name] = []
                    
                    # Get the simple audio volume interface
                    volume = session.SimpleAudioVolume
                    if volume:
                        self.sessions[process_name].append({
                            'session': session,
                            'volume': volume,
                            'pid': session.Process.pid if session.Process else None
                        })
            
            logger.info(f"Found {len(self.sessions)} applications with audio sessions")
            return True
            
        except Exception as e:
            logger.error(f"Error refreshing audio sessions: {e}")
            return False
    
    def get_available_apps(self):
        """Get list of applications currently playing audio"""
        self.refresh_sessions()
        return list(self.sessions.keys())
    
    def get_app_volume(self, app_name):
        """Get current volume level for an application (0.0 to 1.0)"""
        try:
            if app_name in self.sessions:
                # Get the first session for this app
                session_info = self.sessions[app_name][0]
                volume_interface = session_info['volume']
                current_volume = volume_interface.GetMasterVolume()
                logger.info(f"Current volume for {app_name}: {current_volume}")
                return current_volume
            else:
                logger.warning(f"Application {app_name} not found in audio sessions")
                return None
        except Exception as e:
            logger.error(f"Error getting volume for {app_name}: {e}")
            return None
    
    def set_app_volume(self, app_name, volume_level):
        """Set volume level for an application (0.0 to 1.0)"""
        try:
            if app_name in self.sessions:
                # Set volume for all sessions of this app
                for session_info in self.sessions[app_name]:
                    volume_interface = session_info['volume']
                    volume_interface.SetMasterVolume(volume_level, None)
                
                logger.info(f"Set volume for {app_name} to {volume_level}")
                return True
            else:
                logger.warning(f"Application {app_name} not found in audio sessions")
                return False
                
        except Exception as e:
            logger.error(f"Error setting volume for {app_name}: {e}")
            return False
    
    def increase_app_volume(self, app_name, step=0.1):
        """Increase volume for an application by specified step"""
        current_volume = self.get_app_volume(app_name)
        if current_volume is not None:
            new_volume = min(1.0, current_volume + step)
            return self.set_app_volume(app_name, new_volume)
        return False
    
    def decrease_app_volume(self, app_name, step=0.1):
        """Decrease volume for an application by specified step"""
        current_volume = self.get_app_volume(app_name)
        if current_volume is not None:
            new_volume = max(0.0, current_volume - step)
            return self.set_app_volume(app_name, new_volume)
        return False
    
    def mute_app(self, app_name, mute=True):
        """Mute or unmute an application"""
        try:
            if app_name in self.sessions:
                for session_info in self.sessions[app_name]:
                    volume_interface = session_info['volume']
                    volume_interface.SetMute(mute, None)
                
                logger.info(f"{'Muted' if mute else 'Unmuted'} {app_name}")
                return True
            else:
                logger.warning(f"Application {app_name} not found in audio sessions")
                return False
                
        except Exception as e:
            logger.error(f"Error muting {app_name}: {e}")
            return False
    
    def is_app_muted(self, app_name):
        """Check if an application is muted"""
        try:
            if app_name in self.sessions:
                session_info = self.sessions[app_name][0]
                volume_interface = session_info['volume']
                is_muted = volume_interface.GetMute()
                return is_muted
            return None
        except Exception as e:
            logger.error(f"Error checking mute status for {app_name}: {e}")
            return None

# Test the audio controller
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    controller = AudioController()
    apps = controller.get_available_apps()
    
    print("Available applications with audio:")
    for app in apps:
        volume = controller.get_app_volume(app)
        muted = controller.is_app_muted(app)
        print(f"  {app}: Volume={volume:.2f}, Muted={muted}")