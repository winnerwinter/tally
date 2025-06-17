# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Running the Application

Run the main application:
```bash
python3 run_tally.py
```

The application requires PyQt5 to be installed. If not present, install with:
```bash
pip install PyQt5 jsonschema
```

## Architecture Overview

This is a desktop point-tracking application built with PyQt5 that manages "tally lists" - named entries with numeric point values sorted by rank.

### Core Components

- **`run_tally.py`**: Entry point that launches the PyQt5 application
- **`src/core/data_manager.py`**: Handles JSON file I/O and schema validation using jsonschema
- **`src/core/schema.json`**: JSON schema defining the tally data structure
- **`src/core/settings.py`**: Manages user settings (last opened file) stored in `~/.tally/settings.json`
- **`src/ui/pyqt_window.py`**: Main PyQt5 GUI implementation

### Data Structure

Tally files are JSON with this structure:
```json
{
  "title": "List title",
  "entries": [
    {
      "name": "Entry name",
      "value": 10,
      "last_updated": 1703123456.789
    }
  ]
}
```

The `last_updated` timestamp is used for tiebreaking when entries have the same point value - earlier timestamps rank higher.

### Key Features

- **Ranking System**: Entries are sorted by value (descending), then by `last_updated` (ascending) for tiebreaking
- **Position Tracking**: The application tracks position changes between saves and shows movement indicators (🌱 for new, ⬆️ for up, ⬇️ for down, ⚪ for no change)
- **Clipboard Integration**: Simple dump format copies formatted rankings to clipboard
- **File Persistence**: Remembers last opened file across sessions
- **Duplicate Prevention**: Prevents duplicate entry names

### UI Workflow

1. Load existing file or create new one
2. Add/edit entries and modify point values
3. Use "Update" to save changes and capture position changes
4. Use "Copy Simple Dump" to export formatted rankings

### Development Notes

- All file operations use absolute paths and proper error handling
- The application suppresses Tk deprecation warnings on macOS
- Entry selection is tracked by name (not index) to survive re-sorting
- Position change tracking is captured on file saves and clipboard operations