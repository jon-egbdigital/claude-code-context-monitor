# Claude Code Odometer Monitor

A minimal, always-on-top floating desktop widget that displays Claude Code token usage in real-time with an odometer-style interface.

## Features

- **Real-time monitoring**: Displays current token usage from active Claude Code sessions
- **Session identifier**: Shows which project is being monitored (prevents confusion with multiple sessions)
- **Color-coded display**: Visual feedback with green/amber/orange/red based on usage percentage
- **Progress bar**: Graphical representation of context consumption
- **Max5 Plan optimized**: Configured for 88,000 token limit (easily configurable for other plans)
- **One-click compress**: Quick access to `/compress` command when usage exceeds 70%
- **Always-on-top**: Floating widget stays visible above all applications
- **Draggable**: Position anywhere on screen with persistent location memory
- **Dark theme**: Professional dark interface that's easy on the eyes
- **Lightweight**: < 20 MB memory footprint, < 1% CPU usage

## Screenshots

```
┌─────────────────────────────────────┐
│  Claude Code Tokens                │
│  📁 12_CC_ContextMonitor           │  ← Project identifier
│                                     │
│           85.2%                     │  ← Color-coded percentage
│       ███████████░░░░              │  ← Progress bar
│                                     │
│    75,120 / 88,000 tokens          │  ← Token counts
│         [Max5 Plan]                │  ← Plan indicator
│                                     │
│      [Compress Context]            │  ← One-click compress
└─────────────────────────────────────┘
```

## Requirements

- Python 3.8 or higher
- tkinter (included with Python)
- Active Claude Code session

## Installation

1. Clone or download this repository:
   ```bash
   git clone https://github.com/jon-egbdigital/claude-code-context-monitor.git
   cd claude-code-context-monitor
   ```

2. No additional dependencies needed - all libraries are built-in with Python!

## Usage

### Starting the Monitor

#### Manual Launch

Run the monitor from the command line:

```bash
python -m src.main
```

Or on Windows:
```bash
python src\main.py
```

Or use the included batch file:
```bash
run.bat
```

#### Auto-Start on Session Start (Recommended) 🎯

Configure Claude Code to launch the monitor automatically whenever a new session starts.

**Step 1: Create Launch Script**

Create `~/.claude/launch-odometer.bat` (Windows) or `~/.claude/launch-odometer.sh` (Linux/Mac):

**Windows** (`C:\Users\YourUsername\.claude\launch-odometer.bat`):
```batch
@echo off
REM Auto-launch script for Claude Code Odometer Monitor

REM Check if already running (prevent duplicates)
tasklist /FI "IMAGENAME eq pythonw.exe" 2>NUL | find /I /N "pythonw.exe">NUL
if "%ERRORLEVEL%"=="0" (
    exit /b 0
)

REM Launch monitor in background (no console window)
cd /d C:\path\to\claude-code-context-monitor
start "" pythonw src\main.py

exit /b 0
```

**Important**: Replace `C:\path\to\claude-code-context-monitor` with your actual installation path.

**Step 2: Configure Claude Code Hooks**

Edit `~/.claude/settings.json` and add the `SessionStart` hook:

```json
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "cmd /c C:\\Users\\YourUsername\\.claude\\launch-odometer.bat",
            "timeout": 5
          }
        ]
      }
    ]
  }
}
```

**Important**:
- Replace `YourUsername` with your Windows username
- Use double backslashes (`\\`) in JSON file paths
- Keep any existing hooks (Stop, PermissionRequest, etc.)
- Merge with existing `hooks` object if you already have other hooks configured

**Step 3: Test Auto-Start**

1. Close any running monitor windows
2. Exit Claude Code completely
3. Start a new Claude Code session
4. The monitor should appear automatically within 1-2 seconds

### Using the Monitor

1. **Automatic Detection**: The monitor automatically finds and tracks your most recent Claude Code session
2. **Real-time Updates**: Token usage updates every 2 seconds
3. **Color Indicators**:
   - Green (0-70%): Safe usage level
   - Amber (70-90%): Warning - consider compressing soon
   - Orange (90-95%): Danger - compress recommended
   - Red (95-100%+): Critical - compress immediately

4. **Compress Button**:
   - Enabled when usage exceeds 70%
   - Click to copy `/compress` command to clipboard
   - Paste into your Claude Code terminal to compress context

5. **Dragging**: Click and drag anywhere on the window to reposition
6. **Persistence**: Window position is saved and restored on next launch

### Multiple Sessions

When running multiple Claude Code sessions simultaneously:

- **Automatic Switching**: The monitor tracks the **most recently active** session
- **Project Identifier**: The project name (📁) shows which session is currently being monitored
- **Why Values Jump**: If you switch between sessions, the display will update to show the active session's tokens
- **Manual Compress**: When clicking "Compress Context", paste the command into whichever Claude Code terminal you want to compress

**Example**: If you have sessions for "ProjectA" and "ProjectB":
1. Send a message in ProjectA → monitor shows "📁 ProjectA" with its token count
2. Send a message in ProjectB → monitor switches to show "📁 ProjectB" with its token count
3. This helps you track which session you're monitoring at any given time

### Configuration

Edit `src/config.py` to customize settings:

```python
# Change plan limit (for Pro or Max20 plans)
PLAN_LIMIT = PlanLimits.PRO      # 44,000 tokens
PLAN_LIMIT = PlanLimits.MAX5     # 88,000 tokens (default)
PLAN_LIMIT = PlanLimits.MAX20    # 220,000 tokens

# Change refresh interval
REFRESH_INTERVAL_MS = 2000  # 2 seconds (default)

# Adjust window size
WINDOW_WIDTH = 280
WINDOW_HEIGHT = 160

# Customize colors
COLOR_SAFE = "#28A745"      # Green
COLOR_WARNING = "#FFC107"   # Amber
COLOR_DANGER = "#FF6B35"    # Orange
COLOR_CRITICAL = "#DC3545"  # Red
```

## Project Structure

```
claude-code-context-monitor/
├── src/
│   ├── __init__.py           # Package initialization
│   ├── main.py               # Entry point and main loop
│   ├── config.py             # Configuration constants
│   ├── data_reader.py        # JSONL file reading and parsing
│   ├── token_calculator.py   # Token aggregation and calculations
│   ├── ui_widget.py          # Odometer display widget
│   └── compress_handler.py   # Compress command execution
├── tests/                    # Unit tests (optional)
├── requirements.txt          # Dependencies (minimal)
└── README.md                 # This file
```

## How It Works

1. **Session Discovery**: Monitors `~/.claude/projects/**/*.jsonl` for active sessions
2. **Token Extraction**: Parses JSONL entries to sum all token types:
   - input_tokens
   - output_tokens
   - cache_read_input_tokens
   - cache_creation.ephemeral_5m_input_tokens

3. **Real-time Updates**: Polls every 2 seconds for changes
4. **Smart Display**: Calculates percentage and adjusts colors based on thresholds

## Troubleshooting

### "No active session" displayed
- Ensure Claude Code is running
- Verify `~/.claude/projects/` directory exists
- Check that Claude Code has created a session JSONL file

### Window appears off-screen
- Delete `~/.claude-monitor/position.json` to reset position
- Window will center on next launch

### Token count seems incorrect
- Verify your plan limit is set correctly in `config.py`
- Token count includes all types: input, output, and cached tokens
- Wait 2 seconds for updates (refresh interval)

### Compress button doesn't work
- Ensure you're at 70%+ usage to enable the button
- The `/compress` command is copied to clipboard - paste it manually into Claude Code terminal

## Performance

- Memory usage: ~15 MB (measured with Task Manager)
- CPU usage: < 1% during polling
- Startup time: < 500ms
- Update latency: 2 seconds (configurable)

## Future Enhancements

### Planned Features

**High Priority:**
- **Auto-Compress**: Automatically trigger `/compress` when usage exceeds configurable threshold
- **Desktop Notifications**: Toast notifications when approaching token limits
- **Compact Mode**: Minimized view that takes less screen space
- **System Tray Integration**: Minimize to system tray instead of taskbar

**Medium Priority:**
- **Multi-Session Tracking**: Monitor multiple Claude Code sessions simultaneously
- **Cost Tracking**: Track estimated costs based on Anthropic API pricing
- **Trend Indicators**: Visual arrows showing usage trend (increasing/decreasing)
- **Time-to-Limit Estimates**: Predict when you'll hit context limit based on usage rate
- **Launch Delay Configuration**: Add configurable startup delay to avoid boot congestion

**Low Priority:**
- **Cross-Platform Support**: macOS and Linux compatibility
- **Session History**: Track and export historical token usage data
- **Cost Alerts & Budgets**: Set spending alerts and budget limits
- **Configurable Themes**: Light mode, custom color schemes
- **Web Dashboard**: Optional web-based monitoring interface
- **Conditional Launch**: Only auto-start in specific project directories
- **Auto-Close on Session End**: Optional Stop hook to close monitor with session

### Contributing Ideas

Have an idea? [Open an issue](https://github.com/jon-egbdigital/claude-code-context-monitor/issues) or submit a PR!

## License

MIT License - see [LICENSE](LICENSE) file for details.

This project is provided as-is for use with Claude Code.

## Credits

Inspired by the [Claude-Code-Usage-Monitor](https://github.com/Maciek-roboblog/Claude-Code-Usage-Monitor) project.

Built with Python and tkinter for maximum compatibility and minimal footprint.

## Contributing

Contributions are welcome! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Commit your changes**: `git commit -m 'Add amazing feature'`
4. **Push to the branch**: `git push origin feature/amazing-feature`
5. **Open a Pull Request**

### Development Setup

```bash
git clone https://github.com/yourusername/claude-code-context-monitor.git
cd claude-code-context-monitor
python src/main.py
```

## Support

For issues or feature requests, please:
- Open an issue on [GitHub Issues](https://github.com/yourusername/claude-code-context-monitor/issues)
- Check the Claude Code documentation
- Visit Claude Code community forums
