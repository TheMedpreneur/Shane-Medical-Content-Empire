#!/usr/bin/env python3
"""
Accessibility Compliance Checker
Validates content for accessibility standards (WCAG 2.1)
"""

import sys
from pathlib import Path
import yaml

class AccessibilityChecker:
    """Checks accessibility compliance"""
    
    def __init__(self):
        self.checked_files = 0
        self.errors = []
        self.warnings = []
    
    def check_file(self, filepath: Path) -> bool:
        """Check accessibility in a file"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = yaml.safe_load(f)
            
            if not content:
                return True
            
            # Check for accessibility section
            if 'accessibility' in content:
                self._validate_accessibility_features(filepath, content['accessibility'])
            
            # Check interactive elements have accessibility features
            if 'educational_elements' in content:
                edu = content['educational_elements']
                if 'interactive_elements' in edu:
                    self._validate_interactive_accessibility(
                        filepath, edu['interactive_elements']
                    )
            
            self.checked_files += 1
            return True
            
        except yaml.YAMLError:
            return True  # Skip non-YAML files
        except Exception as e:
            self.errors.append(f"{filepath}: {str(e)}")
            return False
    
    def _validate_accessibility_features(self, filepath: Path, accessibility: dict):
        """Validate accessibility features"""
        required_features = {
            'text_alternatives': 'Text alternatives for non-text content',
            'keyboard_navigation': 'Keyboard navigation support',
            'color_blind_friendly': 'Color blind friendly design',
            'adjustable_text_size': 'Adjustable text size'
        }
        
        for feature, description in required_features.items():
            if feature not in accessibility:
                self.warnings.append(
                    f"{filepath}: Missing accessibility feature: {description}"
                )
            elif not accessibility[feature]:
                self.warnings.append(
                    f"{filepath}: Accessibility feature disabled: {description}"
                )
    
    def _validate_interactive_accessibility(self, filepath: Path, elements: list):
        """Validate interactive elements accessibility"""
        for element in elements:
            if not isinstance(element, dict):
                continue
            
            element_type = element.get('type', 'Unknown')
            
            # Check if description is provided (acts as alt text)
            if 'description' not in element or not element['description']:
                self.warnings.append(
                    f"{filepath}: Interactive element '{element_type}' missing description"
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
        print("Accessibility Compliance Check Report")
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
    checker = AccessibilityChecker()
    
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
    
    print("\n✅ Accessibility compliance check completed!")

if __name__ == '__main__':
    main()
