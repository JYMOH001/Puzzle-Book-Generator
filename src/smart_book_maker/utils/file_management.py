"""
File Utilities for Smart Book Maker

This module provides utility functions for file and directory management.
"""

import os
from typing import Dict


def ensure_output_directories(output_dir: str) -> None:
    """
    Ensure all necessary output directories exist.
    
    Args:
        output_dir: Base output directory
    """
    directories = [
        output_dir,
        f"{output_dir}/puzzles",
        f"{output_dir}/solutions", 
        f"{output_dir}/sudokus",
        f"{output_dir}/mazes",
        f"{output_dir}/mazes_png",
        f"{output_dir}/books"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)


def get_sudoku_filenames(puzzle_num: int, difficulty_name: str, output_dir: str) -> Dict[str, str]:
    """
    Get standardized filenames for Sudoku files.
    
    Args:
        puzzle_num: Puzzle number
        difficulty_name: Difficulty level name
        output_dir: Base output directory
        
    Returns:
        Dictionary with file paths for text, puzzle, and solution files
    """
    diff_name_file = difficulty_name.replace(" ", "_").lower()
    
    return {
        "text": f'{output_dir}/sudokus/sudoku_{puzzle_num:03d}_{diff_name_file}.txt',
        "puzzle": f'{output_dir}/puzzles/puzzle_{puzzle_num:03d}_{diff_name_file}.png',
        "solution": f'{output_dir}/solutions/solution_{puzzle_num:03d}_{diff_name_file}.png'
    }


def get_maze_filenames(puzzle_num: int, width: int, height: int, output_dir: str) -> Dict[str, str]:
    """
    Get standardized filenames for Maze files.
    
    Args:
        puzzle_num: Puzzle number
        width: Maze width
        height: Maze height
        output_dir: Base output directory
        
    Returns:
        Dictionary with file paths for text and image files
    """
    return {
        "text": f'{output_dir}/mazes/maze_{puzzle_num:03d}_{width}x{height}.txt',
        "image": f'{output_dir}/mazes_png/maze_{puzzle_num:03d}_{width}x{height}.png'
    }