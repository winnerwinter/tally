#!/usr/bin/env python3

import json
import os
from typing import Optional


class Settings:
    def __init__(self):
        self.settings_dir = os.path.expanduser("~/.tally")
        self.settings_file = os.path.join(self.settings_dir, "settings.json")
        self.settings = self._load_settings()
    
    def _load_settings(self) -> dict:
        """Load settings from file or create default"""
        if os.path.exists(self.settings_file):
            try:
                with open(self.settings_file, 'r') as f:
                    return json.load(f)
            except Exception:
                pass
        
        # Default settings
        return {
            "last_file": None
        }
    
    def _save_settings(self):
        """Save settings to file"""
        try:
            os.makedirs(self.settings_dir, exist_ok=True)
            with open(self.settings_file, 'w') as f:
                json.dump(self.settings, f, indent=2)
        except Exception:
            pass  # Ignore settings save errors
    
    def get_last_file(self) -> Optional[str]:
        """Get the last opened file path"""
        return self.settings.get("last_file")
    
    def set_last_file(self, file_path: Optional[str]):
        """Set the last opened file path"""
        self.settings["last_file"] = file_path
        self._save_settings()