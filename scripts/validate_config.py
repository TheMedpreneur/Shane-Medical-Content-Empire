#!/usr/bin/env python3
"""
Configuration Validation Script
Validates configuration files and system requirements
"""

import json
import sys
import os
import shutil
from pathlib import Path
from typing import Dict, List, Tuple


def check_python_version() -> Tuple[bool, str]:
    """Check if Python version meets requirements"""
    if sys.version_info < (3, 8):
        return False, f"Python {sys.version_info.major}.{sys.version_info.minor} is not supported. Requires Python 3.8+"
    return True, f"Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"


def check_required_packages() -> Tuple[bool, List[str]]:
    """Check if required Python packages are installed"""
    required_packages = [
        'requests',
        'Pillow',
        'python-dotenv',
        'moviepy',
        'pandas',
        'numpy',
        'beautifulsoup4',
        'lxml',
        'tqdm',
        'python-dateutil'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    return len(missing_packages) == 0, missing_packages


def check_system_tools() -> Tuple[bool, List[str]]:
    """Check if required system tools are available"""
    required_tools = ['ffmpeg']
    optional_tools = ['node', 'git']
    
    missing_required = []
    missing_optional = []
    
    for tool in required_tools:
        if not shutil.which(tool):
            missing_required.append(tool)
    
    for tool in optional_tools:
        if not shutil.which(tool):
            missing_optional.append(tool)
    
    return len(missing_required) == 0, missing_required + missing_optional


def validate_config_file(config_path: str) -> Tuple[bool, List[str]]:
    """Validate configuration file structure and values"""
    errors = []
    
    if not os.path.exists(config_path):
        return False, [f"Configuration file not found: {config_path}"]
    
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
    except json.JSONDecodeError as e:
        return False, [f"Invalid JSON in configuration file: {e}"]
    except Exception as e:
        return False, [f"Error reading configuration file: {e}"]
    
    # Required fields
    required_fields = {
        'content_output_path': str,
        'video_resolution': str,
        'video_framerate': int,
        'video_codec': str,
        'audio_bitrate': str,
        'quality_preset': str
    }
    
    for field, field_type in required_fields.items():
        if field not in config:
            errors.append(f"Missing required field: {field}")
        elif not isinstance(config[field], field_type):
            errors.append(f"Invalid type for {field}: expected {field_type.__name__}, got {type(config[field]).__name__}")
    
    # Validate specific values
    if 'video_resolution' in config:
        resolution = config['video_resolution']
        if 'x' not in resolution:
            errors.append("video_resolution must be in format 'WIDTHxHEIGHT' (e.g., '1920x1080')")
        else:
            try:
                width, height = map(int, resolution.split('x'))
                if width <= 0 or height <= 0:
                    errors.append("video_resolution width and height must be positive integers")
            except ValueError:
                errors.append("video_resolution must contain valid integers separated by 'x'")
    
    if 'video_framerate' in config:
        framerate = config['video_framerate']
        if not isinstance(framerate, int) or framerate <= 0:
            errors.append("video_framerate must be a positive integer")
    
    if 'quality_preset' in config:
        preset = config['quality_preset']
        valid_presets = ['low', 'medium', 'high', 'ultra']
        if preset not in valid_presets:
            errors.append(f"quality_preset must be one of: {', '.join(valid_presets)}")
    
    return len(errors) == 0, errors


def check_directories(config_path: str) -> Tuple[bool, List[str]]:
    """Check if required directories exist and are writable"""
    errors = []
    
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
    except:
        return False, ["Cannot read configuration file"]
    
    # Check output directory
    output_path = config.get('content_output_path', './output')
    output_dir = Path(output_path)
    
    if not output_dir.exists():
        try:
            output_dir.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            errors.append(f"Cannot create output directory {output_path}: {e}")
    elif not os.access(output_dir, os.W_OK):
        errors.append(f"Output directory {output_path} is not writable")
    
    # Check UE5 project path if specified
    ue5_path = config.get('ue5_project_path', '/path/to/ue5/project')
    if ue5_path != '/path/to/ue5/project' and not Path(ue5_path).exists():
        errors.append(f"UE5 project path does not exist: {ue5_path}")
    
    return len(errors) == 0, errors


def check_disk_space(config_path: str) -> Tuple[bool, List[str]]:
    """Check available disk space"""
    warnings = []
    
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
    except:
        return True, ["Cannot check disk space - configuration file error"]
    
    output_path = config.get('content_output_path', './output')
    
    try:
        statvfs = os.statvfs(output_path)
        free_space_gb = (statvfs.f_frsize * statvfs.f_bavail) / (1024**3)
        
        if free_space_gb < 1:
            warnings.append(f"Very low disk space: {free_space_gb:.1f}GB available")
        elif free_space_gb < 5:
            warnings.append(f"Low disk space: {free_space_gb:.1f}GB available (recommend 5GB+)")
    except Exception as e:
        warnings.append(f"Cannot check disk space: {e}")
    
    return True, warnings


def main():
    """Main validation function"""
    print("🔍 Medical Content Production System - Configuration Validation")
    print("=" * 60)
    
    config_path = "config/automation.json"
    if len(sys.argv) > 1:
        config_path = sys.argv[1]
    
    all_passed = True
    all_warnings = []
    
    # Check Python version
    print("\n📋 Checking Python version...")
    python_ok, python_msg = check_python_version()
    if python_ok:
        print(f"✅ {python_msg}")
    else:
        print(f"❌ {python_msg}")
        all_passed = False
    
    # Check required packages
    print("\n📦 Checking Python packages...")
    packages_ok, missing_packages = check_required_packages()
    if packages_ok:
        print("✅ All required packages are installed")
    else:
        print(f"❌ Missing required packages: {', '.join(missing_packages)}")
        print("   Install with: pip install -r requirements.txt")
        all_passed = False
    
    # Check system tools
    print("\n🛠️  Checking system tools...")
    tools_ok, missing_tools = check_system_tools()
    if tools_ok:
        print("✅ All required system tools are available")
    else:
        required_missing = [tool for tool in missing_tools if tool in ['ffmpeg']]
        optional_missing = [tool for tool in missing_tools if tool not in ['ffmpeg']]
        
        if required_missing:
            print(f"❌ Missing required tools: {', '.join(required_missing)}")
            all_passed = False
        if optional_missing:
            print(f"⚠️  Missing optional tools: {', '.join(optional_missing)}")
            all_warnings.extend(optional_missing)
    
    # Validate configuration file
    print(f"\n⚙️  Validating configuration file: {config_path}")
    config_ok, config_errors = validate_config_file(config_path)
    if config_ok:
        print("✅ Configuration file is valid")
    else:
        print("❌ Configuration file validation failed:")
        for error in config_errors:
            print(f"   • {error}")
        all_passed = False
    
    # Check directories
    print("\n📁 Checking directories...")
    dirs_ok, dir_errors = check_directories(config_path)
    if dirs_ok:
        print("✅ All directories are accessible")
    else:
        print("❌ Directory issues:")
        for error in dir_errors:
            print(f"   • {error}")
        all_passed = False
    
    # Check disk space
    print("\n💾 Checking disk space...")
    space_ok, space_warnings = check_disk_space(config_path)
    all_warnings.extend(space_warnings)
    if space_warnings:
        for warning in space_warnings:
            print(f"⚠️  {warning}")
    else:
        print("✅ Sufficient disk space available")
    
    # Summary
    print("\n" + "=" * 60)
    if all_passed:
        print("🎉 All validation checks passed!")
        if all_warnings:
            print(f"\n⚠️  Warnings ({len(all_warnings)}):")
            for warning in all_warnings:
                print(f"   • {warning}")
        print("\n✅ System is ready for content production!")
        return 0
    else:
        print("❌ Validation failed. Please fix the issues above before proceeding.")
        return 1


if __name__ == "__main__":
    sys.exit(main())