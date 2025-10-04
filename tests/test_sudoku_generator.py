"""
Tests for Sudoku Generator.
"""

import unittest
import tempfile
import os
from pathlib import Path

from smart_book_maker.generators.sudoku import SudokuGenerator


class TestSudokuGenerator(unittest.TestCase):
    """Test cases for SudokuGenerator class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.generator = SudokuGenerator()
        self.temp_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """Clean up test fixtures."""
        # Clean up temp files
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_is_valid(self):
        """Test the is_valid method."""
        grid = [[0 for _ in range(9)] for _ in range(9)]
        
        # Test valid placement
        self.assertTrue(self.generator.is_valid(grid, 0, 0, 1))
        
        # Test invalid placement (same row)
        grid[0][1] = 1
        self.assertFalse(self.generator.is_valid(grid, 0, 0, 1))
        
        # Reset and test invalid placement (same column)
        grid[0][1] = 0
        grid[1][0] = 1
        self.assertFalse(self.generator.is_valid(grid, 0, 0, 1))
        
        # Reset and test invalid placement (same 3x3 box)
        grid[1][0] = 0
        grid[1][1] = 1
        self.assertFalse(self.generator.is_valid(grid, 0, 0, 1))
    
    def test_generate_complete_grid(self):
        """Test complete grid generation."""
        grid = self.generator.generate_complete_grid()
        
        # Check grid is 9x9
        self.assertEqual(len(grid), 9)
        self.assertEqual(len(grid[0]), 9)
        
        # Check all cells are filled
        for row in grid:
            for cell in row:
                self.assertIn(cell, range(1, 10))
        
        # Check all rows contain 1-9
        for row in grid:
            self.assertEqual(set(row), set(range(1, 10)))
        
        # Check all columns contain 1-9
        for col in range(9):
            column = [grid[row][col] for row in range(9)]
            self.assertEqual(set(column), set(range(1, 10)))
        
        # Check all 3x3 boxes contain 1-9
        for box_row in range(3):
            for box_col in range(3):
                box = []
                for i in range(3):
                    for j in range(3):
                        box.append(grid[box_row * 3 + i][box_col * 3 + j])
                self.assertEqual(set(box), set(range(1, 10)))
    
    def test_remove_numbers(self):
        """Test number removal for puzzle creation."""
        complete_grid = self.generator.generate_complete_grid()
        
        # Test different difficulty levels
        for difficulty in [1, 30, 70, 100, 150]:
            puzzle = self.generator.remove_numbers(complete_grid, difficulty)
            
            # Check grid size
            self.assertEqual(len(puzzle), 9)
            self.assertEqual(len(puzzle[0]), 9)
            
            # Count removed numbers
            removed_count = sum(1 for row in puzzle for cell in row if cell == 0)
            
            # Should have removed some numbers
            self.assertGreater(removed_count, 0)
            
            # Should not have removed all numbers
            self.assertLess(removed_count, 81)
    
    def test_generate_puzzle(self):
        """Test complete puzzle generation."""
        puzzle, solution = self.generator.generate_puzzle(50)
        
        # Check both are 9x9 grids
        self.assertEqual(len(puzzle), 9)
        self.assertEqual(len(solution), 9)
        self.assertEqual(len(puzzle[0]), 9)
        self.assertEqual(len(solution[0]), 9)
        
        # Check solution is complete and valid
        for row in solution:
            for cell in row:
                self.assertIn(cell, range(1, 10))
        
        # Check puzzle has empty cells
        empty_cells = sum(1 for row in puzzle for cell in row if cell == 0)
        self.assertGreater(empty_cells, 0)
        
        # Check puzzle cells match solution where not empty
        for i in range(9):
            for j in range(9):
                if puzzle[i][j] != 0:
                    self.assertEqual(puzzle[i][j], solution[i][j])
    
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
        self.assertEqual(self.generator.get_difficulty_name(126), "Expert")
        self.assertEqual(self.generator.get_difficulty_name(160), "Expert")
    
    def test_save_puzzle_text(self):
        """Test saving puzzle to text file."""
        puzzle = [[1, 2, 0], [0, 0, 3], [2, 3, 1]]
        solution = [[1, 2, 3], [4, 5, 3], [2, 3, 1]]
        
        filename = os.path.join(self.temp_dir, "test_puzzle.txt")
        self.generator.save_puzzle_text(puzzle, solution, filename)
        
        # Check file was created
        self.assertTrue(os.path.exists(filename))
        
        # Check file content
        with open(filename, 'r') as f:
            content = f.read()
            self.assertIn("PUZZLE:", content)
            self.assertIn("SOLUTION:", content)


if __name__ == '__main__':
    unittest.main()