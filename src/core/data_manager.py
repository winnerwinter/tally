#!/usr/bin/env python3

import json
import jsonschema
import os
from typing import Dict, List, Optional


class DataManager:
    def __init__(self, schema_path: str):
        """Initialize the data manager with schema validation"""
        self.schema_path = schema_path
        self.schema = self._load_schema()
        
    def _load_schema(self) -> Dict:
        """Load the JSON schema for validation"""
        try:
            with open(self.schema_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            raise RuntimeError(f"Failed to load schema: {e}")
    
    def validate_data(self, data: Dict) -> bool:
        """Validate data against the schema"""
        try:
            jsonschema.validate(data, self.schema)
            return True
        except jsonschema.exceptions.ValidationError as e:
            raise ValueError(f"Data validation failed: {e.message}")
        except Exception as e:
            raise ValueError(f"Validation error: {e}")
    
    def load_file(self, file_path: str) -> Dict:
        """Load and validate a tally data file"""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON format: {e}")
        except Exception as e:
            raise RuntimeError(f"Failed to read file: {e}")
        
        # Validate against schema
        self.validate_data(data)
        
        return data
    
    def save_file(self, file_path: str, title: str, entries: List[Dict]) -> None:
        """Save tally data to file with validation"""
        data = {
            "title": title,
            "entries": entries
        }
        
        # Validate before saving
        self.validate_data(data)
        
        try:
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            raise RuntimeError(f"Failed to save file: {e}")
    
