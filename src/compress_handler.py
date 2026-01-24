"""Handles /compact command execution for Claude Code"""
import tkinter as tk
from tkinter import messagebox


class CompressHandler:
    """Handles compress command execution"""

    def __init__(self, root: tk.Tk):
        """
        Initialize compress handler.

        Args:
            root: tkinter root window
        """
        self.root = root

    def copy_to_clipboard(self, text: str):
        """
        Copy text to system clipboard.

        Args:
            text: Text to copy
        """
        self.root.clipboard_clear()
        self.root.clipboard_append(text)
        self.root.update()  # Required for clipboard to work

    def execute_compress(self):
        """
        Execute compress command by copying to clipboard and showing notification.

        This is a simpler approach than trying to automate terminal input.
        The user can paste the command into their Claude Code terminal.
        """
        # Copy /compact to clipboard
        self.copy_to_clipboard("/compact")

        # Show notification
        messagebox.showinfo(
            "Compress Command Ready",
            "The command '/compact' has been copied to your clipboard.\n\n"
            "Paste it into your Claude Code terminal to compress the context.",
            parent=self.root
        )


def create_compress_handler(root: tk.Tk) -> CompressHandler:
    """
    Factory function to create compress handler.

    Args:
        root: tkinter root window

    Returns:
        CompressHandler instance
    """
    return CompressHandler(root)
