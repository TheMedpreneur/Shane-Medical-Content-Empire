#!/usr/bin/env python3
"""
Citation and Reference Checker
Validates citations and references in medical content
"""

import sys
import re
from pathlib import Path
import yaml

class CitationChecker:
    """Checks citations and references for completeness"""
    
    def __init__(self):
        self.checked_files = 0
        self.errors = []
        self.warnings = []
    
    def check_file(self, filepath: Path) -> bool:
        """Check citations in a file"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = yaml.safe_load(f)
            
            if not content:
                return True
            
            # Check for references section
            if 'references' in content:
                self._validate_references(filepath, content['references'])
            else:
                # Only warn if it's not a template
                if 'template' not in filepath.name.lower():
                    self.warnings.append(
                        f"{filepath}: No references section found"
                    )
            
            self.checked_files += 1
            return True
            
        except yaml.YAMLError:
            return True  # Skip non-YAML files
        except Exception as e:
            self.errors.append(f"{filepath}: {str(e)}")
            return False
    
    def _validate_references(self, filepath: Path, references: list):
        """Validate references list"""
        if not references:
            self.warnings.append(f"{filepath}: References section is empty")
            return
        
        for i, ref in enumerate(references, 1):
            if not isinstance(ref, dict):
                self.errors.append(
                    f"{filepath}: Reference {i} is not properly formatted"
                )
                continue
            
            # Check for citation
            if 'citation' not in ref or not ref['citation']:
                self.errors.append(
                    f"{filepath}: Reference {i} missing citation"
                )
            
            # Check for DOI or URL for verification
            has_doi = 'doi' in ref and ref['doi']
            has_url = 'url' in ref and ref['url']
            
            if not has_doi and not has_url:
                self.warnings.append(
                    f"{filepath}: Reference {i} has no DOI or URL for verification"
                )
            
            # Validate DOI format if present
            if has_doi:
                doi_pattern = r'^10\.\d{4,}/\S+$'
                if not re.match(doi_pattern, ref['doi']):
                    self.warnings.append(
                        f"{filepath}: Reference {i} has invalid DOI format"
                    )
    
    def check_directory(self, directory: Path) -> bool:
        """Check all files in directory"""
        if not directory.exists():
            return True
        
        success = True
        for filepath in directory.rglob('*.yml'):
            if not self.check_file(filepath):
                success = False
        
        for filepath in directory.rglob('*.yaml'):
            if not self.check_file(filepath):
                success = False
        
        return success
    
    def print_report(self):
        """Print check report"""
        print("\n" + "="*60)
        print("Citation and Reference Check Report")
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
    checker = CitationChecker()
    
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
    
    if not success:
        sys.exit(1)
    
    print("\n✅ Citation check completed!")

if __name__ == '__main__':
    main()
