#!/usr/bin/env python3
"""
Content Quality Metrics Generator
Generates quality metrics for medical educational content
"""

import sys
from pathlib import Path
import yaml
import json

class QualityMetricsGenerator:
    """Generates quality metrics for content"""
    
    def __init__(self):
        self.metrics = {
            'total_files': 0,
            'by_category': {},
            'by_specialty': {},
            'by_difficulty': {},
            'with_references': 0,
            'with_learning_objectives': 0,
            'with_accessibility': 0,
            'peer_reviewed': 0,
            'compliance_coverage': {}
        }
    
    def analyze_file(self, filepath: Path) -> bool:
        """Analyze a single file"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = yaml.safe_load(f)
            
            if not content:
                return True
            
            self.metrics['total_files'] += 1
            
            # Category metrics
            if 'category' in content:
                category = content['category']
                self.metrics['by_category'][category] = \
                    self.metrics['by_category'].get(category, 0) + 1
            
            # Specialty metrics
            specialty_fields = ['medical_specialty', 'body_system']
            for field in specialty_fields:
                if field in content:
                    specialty = content[field]
                    self.metrics['by_specialty'][specialty] = \
                        self.metrics['by_specialty'].get(specialty, 0) + 1
            
            # Difficulty metrics
            if 'difficulty_level' in content:
                level = content['difficulty_level']
                self.metrics['by_difficulty'][level] = \
                    self.metrics['by_difficulty'].get(level, 0) + 1
            
            # Quality indicators
            if 'references' in content and content['references']:
                self.metrics['with_references'] += 1
            
            if 'educational_elements' in content:
                edu = content['educational_elements']
                if 'learning_objectives' in edu and edu['learning_objectives']:
                    self.metrics['with_learning_objectives'] += 1
            
            if 'accessibility' in content:
                self.metrics['with_accessibility'] += 1
            
            # Peer review status
            if 'quality_assurance' in content:
                qa = content['quality_assurance']
                if qa.get('peer_reviewed', False):
                    self.metrics['peer_reviewed'] += 1
            
            # Compliance coverage
            if 'metadata' in content and 'compliance' in content['metadata']:
                for compliance_type in content['metadata']['compliance']:
                    self.metrics['compliance_coverage'][compliance_type] = \
                        self.metrics['compliance_coverage'].get(compliance_type, 0) + 1
            
            return True
            
        except yaml.YAMLError:
            return True  # Skip non-YAML files
        except Exception as e:
            print(f"Warning: Error analyzing {filepath}: {str(e)}")
            return False
    
    def analyze_directory(self, directory: Path):
        """Analyze all files in directory"""
        if not directory.exists():
            return
        
        for filepath in directory.rglob('*.yml'):
            if 'template' not in filepath.name.lower():
                self.analyze_file(filepath)
        
        for filepath in directory.rglob('*.yaml'):
            if 'template' not in filepath.name.lower():
                self.analyze_file(filepath)
    
    def generate_report(self):
        """Generate and print quality metrics report"""
        print("\n" + "="*60)
        print("Content Quality Metrics Report")
        print("="*60)
        
        print(f"\n📊 Total Content Files: {self.metrics['total_files']}")
        
        if self.metrics['by_category']:
            print("\n📁 By Category:")
            for category, count in sorted(self.metrics['by_category'].items()):
                print(f"  • {category}: {count}")
        
        if self.metrics['by_specialty']:
            print("\n🏥 By Specialty/System:")
            for specialty, count in sorted(self.metrics['by_specialty'].items()):
                print(f"  • {specialty}: {count}")
        
        if self.metrics['by_difficulty']:
            print("\n📈 By Difficulty Level:")
            for level, count in sorted(self.metrics['by_difficulty'].items()):
                print(f"  • {level}: {count}")
        
        if self.metrics['total_files'] > 0:
            print("\n✅ Quality Indicators:")
            pct_refs = (self.metrics['with_references'] / self.metrics['total_files']) * 100
            pct_obj = (self.metrics['with_learning_objectives'] / self.metrics['total_files']) * 100
            pct_acc = (self.metrics['with_accessibility'] / self.metrics['total_files']) * 100
            pct_peer = (self.metrics['peer_reviewed'] / self.metrics['total_files']) * 100
            
            print(f"  • With References: {self.metrics['with_references']} ({pct_refs:.1f}%)")
            print(f"  • With Learning Objectives: {self.metrics['with_learning_objectives']} ({pct_obj:.1f}%)")
            print(f"  • With Accessibility Features: {self.metrics['with_accessibility']} ({pct_acc:.1f}%)")
            print(f"  • Peer Reviewed: {self.metrics['peer_reviewed']} ({pct_peer:.1f}%)")
        
        if self.metrics['compliance_coverage']:
            print("\n🔒 Compliance Coverage:")
            for compliance, count in sorted(self.metrics['compliance_coverage'].items()):
                print(f"  • {compliance}: {count} files")
        
        print("\n" + "="*60)
        
        # Save metrics to JSON file
        project_root = Path(__file__).parent.parent.parent
        reports_dir = project_root / 'reports'
        reports_dir.mkdir(exist_ok=True)
        
        metrics_file = reports_dir / 'quality-metrics.json'
        with open(metrics_file, 'w') as f:
            json.dump(self.metrics, f, indent=2)
        
        print(f"\n📄 Metrics saved to: {metrics_file}")

def main():
    """Main function"""
    generator = QualityMetricsGenerator()
    
    project_root = Path(__file__).parent.parent.parent
    
    directories = [
        project_root / 'templates' / 'medical-content',
        project_root / 'content'
    ]
    
    for directory in directories:
        if directory.exists():
            generator.analyze_directory(directory)
    
    generator.generate_report()
    
    print("\n✅ Quality metrics generation completed!")

if __name__ == '__main__':
    main()
