#!/usr/bin/env python3
"""
Educational Standards Validator
Validates content against educational standards and learning objectives
"""

import sys
from pathlib import Path
import yaml

class EducationalStandardsValidator:
    """Validates educational content standards"""
    
    def __init__(self):
        self.validated_files = 0
        self.errors = []
        self.warnings = []
    
    def validate_file(self, filepath: Path) -> bool:
        """Validate educational standards in a file"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = yaml.safe_load(f)
            
            if not content:
                return True
            
            # Check for learning objectives
            if 'educational_elements' in content:
                self._validate_learning_objectives(filepath, content['educational_elements'])
            
            # Check for assessment criteria
            if 'educational_elements' in content:
                self._validate_assessment(filepath, content['educational_elements'])
            
            # Check for accessibility features
            if 'accessibility' in content:
                self._validate_accessibility(filepath, content['accessibility'])
            
            self.validated_files += 1
            return True
            
        except yaml.YAMLError:
            return True  # Skip non-YAML files
        except Exception as e:
            self.errors.append(f"{filepath}: {str(e)}")
            return False
    
    def _validate_learning_objectives(self, filepath: Path, edu_elements: dict):
        """Validate learning objectives"""
        if 'learning_objectives' not in edu_elements:
            self.warnings.append(
                f"{filepath}: No learning objectives defined"
            )
            return
        
        objectives = edu_elements['learning_objectives']
        if not objectives or len(objectives) == 0:
            self.warnings.append(
                f"{filepath}: Learning objectives list is empty"
            )
        
        # Check objectives follow Bloom's taxonomy
        bloom_verbs = [
            'identify', 'describe', 'explain', 'demonstrate', 'analyze',
            'evaluate', 'create', 'recognize', 'understand', 'apply'
        ]
        
        for obj in objectives:
            if isinstance(obj, str):
                obj_lower = obj.lower()
                has_bloom_verb = any(verb in obj_lower for verb in bloom_verbs)
                if not has_bloom_verb:
                    self.warnings.append(
                        f"{filepath}: Learning objective may not use Bloom's taxonomy: '{obj[:50]}...'"
                    )
    
    def _validate_assessment(self, filepath: Path, edu_elements: dict):
        """Validate assessment criteria"""
        if 'assessment_criteria' in edu_elements or 'assessment_methods' in edu_elements:
            return  # Has assessment criteria
        
        self.warnings.append(
            f"{filepath}: No assessment criteria or methods defined"
        )
    
    def _validate_accessibility(self, filepath: Path, accessibility: dict):
        """Validate accessibility features"""
        required_features = [
            'text_alternatives',
            'keyboard_navigation',
            'adjustable_text_size'
        ]
        
        for feature in required_features:
            if feature not in accessibility:
                self.warnings.append(
                    f"{filepath}: Missing accessibility feature: {feature}"
                )
    
    def validate_directory(self, directory: Path) -> bool:
        """Validate all files in directory"""
        if not directory.exists():
            return True
        
        success = True
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
        print("Educational Standards Validation Report")
        print("="*60)
        print(f"\nFiles validated: {self.validated_files}")
        
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
    """Main validation function"""
    validator = EducationalStandardsValidator()
    
    project_root = Path(__file__).parent.parent.parent
    
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
    
    print("\n✅ Educational standards validation completed!")

if __name__ == '__main__':
    main()
