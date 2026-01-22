"""Odometer UI widget using tkinter"""
import tkinter as tk
from tkinter import ttk
from pathlib import Path
try:
    from .config import Config
    from .data_reader import get_current_usage, extract_project_name
    from .token_calculator import TokenCalculator
except ImportError:
    from config import Config
    from data_reader import get_current_usage, extract_project_name
    from token_calculator import TokenCalculator


class OdometerWidget:
    """Floating odometer widget displaying token usage"""

    def __init__(self, root: tk.Tk):
        """
        Initialize the odometer widget.

        Args:
            root: tkinter root window
        """
        self.root = root
        self.calculator = TokenCalculator()
        self.compress_callback = None

        # Configure root window
        self.root.title("Claude Code Tokens")
        self.root.geometry(f"{Config.WINDOW_WIDTH}x{Config.WINDOW_HEIGHT}")
        self.root.configure(bg=Config.BG_COLOR)

        if Config.ALWAYS_ON_TOP:
            self.root.attributes("-topmost", True)

        # Make window draggable
        self._drag_data = {"x": 0, "y": 0}
        self.root.bind("<Button-1>", self._on_drag_start)
        self.root.bind("<B1-Motion>", self._on_drag_motion)

        # Create UI elements
        self._create_widgets()

    def _create_widgets(self):
        """Create all UI elements"""

        # Title label
        self.title_label = tk.Label(
            self.root,
            text="Claude Code Tokens",
            font=("Arial", 10),
            bg=Config.BG_COLOR,
            fg=Config.TEXT_SECONDARY,
        )
        self.title_label.pack(pady=(5, 0))

        # Project name label
        self.project_label = tk.Label(
            self.root,
            text="No active session",
            font=("Arial", 8),
            bg=Config.BG_COLOR,
            fg=Config.TEXT_SECONDARY,
        )
        self.project_label.pack(pady=(0, 5))

        # Large percentage display
        self.percentage_label = tk.Label(
            self.root,
            text="0.0%",
            font=("Arial", 36, "bold"),
            bg=Config.BG_COLOR,
            fg=Config.COLOR_SAFE,
        )
        self.percentage_label.pack(pady=(0, 5))

        # Progress bar (using Canvas)
        self.progress_canvas = tk.Canvas(
            self.root,
            width=260,
            height=20,
            bg=Config.BG_COLOR,
            highlightthickness=0,
        )
        self.progress_canvas.pack(pady=(0, 5))

        # Progress bar background
        self.progress_bg = self.progress_canvas.create_rectangle(
            0, 0, 260, 20,
            fill="#444444",
            outline=""
        )

        # Progress bar foreground
        self.progress_fg = self.progress_canvas.create_rectangle(
            0, 0, 0, 20,
            fill=Config.COLOR_SAFE,
            outline=""
        )

        # Token count label
        self.token_label = tk.Label(
            self.root,
            text="0 / 88,000 tokens",
            font=("Arial", 10),
            bg=Config.BG_COLOR,
            fg=Config.TEXT_COLOR,
        )
        self.token_label.pack()

        # Plan label
        self.plan_label = tk.Label(
            self.root,
            text=f"[{Config.PLAN_NAME} Plan]",
            font=("Arial", 9),
            bg=Config.BG_COLOR,
            fg=Config.TEXT_SECONDARY,
        )
        self.plan_label.pack(pady=(0, 5))

        # Compress button (will be implemented in Phase 3)
        self.compress_button = tk.Button(
            self.root,
            text="Compress Context",
            font=("Arial", 10),
            bg="#555555",
            fg="#888888",
            activebackground="#666666",
            relief=tk.FLAT,
            state=tk.DISABLED,
            command=self._on_compress_click,
        )
        self.compress_button.pack(pady=(5, 5))

    def _on_drag_start(self, event):
        """Handle drag start event"""
        self._drag_data["x"] = event.x
        self._drag_data["y"] = event.y

    def _on_drag_motion(self, event):
        """Handle drag motion event"""
        x = self.root.winfo_x() + (event.x - self._drag_data["x"])
        y = self.root.winfo_y() + (event.y - self._drag_data["y"])
        self.root.geometry(f"+{x}+{y}")

    def _on_compress_click(self):
        """Handle compress button click"""
        if self.compress_callback:
            self.compress_callback()

    def set_compress_callback(self, callback):
        """
        Set callback function for compress button.

        Args:
            callback: Function to call when compress button is clicked
        """
        self.compress_callback = callback

    def update_display(self):
        """Update display with current token usage"""
        total_tokens, session_path = get_current_usage()

        if session_path is None:
            # No active session
            self._show_no_session()
            return

        # Extract and display project name
        project_name = extract_project_name(session_path)
        self.project_label.config(text=f"📁 {project_name}")

        # Get usage data
        usage_data = self.calculator.get_usage_data(total_tokens)

        # Update percentage label
        pct = usage_data["percentage"]
        color = usage_data["color"]
        self.percentage_label.config(
            text=f"{pct:.1f}%",
            fg=color
        )

        # Update progress bar
        bar_width = int((pct / 100) * 260)
        bar_width = min(bar_width, 260)  # Cap at 100%
        self.progress_canvas.coords(self.progress_fg, 0, 0, bar_width, 20)
        self.progress_canvas.itemconfig(self.progress_fg, fill=color)

        # Update token count label
        tokens = usage_data["tokens"]
        limit = usage_data["plan_limit"]
        self.token_label.config(
            text=f"{tokens:,} / {limit:,} tokens",
            fg=Config.TEXT_COLOR
        )

        # Update compress button
        if usage_data["compress_enabled"]:
            self.compress_button.config(
                state=tk.NORMAL,
                bg="#4CAF50",
                fg="#FFFFFF"
            )
        else:
            self.compress_button.config(
                state=tk.DISABLED,
                bg="#555555",
                fg="#888888"
            )

    def _show_no_session(self):
        """Show 'No active session' state"""
        self.project_label.config(text="No active session")

        self.percentage_label.config(
            text="--",
            fg=Config.COLOR_INACTIVE
        )

        # Reset progress bar
        self.progress_canvas.coords(self.progress_fg, 0, 0, 0, 20)

        self.token_label.config(
            text="Waiting for Claude Code...",
            fg=Config.TEXT_SECONDARY
        )

        # Disable compress button
        self.compress_button.config(
            state=tk.DISABLED,
            bg="#555555",
            fg="#888888"
        )
