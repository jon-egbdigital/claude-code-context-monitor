"""Data reader for Claude Code JSONL log files"""
import json
from pathlib import Path
from typing import Optional, Tuple
try:
    from .config import Config
except ImportError:
    from config import Config


def extract_project_name(session_path: Path) -> str:
    """
    Extract readable project name from session file path.

    Claude Code stores sessions in: ~/.claude/projects/<encoded-path>/<session-id>.jsonl
    Where <encoded-path> uses '--' as separator (e.g., 'E--projects--myapp')

    Args:
        session_path: Path to the session JSONL file

    Returns:
        Readable project name (last component of decoded path)
    """
    try:
        # Get the parent directory name (encoded project path)
        encoded_path = session_path.parent.name

        # Decode: replace '--' with path separator and get last component
        # E--10-CLAUDE-CODE--12-CC-ContextMonitor -> E:\10_CLAUDE_CODE\12_CC_ContextMonitor
        decoded_path = encoded_path.replace('--', '\\')

        # Return just the last folder name for brevity
        # E:\10_CLAUDE_CODE\12_CC_ContextMonitor -> 12_CC_ContextMonitor
        project_name = Path(decoded_path).name

        return project_name if project_name else "Unknown Project"
    except (AttributeError, IndexError):
        return "Unknown Project"


def find_active_session() -> Optional[Path]:
    """
    Find the most recently active Claude Code session JSONL file.

    Returns:
        Path to the most recent JSONL file, or None if no files found
    """
    claude_dir = Config.CLAUDE_PROJECTS_DIR

    if not claude_dir.exists():
        return None

    try:
        jsonl_files = list(claude_dir.glob("**/*.jsonl"))
    except (PermissionError, OSError):
        return None

    if not jsonl_files:
        return None

    # Return the most recently modified file
    return max(jsonl_files, key=lambda p: p.stat().st_mtime)


def extract_tokens_from_entry(entry: dict) -> int:
    """
    Extract total tokens from a single JSONL entry.

    Sums all token types:
    - input_tokens
    - output_tokens
    - cache_read_input_tokens
    - cache_creation.ephemeral_5m_input_tokens

    Args:
        entry: Parsed JSONL entry dictionary

    Returns:
        Total token count for this entry
    """
    if entry.get("type") != "assistant":
        return 0

    usage = entry.get("message", {}).get("usage", {})

    tokens = (
        usage.get("input_tokens", 0) +
        usage.get("output_tokens", 0) +
        usage.get("cache_read_input_tokens", 0)
    )

    # Add cache creation tokens
    cache_creation = usage.get("cache_creation", {})
    tokens += cache_creation.get("ephemeral_5m_input_tokens", 0)

    return tokens


def read_session_tokens(jsonl_path: Path) -> int:
    """
    Read current token usage from a JSONL session file.

    Returns the token count from the MOST RECENT assistant message,
    which represents the current context size (not the sum of all messages).

    Args:
        jsonl_path: Path to the JSONL file

    Returns:
        Current token count from the most recent entry
    """
    last_tokens = 0

    try:
        with open(jsonl_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue

                try:
                    entry = json.loads(line)
                    tokens = extract_tokens_from_entry(entry)
                    if tokens > 0:  # Only update if this is an assistant message
                        last_tokens = tokens
                except json.JSONDecodeError:
                    # Skip invalid JSON lines
                    continue

    except (FileNotFoundError, PermissionError, OSError):
        return 0

    return last_tokens


def get_current_usage() -> tuple[int, Optional[Path]]:
    """
    Get current token usage from the most active session.

    Returns:
        Tuple of (total_tokens, session_path)
        If no active session, returns (0, None)
    """
    session_path = find_active_session()

    if session_path is None:
        return 0, None

    total_tokens = read_session_tokens(session_path)
    return total_tokens, session_path
