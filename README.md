# HotVolume - Application Volume Controller

A Windows desktop application that allows you to control the volume of specific applications using global hotkeys. Perfect for gamers who want to quickly adjust Spotify volume while playing CS2, or control Discord volume during meetings.

## Features

- **Individual App Volume Control**: Control volume for specific applications independently
- **Global Hotkeys**: System-wide keyboard shortcuts that work in any application
- **System Tray Integration**: Easy access through system tray icon
- **Real-time Audio Detection**: Automatically detects applications currently producing audio
- **Customizable Mappings**: Configure your own hotkey combinations
- **Quick Controls**: Right-click tray menu for instant volume adjustments

## Default Hotkeys

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
| `Ctrl+Shift+F10` | CS2 | Volume Down |
| `Ctrl+Shift+F11` | CS2 | Volume Up |
| `Ctrl+Shift+F12` | CS2 | Toggle Mute |

## Installation & Usage

### Requirements
- Windows 10/11
- Python 3.7 or higher

### Setup
1. Install dependencies:
   ```bash
   pip install -r backend/requirements.txt
   ```

2. Run the application:
   ```bash
   python run_hotvolume.py
   ```

### Usage
1. **System Tray**: Look for the HotVolume icon in your system tray
2. **Quick Controls**: Right-click the tray icon for instant volume controls
3. **Configuration**: Select "Configure Hotkeys" from the tray menu to customize
4. **Hotkeys**: Use the default hotkeys or configure your own

### Configuration
- Right-click the tray icon and select "Configure Hotkeys"
- Add new hotkey combinations for any application
- Set custom volume step sizes
- Enable/disable hotkey listening

## How It Works

HotVolume uses the Windows Audio Session API (WASAPI) to control individual application volumes. It:

1. **Detects Audio Sessions**: Scans for applications currently producing audio
2. **Registers Global Hotkeys**: Uses Windows API to capture hotkeys system-wide
3. **Controls Volume**: Adjusts volume levels for specific application sessions
4. **Provides UI**: System tray and configuration GUI for easy management

## Supported Applications

HotVolume works with any Windows application that produces audio, including:
- **Music/Media**: Spotify, YouTube, VLC, Windows Media Player, iTunes
- **Browsers**: Chrome, Firefox, Edge
- **Communication**: Discord, Teams, Zoom, Skype
- **Games**: Steam games, CS2, any DirectSound/WASAPI game
- **And many more...**

## Technical Details

### Components
- **Audio Controller**: Windows Audio Session API integration
- **Hotkey Manager**: Global keyboard shortcut handling
- **App Detector**: Process and window detection
- **System Tray**: Background operation and quick access
- **Configuration GUI**: User-friendly setup interface

### Libraries Used
- `pycaw`: Windows Audio Session API wrapper
- `keyboard`: Global hotkey detection
- `pystray`: System tray interface
- `tkinter`: Configuration GUI
- `psutil`: Process detection

## Troubleshooting

### Common Issues

1. **Hotkeys not working**: 
   - Check if another application is using the same hotkey combination
   - Try different hotkey combinations
   - Restart the application

2. **Application not detected**:
   - Make sure the target application is playing audio
   - Use "Refresh Apps" in the configuration window
   - Check if the application name matches exactly

3. **No system tray icon**:
   - Check Windows notification area settings
   - Look in the "hidden icons" area
   - Restart the application

### Debug Mode
Run with debug logging:
```bash
python run_hotvolume.py --test
```

## Contributing

This is a desktop application for Windows volume control. Feel free to suggest improvements or report issues.

## License

This project is for educational and personal use.
