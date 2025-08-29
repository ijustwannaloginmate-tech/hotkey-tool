# HotVolume v1.1 - Application Volume Controller

A Windows desktop application that allows you to control the volume of specific applications using global hotkeys. Perfect for gamers who want to quickly adjust Spotify volume while playing CS2, or control Discord volume during meetings.

## 🆕 Version 1.1 Features

- ✅ **Configuration Saving**: Custom hotkeys now save automatically
- ✅ **Background Operation**: App stays in system tray when config window is closed  
- ✅ **Updated Spotify Support**: Works with both Spotify.exe and spotify.exe
- ✅ **Improved Stability**: Better error handling and logging

## 🚀 Features

- **Individual App Volume Control**: Control volume for specific applications independently
- **Global Hotkeys**: System-wide keyboard shortcuts that work in any application
- **System Tray Integration**: Easy access through system tray icon
- **Real-time Audio Detection**: Automatically detects applications currently producing audio
- **Customizable Mappings**: Configure your own hotkey combinations
- **Quick Controls**: Right-click tray menu for instant volume adjustments
- **Persistent Settings**: Your configurations save automatically

## ⌨️ Default Hotkeys

| Hotkey | Application | Action |
|--------|------------|--------|
| `Ctrl+Shift+F1` | Spotify | Volume Down |
| `Ctrl+Shift+F2` | Spotify | Volume Up |
| `Ctrl+Shift+F3` | Spotify | Toggle Mute |
| `Ctrl+Shift+F4` | Chrome | Volume Down |
| `Ctrl+Shift+F5` | Chrome | Volume Up |
| `Ctrl+Shift+F6` | Chrome | Toggle Mute |
| `Ctrl+Shift+F7` | Discord | Volume Down |
| `Ctrl+Shift+F8` | Discord | Volume Up |
| `Ctrl+Shift+F9` | Discord | Toggle Mute |

## 💻 Installation & Usage

### Requirements
- Windows 10/11
- Python 3.7 or higher

### Quick Setup
1. **Automated Installation**: Double-click `install_windows.bat`
2. **Start Application**: Double-click `start_hotvolume.bat`
3. **Look for Tray Icon**: Find the volume icon in your system tray

### Manual Installation
```bash
pip install -r backend/requirements.txt
python run_hotvolume.py
```

## 🎮 Usage Examples

### Gaming Scenario (CS2 + Spotify)
1. Start playing music on Spotify
2. Launch Counter-Strike 2
3. While in-game, press `Ctrl+Shift+F1` to reduce Spotify volume
4. Press `Ctrl+Shift+F2` to increase Spotify volume
5. Press `Ctrl+Shift+F3` to mute/unmute Spotify instantly

### Meeting Scenario
- `Ctrl+Shift+F7/F8/F9` to control Discord during meetings
- `Ctrl+Shift+F4/F5/F6` to control Chrome (YouTube, etc.)

## ⚙️ Configuration

### Adding Custom Hotkeys
1. Right-click the system tray icon
2. Select "Configure Hotkeys"
3. Add new hotkey combinations for any application
4. Settings save automatically
5. Close window - app continues running in tray

### Supported Applications
HotVolume works with **any Windows application** that produces audio:
- **Music/Media**: Spotify, YouTube, VLC, iTunes, Windows Media Player, Groove
- **Browsers**: Chrome, Firefox, Edge (YouTube, streaming sites)
- **Communication**: Discord, Teams, Zoom, Skype, Slack
- **Games**: Steam games, CS2, CSGO, any game with audio
- **Creative**: Audacity, OBS Studio, streaming software
- **And many more...**

## 🔧 How It Works

HotVolume uses the Windows Audio Session API (WASAPI) to control individual application volumes:

1. **Audio Session Detection**: Scans Windows audio sessions for active applications
2. **Global Hotkey Registration**: Registers system-wide keyboard shortcuts
3. **Volume Control**: Adjusts volume levels for specific application sessions
4. **System Tray Operation**: Runs silently in background with easy access
5. **Configuration Persistence**: Saves your settings to `hotkey_config.json`

## 🗂️ File Structure
```
📁 HotVolume_v1.1/
├── 🎯 backend/server.py          - Main application
├── 🔊 backend/audio_controller.py - Volume control logic
├── 🎮 backend/hotkey_manager.py   - Hotkey handling (with saving)
├── 🔍 backend/app_detector.py     - App detection
├── 📊 backend/tray_interface.py   - System tray
├── ⚙️ backend/config_gui.py      - Configuration GUI
├── 🚀 run_hotvolume.py           - Launcher script
├── 📋 backend/requirements.txt    - Dependencies
├── 🪟 install_windows.bat        - Auto installer
├── ▶️ start_hotvolume.bat        - Quick launcher
└── 📖 README.md                  - This documentation
```

## 🛠️ Troubleshooting

### Common Issues

1. **Hotkeys not working**: 
   - Restart HotVolume
   - Check if another app uses the same hotkey
   - Try different key combinations

2. **Application not detected**:
   - Ensure the app is playing audio (not paused)
   - Right-click tray → "Refresh Apps"
   - Check exact application name in config

3. **No system tray icon**:
   - Check Windows notification area settings
   - Look in "Show hidden icons"
   - Run as Administrator if needed

4. **Settings not saving**:
   - Check that `hotkey_config.json` file is created
   - Ensure write permissions in app directory

### Debug Mode
```bash
python run_hotvolume.py --test
```

## 📝 Version History

### v1.1 (Current)
- ✅ Configuration saving (`hotkey_config.json`)
- ✅ Background operation (tray stays active)
- ✅ Updated Spotify.exe support
- ✅ Improved error handling

### v1.0
- Initial release with basic functionality

## 🎯 Perfect For

- **Gamers**: Control music/Discord while gaming
- **Streamers**: Adjust audio levels during streams  
- **Remote Workers**: Manage meeting audio quickly
- **Content Creators**: Fine-tune audio during recording
- **Anyone**: Who wants quick audio control without leaving their current app

## 📄 License

This project is for educational and personal use.

---

**🎵 Enjoy perfect audio control with HotVolume v1.1! 🎮**