# Smart Book Maker

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.7+-blue.svg)
![Version](https://img.shields.io/badge/version-1.0.0-green.svg)

A Python library and command-line tool for generating professional puzzle books including Sudoku and Maze puzzles. Create print-ready PDF books with customizable difficulty levels, professional layouts, and high-quality formatting.

## 🌟 Features

- **Multiple Puzzle Types**: Generate Sudoku and Maze puzzles
- **Difficulty Progression**: 5 difficulty levels from beginner to expert
- **Professional PDF Output**: Print-ready books with proper formatting
- **Customizable Generation**: Configure puzzle count, output directories, and difficulty
- **Clean Organization**: Separate folders for puzzles, solutions, and assets
- **Command Line Interface**: Easy-to-use CLI for batch operations
- **Extensible Architecture**: Well-structured codebase for adding new puzzle types

## 📚 Supported Puzzle Types

### Sudoku Puzzles
- **Very Easy (1-25)**: 45-50 given clues - Perfect for beginners
- **Easy (26-55)**: 40-45 given clues - Building confidence  
- **Medium (56-90)**: 32-40 given clues - Testing skills
- **Hard (91-125)**: 28-32 given clues - Challenging puzzles
- **Expert (126-160)**: 22-28 given clues - Master level

### Maze Puzzles
- **Very Easy (5x5)**: Small mazes perfect for beginners
- **Easy (12x12)**: Slightly larger with more path options
- **Medium (20x20)**: Moderate complexity requiring strategy
- **Hard (35x35)**: Complex mazes with many dead ends
- **Very Hard (50x50)**: Massive labyrinths for experts

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/TheUnknown550/Smart-Book-Maker.git
cd Smart-Book-Maker

# Install dependencies
pip install -r requirements.txt

# Install the package (optional)
pip install -e .
```

### Basic Usage

#### Generate Sudoku Puzzles and Book
```bash
# Generate 160 Sudoku puzzles and create a complete book
python -m smart_book_maker.cli all sudoku --count 160

# Or use the installed command (if you installed the package)
smart-book-maker all sudoku --count 160
```

#### Generate Maze Puzzles and Book
```bash
# Generate 160 Maze puzzles and create a complete book
python -m smart_book_maker.cli all maze --count 160
```

#### Individual Operations
```bash
# Generate only puzzles
python -m smart_book_maker.cli generate sudoku --count 100
python -m smart_book_maker.cli generate maze --count 100

# Create only the book (requires existing puzzles)
python -m smart_book_maker.cli create sudoku-book
python -m smart_book_maker.cli create maze-book
```

### Using as a Library

```python
from smart_book_maker.generators.sudoku import SudokuGenerator
from smart_book_maker.pdf.sudoku_book import SudokuBookPDF

# Generate a single puzzle
generator = SudokuGenerator()
puzzle, solution = generator.generate_puzzle(difficulty=50)

# Create a book
book = SudokuBookPDF("my_sudoku_book.pdf")
book.create_book("output/puzzles", "output/solutions")
```

## 📁 Project Structure

```
Smart-Book-Maker/
├── src/smart_book_maker/          # Main package
│   ├── generators/                # Puzzle generators
│   │   ├── sudoku.py             # Sudoku puzzle generation
│   │   └── maze.py               # Maze puzzle generation
│   ├── pdf/                      # PDF book creators
│   │   ├── sudoku_book.py        # Sudoku book PDF generator
│   │   └── maze_book.py          # Maze book PDF generator
│   ├── utils/                    # Utility functions
│   │   └── file_utils.py         # File and directory helpers
│   └── cli.py                    # Command line interface
├── examples/                     # Example usage scripts
├── tests/                        # Unit tests
├── output/                       # Generated content (created at runtime)
│   ├── puzzles/                  # Puzzle images
│   ├── solutions/               # Solution images
│   ├── mazes/                   # Maze text files
│   ├── mazes_png/               # Maze images
│   └── books/                   # Generated PDF books
├── assets/                       # Static assets (images, fonts, etc.)
├── requirements.txt              # Python dependencies
├── setup.py                     # Package setup
├── LICENSE                      # MIT License
├── CONTRIBUTING.md              # Contribution guidelines
└── README.md                    # This file
```

## 🛠️ Development

### Setting up Development Environment

```bash
# Clone and enter directory
git clone https://github.com/TheUnknown550/Smart-Book-Maker.git
cd Smart-Book-Maker

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies including development tools
pip install -r requirements.txt
pip install -e ".[dev]"
```

### Running Tests

```bash
# Run all tests
python -m pytest

# Run with coverage
python -m pytest --cov=smart_book_maker

# Run specific test file
python -m pytest tests/test_sudoku_generator.py
```

### Code Formatting

```bash
# Format code with black
black src/ tests/ examples/

# Sort imports
isort src/ tests/ examples/

# Type checking
mypy src/
```

## 📖 API Documentation

### SudokuGenerator

```python
from smart_book_maker.generators.sudoku import SudokuGenerator

generator = SudokuGenerator()

# Generate a complete puzzle and solution
puzzle, solution = generator.generate_puzzle(difficulty=50)

# Save as text file
generator.save_puzzle_text(puzzle, solution, "puzzle.txt")

# Save as images
generator.save_puzzle_image(puzzle, "puzzle.png")
generator.save_solution_image(solution, puzzle, "solution.png")
```

### MazeGenerator

```python
from smart_book_maker.generators.maze import MazeGenerator

generator = MazeGenerator()

# Generate a maze
maze, width, height, cell_size = generator.generate_puzzle(level=50)

# Save as text and image
generator.save_maze_text(maze, "maze.txt")
generator.save_maze_image(maze, "maze.png", cell_size)
```

### Creating Books

```python
from smart_book_maker.pdf.sudoku_book import SudokuBookPDF

# Create a Sudoku book
book = SudokuBookPDF("my_book.pdf")
book.create_book("puzzles_dir", "solutions_dir")
```

## 🎯 Use Cases

- **Educational Material**: Create puzzle books for schools and educational programs
- **Print-on-Demand Publishing**: Generate books for platforms like Amazon KDP
- **Personal Use**: Create custom puzzle books for family and friends  
- **Commercial Use**: Generate content for puzzle magazines and publications
- **Brain Training Apps**: Use as a backend for puzzle generation in applications

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Ways to Contribute

- Add new puzzle types (Word Search, Crosswords, etc.)
- Improve existing generators with better algorithms
- Add new PDF layouts and themes
- Write tests and improve documentation
- Fix bugs and optimize performance
- Create example projects and tutorials

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔗 Links

- **GitHub Repository**: [https://github.com/TheUnknown550/Smart-Book-Maker](https://github.com/TheUnknown550/Smart-Book-Maker)
- **Issues**: [https://github.com/TheUnknown550/Smart-Book-Maker/issues](https://github.com/TheUnknown550/Smart-Book-Maker/issues)
- **Documentation**: Coming soon!

## 🏆 Acknowledgments

- Built with [ReportLab](https://www.reportlab.com/) for PDF generation
- Image processing with [Pillow](https://python-pillow.org/)
- Inspired by the need for high-quality, customizable puzzle book generation

## 📊 Requirements

- **Python**: 3.7 or higher
- **Dependencies**: See [requirements.txt](requirements.txt)
- **System**: Cross-platform (Windows, macOS, Linux)
- **Memory**: Recommended 512MB+ RAM for large book generation
- **Storage**: Variable based on output size (typically 1-100MB per book)

---

**Created with ❤️ by the Smart Book Maker Contributors**
