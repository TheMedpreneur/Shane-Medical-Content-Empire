#!/usr/bin/env python3
"""
Medical Content Schema Validator
Validates medical content files against defined schemas
"""

import os
import sys
import yaml
import json
from pathlib import Path
from typing import Dict, List, Any

class ContentSchemaValidator:
    """Validates medical content against schemas"""
    
    REQUIRED_FIELDS = {
        'procedure': ['title', 'category', 'medical_specialty', 'content', 'metadata'],
        'anatomy': ['title', 'category', 'body_system', 'content', 'metadata'],
        'clinical_case': ['title', 'category', 'medical_specialty', 'patient_presentation', 'metadata']
    }
    
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.validated_files = 0
    
    def validate_file(self, filepath: Path) -> bool:
        """Validate a single content file"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = yaml.safe_load(f)
            
            if not content:
                self.errors.append(f"{filepath}: Empty file")
                return False
            
            category = content.get('category', '')
            
            # Check required fields
            if category in self.REQUIRED_FIELDS:
                required = self.REQUIRED_FIELDS[category]
                for field in required:
                    if field not in content:
                        self.errors.append(f"{filepath}: Missing required field '{field}'")
                        return False
            
            # Validate metadata
            if 'metadata' in content:
                self._validate_metadata(filepath, content['metadata'])
            
            # Validate compliance
            if 'metadata' in content and 'compliance' in content['metadata']:
                self._validate_compliance(filepath, content['metadata']['compliance'])
            
            self.validated_files += 1
            return True
            
        except yaml.YAMLError as e:
            self.errors.append(f"{filepath}: YAML parsing error - {str(e)}")
            return False
        except Exception as e:
            self.errors.append(f"{filepath}: Validation error - {str(e)}")
            return False
    
    def _validate_metadata(self, filepath: Path, metadata: Dict[str, Any]):
        """Validate metadata section"""
        required_metadata = ['author', 'version']
        for field in required_metadata:
            if field not in metadata or not metadata[field]:
                self.warnings.append(f"{filepath}: Metadata field '{field}' is empty")
    
    def _validate_compliance(self, filepath: Path, compliance: List[str]):
        """Validate compliance requirements"""
        valid_compliance = ['HIPAA', 'FDA_21_CFR_Part_11', 'GDPR', 'HIPAA_Compliant', 
                           'PHI_Removed', 'Educational_Standards']
        for item in compliance:
            if item not in valid_compliance:
                self.warnings.append(f"{filepath}: Unknown compliance type '{item}'")
    
    def validate_directory(self, directory: Path) -> bool:
        """Validate all content files in a directory"""
        success = True
        
        if not directory.exists():
            print(f"Directory not found: {directory}")
            return True  # Not an error if templates haven't been used yet
        
        for filepath in directory.rglob('*.yml'):
            if 'template' not in filepath.name.lower():
                if not self.validate_file(filepath):
                    success = False
        
        for filepath in directory.rglob('*.yaml'):
            if 'template' not in filepath.name.lower():
                if not self.validate_file(filepath):
                    success = False
        
        return success
    
    def print_report(self):
        """Print validation report"""
        print("\n" + "="*60)
        print("Medical Content Schema Validation Report")
        print("="*60)
        print(f"\nFiles validated: {self.validated_files}")
        
        if self.errors:
            print(f"\nErrors found: {len(self.errors)}")
            for error in self.errors:
                print(f"  ❌ {error}")
        else:
            print("\n✅ No errors found")
        
        if self.warnings:
            print(f"\nWarnings: {len(self.warnings)}")
            for warning in self.warnings:
                print(f"  ⚠️  {warning}")
        else:
            print("✅ No warnings")
        
        print("\n" + "="*60)

def main():
    """Main validation function"""
    validator = ContentSchemaValidator()
    
    # Get project root
    project_root = Path(__file__).parent.parent.parent
    
    # Validate content directories
    directories = [
        project_root / 'templates' / 'medical-content',
        project_root / 'content'
    ]
    
    success = True
    for directory in directories:
        if directory.exists():
            if not validator.validate_directory(directory):
                success = False
    
    validator.print_report()
    
    if not success:
        sys.exit(1)
    
    print("\n✅ Schema validation completed successfully!")

if __name__ == '__main__':
    main()
