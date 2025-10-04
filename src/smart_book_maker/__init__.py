"""
Smart Book Maker - A Python library for generating puzzle books.

This package provides tools for generating various types of puzzle books
including Sudoku and Maze puzzles with professional PDF output.
"""

__version__ = "1.0.0"
__author__ = "Smart Book Maker Contributors"

from .generators.sudoku import SudokuGenerator
from .generators.maze import MazeGenerator
from .pdf.sudoku_book import SudokuBookPDF
from .pdf.maze_book import MazeBookPDF

__all__ = [
    "SudokuGenerator",
    "MazeGenerator", 
    "SudokuBookPDF",
    "MazeBookPDF",
]