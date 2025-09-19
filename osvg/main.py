"""
Entry point for the Video Game Database System.
"""

import os
import sys

# Add parent directory to path so we can import our modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from osvg.interface import main as interface_main


def main() -> None:
    """Launch the video game database interface."""
    print("🎮 Starting Video Game Database System...")
    interface_main()


if __name__ == "__main__":
    main()
