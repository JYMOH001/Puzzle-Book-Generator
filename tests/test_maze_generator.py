"""
Tests for Maze Generator.
"""

import unittest
import tempfile
import os

from smart_book_maker.generators.maze import MazeGenerator


class TestMazeGenerator(unittest.TestCase):
    """Test cases for MazeGenerator class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.generator = MazeGenerator()
        self.temp_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """Clean up test fixtures."""
        # Clean up temp files
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_generate_maze(self):
        """Test maze generation."""
        width, height = 5, 5
        maze = self.generator.generate_maze(width, height)
        
        # Check maze dimensions
        expected_width = 2 * width + 1
        expected_height = 2 * height + 1
        self.assertEqual(len(maze), expected_height)
        self.assertEqual(len(maze[0]), expected_width)
        
        # Check start and end positions
        self.assertEqual(maze[1][0], 'S')  # Start
        self.assertEqual(maze[2 * height - 1][2 * width], 'E')  # End
        
        # Check maze contains walls and paths
        has_walls = any('#' in row for row in maze)
        has_paths = any(' ' in row for row in maze)
        self.assertTrue(has_walls)
        self.assertTrue(has_paths)
    
    def test_difficulty_params(self):
        """Test difficulty parameter mapping."""
        test_cases = [
            (1, (5, 5)),      # Very easy
            (25, (5, 5)),     # Very easy
            (26, (12, 12)),   # Easy
            (55, (12, 12)),   # Easy
            (56, (20, 20)),   # Medium
            (90, (20, 20)),   # Medium
            (91, (35, 35)),   # Hard
            (125, (35, 35)),  # Hard
            (126, (50, 50)),  # Very hard
            (160, (50, 50)),  # Very hard
        ]
        
        for level, expected in test_cases:
            result = self.generator.get_difficulty_params(level)
            self.assertEqual(result, expected)
    
    def test_cell_size(self):
        """Test cell size calculation."""
        test_cases = [
            (5, 32),
            (12, 24),
            (20, 16),
            (35, 10),
            (50, 7),
        ]
        
        for width, expected_size in test_cases:
            result = self.generator.get_cell_size(width)
            self.assertEqual(result, expected_size)
    
    def test_generate_puzzle(self):
        """Test complete puzzle generation."""
        level = 50
        maze, width, height, cell_size = self.generator.generate_puzzle(level)
        
        # Check returned values are reasonable
        self.assertIsInstance(maze, list)
        self.assertIsInstance(width, int)
        self.assertIsInstance(height, int)
        self.assertIsInstance(cell_size, int)
        
        # Check maze dimensions match width/height
        expected_width = 2 * width + 1
        expected_height = 2 * height + 1
        self.assertEqual(len(maze), expected_height)
        self.assertEqual(len(maze[0]), expected_width)
    
    def test_difficulty_name(self):
        """Test difficulty name mapping."""
        self.assertEqual(self.generator.get_difficulty_name(1), "Very Easy")
        self.assertEqual(self.generator.get_difficulty_name(25), "Very Easy")
        self.assertEqual(self.generator.get_difficulty_name(26), "Easy")
        self.assertEqual(self.generator.get_difficulty_name(55), "Easy")
        self.assertEqual(self.generator.get_difficulty_name(56), "Medium")
        self.assertEqual(self.generator.get_difficulty_name(90), "Medium")
        self.assertEqual(self.generator.get_difficulty_name(91), "Hard")
        self.assertEqual(self.generator.get_difficulty_name(125), "Hard")
        self.assertEqual(self.generator.get_difficulty_name(126), "Very Hard")
        self.assertEqual(self.generator.get_difficulty_name(160), "Very Hard")
    
    def test_save_maze_text(self):
        """Test saving maze to text file."""
        maze = [['#', '#', '#'], ['S', ' ', 'E'], ['#', '#', '#']]
        
        filename = os.path.join(self.temp_dir, "test_maze.txt")
        self.generator.save_maze_text(maze, filename)
        
        # Check file was created
        self.assertTrue(os.path.exists(filename))
        
        # Check file content
        with open(filename, 'r') as f:
            lines = f.readlines()
            self.assertEqual(len(lines), 3)
            self.assertIn('S', lines[1])
            self.assertIn('E', lines[1])


if __name__ == '__main__':
    unittest.main()