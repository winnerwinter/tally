# Tally - Point Tracker

A simple desktop application for tracking points and rankings among friends, teams, or any group of named entries.

## What is Tally?

Tally is a lightweight point-tracking application perfect for keeping score in games, contests, or any situation where you need to track and rank performance. Whether you're scoring game nights with friends, tracking team performance, or managing any kind of leaderboard, Tally makes it simple and visual.

## Features

- **Visual Rankings**: Entries are automatically sorted by points, showing clear rankings
- **Smart Tiebreaking**: When entries have the same points, they're ranked by who achieved that score first
- **Change Tracking**: See how positions have changed since your last save with visual indicators
- **Easy Management**: Add entries, edit names, and adjust points with simple +/- buttons
- **Export Friendly**: Copy formatted rankings to share anywhere
- **File-Based**: Your data is stored in simple JSON files you can backup or share

## Getting Started

### Prerequisites

- Python 3.x
- PyQt5 and jsonschema libraries

### Installation

1. Clone or download this repository
2. Install required dependencies:
   ```bash
   pip install PyQt5 jsonschema
   ```

### Running Tally

From command line:
```bash
python3 run_tally.py
```

**Easy Launch (macOS)**: Double-click `Tally.command` in Finder for one-click startup without using the terminal.

## How to Use

### Creating a New Tally List

1. Click **"📄 New File"** to create a new tally list
2. Choose where to save your file (it will be a .json file)
3. Edit the title at the top of the window
4. Start adding entries!

### Adding Entries

1. Type a name in the "Add Entry" field
2. Press Enter or click **"Add"**
3. New entries start with 0 points

### Managing Points

1. **Select an entry** from the list by clicking on it
2. Use **"➕ +1"** and **"➖ -1"** buttons to adjust points
3. Rankings update automatically as you make changes

### Editing Entry Names

- **Double-click** any entry to edit its name
- Entry names must be unique

### Saving and Tracking Changes

1. Click **"💾 Update"** to save your changes to the file
2. After saving, position changes are tracked with indicators:
   - 🌱 New entries
   - ⬆️ Moved up in ranking
   - ⬇️ Moved down in ranking
   - ⚪ No change in position

### Sharing Results

- Click **"📋 Copy Simple Dump"** to copy a formatted ranking to your clipboard
- Perfect for pasting into chat apps, emails, or documents

### Loading Existing Files

- Click **"📂 Load File"** to open a previously saved tally list
- The app remembers your last opened file

## Example Output

When you copy results, they look like this:

```
Game Night Scores
=================

 1 🌱 - Alice            15 points
 2 ⬆️+1 Bob              12 points
 3 ⬇️-1 Charlie          10 points
 4 ⚪ = Dave              8 points
```

## File Format

Tally files are JSON format with this structure:

```json
{
  "title": "My Tally List",
  "entries": [
    {
      "name": "Entry Name",
      "value": 10,
      "last_updated": 1703123456.789
    }
  ]
}
```

## Tips

- **No Ties**: If entries have the same points, the one who reached that score first ranks higher
- **Unique Names**: Each entry must have a unique name
- **Auto-Save**: The app remembers your last file and reopens it automatically
- **Settings Storage**: The app creates a `~/.tally` directory to remember your last opened file
- **Backup**: Your tally files are just JSON - easy to backup or share

---

*Simple. Visual. Effective.*

**Vibe coded by Claude** - This entire application was designed and built through natural conversation, turning a casual idea into a fully functional desktop app. Sometimes the best tools come from just describing what you need!