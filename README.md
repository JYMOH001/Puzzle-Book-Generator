# Puzzle Book Generator

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.7+-blue.svg)
![Version](https://img.shields.io/badge/version-1.0.0-green.svg)

**Smart Book Maker** is a powerful Python library and command-line tool for generating professional puzzle books. Create print-ready PDF books with customizable difficulty levels, adaptive puzzle counts, and professional layouts.

## � Features

- **🧩 Multiple Puzzle Types**: Generate Sudoku and Maze puzzles
- **📈 Adaptive Difficulty**: Automatically distributes puzzles across 5 difficulty levels
- **📖 Custom Books**: Create books with custom titles, puzzle counts, and themes  
- **🖨️ Print-Ready PDFs**: Professional layouts suitable for publishing
- **⚡ Easy CLI**: Simple command-line interface for batch operations
- **🔧 Extensible**: Well-structured codebase for adding new puzzle types
- **🎨 Customizable**: Configure book titles, difficulty distributions, and output

## 🚀 Quick Start

### Installation

1. **Clone the repository**:
```bash
git clone https://github.com/TheUnknown550/Smart-Book-Maker.git
cd Smart-Book-Maker
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Test the installation**:
```bash
python test_setup.py
```

### Basic Usage

> **💡 Quick Tip**: Use the `all` command for a complete workflow that generates puzzles AND creates a PDF book!

#### Generate a Complete Sudoku Book (Recommended)
```bash
# Generate 100 Sudoku puzzles and create a complete book
python -m smart_book_maker.cli all sudoku --count 100

# Create a custom book with your own title
python -m smart_book_maker.cli all sudoku --count 50 --title "My Sudoku Collection" --subtitle "Custom Puzzles for Brain Training"
```

#### Generate a Complete Maze Book
```bash
# Generate 80 Maze puzzles and create a complete book  
python -m smart_book_maker.cli all maze --count 80
```

#### Individual Operations

**⚠️ Important**: The `generate` command creates puzzle files but does NOT create a PDF book!

```bash
# Generate only puzzles (no book created)
python -m smart_book_maker.cli generate sudoku --count 50
python -m smart_book_maker.cli generate maze --count 30

# Create book from existing puzzles (no new puzzles generated)
python -m smart_book_maker.cli create sudoku-book --total-puzzles 50
python -m smart_book_maker.cli create maze-book
```

## 📖 Detailed Usage

### Command Line Interface

The CLI supports three main commands with different purposes:

| Command | Generates Puzzles | Creates PDF Book | Use Case |
|---------|------------------|-----------------|----------|
| `generate` | ✅ Yes | ❌ No | Create puzzle files only |
| `create` | ❌ No | ✅ Yes | Make PDF from existing puzzles |
| `all` | ✅ Yes | ✅ Yes | Complete workflow (recommended) |

#### Generate Puzzles Only
**Creates puzzle/solution files but NO PDF book**
```bash
# Generate Sudoku puzzles (files only)
python -m smart_book_maker.cli generate sudoku --count 100 --output-dir my_puzzles

# Generate Maze puzzles (files only)
python -m smart_book_maker.cli generate maze --count 50 --output-dir my_mazes
```

#### Create Books Only
**Creates PDF book from existing puzzle files (does NOT generate new puzzles)**
```bash
# Create Sudoku book with custom settings
python -m smart_book_maker.cli create sudoku-book \\
    --output-dir my_puzzles \\
    --filename "Custom_Sudoku_Book.pdf" \\
    --title "Advanced Sudoku" \\
    --subtitle "Challenge Your Mind" \\
    --total-puzzles 100

# Create Maze book
python -m smart_book_maker.cli create maze-book \\
    --output-dir my_mazes \\
    --filename "My_Maze_Adventure.pdf"
```

#### All-in-One (Generate + Create Book)
**Generates puzzles AND creates PDF book in one command (recommended for most users)**
```bash
# Complete Sudoku workflow with custom book
python -m smart_book_maker.cli all sudoku \\
    --count 75 \\
    --title "Brain Gym Sudoku" \\
    --subtitle "75 Challenging Puzzles" \\
    --filename "Brain_Gym_Sudoku.pdf"

# Complete Maze workflow
python -m smart_book_maker.cli all maze \\
    --count 60 \\
    --filename "Maze_Master_Challenge.pdf"
```

### Using as a Python Library

```python
from smart_book_maker.generators.sudoku import SudokuGenerator
from smart_book_maker.pdf.sudoku_book import SudokuBookPDF

# Generate individual puzzles
generator = SudokuGenerator()
puzzle, solution = generator.generate_puzzle(difficulty=25, total_puzzles=100)

# Create a custom book
book = SudokuBookPDF(
    output_filename="My_Custom_Book.pdf",
    book_title="Daily Sudoku", 
    book_subtitle="Perfect for Coffee Breaks",
    total_puzzles=50
)
book.create_book("output/puzzles", "output/solutions")
```

## 📂 Output Structure

After running the tool, your files will be organized as follows:

```
output/
├── puzzles/          # Sudoku puzzle images (.png)
├── solutions/        # Sudoku solution images (.png)
├── sudokus/          # Sudoku text files (.txt)
├── mazes/            # Maze text files (.txt)
├── mazes_png/        # Maze images (.png)
└── books/            # Generated PDF books
    ├── Complete_Sudoku_Puzzle_Book.pdf
    └── Complete_Maze_Puzzle_Book.pdf
```

## 🎚️ Adaptive Difficulty System

Smart Book Maker automatically distributes puzzles across 5 difficulty levels based on your total puzzle count:

### Sudoku Difficulties
- **Very Easy**: 45-50 clues (great for beginners)
- **Easy**: 40-45 clues (building confidence)
- **Medium**: 32-40 clues (testing skills) 
- **Hard**: 28-32 clues (challenging)
- **Expert**: 22-28 clues (master level)

### Maze Sizes
- **Very Easy**: 5×5 grids
- **Easy**: 12×12 grids
- **Medium**: 20×20 grids
- **Hard**: 35×35 grids
- **Very Hard**: 50×50 grids

**Example**: If you generate 50 puzzles, you'll get 10 puzzles of each difficulty level. If you generate 100 puzzles, you'll get 20 of each level.

## �️ Advanced Configuration

### Custom Difficulty Distribution

```python
# Create a book with specific puzzle counts
from smart_book_maker.generators.sudoku import SudokuGenerator

generator = SudokuGenerator()

# Generate puzzles with custom total count
for i in range(1, 51):  # 50 puzzles total
    puzzle, solution = generator.generate_puzzle(i, total_puzzles=50)
    difficulty = generator.get_difficulty_name(i, total_puzzles=50)
    print(f"Puzzle {i}: {difficulty}")
```

### Multiple Books from Same Puzzles

```bash
# Generate puzzles once
python -m smart_book_maker.cli generate sudoku --count 100

# Create multiple books with different titles
python -m smart_book_maker.cli create sudoku-book --title "Sudoku Volume 1" --filename "Volume1.pdf"
python -m smart_book_maker.cli create sudoku-book --title "Sudoku Volume 2" --filename "Volume2.pdf"
```

## 🧪 Development & Testing

### Run Tests
```bash
# Run the setup test
python test_setup.py

# Run unit tests (if you have pytest installed)
python -m pytest tests/
```

### Code Structure
```
src/smart_book_maker/
├── generators/       # Puzzle generation logic
├── pdf/             # PDF book creation
├── utils/           # Helper functions
└── cli.py           # Command-line interface
```

## ❗ Troubleshooting

### Common Issues

**1. "No module named 'reportlab'" error**
```bash
pip install reportlab pillow
```

**2. "Permission denied" when creating PDFs**
- Make sure no PDF files are open in another program
- Check that you have write permissions to the output directory

**3. Images not generating properly**
- Ensure you have the Pillow library installed: `pip install pillow`
- Try running with a smaller puzzle count first

**4. CLI not working**
```bash
# Make sure you're in the project directory
cd Smart-Book-Maker

# Try running the module directly
python -m smart_book_maker.cli --help
```

## 📋 Requirements

- **Python**: 3.7 or higher
- **Dependencies**: `pillow` and `reportlab` (see requirements.txt)
- **Memory**: 512MB+ RAM recommended for large books
- **Storage**: 1-100MB per book depending on puzzle count

## 🤝 Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Ways to Contribute
- Add new puzzle types (Word Search, Crosswords, etc.)
- Improve puzzle generation algorithms
- Create new PDF layouts and themes
- Write tests and improve documentation
- Fix bugs and optimize performance

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🎉 Examples

### Create a Mini Sudoku Book
```bash
python -m smart_book_maker.cli all sudoku \\
    --count 25 \\
    --title "Sudoku Starter Pack" \\
    --subtitle "Perfect for Beginners" \\
    --filename "Starter_Sudoku.pdf"
```

### Create a Mega Maze Collection
```bash
python -m smart_book_maker.cli all maze \\
    --count 200 \\
    --filename "Ultimate_Maze_Challenge.pdf"
```

### Generate Puzzles for Multiple Books
```bash
# Generate a large set of puzzles
python -m smart_book_maker.cli generate sudoku --count 300

# Create themed books from the same puzzles
python -m smart_book_maker.cli create sudoku-book \\
    --title "Morning Sudoku" \\
    --subtitle "Start Your Day Right" \\
    --total-puzzles 100 \\
    --filename "Morning_Sudoku.pdf"

python -m smart_book_maker.cli create sudoku-book \\
    --title "Evening Sudoku" \\
    --subtitle "Relax and Unwind" \\
    --total-puzzles 100 \\
    --filename "Evening_Sudoku.pdf"
```

---

**Happy Puzzle Making! 🧩📚**
