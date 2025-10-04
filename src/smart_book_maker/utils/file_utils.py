"""
Utility functions for file operations and directory management.
"""

import os
from typing import List


def ensure_directory(path: str) -> None:
    """
    Ensure a directory exists, create it if it doesn't.
    
    Args:
        path: Directory path to create
    """
    os.makedirs(path, exist_ok=True)


def ensure_output_directories(base_path: str = "output") -> None:
    """
    Create all necessary output directories.
    
    Args:
        base_path: Base output directory
    """
    directories = [
        f"{base_path}/sudokus",
        f"{base_path}/puzzles", 
        f"{base_path}/solutions",
        f"{base_path}/mazes",
        f"{base_path}/mazes_png",
        f"{base_path}/books"
    ]
    
    for directory in directories:
        ensure_directory(directory)


def get_sudoku_filenames(puzzle_num: int, difficulty_name: str, base_path: str = "output") -> dict:
    """
    Generate standardized filenames for sudoku files.
    
    Args:
        puzzle_num: Puzzle number
        difficulty_name: Difficulty level name
        base_path: Base output directory
        
    Returns:
        Dictionary with text, puzzle, and solution filenames
    """
    clean_diff = difficulty_name.replace(" ", "_").lower()
    return {
        "text": f"{base_path}/sudokus/sudoku_{puzzle_num:03d}_{clean_diff}.txt",
        "puzzle": f"{base_path}/puzzles/puzzle_{puzzle_num:03d}_{clean_diff}.png",
        "solution": f"{base_path}/solutions/solution_{puzzle_num:03d}_{clean_diff}.png"
    }


def get_maze_filenames(puzzle_num: int, width: int, height: int, base_path: str = "output") -> dict:
    """
    Generate standardized filenames for maze files.
    
    Args:
        puzzle_num: Puzzle number
        width: Maze width
        height: Maze height
        base_path: Base output directory
        
    Returns:
        Dictionary with text and image filenames
    """
    return {
        "text": f"{base_path}/mazes/maze_{puzzle_num:03d}_{width}x{height}.txt",
        "image": f"{base_path}/mazes_png/maze_{puzzle_num:03d}_{width}x{height}.png"
    }