"""
Application Process Detection
Handles detection and monitoring of running applications
"""

import psutil
import pygetwindow as gw
import logging
from typing import List, Dict
import time

logger = logging.getLogger(__name__)

class AppDetector:
    def __init__(self):
        """Initialize the application detector"""
        self.common_apps = {
            'spotify.exe': 'Spotify',
            'Spotify.exe': 'Spotify',
            'chrome.exe': 'Google Chrome',
            'firefox.exe': 'Mozilla Firefox',
            'msedge.exe': 'Microsoft Edge',
            'discord.exe': 'Discord',
            'cs2.exe': 'Counter-Strike 2',
            'csgo.exe': 'Counter-Strike: Global Offensive',
            'steam.exe': 'Steam',
            'vlc.exe': 'VLC Media Player',
            'winamp.exe': 'Winamp',
            'foobar2000.exe': 'Foobar2000',
            'musicbee.exe': 'MusicBee',
            'itunes.exe': 'iTunes',
            'wmplayer.exe': 'Windows Media Player',
            'groove.exe': 'Groove Music',
            'deezer.exe': 'Deezer',
            'tidal.exe': 'Tidal',
            'youtube.exe': 'YouTube Music',
            'amazonmusic.exe': 'Amazon Music',
            'audacity.exe': 'Audacity',
            'obs64.exe': 'OBS Studio',
            'obs32.exe': 'OBS Studio',
            'streamlabs obs.exe': 'Streamlabs OBS',
            'teams.exe': 'Microsoft Teams',
            'zoom.exe': 'Zoom',
            'skype.exe': 'Skype',
            'slack.exe': 'Slack'
        }
    
    def get_running_processes(self) -> List[Dict]:
        """Get all currently running processes"""
        processes = []
        try:
            for process in psutil.process_iter(['pid', 'name', 'exe']):
                try:
                    proc_info = process.info
                    if proc_info['name'] and proc_info['exe']:
                        display_name = self.common_apps.get(proc_info['name'].lower(), proc_info['name'])
                        processes.append({
                            'pid': proc_info['pid'],
                            'name': proc_info['name'],
                            'exe': proc_info['exe'],
                            'display_name': display_name
                        })
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
        except Exception as e:
            logger.error(f"Error getting running processes: {e}")
        
        return processes
    
    def get_audio_capable_apps(self) -> List[Dict]:
        """Get applications that are likely to produce audio"""
        audio_keywords = [
            'spotify', 'chrome', 'firefox', 'edge', 'discord', 'steam',
            'vlc', 'winamp', 'foobar', 'itunes', 'groove', 'music',
            'media', 'player', 'youtube', 'deezer', 'tidal', 'amazon',
            'audacity', 'obs', 'teams', 'zoom', 'skype', 'slack',
            'cs2', 'csgo', 'game', 'audio', 'sound'
        ]
        
        all_processes = self.get_running_processes()
        audio_apps = []
        
        for process in all_processes:
            process_name = process['name'].lower()
            exe_path = process['exe'].lower() if process['exe'] else ''
            
            # Check if process name or path contains audio-related keywords
            if any(keyword in process_name or keyword in exe_path for keyword in audio_keywords):
                audio_apps.append(process)
            
            # Also include processes that are in our common apps list
            elif process_name in self.common_apps:
                audio_apps.append(process)
        
        return audio_apps
    
    def get_visible_windows(self) -> List[Dict]:
        """Get all visible windows"""
        windows = []
        try:
            for window in gw.getAllWindows():
                if window.title and window.visible and not window.isMinimized:
                    windows.append({
                        'title': window.title,
                        'pid': None,  # pygetwindow doesn't provide PID directly
                        'x': window.left,
                        'y': window.top,
                        'width': window.width,
                        'height': window.height
                    })
        except Exception as e:
            logger.error(f"Error getting visible windows: {e}")
        
        return windows
    
    def find_process_by_name(self, process_name: str) -> List[Dict]:
        """Find processes by name (partial match)"""
        matching_processes = []
        all_processes = self.get_running_processes()
        
        for process in all_processes:
            if process_name.lower() in process['name'].lower():
                matching_processes.append(process)
        
        return matching_processes
    
    def is_process_running(self, process_name: str) -> bool:
        """Check if a specific process is running"""
        try:
            for process in psutil.process_iter(['name']):
                if process.info['name'] and process_name.lower() in process.info['name'].lower():
                    return True
        except Exception as e:
            logger.error(f"Error checking if process {process_name} is running: {e}")
        
        return False
    
    def get_process_by_pid(self, pid: int) -> Dict:
        """Get process information by PID"""
        try:
            process = psutil.Process(pid)
            return {
                'pid': pid,
                'name': process.name(),
                'exe': process.exe(),
                'display_name': self.common_apps.get(process.name().lower(), process.name())
            }
        except (psutil.NoSuchProcess, psutil.AccessDenied) as e:
            logger.error(f"Error getting process with PID {pid}: {e}")
            return None
    
    def monitor_processes(self, callback=None, interval=5):
        """Monitor processes for changes (for future use)"""
        previous_processes = set()
        
        while True:
            try:
                current_processes = set(p['name'] for p in self.get_running_processes())
                
                # New processes
                new_processes = current_processes - previous_processes
                if new_processes and callback:
                    callback('added', list(new_processes))
                
                # Closed processes
                closed_processes = previous_processes - current_processes
                if closed_processes and callback:
                    callback('removed', list(closed_processes))
                
                previous_processes = current_processes
                time.sleep(interval)
                
            except KeyboardInterrupt:
                logger.info("Process monitoring stopped")
                break
            except Exception as e:
                logger.error(f"Error in process monitoring: {e}")
                time.sleep(interval)

# Test the app detector
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    detector = AppDetector()
    
    print("Audio-capable applications:")
    audio_apps = detector.get_audio_capable_apps()
    for app in audio_apps[:10]:  # Show first 10
        print(f"  {app['display_name']} ({app['name']}) - PID: {app['pid']}")
    
    print(f"\nTotal audio-capable apps found: {len(audio_apps)}")
    
    # Test if Spotify is running
    if detector.is_process_running('spotify'):
        print("\nSpotify is currently running!")
    else:
        print("\nSpotify is not running.")