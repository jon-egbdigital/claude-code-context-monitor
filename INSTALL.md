# Installation Guide

## Prerequisites

### Python Installation

This project requires Python 3.8 or higher. Check if Python is installed:

```bash
python --version
```

If Python is not installed:

**Windows:**
1. Download Python from [python.org](https://www.python.org/downloads/)
2. Run the installer
3. **IMPORTANT**: Check "Add Python to PATH" during installation
4. Verify installation: `python --version`

**macOS:**
```bash
brew install python3
```

**Linux:**
```bash
sudo apt-get update
sudo apt-get install python3 python3-tk
```

### Verify tkinter

tkinter should be included with Python. Test it:

```python
python -c "import tkinter; print('tkinter OK')"
```

If you get an error on Linux:
```bash
sudo apt-get install python3-tk
```

## Installation Steps

### 1. Download the Project

Clone the repository:
```bash
git clone https://github.com/jon-egbdigital/claude-code-context-monitor.git
cd claude-code-context-monitor
```

### 2. Verify Files

Ensure all files are present:
```
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── data_reader.py
│   ├── token_calculator.py
│   ├── ui_widget.py
│   └── compress_handler.py
├── tests/
│   ├── test_token_calculator.py
│   └── test_data_reader.py
├── README.md
├── INSTALL.md
├── requirements.txt
├── run.bat
└── run_tests.bat
```

### 3. Run Tests (Optional)

Verify the installation by running tests:

**Windows:**
```bash
run_tests.bat
```

**macOS/Linux:**
```bash
python tests/test_token_calculator.py
python tests/test_data_reader.py
```

### 4. Launch the Monitor

**Windows:**
```bash
run.bat
```

Or manually:
```bash
python src\main.py
```

**macOS/Linux:**
```bash
python3 -m src.main
```

## First Launch

On first launch, the monitor will:
1. Create config directory at `~/.claude-monitor/`
2. Center itself on your screen
3. Display "No active session" if Claude Code is not running
4. Begin monitoring once you start a Claude Code session

## Configuration

### Change Your Plan Limit

Edit `src/config.py`:

```python
# For Pro plan (44k tokens)
PLAN_LIMIT = PlanLimits.PRO

# For Max5 plan (88k tokens) - DEFAULT
PLAN_LIMIT = PlanLimits.MAX5

# For Max20 plan (220k tokens)
PLAN_LIMIT = PlanLimits.MAX20
```

Don't forget to update the plan name:
```python
PLAN_NAME = "Pro"  # or "Max5" or "Max20"
```

### Adjust Update Frequency

Change polling interval (in milliseconds):
```python
REFRESH_INTERVAL_MS = 2000  # 2 seconds (default)
REFRESH_INTERVAL_MS = 1000  # 1 second (more responsive)
REFRESH_INTERVAL_MS = 5000  # 5 seconds (lower CPU usage)
```

### Customize Colors

Modify color thresholds in `src/config.py`:
```python
COLOR_SAFE = "#28A745"      # Green (0-70%)
COLOR_WARNING = "#FFC107"   # Amber (70-90%)
COLOR_DANGER = "#FF6B35"    # Orange (90-95%)
COLOR_CRITICAL = "#DC3545"  # Red (95-100%)
```

## Troubleshooting

### Python not found

**Windows:**
- Reinstall Python with "Add to PATH" option checked
- Or manually add Python to PATH in System Environment Variables

**macOS/Linux:**
- Use `python3` instead of `python`
- Install Python via package manager

### tkinter not found

**Windows:**
- Reinstall Python with "tcl/tk and IDLE" option checked

**Linux:**
```bash
sudo apt-get install python3-tk
```

**macOS:**
```bash
brew install python-tk
```

### Monitor shows "No active session"

1. Ensure Claude Code is running
2. Check that `~/.claude/projects/` directory exists
3. Verify Claude Code has created at least one JSONL log file
4. Wait 2 seconds for the next polling cycle

### Window appears off-screen

Delete the position file to reset:
```bash
# Windows
del %USERPROFILE%\.claude-monitor\position.json

# macOS/Linux
rm ~/.claude-monitor/position.json
```

### Permission errors reading JSONL files

Ensure the monitor has read access to:
- `~/.claude/projects/` directory
- All subdirectories and `.jsonl` files

## Usage Tips

### Starting with Windows

Create a shortcut to `run.bat` on your desktop for quick access.

### Starting with macOS/Linux

Add an alias to your shell profile:
```bash
alias claude-monitor="python3 /path/to/src/main.py"
```

### Auto-start on Boot

**Windows:**
1. Press `Win+R`
2. Type `shell:startup`
3. Create shortcut to `run.bat` in the folder

**macOS:**
1. System Preferences → Users & Groups → Login Items
2. Add `python3 /path/to/src/main.py`

**Linux:**
Add to your desktop environment's autostart applications.

## Next Steps

Once installed:
1. Start a Claude Code session
2. Run the monitor
3. Generate some token usage
4. Watch the percentage update in real-time
5. Test the compress button when usage exceeds 70%

For more information, see [README.md](README.md).
