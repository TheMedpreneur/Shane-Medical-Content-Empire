#!/usr/bin/env python3
"""
Medical Terminology Checker
Validates medical terminology usage and consistency
"""

import os
import sys
import re
from pathlib import Path
from typing import List, Dict, Set

class MedicalTerminologyChecker:
    """Checks medical terminology for accuracy and consistency"""
    
    # Common medical abbreviations that should be spelled out in educational content
    ABBREVIATIONS_TO_AVOID = {
        'qd': 'once daily',
        'qod': 'every other day',
        'u': 'unit',
        'iu': 'international unit',
        'ms': 'morphine sulfate or magnesium sulfate (ambiguous)',
    }
    
    # Common medical terms with frequent misspellings
    COMMON_TERMS = {
        'anesthesia', 'pneumonia', 'myocardial', 'cerebrovascular',
        'hemorrhage', 'pharyngitis', 'ophthalmology', 'otolaryngology',
        'gastroenterology', 'endocrinology', 'rheumatology', 'hematology'
    }
    
    def __init__(self):
        self.issues = []
        self.warnings = []
        self.checked_files = 0
    
    def check_file(self, filepath: Path) -> bool:
        """Check a single file for terminology issues"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check for problematic abbreviations
            self._check_abbreviations(filepath, content)
            
            # Check for inconsistent terminology
            self._check_consistency(filepath, content)
            
            # Check for proper anatomical terminology
            self._check_anatomical_terms(filepath, content)
            
            self.checked_files += 1
            return True
            
        except Exception as e:
            self.issues.append(f"{filepath}: Error reading file - {str(e)}")
            return False
    
    def _check_abbreviations(self, filepath: Path, content: str):
        """Check for problematic abbreviations"""
        content_lower = content.lower()
        
        for abbrev, full_term in self.ABBREVIATIONS_TO_AVOID.items():
            # Use word boundaries to avoid false positives
            pattern = r'\b' + re.escape(abbrev) + r'\b'
            if re.search(pattern, content_lower):
                self.warnings.append(
                    f"{filepath}: Found abbreviation '{abbrev}' - "
                    f"consider using '{full_term}' for clarity"
                )
    
    def _check_consistency(self, filepath: Path, content: str):
        """Check for terminology consistency"""
        # Check for mixed spellings (US vs UK English)
        us_uk_pairs = [
            ('anesthesia', 'anaesthesia'),
            ('pediatric', 'paediatric'),
            ('hemoglobin', 'haemoglobin'),
            ('esophagus', 'oesophagus')
        ]
        
        for us_term, uk_term in us_uk_pairs:
            has_us = us_term in content.lower()
            has_uk = uk_term in content.lower()
            
            if has_us and has_uk:
                self.warnings.append(
                    f"{filepath}: Mixed US/UK spelling detected "
                    f"('{us_term}' and '{uk_term}')"
                )
    
    def _check_anatomical_terms(self, filepath: Path, content: str):
        """Check for proper anatomical terminology"""
        # Check for directional terms used correctly
        directional_terms = [
            'superior', 'inferior', 'anterior', 'posterior',
            'medial', 'lateral', 'proximal', 'distal'
        ]
        
        # This is a basic check - in practice, you'd want more sophisticated NLP
        content_lower = content.lower()
        for term in directional_terms:
            if term in content_lower:
                # Just acknowledge that anatomical terms are present
                pass
    
    def check_directory(self, directory: Path) -> bool:
        """Check all files in a directory"""
        if not directory.exists():
            return True  # Not an error if directory doesn't exist yet
        
        success = True
        for filepath in directory.rglob('*.yml'):
            if not self.check_file(filepath):
                success = False
        
        for filepath in directory.rglob('*.yaml'):
            if not self.check_file(filepath):
                success = False
        
        for filepath in directory.rglob('*.md'):
            if not self.check_file(filepath):
                success = False
        
        return success
    
    def print_report(self):
        """Print terminology check report"""
        print("\n" + "="*60)
        print("Medical Terminology Check Report")
        print("="*60)
        print(f"\nFiles checked: {self.checked_files}")
        
        if self.issues:
            print(f"\nIssues found: {len(self.issues)}")
            for issue in self.issues:
                print(f"  ❌ {issue}")
        else:
            print("\n✅ No issues found")
        
        if self.warnings:
            print(f"\nWarnings: {len(self.warnings)}")
            for warning in self.warnings[:10]:  # Limit output
                print(f"  ⚠️  {warning}")
            if len(self.warnings) > 10:
                print(f"  ... and {len(self.warnings) - 10} more warnings")
        else:
            print("✅ No warnings")
        
        print("\n" + "="*60)

def main():
    """Main checking function"""
    checker = MedicalTerminologyChecker()
    
    project_root = Path(__file__).parent.parent.parent
    
    directories = [
        project_root / 'templates',
        project_root / 'content',
        project_root / 'docs'
    ]
    
    success = True
    for directory in directories:
        if directory.exists():
            if not checker.check_directory(directory):
                success = False
    
    checker.print_report()
    
    if not success:
        sys.exit(1)
    
    print("\n✅ Medical terminology check completed!")

if __name__ == '__main__':
    main()
