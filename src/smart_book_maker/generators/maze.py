"""
Maze Generator Module

This module provides functionality to generate maze puzzles with various
difficulty levels and save them as images and text files.
"""

import random
import os
from typing import List, Tuple
from PIL import Image, ImageDraw


class MazeGenerator:
    """A class for generating maze puzzles with configurable difficulty levels."""
    
    def __init__(self):
        """Initialize the Maze generator."""
        pass
    
    def generate_maze(self, width: int, height: int) -> List[List[str]]:
        """
        Generate a maze using iterative backtracking algorithm.
        
        Args:
            width: Width of the maze in cells
            height: Height of the maze in cells
            
        Returns:
            A 2D list representing the maze where '#' is wall, ' ' is path,
            'S' is start, and 'E' is end
        """
        # Iterative backtracking maze generation (no recursion)
        maze = [['#'] * (2 * width + 1) for _ in range(2 * height + 1)]
        stack = [(0, 0)]
        maze[1][1] = ' '
        visited = set()
        visited.add((0, 0))
        
        while stack:
            x, y = stack[-1]
            dirs = [(0, 1), (1, 0), (0, -1), (-1, 0)]
            random.shuffle(dirs)
            found = False
            
            for dx, dy in dirs:
                nx, ny = x + dx, y + dy
                if 0 <= nx < width and 0 <= ny < height and (nx, ny) not in visited:
                    maze[y * 2 + 1 + dy][x * 2 + 1 + dx] = ' '
                    maze[ny * 2 + 1][nx * 2 + 1] = ' '
                    stack.append((nx, ny))
                    visited.add((nx, ny))
                    found = True
                    break
            
            if not found:
                stack.pop()
        
        # Add entrance and exit
        maze[1][0] = 'S'  # Start at top-left
        maze[2 * height - 1][2 * width] = 'E'  # End at bottom-right
        
        return maze
    
    def save_maze_text(self, maze: List[List[str]], filename: str) -> None:
        """
        Save maze to a text file.
        
        Args:
            maze: The maze grid
            filename: Output filename
        """
        with open(filename, 'w') as f:
            for row in maze:
                f.write(''.join(row) + '\n')
    
    def save_maze_image(self, maze: List[List[str]], filename: str, 
                       cell_size: int = 20, wall_color: Tuple[int, int, int] = (0, 0, 0),
                       path_color: Tuple[int, int, int] = (255, 255, 255)) -> None:
        """
        Save maze as an image file.
        
        Args:
            maze: The maze grid
            filename: Output filename
            cell_size: Size of each cell in pixels
            wall_color: RGB color for walls
            path_color: RGB color for paths
        """
        height = len(maze)
        width = len(maze[0])
        img = Image.new('RGB', (width * cell_size, height * cell_size), path_color)
        draw = ImageDraw.Draw(img)
        
        # Draw maze cells
        for y, row in enumerate(maze):
            for x, cell in enumerate(row):
                color = path_color
                if cell == '#':
                    color = wall_color
                draw.rectangle([
                    x * cell_size, y * cell_size,
                    (x + 1) * cell_size - 1, (y + 1) * cell_size - 1
                ], fill=color)
        
        # Draw start and end markers
        for y, row in enumerate(maze):
            for x, cell in enumerate(row):
                if cell == 'S':
                    # Draw start arrow (right-pointing triangle)
                    cx = x * cell_size + cell_size // 2
                    cy = y * cell_size + cell_size // 2
                    size = cell_size // 2
                    arrow = [
                        (cx - size // 2, cy - size // 2),
                        (cx - size // 2, cy + size // 2),
                        (cx + size // 2, cy)
                    ]
                    draw.polygon(arrow, fill=(0, 128, 255))
                elif cell == 'E':
                    # Draw a flag for the end
                    cx = x * cell_size + cell_size // 2
                    cy = y * cell_size + cell_size // 2
                    flag_height = cell_size // 2
                    flag_width = cell_size // 3
                    # Flag pole
                    draw.line([
                        (cx, cy - flag_height // 2),
                        (cx, cy + flag_height // 2)
                    ], fill=(255, 0, 0), width=2)
                    # Flag triangle
                    flag = [
                        (cx, cy - flag_height // 2),
                        (cx + flag_width, cy - flag_height // 2 + flag_width // 2),
                        (cx, cy - flag_height // 2 + flag_width)
                    ]
                    draw.polygon(flag, fill=(255, 0, 0))
        
        img.save(filename)
    
    def get_difficulty_params(self, level: int) -> Tuple[int, int]:
        """
        Get maze dimensions based on difficulty level.
        
        Args:
            level: Difficulty level (1-160)
            
        Returns:
            Tuple of (width, height) for the maze
        """
        if level <= 25:
            return 5, 5  # Very easy
        elif level <= 55:
            return 12, 12  # Easy
        elif level <= 90:
            return 20, 20  # Medium
        elif level <= 125:
            return 35, 35  # Hard
        else:
            return 50, 50  # Very hard
    
    def get_cell_size(self, width: int) -> int:
        """
        Get appropriate cell size for rendering based on maze width.
        
        Args:
            width: Width of the maze
            
        Returns:
            Cell size in pixels
        """
        if width <= 5:
            return 32
        elif width <= 12:
            return 24
        elif width <= 20:
            return 16
        elif width <= 35:
            return 10
        else:
            return 7
    
    def generate_puzzle(self, level: int) -> Tuple[List[List[str]], int, int, int]:
        """
        Generate a complete maze puzzle for the given level.
        
        Args:
            level: Difficulty level (1-160)
            
        Returns:
            Tuple of (maze, width, height, cell_size)
        """
        width, height = self.get_difficulty_params(level)
        maze = self.generate_maze(width, height)
        cell_size = self.get_cell_size(width)
        return maze, width, height, cell_size

    @staticmethod
    def get_difficulty_name(level: int) -> str:
        """
        Get difficulty name based on level.
        
        Args:
            level: Puzzle number (1-160)
            
        Returns:
            Difficulty level name
        """
        if level <= 25:
            return "Very Easy"
        elif level <= 55:
            return "Easy"
        elif level <= 90:
            return "Medium"
        elif level <= 125:
            return "Hard"
        else:
            return "Very Hard"