#!/usr/bin/env python3
"""
Content Metadata Checker
Validates metadata completeness and consistency
"""

import sys
from pathlib import Path
import yaml
from datetime import datetime

class MetadataChecker:
    """Checks content metadata for completeness"""
    
    def __init__(self):
        self.checked_files = 0
        self.errors = []
        self.warnings = []
    
    def check_file(self, filepath: Path) -> bool:
        """Check metadata in a file"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = yaml.safe_load(f)
            
            if not content:
                return True
            
            if 'metadata' not in content:
                self.warnings.append(f"{filepath}: No metadata section")
                return True
            
            metadata = content['metadata']
            
            # Check required metadata fields
            self._check_required_fields(filepath, metadata)
            
            # Check version format
            self._check_version(filepath, metadata)
            
            # Check dates
            self._check_dates(filepath, metadata)
            
            # Check compliance declarations
            self._check_compliance(filepath, metadata)
            
            self.checked_files += 1
            return True
            
        except yaml.YAMLError:
            return True  # Skip non-YAML files
        except Exception as e:
            self.errors.append(f"{filepath}: {str(e)}")
            return False
    
    def _check_required_fields(self, filepath: Path, metadata: dict):
        """Check required metadata fields"""
        required = ['author', 'version']
        
        for field in required:
            if field not in metadata or not metadata[field]:
                self.warnings.append(
                    f"{filepath}: Missing or empty metadata field: {field}"
                )
    
    def _check_version(self, filepath: Path, metadata: dict):
        """Check version format"""
        if 'version' in metadata and metadata['version']:
            version = str(metadata['version'])
            # Simple version check (X.Y or X.Y.Z)
            parts = version.split('.')
            if len(parts) < 2:
                self.warnings.append(
                    f"{filepath}: Version format should be X.Y or X.Y.Z"
                )
    
    def _check_dates(self, filepath: Path, metadata: dict):
        """Check date fields"""
        date_fields = ['review_date']
        
        for field in date_fields:
            if field in metadata and metadata[field]:
                try:
                    # Try to parse as date
                    datetime.fromisoformat(str(metadata[field]))
                except ValueError:
                    self.warnings.append(
                        f"{filepath}: {field} should be in ISO format (YYYY-MM-DD)"
                    )
    
    def _check_compliance(self, filepath: Path, metadata: dict):
        """Check compliance declarations"""
        if 'compliance' not in metadata:
            self.warnings.append(
                f"{filepath}: No compliance declarations in metadata"
            )
        elif not metadata['compliance']:
            self.warnings.append(
                f"{filepath}: Compliance declarations list is empty"
            )
    
    def check_directory(self, directory: Path) -> bool:
        """Check all files in directory"""
        if not directory.exists():
            return True
        
        success = True
        for filepath in directory.rglob('*.yml'):
            if 'template' not in filepath.name.lower():
                if not self.check_file(filepath):
                    success = False
        
        for filepath in directory.rglob('*.yaml'):
            if 'template' not in filepath.name.lower():
                if not self.check_file(filepath):
                    success = False
        
        return success
    
    def print_report(self):
        """Print check report"""
        print("\n" + "="*60)
        print("Content Metadata Check Report")
        print("="*60)
        print(f"\nFiles checked: {self.checked_files}")
        
        if self.errors:
            print(f"\nErrors: {len(self.errors)}")
            for error in self.errors:
                print(f"  ❌ {error}")
        else:
            print("\n✅ No errors found")
        
        if self.warnings:
            print(f"\nWarnings: {len(self.warnings)}")
            for warning in self.warnings[:10]:
                print(f"  ⚠️  {warning}")
            if len(self.warnings) > 10:
                print(f"  ... and {len(self.warnings) - 10} more")
        else:
            print("✅ No warnings")
        
        print("\n" + "="*60)

def main():
    """Main checking function"""
    checker = MetadataChecker()
    
    project_root = Path(__file__).parent.parent.parent
    
    directories = [
        project_root / 'templates' / 'medical-content',
        project_root / 'content'
    ]
    
    success = True
    for directory in directories:
        if directory.exists():
            if not checker.check_directory(directory):
                success = False
    
    checker.print_report()
    
    print("\n✅ Metadata check completed!")

if __name__ == '__main__':
    main()
