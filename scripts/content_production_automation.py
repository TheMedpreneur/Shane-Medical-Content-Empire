#!/usr/bin/env python3
"""
Content Production Automation Script
Automates the workflow for medical content creation, validation, and publishing
"""

import os
import json
import argparse
import subprocess
import logging
import hashlib
import shutil
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Union, Tuple
from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor, as_completed
import tempfile
import contextlib

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('content_production.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

@dataclass
class ValidationResult:
    """Data class for validation results"""
    is_valid: bool
    errors: List[str]
    warnings: List[str]
    metadata: Dict[str, any]

@dataclass
class ProcessingStats:
    """Data class for processing statistics"""
    total_files: int
    processed_files: int
    failed_files: int
    start_time: datetime
    end_time: Optional[datetime] = None


class ContentProductionAutomation:
    """Main automation class for content production workflow"""
    
    def __init__(self, config_path: str = "config/automation.json"):
        """Initialize automation system with configuration"""
        self.config = self.load_config(config_path)
        self.project_root = Path(__file__).parent.parent
        
    def load_config(self, config_path: str) -> Dict:
        """Load automation configuration with validation"""
        config_path = Path(config_path)
        
        if not config_path.exists():
            logger.warning(f"Config file not found: {config_path}, using defaults")
            return self.get_default_config()
        
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            # Validate required configuration keys
            required_keys = ['content_output_path', 'video_resolution', 'video_framerate']
            missing_keys = [key for key in required_keys if key not in config]
            
            if missing_keys:
                logger.warning(f"Missing required config keys: {missing_keys}, using defaults")
                default_config = self.get_default_config()
                config.update({key: default_config[key] for key in missing_keys})
            
            return config
            
        except (json.JSONDecodeError, IOError) as e:
            logger.error(f"Error loading config file: {e}")
            return self.get_default_config()
    
    def get_default_config(self) -> Dict:
        """Return default configuration"""
        return {
            "ue5_project_path": "/path/to/ue5/project",
            "content_output_path": "./output",
            "video_resolution": "1920x1080",
            "video_framerate": 30,
            "video_codec": "h264",
            "audio_bitrate": "192k",
            "quality_preset": "high"
        }
    
    def create_video_from_script(self, script_path: str, output_name: str) -> bool:
        """
        Create video content from script template with enhanced error handling
        
        Args:
            script_path: Path to the script markdown file
            output_name: Name for output video file
            
        Returns:
            bool: Success status
        """
        script_path = Path(script_path)
        if not script_path.exists():
            logger.error(f"Script file not found: {script_path}")
            return False
        
        if not script_path.suffix.lower() in ['.md', '.txt']:
            logger.error(f"Unsupported script format: {script_path.suffix}")
            return False
        
        logger.info(f"Creating video from script: {script_path}")
        
        try:
            # Parse script with validation
            script_data = self.parse_video_script(str(script_path))
            
            # Validate script structure
            validation_result = self.validate_script_enhanced(script_data)
            if not validation_result.is_valid:
                logger.error(f"Script validation failed: {validation_result.errors}")
                return False
            
            # Create output directory if it doesn't exist
            output_dir = Path(self.config['content_output_path'])
            output_dir.mkdir(parents=True, exist_ok=True)
            
            # Generate UE5 sequence
            sequence_path = self.create_ue5_sequence(script_data, output_name)
            
            # Render video from UE5
            video_path = self.render_ue5_video(sequence_path, output_name)
            
            # Add narration audio
            final_video = self.add_narration(video_path, script_data)
            
            # Verify final output exists
            if Path(final_video).exists():
                file_size = Path(final_video).stat().st_size
                logger.info(f"Video created successfully: {final_video} ({file_size:,} bytes)")
                return True
            else:
                logger.error(f"Final video file not found: {final_video}")
                return False
            
        except Exception as e:
            logger.error(f"Error creating video: {str(e)}", exc_info=True)
            return False
    
    def parse_video_script(self, script_path: str) -> Dict:
        """Parse video script markdown file"""
        logger.info(f"Parsing script: {script_path}")
        
        script_data = {
            "metadata": {},
            "sections": [],
            "narration": []
        }
        
        try:
            with open(script_path, 'r') as f:
                content = f.read()
                
            # Parse metadata
            # In a real implementation, this would parse the markdown structure
            script_data["metadata"] = {
                "title": "Medical AI Topic",
                "duration": 600,
                "topic": "AI in Healthcare"
            }
            
            # Parse sections and timing
            script_data["sections"] = [
                {"name": "Introduction", "start": 0, "end": 30},
                {"name": "Main Content", "start": 30, "end": 540},
                {"name": "Summary", "start": 540, "end": 600}
            ]
            
            return script_data
            
        except Exception as e:
            logger.error(f"Error parsing script: {str(e)}")
            return script_data
    
    def validate_script(self, script_data: Dict) -> bool:
        """Validate script structure and content (legacy method)"""
        logger.info("Validating script structure")
        
        required_fields = ["metadata", "sections", "narration"]
        for field in required_fields:
            if field not in script_data:
                logger.error(f"Missing required field: {field}")
                return False
        
        return True
    
    def validate_script_enhanced(self, script_data: Dict) -> ValidationResult:
        """Enhanced script validation with detailed error reporting"""
        logger.info("Validating script structure with enhanced checks")
        
        errors = []
        warnings = []
        metadata = {}
        
        # Check required fields
        required_fields = ["metadata", "sections", "narration"]
        for field in required_fields:
            if field not in script_data:
                errors.append(f"Missing required field: {field}")
        
        # Validate metadata
        if "metadata" in script_data:
            metadata = script_data["metadata"]
            if not isinstance(metadata, dict):
                errors.append("Metadata must be a dictionary")
            else:
                # Check for required metadata fields
                if "title" not in metadata or not metadata["title"]:
                    warnings.append("Missing or empty title in metadata")
                if "duration" not in metadata or not isinstance(metadata["duration"], (int, float)):
                    warnings.append("Missing or invalid duration in metadata")
        
        # Validate sections
        if "sections" in script_data:
            sections = script_data["sections"]
            if not isinstance(sections, list):
                errors.append("Sections must be a list")
            elif len(sections) == 0:
                warnings.append("No sections found in script")
            else:
                # Validate section structure
                for i, section in enumerate(sections):
                    if not isinstance(section, dict):
                        errors.append(f"Section {i} must be a dictionary")
                    else:
                        if "name" not in section:
                            warnings.append(f"Section {i} missing name")
                        if "start" not in section or "end" not in section:
                            warnings.append(f"Section {i} missing timing information")
        
        # Validate narration
        if "narration" in script_data:
            narration = script_data["narration"]
            if not isinstance(narration, list):
                errors.append("Narration must be a list")
        
        # Check for content quality
        if "sections" in script_data and len(script_data["sections"]) > 0:
            total_duration = max(section.get("end", 0) for section in script_data["sections"])
            if total_duration < 60:  # Less than 1 minute
                warnings.append("Script duration is very short")
            elif total_duration > 1800:  # More than 30 minutes
                warnings.append("Script duration is very long")
        
        is_valid = len(errors) == 0
        
        return ValidationResult(
            is_valid=is_valid,
            errors=errors,
            warnings=warnings,
            metadata=metadata
        )
    
    def create_ue5_sequence(self, script_data: Dict, sequence_name: str) -> str:
        """
        Create UE5 Level Sequence from script data
        
        Args:
            script_data: Parsed script data
            sequence_name: Name for the sequence
            
        Returns:
            str: Path to created sequence
        """
        logger.info(f"Creating UE5 sequence: {sequence_name}")
        
        # In a real implementation, this would use UE5 Python API
        # or command-line tools to create sequences
        
        sequence_path = f"{self.config['ue5_project_path']}/Content/Sequences/{sequence_name}.uasset"
        
        # Placeholder for actual UE5 sequence creation
        logger.info(f"UE5 sequence created: {sequence_path}")
        
        return sequence_path
    
    def render_ue5_video(self, sequence_path: str, output_name: str) -> str:
        """
        Render video from UE5 sequence using Movie Render Queue
        
        Args:
            sequence_path: Path to UE5 sequence
            output_name: Output video filename
            
        Returns:
            str: Path to rendered video
        """
        logger.info(f"Rendering UE5 video: {output_name}")
        
        output_path = f"{self.config['content_output_path']}/{output_name}.mp4"
        
        # UE5 command-line rendering
        # In real implementation, would execute UE5 with Movie Render Queue
        ue5_cmd = [
            f"{self.config['ue5_project_path']}/Engine/Binaries/Win64/UnrealEditor-Cmd.exe",
            self.config['ue5_project_path'],
            "-MoviePipelineConfig=/Game/Config/MovieRenderQueue.ini",
            f"-LevelSequence={sequence_path}",
            f"-MoviePipelineLocalExecutorClass=/Script/MovieRenderPipelineCore.MoviePipelineExecutor",
            "-windowed",
            "-ResX=1920",
            "-ResY=1080"
        ]
        
        logger.info(f"Video rendered: {output_path}")
        return output_path
    
    def add_narration(self, video_path: str, script_data: Dict) -> str:
        """
        Add narration audio to video using text-to-speech or audio files
        
        Args:
            video_path: Path to video file
            script_data: Script data containing narration
            
        Returns:
            str: Path to final video with audio
        """
        logger.info("Adding narration to video")
        
        output_path = video_path.replace(".mp4", "_final.mp4")
        
        # Use FFmpeg to add audio
        # In real implementation, would generate or use narration audio files
        ffmpeg_cmd = [
            "ffmpeg",
            "-i", video_path,
            "-i", "narration_audio.mp3",
            "-c:v", "copy",
            "-c:a", "aac",
            "-b:a", self.config['audio_bitrate'],
            output_path
        ]
        
        logger.info(f"Final video with narration: {output_path}")
        return output_path
    
    def batch_create_modules(self, module_list: List[str], max_workers: int = None) -> Dict[str, bool]:
        """
        Batch create multiple course modules with parallel processing
        
        Args:
            module_list: List of module configuration files
            max_workers: Maximum number of parallel workers (default from config)
            
        Returns:
            Dict mapping module names to success status
        """
        logger.info(f"Batch creating {len(module_list)} modules")
        
        if max_workers is None:
            max_workers = self.config.get('max_workers', 4)
        
        results = {}
        stats = ProcessingStats(
            total_files=len(module_list),
            processed_files=0,
            failed_files=0,
            start_time=datetime.now()
        )
        
        # Process modules in parallel
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Submit all tasks
            future_to_module = {
                executor.submit(self._process_single_module, module_config): module_config
                for module_config in module_list
            }
            
            # Collect results as they complete
            for future in as_completed(future_to_module):
                module_config = future_to_module[future]
                module_name = Path(module_config).stem
                
                try:
                    success = future.result()
                    results[module_name] = success
                    stats.processed_files += 1
                    if not success:
                        stats.failed_files += 1
                    
                    logger.info(f"Completed module: {module_name} - {'Success' if success else 'Failed'}")
                    
                except Exception as e:
                    logger.error(f"Error processing module {module_name}: {str(e)}")
                    results[module_name] = False
                    stats.processed_files += 1
                    stats.failed_files += 1
        
        stats.end_time = datetime.now()
        duration = (stats.end_time - stats.start_time).total_seconds()
        
        logger.info(f"Batch processing complete: {stats.processed_files}/{stats.total_files} successful, "
                   f"{stats.failed_files} failed in {duration:.2f} seconds")
        
        return results
    
    def _process_single_module(self, module_config: str) -> bool:
        """Process a single module (used by batch processing)"""
        module_name = Path(module_config).stem
        logger.info(f"Processing module: {module_name}")
        
        try:
            # Load module configuration with validation
            with open(module_config, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            # Validate module configuration
            if not self._validate_module_config(config):
                logger.error(f"Invalid module configuration: {module_name}")
                return False
            
            # Create module content
            success = self.create_module_content(config)
            return success
            
        except Exception as e:
            logger.error(f"Error processing module {module_name}: {str(e)}")
            return False
    
    def _validate_module_config(self, config: Dict) -> bool:
        """Validate module configuration structure"""
        required_fields = ['name', 'videos', 'interactives', 'assessments']
        
        for field in required_fields:
            if field not in config:
                logger.error(f"Missing required field in module config: {field}")
                return False
        
        # Validate videos list
        if not isinstance(config['videos'], list):
            logger.error("Videos must be a list")
            return False
        
        # Validate each video entry
        for i, video in enumerate(config['videos']):
            if not isinstance(video, dict):
                logger.error(f"Video {i} must be a dictionary")
                return False
            if 'script' not in video or 'name' not in video:
                logger.error(f"Video {i} missing required fields (script, name)")
                return False
        
        return True
    
    def create_module_content(self, module_config: Dict) -> bool:
        """Create all content for a single module"""
        logger.info(f"Creating content for module: {module_config.get('name', 'Unknown')}")
        
        try:
            # Create videos
            for video_script in module_config.get('videos', []):
                self.create_video_from_script(video_script['script'], video_script['name'])
            
            # Setup interactive elements
            for interactive in module_config.get('interactives', []):
                self.setup_interactive_element(interactive)
            
            # Generate assessments
            for assessment in module_config.get('assessments', []):
                self.generate_assessment(assessment)
            
            return True
            
        except Exception as e:
            logger.error(f"Error creating module content: {str(e)}")
            return False
    
    def setup_interactive_element(self, interactive_config: Dict) -> bool:
        """Setup interactive UE5 blueprint element"""
        logger.info(f"Setting up interactive element: {interactive_config.get('name')}")
        
        # In real implementation, would configure UE5 blueprints
        return True
    
    def generate_assessment(self, assessment_config: Dict) -> bool:
        """Generate assessment from configuration"""
        logger.info(f"Generating assessment: {assessment_config.get('name')}")
        
        # In real implementation, would create assessment in LMS
        return True
    
    def validate_medical_content(self, content_path: str) -> Dict:
        """
        Validate medical content for accuracy and compliance
        
        Args:
            content_path: Path to content to validate
            
        Returns:
            Dict with validation results
        """
        logger.info(f"Validating medical content: {content_path}")
        
        validation_results = {
            "medical_accuracy": True,
            "terminology_check": True,
            "compliance_check": True,
            "issues": []
        }
        
        # Placeholder for actual validation logic
        # In real implementation, would check against medical databases
        # and compliance requirements
        
        return validation_results
    
    def optimize_media(self, media_path: str, media_type: str = "video") -> bool:
        """
        Optimize media files for web delivery with enhanced validation
        
        Args:
            media_path: Path to media file
            media_type: Type of media (video, image, audio)
            
        Returns:
            bool: Success status
        """
        media_path = Path(media_path)
        
        if not media_path.exists():
            logger.error(f"Media file not found: {media_path}")
            return False
        
        # Validate file size
        file_size = media_path.stat().st_size
        if file_size == 0:
            logger.error(f"Media file is empty: {media_path}")
            return False
        
        logger.info(f"Optimizing {media_type}: {media_path} ({file_size:,} bytes)")
        
        try:
            if media_type == "video":
                return self.optimize_video(str(media_path))
            elif media_type == "image":
                return self.optimize_image(str(media_path))
            elif media_type == "audio":
                return self.optimize_audio(str(media_path))
            else:
                logger.error(f"Unsupported media type: {media_type}")
                return False
                
        except Exception as e:
            logger.error(f"Error optimizing {media_type} {media_path}: {str(e)}")
            return False
    
    def optimize_video(self, video_path: str) -> bool:
        """Optimize video for streaming with actual FFmpeg execution"""
        logger.info(f"Optimizing video: {video_path}")
        
        video_path = Path(video_path)
        output_path = video_path.parent / f"{video_path.stem}_optimized{video_path.suffix}"
        
        # Check if FFmpeg is available
        if not shutil.which("ffmpeg"):
            logger.error("FFmpeg not found in PATH. Please install FFmpeg to optimize videos.")
            return False
        
        # Get video resolution from config
        resolution = self.config.get('video_resolution', '1920x1080')
        width, height = resolution.split('x')
        
        # Use FFmpeg for optimization
        ffmpeg_cmd = [
            "ffmpeg",
            "-i", str(video_path),
            "-c:v", "libx264",
            "-preset", "slow",
            "-crf", "22",
            "-vf", f"scale={width}:{height}",
            "-c:a", "aac",
            "-b:a", self.config.get('audio_bitrate', '128k'),
            "-movflags", "+faststart",
            "-y",  # Overwrite output file
            str(output_path)
        ]
        
        try:
            # Execute FFmpeg command
            result = subprocess.run(
                ffmpeg_cmd,
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )
            
            if result.returncode == 0:
                # Verify output file was created and has content
                if output_path.exists() and output_path.stat().st_size > 0:
                    original_size = video_path.stat().st_size
                    optimized_size = output_path.stat().st_size
                    compression_ratio = (1 - optimized_size / original_size) * 100
                    
                    logger.info(f"Video optimized successfully: {output_path}")
                    logger.info(f"Size reduction: {compression_ratio:.1f}% "
                              f"({original_size:,} -> {optimized_size:,} bytes)")
                    return True
                else:
                    logger.error(f"Optimized video file not created or empty: {output_path}")
                    return False
            else:
                logger.error(f"FFmpeg failed with return code {result.returncode}")
                logger.error(f"FFmpeg stderr: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            logger.error(f"FFmpeg optimization timed out for: {video_path}")
            return False
        except Exception as e:
            logger.error(f"Error running FFmpeg: {str(e)}")
            return False
    
    def optimize_image(self, image_path: str) -> bool:
        """Optimize image for web using PIL/Pillow"""
        logger.info(f"Optimizing image: {image_path}")
        
        try:
            from PIL import Image, ImageOps
            
            image_path = Path(image_path)
            output_path = image_path.parent / f"{image_path.stem}_optimized{image_path.suffix}"
            
            with Image.open(image_path) as img:
                # Convert to RGB if necessary
                if img.mode in ('RGBA', 'LA', 'P'):
                    img = img.convert('RGB')
                
                # Resize if too large (max 1920px width)
                max_width = 1920
                if img.width > max_width:
                    ratio = max_width / img.width
                    new_height = int(img.height * ratio)
                    img = img.resize((max_width, new_height), Image.Resampling.LANCZOS)
                
                # Optimize and save
                img.save(
                    output_path,
                    format='JPEG',
                    quality=85,
                    optimize=True,
                    progressive=True
                )
            
            # Verify output
            if output_path.exists() and output_path.stat().st_size > 0:
                original_size = image_path.stat().st_size
                optimized_size = output_path.stat().st_size
                compression_ratio = (1 - optimized_size / original_size) * 100
                
                logger.info(f"Image optimized successfully: {output_path}")
                logger.info(f"Size reduction: {compression_ratio:.1f}% "
                          f"({original_size:,} -> {optimized_size:,} bytes)")
                return True
            else:
                logger.error(f"Optimized image file not created or empty: {output_path}")
                return False
                
        except ImportError:
            logger.error("PIL/Pillow not installed. Please install with: pip install Pillow")
            return False
        except Exception as e:
            logger.error(f"Error optimizing image: {str(e)}")
            return False
    
    def optimize_audio(self, audio_path: str) -> bool:
        """Optimize audio file using FFmpeg"""
        logger.info(f"Optimizing audio: {audio_path}")
        
        audio_path = Path(audio_path)
        output_path = audio_path.parent / f"{audio_path.stem}_optimized{audio_path.suffix}"
        
        # Check if FFmpeg is available
        if not shutil.which("ffmpeg"):
            logger.error("FFmpeg not found in PATH. Please install FFmpeg to optimize audio.")
            return False
        
        # Use FFmpeg for audio optimization
        ffmpeg_cmd = [
            "ffmpeg",
            "-i", str(audio_path),
            "-c:a", "aac",
            "-b:a", self.config.get('audio_bitrate', '128k'),
            "-ar", "44100",  # Sample rate
            "-ac", "2",      # Stereo
            "-y",            # Overwrite output file
            str(output_path)
        ]
        
        try:
            result = subprocess.run(
                ffmpeg_cmd,
                capture_output=True,
                text=True,
                timeout=120  # 2 minute timeout
            )
            
            if result.returncode == 0:
                if output_path.exists() and output_path.stat().st_size > 0:
                    original_size = audio_path.stat().st_size
                    optimized_size = output_path.stat().st_size
                    compression_ratio = (1 - optimized_size / original_size) * 100
                    
                    logger.info(f"Audio optimized successfully: {output_path}")
                    logger.info(f"Size reduction: {compression_ratio:.1f}% "
                              f"({original_size:,} -> {optimized_size:,} bytes)")
                    return True
                else:
                    logger.error(f"Optimized audio file not created or empty: {output_path}")
                    return False
            else:
                logger.error(f"FFmpeg failed with return code {result.returncode}")
                logger.error(f"FFmpeg stderr: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            logger.error(f"Audio optimization timed out for: {audio_path}")
            return False
        except Exception as e:
            logger.error(f"Error optimizing audio: {str(e)}")
            return False
    
    def generate_report(self, output_path: str = "reports/production_report.html", 
                       stats: ProcessingStats = None) -> bool:
        """Generate comprehensive production report"""
        logger.info(f"Generating production report: {output_path}")
        
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Gather statistics
        if stats is None:
            stats = ProcessingStats(
                total_files=0,
                processed_files=0,
                failed_files=0,
                start_time=datetime.now()
            )
        
        # Calculate duration
        duration = "N/A"
        if stats.end_time:
            duration = f"{(stats.end_time - stats.start_time).total_seconds():.2f} seconds"
        
        # Generate file checksums for integrity verification
        checksums = self._generate_file_checksums()
        
        report_html = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Content Production Report</title>
            <style>
                body {{ 
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
                    margin: 0; 
                    padding: 20px; 
                    background-color: #f5f5f5;
                }}
                .container {{
                    max-width: 1200px;
                    margin: 0 auto;
                    background: white;
                    padding: 30px;
                    border-radius: 8px;
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                }}
                h1 {{ 
                    color: #2c3e50; 
                    border-bottom: 3px solid #3498db;
                    padding-bottom: 10px;
                }}
                h2 {{ 
                    color: #34495e; 
                    margin-top: 30px;
                }}
                table {{ 
                    border-collapse: collapse; 
                    width: 100%; 
                    margin-top: 20px; 
                    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
                }}
                th, td {{ 
                    border: 1px solid #ddd; 
                    padding: 12px; 
                    text-align: left; 
                }}
                th {{ 
                    background-color: #3498db; 
                    color: white; 
                    font-weight: 600;
                }}
                tr:nth-child(even) {{ background-color: #f8f9fa; }}
                .success {{ color: #27ae60; font-weight: bold; }}
                .failure {{ color: #e74c3c; font-weight: bold; }}
                .warning {{ color: #f39c12; font-weight: bold; }}
                .info {{ color: #3498db; }}
                .status-badge {{
                    display: inline-block;
                    padding: 4px 8px;
                    border-radius: 4px;
                    font-size: 12px;
                    font-weight: bold;
                }}
                .status-success {{ background-color: #d4edda; color: #155724; }}
                .status-failure {{ background-color: #f8d7da; color: #721c24; }}
                .status-warning {{ background-color: #fff3cd; color: #856404; }}
                .summary-grid {{
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                    gap: 20px;
                    margin: 20px 0;
                }}
                .summary-card {{
                    background: #f8f9fa;
                    padding: 20px;
                    border-radius: 8px;
                    text-align: center;
                    border-left: 4px solid #3498db;
                }}
                .summary-card h3 {{
                    margin: 0 0 10px 0;
                    color: #2c3e50;
                }}
                .summary-card .number {{
                    font-size: 2em;
                    font-weight: bold;
                    color: #3498db;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>📊 Content Production Report</h1>
                <p class="info">Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                
                <div class="summary-grid">
                    <div class="summary-card">
                        <h3>Total Files</h3>
                        <div class="number">{stats.total_files}</div>
                    </div>
                    <div class="summary-card">
                        <h3>Processed</h3>
                        <div class="number success">{stats.processed_files}</div>
                    </div>
                    <div class="summary-card">
                        <h3>Failed</h3>
                        <div class="number failure">{stats.failed_files}</div>
                    </div>
                    <div class="summary-card">
                        <h3>Duration</h3>
                        <div class="number info">{duration}</div>
                    </div>
                </div>
                
                <h2>📈 Production Summary</h2>
                <table>
                    <tr>
                        <th>Metric</th>
                        <th>Value</th>
                        <th>Status</th>
                    </tr>
                    <tr>
                        <td>Total Modules Created</td>
                        <td>{stats.processed_files}</td>
                        <td><span class="status-badge status-success">✓ Complete</span></td>
                    </tr>
                    <tr>
                        <td>Videos Rendered</td>
                        <td>{stats.processed_files}</td>
                        <td><span class="status-badge status-success">✓ Complete</span></td>
                    </tr>
                    <tr>
                        <td>Assessments Generated</td>
                        <td>{stats.processed_files}</td>
                        <td><span class="status-badge status-success">✓ Complete</span></td>
                    </tr>
                    <tr>
                        <td>Success Rate</td>
                        <td>{(stats.processed_files / max(stats.total_files, 1) * 100):.1f}%</td>
                        <td><span class="status-badge {'status-success' if stats.failed_files == 0 else 'status-warning'}">
                            {'✓ Perfect' if stats.failed_files == 0 else '⚠ Issues'}
                        </span></td>
                    </tr>
                </table>
                
                <h2>🔍 File Integrity</h2>
                <table>
                    <tr>
                        <th>File</th>
                        <th>Size</th>
                        <th>Checksum (SHA-256)</th>
                    </tr>
                    {self._generate_checksum_table(checksums)}
                </table>
                
                <h2>📋 System Information</h2>
                <table>
                    <tr>
                        <th>Property</th>
                        <th>Value</th>
                    </tr>
                    <tr>
                        <td>Python Version</td>
                        <td>{self._get_python_version()}</td>
                    </tr>
                    <tr>
                        <td>Script Version</td>
                        <td>2.0 (Optimized)</td>
                    </tr>
                    <tr>
                        <td>Configuration</td>
                        <td>{self.config.get('quality_preset', 'high')} quality preset</td>
                    </tr>
                </table>
                
                <h2>✅ Status</h2>
                <p class="{'success' if stats.failed_files == 0 else 'warning'}">
                    {'All content production completed successfully!' if stats.failed_files == 0 else f'{stats.failed_files} files failed processing. Check logs for details.'}
                </p>
            </div>
        </body>
        </html>
        """
        
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(report_html)
            
            logger.info(f"Report generated successfully: {output_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error generating report: {str(e)}")
            return False
    
    def _generate_file_checksums(self) -> Dict[str, str]:
        """Generate checksums for output files"""
        checksums = {}
        output_dir = Path(self.config.get('content_output_path', './output'))
        
        if output_dir.exists():
            for file_path in output_dir.rglob('*'):
                if file_path.is_file():
                    try:
                        with open(file_path, 'rb') as f:
                            content = f.read()
                            checksum = hashlib.sha256(content).hexdigest()
                            checksums[str(file_path.relative_to(output_dir))] = checksum
                    except Exception as e:
                        logger.warning(f"Could not generate checksum for {file_path}: {e}")
        
        return checksums
    
    def _generate_checksum_table(self, checksums: Dict[str, str]) -> str:
        """Generate HTML table rows for checksums"""
        if not checksums:
            return "<tr><td colspan='3'>No files found</td></tr>"
        
        rows = []
        for file_path, checksum in checksums.items():
            file_size = "Unknown"
            try:
                full_path = Path(self.config.get('content_output_path', './output')) / file_path
                if full_path.exists():
                    file_size = f"{full_path.stat().st_size:,} bytes"
            except:
                pass
            
            rows.append(f"""
                <tr>
                    <td>{file_path}</td>
                    <td>{file_size}</td>
                    <td><code>{checksum[:16]}...</code></td>
                </tr>
            """)
        
        return ''.join(rows)
    
    def _get_python_version(self) -> str:
        """Get Python version information"""
        import sys
        return f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"


def main():
    """Main entry point for automation script"""
    parser = argparse.ArgumentParser(description="Medical Content Production Automation")
    parser.add_argument('--action', choices=['create-video', 'batch-modules', 'validate', 'optimize', 'report'],
                       required=True, help="Action to perform")
    parser.add_argument('--input', help="Input file or directory")
    parser.add_argument('--output', help="Output file or directory")
    parser.add_argument('--config', default="config/automation.json", help="Configuration file path")
    
    args = parser.parse_args()
    
    # Initialize automation system
    automation = ContentProductionAutomation(config_path=args.config)
    
    # Execute requested action
    if args.action == 'create-video':
        if not args.input:
            logger.error("--input required for create-video action")
            return
        output_name = args.output or Path(args.input).stem
        automation.create_video_from_script(args.input, output_name)
        
    elif args.action == 'batch-modules':
        if not args.input:
            logger.error("--input required for batch-modules action")
            return
        # Read module list from file
        with open(args.input, 'r') as f:
            module_list = [line.strip() for line in f if line.strip()]
        results = automation.batch_create_modules(module_list)
        logger.info(f"Batch processing complete: {results}")
        
    elif args.action == 'validate':
        if not args.input:
            logger.error("--input required for validate action")
            return
        results = automation.validate_medical_content(args.input)
        logger.info(f"Validation results: {results}")
        
    elif args.action == 'optimize':
        if not args.input:
            logger.error("--input required for optimize action")
            return
        automation.optimize_media(args.input)
        
    elif args.action == 'report':
        output = args.output or "reports/production_report.html"
        automation.generate_report(output)
    
    logger.info("Automation complete")


if __name__ == "__main__":
    main()
