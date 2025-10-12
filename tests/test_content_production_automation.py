#!/usr/bin/env python3
"""
Test suite for Content Production Automation Script
"""

import unittest
import tempfile
import json
import os
from pathlib import Path
from unittest.mock import patch, MagicMock
import sys

# Add the scripts directory to the path
sys.path.insert(0, str(Path(__file__).parent.parent / 'scripts'))

from content_production_automation import ContentProductionAutomation, ValidationResult, ProcessingStats


class TestContentProductionAutomation(unittest.TestCase):
    """Test cases for ContentProductionAutomation class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.temp_dir = tempfile.mkdtemp()
        self.config_path = os.path.join(self.temp_dir, 'test_config.json')
        
        # Create test configuration
        test_config = {
            "content_output_path": os.path.join(self.temp_dir, 'output'),
            "video_resolution": "1920x1080",
            "video_framerate": 30,
            "video_codec": "h264",
            "audio_bitrate": "128k",
            "quality_preset": "high",
            "max_workers": 2
        }
        
        with open(self.config_path, 'w') as f:
            json.dump(test_config, f)
        
        self.automation = ContentProductionAutomation(self.config_path)
    
    def tearDown(self):
        """Clean up test fixtures"""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_load_config_valid(self):
        """Test loading valid configuration"""
        config = self.automation.load_config(self.config_path)
        self.assertEqual(config['video_resolution'], '1920x1080')
        self.assertEqual(config['video_framerate'], 30)
    
    def test_load_config_missing_file(self):
        """Test loading missing configuration file"""
        config = self.automation.load_config('nonexistent.json')
        self.assertEqual(config['video_resolution'], '1920x1080')  # Should use defaults
    
    def test_load_config_invalid_json(self):
        """Test loading invalid JSON configuration"""
        invalid_config_path = os.path.join(self.temp_dir, 'invalid.json')
        with open(invalid_config_path, 'w') as f:
            f.write('invalid json content')
        
        config = self.automation.load_config(invalid_config_path)
        self.assertEqual(config['video_resolution'], '1920x1080')  # Should use defaults
    
    def test_validate_script_enhanced_valid(self):
        """Test enhanced script validation with valid data"""
        valid_script_data = {
            "metadata": {
                "title": "Test Video",
                "duration": 300
            },
            "sections": [
                {"name": "Introduction", "start": 0, "end": 30},
                {"name": "Main Content", "start": 30, "end": 270},
                {"name": "Conclusion", "start": 270, "end": 300}
            ],
            "narration": ["Narration line 1", "Narration line 2"]
        }
        
        result = self.automation.validate_script_enhanced(valid_script_data)
        self.assertTrue(result.is_valid)
        self.assertEqual(len(result.errors), 0)
    
    def test_validate_script_enhanced_invalid(self):
        """Test enhanced script validation with invalid data"""
        invalid_script_data = {
            "metadata": "not a dict",  # Should be dict
            "sections": "not a list",  # Should be list
            # Missing narration
        }
        
        result = self.automation.validate_script_enhanced(invalid_script_data)
        self.assertFalse(result.is_valid)
        self.assertGreater(len(result.errors), 0)
    
    def test_validate_script_enhanced_warnings(self):
        """Test enhanced script validation with warnings"""
        script_data_with_warnings = {
            "metadata": {
                "title": "",  # Empty title should generate warning
                "duration": "not a number"  # Invalid duration
            },
            "sections": [
                {"name": "Short Section", "start": 0, "end": 30}  # Very short duration
            ],
            "narration": []
        }
        
        result = self.automation.validate_script_enhanced(script_data_with_warnings)
        self.assertTrue(result.is_valid)  # Should still be valid
        self.assertGreater(len(result.warnings), 0)
    
    def test_validate_module_config_valid(self):
        """Test module configuration validation with valid data"""
        valid_config = {
            "name": "Test Module",
            "videos": [
                {"script": "script1.md", "name": "video1"},
                {"script": "script2.md", "name": "video2"}
            ],
            "interactives": [],
            "assessments": []
        }
        
        self.assertTrue(self.automation._validate_module_config(valid_config))
    
    def test_validate_module_config_invalid(self):
        """Test module configuration validation with invalid data"""
        invalid_config = {
            "name": "Test Module",
            # Missing required fields
        }
        
        self.assertFalse(self.automation._validate_module_config(invalid_config))
    
    def test_optimize_media_nonexistent_file(self):
        """Test media optimization with nonexistent file"""
        result = self.automation.optimize_media("nonexistent.mp4", "video")
        self.assertFalse(result)
    
    def test_optimize_media_empty_file(self):
        """Test media optimization with empty file"""
        empty_file = os.path.join(self.temp_dir, 'empty.mp4')
        Path(empty_file).touch()
        
        result = self.automation.optimize_media(empty_file, "video")
        self.assertFalse(result)
    
    @patch('shutil.which')
    def test_optimize_video_no_ffmpeg(self, mock_which):
        """Test video optimization when FFmpeg is not available"""
        mock_which.return_value = None
        
        # Create a test video file
        test_video = os.path.join(self.temp_dir, 'test.mp4')
        with open(test_video, 'wb') as f:
            f.write(b'fake video content')
        
        result = self.automation.optimize_video(test_video)
        self.assertFalse(result)
    
    def test_generate_file_checksums(self):
        """Test file checksum generation"""
        # Create test files
        output_dir = Path(self.temp_dir) / 'output'
        output_dir.mkdir()
        
        test_file1 = output_dir / 'test1.txt'
        test_file1.write_text('test content 1')
        
        test_file2 = output_dir / 'test2.txt'
        test_file2.write_text('test content 2')
        
        # Update config to point to test output directory
        self.automation.config['content_output_path'] = str(output_dir)
        
        checksums = self.automation._generate_file_checksums()
        
        self.assertEqual(len(checksums), 2)
        self.assertIn('test1.txt', checksums)
        self.assertIn('test2.txt', checksums)
        
        # Verify checksums are valid SHA-256 hashes
        for checksum in checksums.values():
            self.assertEqual(len(checksum), 64)  # SHA-256 is 64 hex characters
            self.assertTrue(all(c in '0123456789abcdef' for c in checksum))
    
    def test_processing_stats(self):
        """Test ProcessingStats dataclass"""
        stats = ProcessingStats(
            total_files=10,
            processed_files=8,
            failed_files=2,
            start_time=Path(__file__).stat().st_mtime
        )
        
        self.assertEqual(stats.total_files, 10)
        self.assertEqual(stats.processed_files, 8)
        self.assertEqual(stats.failed_files, 2)
        self.assertIsNone(stats.end_time)
    
    def test_validation_result(self):
        """Test ValidationResult dataclass"""
        result = ValidationResult(
            is_valid=True,
            errors=[],
            warnings=['Warning 1', 'Warning 2'],
            metadata={'title': 'Test'}
        )
        
        self.assertTrue(result.is_valid)
        self.assertEqual(len(result.errors), 0)
        self.assertEqual(len(result.warnings), 2)
        self.assertEqual(result.metadata['title'], 'Test')


class TestIntegration(unittest.TestCase):
    """Integration tests for the automation system"""
    
    def setUp(self):
        """Set up integration test fixtures"""
        self.temp_dir = tempfile.mkdtemp()
        self.config_path = os.path.join(self.temp_dir, 'integration_config.json')
        
        # Create test configuration
        test_config = {
            "content_output_path": os.path.join(self.temp_dir, 'output'),
            "video_resolution": "1920x1080",
            "video_framerate": 30,
            "video_codec": "h264",
            "audio_bitrate": "128k",
            "quality_preset": "high",
            "max_workers": 1
        }
        
        with open(self.config_path, 'w') as f:
            json.dump(test_config, f)
        
        self.automation = ContentProductionAutomation(self.config_path)
    
    def tearDown(self):
        """Clean up integration test fixtures"""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_create_video_from_script_nonexistent_file(self):
        """Test video creation with nonexistent script file"""
        result = self.automation.create_video_from_script("nonexistent.md", "test_video")
        self.assertFalse(result)
    
    def test_create_video_from_script_invalid_extension(self):
        """Test video creation with invalid file extension"""
        # Create a file with invalid extension
        invalid_file = os.path.join(self.temp_dir, 'test.txt')
        with open(invalid_file, 'w') as f:
            f.write('test content')
        
        result = self.automation.create_video_from_script(invalid_file, "test_video")
        self.assertFalse(result)
    
    def test_batch_create_modules_empty_list(self):
        """Test batch module creation with empty list"""
        results = self.automation.batch_create_modules([])
        self.assertEqual(len(results), 0)
    
    def test_generate_report(self):
        """Test report generation"""
        report_path = os.path.join(self.temp_dir, 'test_report.html')
        
        stats = ProcessingStats(
            total_files=5,
            processed_files=4,
            failed_files=1,
            start_time=Path(__file__).stat().st_mtime
        )
        
        result = self.automation.generate_report(report_path, stats)
        self.assertTrue(result)
        self.assertTrue(os.path.exists(report_path))
        
        # Verify report content
        with open(report_path, 'r') as f:
            content = f.read()
            self.assertIn('Content Production Report', content)
            self.assertIn('Total Files', content)
            self.assertIn('5', content)  # Should contain the total files count


if __name__ == '__main__':
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add test cases
    test_suite.addTest(unittest.makeSuite(TestContentProductionAutomation))
    test_suite.addTest(unittest.makeSuite(TestIntegration))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Exit with appropriate code
    exit(0 if result.wasSuccessful() else 1)