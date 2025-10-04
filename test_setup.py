#!/usr/bin/env python3
"""
Quick test script to verify the Smart Book Maker installation and structure.
"""

import sys
import os
from pathlib import Path

# Add the src directory to the path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

def test_imports():
    """Test that all modules can be imported."""
    print("Testing imports...")
    
    try:
        from smart_book_maker.generators.sudoku import SudokuGenerator
        print("✓ Sudoku generator import successful")
    except ImportError as e:
        print(f"✗ Sudoku generator import failed: {e}")
        return False
    
    try:
        from smart_book_maker.generators.maze import MazeGenerator
        print("✓ Maze generator import successful")
    except ImportError as e:
        print(f"✗ Maze generator import failed: {e}")
        return False
    
    try:
        from smart_book_maker.pdf.sudoku_book import SudokuBookPDF
        print("✓ Sudoku PDF import successful")
    except ImportError as e:
        print(f"✗ Sudoku PDF import failed: {e}")
        return False
    
    try:
        from smart_book_maker.pdf.maze_book import MazeBookPDF
        print("✓ Maze PDF import successful")
    except ImportError as e:
        print(f"✗ Maze PDF import failed: {e}")
        return False
    
    return True

def test_generation():
    """Test basic puzzle generation."""
    print("\\nTesting puzzle generation...")
    
    try:
        from smart_book_maker.generators.sudoku import SudokuGenerator
        generator = SudokuGenerator()
        puzzle, solution = generator.generate_puzzle(1)
        print(f"✓ Generated Sudoku puzzle with {sum(1 for row in puzzle for cell in row if cell != 0)} clues")
    except Exception as e:
        print(f"✗ Sudoku generation failed: {e}")
        return False
    
    try:
        from smart_book_maker.generators.maze import MazeGenerator
        generator = MazeGenerator()
        maze, width, height, cell_size = generator.generate_puzzle(1)
        print(f"✓ Generated {width}x{height} maze with cell size {cell_size}")
    except Exception as e:
        print(f"✗ Maze generation failed: {e}")
        return False
    
    return True

def test_cli():
    """Test CLI availability."""
    print("\\nTesting CLI...")
    
    cli_path = Path(__file__).parent / "src" / "smart_book_maker" / "cli.py"
    if cli_path.exists():
        print("✓ CLI module found")
        return True
    else:
        print("✗ CLI module not found")
        return False

def test_directory_structure():
    """Test that the directory structure is correct."""
    print("\\nTesting directory structure...")
    
    base_path = Path(__file__).parent
    required_dirs = [
        "src/smart_book_maker/generators",
        "src/smart_book_maker/pdf", 
        "src/smart_book_maker/utils",
        "examples",
        "tests",
        "output"
    ]
    
    all_good = True
    for dir_path in required_dirs:
        full_path = base_path / dir_path
        if full_path.exists():
            print(f"✓ {dir_path} exists")
        else:
            print(f"✗ {dir_path} missing")
            all_good = False
    
    return all_good

def main():
    """Run all tests."""
    print("Smart Book Maker - Structure Test")
    print("=" * 40)
    
    tests = [
        test_directory_structure,
        test_imports,
        test_generation,
        test_cli
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"✗ Test {test.__name__} failed with exception: {e}")
            results.append(False)
    
    print("\\n" + "=" * 40)
    if all(results):
        print("🎉 All tests passed! Smart Book Maker is ready to use.")
        print("\\nTry running:")
        print("  python -m smart_book_maker.cli --help")
        return 0
    else:
        print("❌ Some tests failed. Please check the setup.")
        return 1

if __name__ == "__main__":
    sys.exit(main())