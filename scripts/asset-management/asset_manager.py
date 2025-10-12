#!/usr/bin/env python3
"""
UE5 Asset Manager
Manages Unreal Engine 5 medical content assets
"""

import os
import sys
import json
from pathlib import Path
from typing import List, Dict
import hashlib

class UE5AssetManager:
    """Manages UE5 medical content assets"""
    
    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.asset_registry = {}
        self.registry_file = project_root / 'asset-registry.json'
    
    def scan_assets(self, asset_dir: Path) -> Dict:
        """Scan directory for UE5 assets"""
        asset_types = {
            '.uasset': 'UE5 Asset',
            '.umap': 'UE5 Level',
            '.fbx': '3D Model',
            '.obj': '3D Model',
            '.png': 'Texture',
            '.jpg': 'Texture',
            '.tga': 'Texture',
            '.mp4': 'Video',
            '.wav': 'Audio',
            '.mp3': 'Audio'
        }
        
        assets = []
        
        if not asset_dir.exists():
            print(f"Asset directory not found: {asset_dir}")
            return assets
        
        for filepath in asset_dir.rglob('*'):
            if filepath.is_file():
                ext = filepath.suffix.lower()
                if ext in asset_types:
                    asset_info = {
                        'path': str(filepath.relative_to(self.project_root)),
                        'name': filepath.name,
                        'type': asset_types[ext],
                        'size': filepath.stat().st_size,
                        'checksum': self._calculate_checksum(filepath)
                    }
                    assets.append(asset_info)
        
        return assets
    
    def _calculate_checksum(self, filepath: Path) -> str:
        """Calculate file checksum"""
        try:
            with open(filepath, 'rb') as f:
                file_hash = hashlib.md5()
                chunk = f.read(8192)
                while chunk:
                    file_hash.update(chunk)
                    chunk = f.read(8192)
                return file_hash.hexdigest()
        except Exception:
            return ""
    
    def generate_registry(self):
        """Generate asset registry"""
        print("Generating asset registry...")
        
        # Common UE5 asset directories
        asset_dirs = [
            self.project_root / 'UnrealProject' / 'Content',
            self.project_root / 'Assets' / '3D_Models',
            self.project_root / 'Assets' / 'Textures',
            self.project_root / 'Assets' / 'Audio',
            self.project_root / 'Assets' / 'Video'
        ]
        
        all_assets = []
        for asset_dir in asset_dirs:
            if asset_dir.exists():
                assets = self.scan_assets(asset_dir)
                all_assets.extend(assets)
        
        self.asset_registry = {
            'version': '1.0',
            'total_assets': len(all_assets),
            'assets': all_assets,
            'categories': self._categorize_assets(all_assets)
        }
        
        # Save registry
        with open(self.registry_file, 'w') as f:
            json.dump(self.asset_registry, f, indent=2)
        
        print(f"Asset registry saved to: {self.registry_file}")
        print(f"Total assets: {len(all_assets)}")
    
    def _categorize_assets(self, assets: List[Dict]) -> Dict:
        """Categorize assets by type"""
        categories = {}
        for asset in assets:
            asset_type = asset['type']
            if asset_type not in categories:
                categories[asset_type] = 0
            categories[asset_type] += 1
        return categories
    
    def validate_assets(self) -> bool:
        """Validate asset integrity"""
        print("\nValidating assets...")
        
        if not self.registry_file.exists():
            print("No asset registry found. Run generate_registry first.")
            return False
        
        with open(self.registry_file, 'r') as f:
            registry = json.load(f)
        
        issues = []
        for asset in registry['assets']:
            filepath = self.project_root / asset['path']
            
            if not filepath.exists():
                issues.append(f"Missing: {asset['path']}")
                continue
            
            # Check size
            current_size = filepath.stat().st_size
            if current_size != asset['size']:
                issues.append(f"Size changed: {asset['path']}")
            
            # Check checksum
            current_checksum = self._calculate_checksum(filepath)
            if current_checksum != asset['checksum']:
                issues.append(f"Modified: {asset['path']}")
        
        if issues:
            print(f"\n⚠️  Found {len(issues)} asset issues:")
            for issue in issues[:10]:
                print(f"  • {issue}")
            if len(issues) > 10:
                print(f"  ... and {len(issues) - 10} more")
            return False
        else:
            print("✅ All assets validated successfully!")
            return True
    
    def print_statistics(self):
        """Print asset statistics"""
        if not self.asset_registry:
            if self.registry_file.exists():
                with open(self.registry_file, 'r') as f:
                    self.asset_registry = json.load(f)
            else:
                print("No asset registry available.")
                return
        
        print("\n" + "="*60)
        print("UE5 Asset Statistics")
        print("="*60)
        print(f"\nTotal Assets: {self.asset_registry['total_assets']}")
        
        if self.asset_registry['categories']:
            print("\nAssets by Type:")
            for asset_type, count in sorted(self.asset_registry['categories'].items()):
                print(f"  • {asset_type}: {count}")
        
        total_size = sum(asset['size'] for asset in self.asset_registry['assets'])
        print(f"\nTotal Size: {total_size / (1024*1024):.2f} MB")
        
        print("="*60)

def main():
    """Main function"""
    project_root = Path(__file__).parent.parent.parent
    
    manager = UE5AssetManager(project_root)
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == 'scan':
            manager.generate_registry()
            manager.print_statistics()
        elif command == 'validate':
            manager.validate_assets()
        elif command == 'stats':
            manager.print_statistics()
        else:
            print(f"Unknown command: {command}")
            print("Usage: asset_manager.py [scan|validate|stats]")
            sys.exit(1)
    else:
        # Default: generate registry
        manager.generate_registry()
        manager.print_statistics()
    
    print("\n✅ Asset management completed!")

if __name__ == '__main__':
    main()
