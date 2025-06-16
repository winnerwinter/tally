#!/usr/bin/env python3

import sys
import os

# Suppress Tk deprecation warning on macOS
os.environ['TK_SILENCE_DEPRECATION'] = '1'

# Add the src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from ui.pyqt_window import main

if __name__ == "__main__":
    main()