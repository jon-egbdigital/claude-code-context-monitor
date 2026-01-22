"""Configuration constants for Claude Code Odometer Monitor"""
from pathlib import Path


class PlanLimits:
    """Token limits for different Claude Code plans"""
    PRO = 44000
    MAX5 = 88000
    MAX20 = 220000
    SONNET_45 = 200000  # Sonnet 4.5 context window


class Config:
    """Main configuration for the odometer monitor"""

    # Plan settings
    PLAN_LIMIT = PlanLimits.SONNET_45
    PLAN_NAME = "Sonnet 4.5"

    # Polling settings
    REFRESH_INTERVAL_MS = 2000  # 2 seconds

    # Claude Code directories
    CLAUDE_PROJECTS_DIR = Path.home() / ".claude" / "projects"

    # Window settings
    WINDOW_WIDTH = 280
    WINDOW_HEIGHT = 160  # Increased to accommodate project name label
    ALWAYS_ON_TOP = True

    # Color thresholds and values
    COLOR_SAFE = "#28A745"      # Green (0-70%)
    COLOR_WARNING = "#FFC107"   # Amber (70-90%)
    COLOR_DANGER = "#FF6B35"    # Orange (90-95%)
    COLOR_CRITICAL = "#DC3545"  # Red (95-100%)
    COLOR_INACTIVE = "#808080"  # Gray (no session)

    # Theme colors
    BG_COLOR = "#2C2C2C"       # Dark background
    TEXT_COLOR = "#FFFFFF"      # White text
    TEXT_SECONDARY = "#AAAAAA"  # Gray text

    # Compress button settings
    COMPRESS_THRESHOLD = 70.0  # Enable button at 70% usage

    # Persistence
    CONFIG_DIR = Path.home() / ".claude-monitor"
    POSITION_FILE = CONFIG_DIR / "position.json"
