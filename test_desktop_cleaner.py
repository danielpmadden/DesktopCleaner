#!/usr/bin/env python3
"""Unit tests for :mod:`desktop_cleaner`.

The test suite exercises the public surface area exposed by the desktop
organisation utility. Every test is thoroughly documented so future
maintainers can quickly understand *why* each assertion exists.
"""

import os
import json
import shutil
import tempfile
import unittest
from unittest.mock import patch

# Import the module to test. We insert the repository root into ``sys.path`` so
# the module can be imported regardless of where the tests are executed from.
import sys

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
import desktop_cleaner


class TestDesktopCleanup(unittest.TestCase):
    """Comprehensive behavioural tests for the desktop cleaner helpers."""
    
    def setUp(self):
        """Set up test environment."""
        # Create a temporary directory
        self.test_dir = tempfile.mkdtemp()
        
        # Create a deterministic set of files representing each category.
        self.test_files = {
            'document.pdf': 'Documents',
            'image.jpg': 'Images',
            'song.mp3': 'Audio',
            'code.py': 'Code',
            'archive.zip': 'Archives',
            'random.xyz': 'Others'
        }

        for file_name in self.test_files.keys():
            with open(os.path.join(self.test_dir, file_name), 'w') as f:
                f.write('test content')

        # Hidden files should be ignored by the cleanup routine. Creating one
        # ensures that behaviour is exercised by ``test_cleanup_desktop``.
        with open(os.path.join(self.test_dir, '.hidden'), 'w') as f:
            f.write('secret')
    
    def tearDown(self):
        """Clean up after tests."""
        shutil.rmtree(self.test_dir)
    
    def test_get_desktop_path(self):
        """Test the get_desktop_path function."""
        desktop_path = desktop_cleaner.get_desktop_path()
        # The desktop folder is not guaranteed to exist in headless CI
        # environments, therefore we avoid asserting its presence on disk. It is
        # sufficient to ensure the computed path is located inside the user's
        # home directory and ends with "Desktop".
        self.assertTrue(desktop_path.endswith('Desktop'))
        self.assertTrue(desktop_path.startswith(os.path.expanduser('~')))

    def test_categorize_file(self):
        """Test the categorize_file function."""
        categories = desktop_cleaner.load_config()

        self.assertEqual(desktop_cleaner.categorize_file('test.pdf', categories), 'Documents')
        self.assertEqual(desktop_cleaner.categorize_file('image.jpg', categories), 'Images')
        self.assertEqual(desktop_cleaner.categorize_file('script.py', categories), 'Code')
        self.assertEqual(desktop_cleaner.categorize_file('unknown.xyz', categories), 'Others')
    
    def test_ensure_folders_exist(self):
        """Test the ensure_folders_exist function."""
        categories = {'Test1': [], 'Test2': []}
        desktop_cleaner.ensure_folders_exist(self.test_dir, categories)
        
        self.assertTrue(os.path.exists(os.path.join(self.test_dir, 'Test1')))
        self.assertTrue(os.path.exists(os.path.join(self.test_dir, 'Test2')))
    
    def test_move_file(self):
        """Test the move_file function."""
        # Create destination folder
        dest_folder = os.path.join(self.test_dir, 'Destination')
        os.makedirs(dest_folder)
        
        # Create a test file
        test_file = os.path.join(self.test_dir, 'test_move.txt')
        with open(test_file, 'w') as f:
            f.write('test content')
        
        # Test moving the file
        result = desktop_cleaner.move_file(test_file, dest_folder)
        self.assertTrue(result)
        self.assertTrue(os.path.exists(os.path.join(dest_folder, 'test_move.txt')))
        self.assertFalse(os.path.exists(test_file))
    
    def test_move_file_dry_run(self):
        """Test the move_file function in dry-run mode."""
        # Create destination folder
        dest_folder = os.path.join(self.test_dir, 'Destination')
        os.makedirs(dest_folder)
        
        # Create a test file
        test_file = os.path.join(self.test_dir, 'test_dry_run.txt')
        with open(test_file, 'w') as f:
            f.write('test content')
        
        # Test moving the file in dry-run mode
        result = desktop_cleaner.move_file(test_file, dest_folder, dry_run=True)
        self.assertTrue(result)
        self.assertFalse(os.path.exists(os.path.join(dest_folder, 'test_dry_run.txt')))
        self.assertTrue(os.path.exists(test_file))
    
    @patch('desktop_cleaner.move_file')
    def test_cleanup_desktop(self, mock_move):
        """Test the main cleanup_desktop function."""
        # Configure the mock
        mock_move.return_value = True

        # Call the function
        desktop_cleaner.cleanup_desktop(self.test_dir)

        # Check if move_file was called for each test file
        self.assertEqual(mock_move.call_count, len(self.test_files))

        # Ensure hidden files and shortcuts were skipped.
        processed_files = {call.args[0] for call in mock_move.call_args_list}
        self.assertNotIn(os.path.join(self.test_dir, '.hidden'), processed_files)

        # Check if log file was created
        log_file = os.path.join(self.test_dir, 'desktop_cleanup_log.json')
        self.assertTrue(os.path.exists(log_file))

        # Verify log file contents
        with open(log_file, 'r') as f:
            log_data = json.load(f)
            self.assertEqual(len(log_data['files']), len(self.test_files))
            self.assertTrue(all(entry['success'] for entry in log_data['files']))

    def test_load_config(self):
        """Test loading configuration."""
        # Test with default config
        config = desktop_cleaner.load_config()
        self.assertIn('Documents', config)
        self.assertIn('Images', config)

        # Test with custom config
        config_path = os.path.join(self.test_dir, 'test_config.json')
        with open(config_path, 'w') as f:
            json.dump({'TestCategory': ['.test']}, f)

        custom_config = desktop_cleaner.load_config(config_path)
        self.assertIn('TestCategory', custom_config)


if __name__ == '__main__':
    unittest.main()
