#!/usr/bin/env python3

import sys
import time
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, 
                             QWidget, QPushButton, QLineEdit, QListWidget, QLabel, 
                             QListWidgetItem, QMessageBox, QInputDialog, QFileDialog)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QClipboard

# Import our modules
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from core.data_manager import DataManager
from core.settings import Settings


class PyQtTallyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tally - Point Tracker")
        self.setGeometry(100, 100, 600, 500)
        
        # Get clipboard reference
        self.clipboard = QApplication.clipboard()
        
        # Current data
        self.title = "New Tally List"
        self.entries = []
        self.selected_entry_name = None  # Track by name instead of index
        self.current_file_path = None    # Track the current file
        self.previous_positions = {}     # Track previous positions for change indicators
        
        # Initialize data manager and settings
        schema_path = os.path.join(os.path.dirname(__file__), '..', 'core', 'schema.json')
        self.data_manager = DataManager(schema_path)
        self.settings = Settings()
        
        self.setup_ui()
        self.load_last_file_or_start_empty()
        
    def setup_ui(self):
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        layout = QVBoxLayout(central_widget)
        
        # File operations
        file_layout = QHBoxLayout()
        self.load_btn = QPushButton("📂 Load File")
        self.new_btn = QPushButton("📄 New File") 
        self.update_btn = QPushButton("💾 Update")
        
        self.load_btn.clicked.connect(self.load_file)
        self.new_btn.clicked.connect(self.new_file)
        self.update_btn.clicked.connect(self.update_file)
        
        file_layout.addWidget(self.load_btn)
        file_layout.addWidget(self.new_btn)
        file_layout.addStretch()
        file_layout.addWidget(self.update_btn)
        layout.addLayout(file_layout)
        
        # Title section
        title_layout = QHBoxLayout()
        title_label = QLabel("Title:")
        self.title_edit = QLineEdit(self.title)
        self.title_edit.setFont(QFont("Arial", 12, QFont.Bold))
        self.title_edit.textChanged.connect(self.on_title_changed)
        
        title_layout.addWidget(title_label)
        title_layout.addWidget(self.title_edit)
        layout.addLayout(title_layout)
        
        # Add entry section
        add_layout = QHBoxLayout()
        add_label = QLabel("Add Entry:")
        self.add_edit = QLineEdit()
        self.add_edit.setPlaceholderText("Enter name here...")
        self.add_btn = QPushButton("Add")
        
        self.add_edit.returnPressed.connect(self.add_entry)
        self.add_btn.clicked.connect(self.add_entry)
        
        add_layout.addWidget(add_label)
        add_layout.addWidget(self.add_edit)
        add_layout.addWidget(self.add_btn)
        layout.addLayout(add_layout)
        
        # Entries list
        self.entries_list = QListWidget()
        self.entries_list.setFont(QFont("Courier", 11))
        self.entries_list.itemClicked.connect(self.on_item_selected)
        self.entries_list.itemDoubleClicked.connect(self.edit_selected_name)
        layout.addWidget(self.entries_list)
        
        # Control buttons
        control_layout = QHBoxLayout()
        self.increment_btn = QPushButton("➕ +1")
        self.decrement_btn = QPushButton("➖ -1") 
        self.edit_name_btn = QPushButton("✏️ Edit Name")
        
        self.increment_btn.clicked.connect(self.increment_selected)
        self.decrement_btn.clicked.connect(self.decrement_selected)
        self.edit_name_btn.clicked.connect(self.edit_selected_name)
        
        control_layout.addWidget(self.increment_btn)
        control_layout.addWidget(self.decrement_btn)
        control_layout.addWidget(self.edit_name_btn)
        control_layout.addStretch()
        layout.addLayout(control_layout)
        
        # Instructions
        instructions = QLabel("Double-click entry to edit name | Select entry and use +/- buttons")
        instructions.setStyleSheet("color: gray; font-size: 10px;")
        layout.addWidget(instructions)
        
        # Bottom buttons
        bottom_layout = QHBoxLayout()
        self.copy_simple_btn = QPushButton("📋 Copy Simple Dump")
        self.preview_btn = QPushButton("👀 Preview")
        self.copy_changes_btn = QPushButton("🔄 Update & Copy Changes")
        
        self.copy_simple_btn.clicked.connect(self.copy_simple_dump)
        self.preview_btn.clicked.connect(self.preview_simple_dump)
        self.copy_changes_btn.clicked.connect(self.update_and_copy_changes)
        
        bottom_layout.addWidget(self.copy_simple_btn)
        bottom_layout.addWidget(self.preview_btn)
        bottom_layout.addStretch()
        bottom_layout.addWidget(self.copy_changes_btn)
        layout.addLayout(bottom_layout)
        
    def load_last_file_or_start_empty(self):
        """Load the last opened file, or start with empty data"""
        last_file = self.settings.get_last_file()
        
        if last_file and os.path.exists(last_file):
            try:
                data = self.data_manager.load_file(last_file)
                self.title = data["title"]
                self.entries = data["entries"]
                self.current_file_path = last_file
                self.title_edit.setText(self.title)
                self.refresh_display()
                self.update_window_title()
                # Capture initial positions as baseline
                self._capture_current_positions()
                return
            except Exception:
                # If loading fails, just start empty
                pass
        
        # Start with empty data
        self.title = "New Tally List"
        self.entries = []
        self.current_file_path = None
        self.title_edit.setText(self.title)
        self.refresh_display()
        self.update_window_title()
        # Capture initial positions as baseline (empty, but sets up tracking)
        self._capture_current_positions()
        
    def refresh_display(self):
        """Update the list with current entries"""
        self.entries_list.clear()
        
        # Sort entries by value (desc) then by last_updated (asc for tiebreaking)
        sorted_entries = sorted(self.entries, key=lambda x: (-x["value"], x["last_updated"]))
        
        # Add entries to list
        selected_row = -1
        for rank, entry in enumerate(sorted_entries, 1):
            text = f"#{rank:2d}  {entry['name']:<20} {entry['value']:3d} points"
            item = QListWidgetItem(text)
            item.setData(Qt.UserRole, entry['name'])  # Store the entry name
            self.entries_list.addItem(item)
            
            # Check if this is the previously selected entry
            if self.selected_entry_name == entry['name']:
                selected_row = rank - 1
        
        # Restore selection to follow the entry
        if selected_row >= 0:
            self.entries_list.setCurrentRow(selected_row)
    
    def on_title_changed(self, text):
        """Handle title changes"""
        self.title = text
    
    def on_item_selected(self, item):
        """Handle item selection"""
        self.selected_entry_name = item.data(Qt.UserRole)
        
    def add_entry(self):
        """Add a new entry"""
        name = self.add_edit.text().strip()
        if not name:
            return
            
        # Check for duplicate names
        if any(entry["name"] == name for entry in self.entries):
            QMessageBox.warning(self, "Duplicate Name", f"Entry '{name}' already exists!")
            return
        
        self.entries.append({
            "name": name,
            "value": 0,
            "last_updated": time.time()
        })
        self.add_edit.clear()
        self.selected_entry_name = None
        self.refresh_display()
    
    def increment_selected(self):
        """Increment the selected entry"""
        if not self.selected_entry_name:
            QMessageBox.information(self, "No Selection", "Please select an entry first")
            return
        
        # Find and update the entry
        for entry in self.entries:
            if entry["name"] == self.selected_entry_name:
                entry["value"] += 1
                entry["last_updated"] = time.time()
                break
        
        self.refresh_display()
    
    def decrement_selected(self):
        """Decrement the selected entry"""
        if not self.selected_entry_name:
            QMessageBox.information(self, "No Selection", "Please select an entry first")
            return
        
        # Find and update the entry
        for entry in self.entries:
            if entry["name"] == self.selected_entry_name:
                entry["value"] -= 1
                entry["last_updated"] = time.time()
                break
        
        self.refresh_display()
    
    def edit_selected_name(self):
        """Edit the name of the selected entry"""
        if not self.selected_entry_name:
            QMessageBox.information(self, "No Selection", "Please select an entry first")
            return
        
        # Find the selected entry
        selected_entry = None
        for entry in self.entries:
            if entry["name"] == self.selected_entry_name:
                selected_entry = entry
                break
        
        if not selected_entry:
            return
        
        new_name, ok = QInputDialog.getText(self, "Edit Name", 
                                           f"Enter new name for '{selected_entry['name']}':", 
                                           text=selected_entry['name'])
        
        if not ok or not new_name.strip():
            return
            
        new_name = new_name.strip()
        
        # Check for duplicates
        if any(e["name"] == new_name for e in self.entries if e["name"] != selected_entry["name"]):
            QMessageBox.warning(self, "Duplicate Name", f"Entry '{new_name}' already exists!")
            return
        
        # Update the entry and selected name
        selected_entry["name"] = new_name
        self.selected_entry_name = new_name  # Update our tracking
        
        self.refresh_display()
    
    # File operations
    def load_file(self):
        """Load a tally file"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, 
            "Load Tally File", 
            "", 
            "JSON Files (*.json);;All Files (*)"
        )
        
        if not file_path:
            return
        
        try:
            data = self.data_manager.load_file(file_path)
            
            # Load the data into the UI
            self.title = data["title"]
            self.entries = data["entries"]
            self.current_file_path = file_path
            self.selected_entry_name = None
            
            # Save as last opened file
            self.settings.set_last_file(file_path)
            
            # Update UI
            self.title_edit.setText(self.title)
            self.refresh_display()
            self.update_window_title()
            
            # Capture initial positions as baseline
            self._capture_current_positions()
            
            QMessageBox.information(self, "Success", f"Loaded file: {os.path.basename(file_path)}")
            
        except Exception as e:
            QMessageBox.critical(self, "Error Loading File", f"Failed to load file:\n{str(e)}")
        
    def new_file(self):
        """Create a new empty tally file"""
        # Ask user where to save the new file
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Create New Tally File",
            "new_tally.json",
            "JSON Files (*.json);;All Files (*)"
        )
        
        if not file_path:
            return
            
        if not file_path.endswith('.json'):
            file_path += '.json'
        
        # Reset to empty state
        self.title = "New Tally List"
        self.entries = []
        self.selected_entry_name = None
        self.current_file_path = file_path
        
        # Save the empty file
        try:
            self.data_manager.save_file(file_path, self.title, self.entries)
            self.settings.set_last_file(file_path)
            
            # Update UI
            self.title_edit.setText(self.title)
            self.refresh_display()
            self.update_window_title()
            
            # Capture initial positions as baseline
            self._capture_current_positions()
            
            QMessageBox.information(self, "Success", f"Created new file: {os.path.basename(file_path)}")
        except Exception as e:
            QMessageBox.critical(self, "Error Creating File", f"Failed to create file:\n{str(e)}")
        
    def update_file(self):
        """Update/save current tally data to the current file"""
        if not self.current_file_path:
            QMessageBox.warning(self, "No File", "No file is currently open. Use 'New File' to create one or 'Load File' to open an existing file.")
            return
        
        try:
            self.data_manager.save_file(self.current_file_path, self.title, self.entries)
            QMessageBox.information(self, "Updated", f"Updated file: {os.path.basename(self.current_file_path)}")
        except Exception as e:
            QMessageBox.critical(self, "Error Updating File", f"Failed to update file:\n{str(e)}")
    
    def update_window_title(self):
        """Update the window title to show current file"""
        if self.current_file_path:
            filename = os.path.basename(self.current_file_path)
            self.setWindowTitle(f"Tally - {filename}")
        else:
            self.setWindowTitle("Tally - Point Tracker")
        
    def copy_simple_dump(self):
        """Copy a simple text dump of the current state to clipboard"""
        # Generate the dump text
        dump_text = self.generate_simple_dump()
        
        # Copy to clipboard
        self.clipboard.setText(dump_text)
        
        # Capture current positions for next comparison
        self._capture_current_positions()
        
        # Show confirmation
        lines_count = len(self.entries)
        QMessageBox.information(self, "Copied", f"Copied {lines_count} entries to clipboard")
    
    def generate_simple_dump(self) -> str:
        """Generate a simple human-readable dump of the current state"""
        if not self.entries:
            return f"{self.title}\n(No entries)"
        
        # Sort entries the same way as the display
        sorted_entries = sorted(self.entries, key=lambda x: (-x["value"], x["last_updated"]))
        
        lines = [self.title, "=" * len(self.title), ""]
        
        for rank, entry in enumerate(sorted_entries, 1):
            change_indicator = self._get_position_change_indicator(entry['name'], rank)
            line = f"{rank:2d} {change_indicator} {entry['name']:<20} {entry['value']:3d} points"
            lines.append(line)
        
        return "\n".join(lines)
    
    def _get_position_change_indicator(self, name: str, current_position: int) -> str:
        """Get the position change indicator for an entry"""
        if name not in self.previous_positions:
            return "⚪ -"  # No previous state
        
        previous_position = self.previous_positions[name]
        
        if current_position < previous_position:  # Position improved (lower number = better rank)
            change = previous_position - current_position
            return f"⬆️+{change}"
        elif current_position > previous_position:  # Position declined
            change = current_position - previous_position
            return f"⬇️-{change}"
        else:  # Position stayed the same
            return "⚪ ="
    
    def _capture_current_positions(self):
        """Capture current positions as previous state for next comparison"""
        sorted_entries = sorted(self.entries, key=lambda x: (-x["value"], x["last_updated"]))
        self.previous_positions = {}
        for rank, entry in enumerate(sorted_entries, 1):
            self.previous_positions[entry['name']] = rank
    
    def preview_simple_dump(self):
        """Show a preview of what will be copied"""
        dump_text = self.generate_simple_dump()
        
        # Create a message box with the preview
        msg = QMessageBox(self)
        msg.setWindowTitle("Preview - Simple Dump")
        msg.setText("This is what will be copied to clipboard:")
        msg.setDetailedText(dump_text)
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        
        # Rename buttons
        copy_btn = msg.button(QMessageBox.Ok)
        copy_btn.setText("📋 Copy to Clipboard")
        cancel_btn = msg.button(QMessageBox.Cancel)
        cancel_btn.setText("Close")
        
        # Show dialog and handle result
        result = msg.exec_()
        if result == QMessageBox.Ok:
            self.clipboard.setText(dump_text)
            # Capture current positions for next comparison
            self._capture_current_positions()
            QMessageBox.information(self, "Copied", f"Copied {len(self.entries)} entries to clipboard")
        
    def update_and_copy_changes(self):
        QMessageBox.information(self, "TODO", "Update and copy changes functionality coming soon")


def main():
    app = QApplication(sys.argv)
    window = PyQtTallyApp()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()