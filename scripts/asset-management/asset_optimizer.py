#!/usr/bin/env python3
"""
Asset Optimizer
Optimizes UE5 assets for performance
"""

import sys
from pathlib import Path

class AssetOptimizer:
    """Optimizes assets for UE5 performance"""
    
    def __init__(self):
        self.optimized_count = 0
        self.recommendations = []
    
    def analyze_textures(self, texture_dir: Path):
        """Analyze texture assets"""
        print("Analyzing textures...")
        
        if not texture_dir.exists():
            print(f"Texture directory not found: {texture_dir}")
            return
        
        texture_exts = ['.png', '.jpg', '.jpeg', '.tga', '.bmp']
        
        for filepath in texture_dir.rglob('*'):
            if filepath.suffix.lower() in texture_exts:
                size = filepath.stat().st_size
                
                # Recommend optimization for large textures
                if size > 10 * 1024 * 1024:  # > 10MB
                    self.recommendations.append({
                        'file': str(filepath.name),
                        'type': 'Texture',
                        'issue': 'Large file size',
                        'recommendation': 'Consider using compressed texture format (DXT/BC)',
                        'size_mb': size / (1024 * 1024)
                    })
    
    def analyze_models(self, model_dir: Path):
        """Analyze 3D model assets"""
        print("Analyzing 3D models...")
        
        if not model_dir.exists():
            print(f"Model directory not found: {model_dir}")
            return
        
        model_exts = ['.fbx', '.obj', '.blend']
        
        for filepath in model_dir.rglob('*'):
            if filepath.suffix.lower() in model_exts:
                size = filepath.stat().st_size
                
                # Recommend optimization for large models
                if size > 50 * 1024 * 1024:  # > 50MB
                    self.recommendations.append({
                        'file': str(filepath.name),
                        'type': '3D Model',
                        'issue': 'Large file size',
                        'recommendation': 'Consider reducing polygon count or using LODs',
                        'size_mb': size / (1024 * 1024)
                    })
    
    def print_report(self):
        """Print optimization report"""
        print("\n" + "="*60)
        print("Asset Optimization Report")
        print("="*60)
        
        if self.recommendations:
            print(f"\n📊 Found {len(self.recommendations)} optimization opportunities:\n")
            
            for i, rec in enumerate(self.recommendations[:10], 1):
                print(f"{i}. {rec['file']}")
                print(f"   Type: {rec['type']}")
                print(f"   Issue: {rec['issue']}")
                print(f"   Size: {rec['size_mb']:.2f} MB")
                print(f"   💡 {rec['recommendation']}")
                print()
            
            if len(self.recommendations) > 10:
                print(f"... and {len(self.recommendations) - 10} more recommendations")
        else:
            print("\n✅ No optimization issues found!")
        
        print("\n📋 General Optimization Tips:")
        print("  • Use appropriate texture compression (DXT1/BC1 for diffuse)")
        print("  • Implement LOD (Level of Detail) for 3D models")
        print("  • Keep texture resolutions power-of-two (1024, 2048, 4096)")
        print("  • Use atlases to reduce draw calls")
        print("  • Optimize polygon count for medical models")
        
        print("\n" + "="*60)

def main():
    """Main optimization function"""
    optimizer = AssetOptimizer()
    
    project_root = Path(__file__).parent.parent.parent
    
    # Analyze different asset types
    texture_dirs = [
        project_root / 'UnrealProject' / 'Content' / 'Textures',
        project_root / 'Assets' / 'Textures'
    ]
    
    model_dirs = [
        project_root / 'UnrealProject' / 'Content' / 'Models',
        project_root / 'Assets' / '3D_Models'
    ]
    
    for texture_dir in texture_dirs:
        optimizer.analyze_textures(texture_dir)
    
    for model_dir in model_dirs:
        optimizer.analyze_models(model_dir)
    
    optimizer.print_report()
    
    print("\n✅ Asset optimization analysis completed!")

if __name__ == '__main__':
    main()
