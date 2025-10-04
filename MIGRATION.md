# Migration Guide

This guide helps you migrate from the old file structure to the new organized structure.

## What Changed

The project has been restructured for better organization and to follow Python package standards:

### Old Structure (Before v1.0.0)
```
Smart-Book-Maker/
├── sudoku_generate.py
├── maze_generate.py  
├── sudoku_complete_book_pdf.py
├── maze_book_pdf.py
├── puzzles/
├── solutions/
├── mazes/
├── mazes_png/
├── sudokus/
└── *.pdf files
```

### New Structure (v1.0.0+)
```
Smart-Book-Maker/
├── src/smart_book_maker/        # Main package
│   ├── generators/              # Puzzle generators
│   ├── pdf/                     # PDF creators
│   ├── utils/                   # Utilities
│   └── cli.py                   # Command line interface
├── examples/                    # Example scripts
├── tests/                       # Unit tests
├── output/                      # Generated content
│   ├── puzzles/
│   ├── solutions/
│   ├── mazes/
│   ├── mazes_png/
│   ├── sudokus/
│   └── books/                   # PDF files
└── assets/                      # Static assets
```

## Migration Steps

### 1. Update Your Scripts

#### Old Way:
```python
# Old imports
from sudoku_generate import SudokuGenerator
import sudoku_complete_book_pdf

# Old usage
generator = SudokuGenerator()
# ... generate puzzles manually
```

#### New Way:
```python
# New imports
from smart_book_maker.generators.sudoku import SudokuGenerator
from smart_book_maker.pdf.sudoku_book import SudokuBookPDF

# New usage - much simpler!
generator = SudokuGenerator()
puzzle, solution = generator.generate_puzzle(50)

# Create book easily
book = SudokuBookPDF("my_book.pdf")
book.create_book("output/puzzles", "output/solutions")
```

### 2. Use the New CLI

#### Old Way:
```bash
python sudoku_generate.py
python sudoku_complete_book_pdf.py
```

#### New Way:
```bash
# Generate puzzles and create book in one command
python -m smart_book_maker.cli all sudoku --count 160

# Or use individual commands
python -m smart_book_maker.cli generate sudoku --count 160
python -m smart_book_maker.cli create sudoku-book
```

### 3. Update File Paths

All generated files now go into the `output/` directory:
- Puzzles: `output/puzzles/`
- Solutions: `output/solutions/`
- Mazes: `output/mazes/` and `output/mazes_png/`
- Books: `output/books/`

### 4. Legacy File Compatibility

The new version can work with your existing files! Just move them:

```bash
# Move existing files to new structure
mkdir output
mkdir output/books
mv puzzles/ output/
mv solutions/ output/
mv mazes/ output/
mv mazes_png/ output/
mv sudokus/ output/
mv *.pdf output/books/
```

## Benefits of the New Structure

1. **Better Organization**: Clear separation of code, tests, examples, and output
2. **Package Standards**: Follows Python packaging best practices
3. **Easier Installation**: Can be installed as a package with `pip install -e .`
4. **Better Testing**: Comprehensive test suite
5. **CLI Interface**: Much easier to use from command line
6. **Extensibility**: Easy to add new puzzle types and features
7. **Documentation**: Better organized with examples and API docs

## Backward Compatibility

- The core algorithms remain the same
- Generated files have the same format
- Existing PDF files work exactly the same
- File naming conventions are preserved

## Getting Help

If you need help migrating:
1. Check the [examples/](examples/) directory for usage patterns
2. Read the updated [README.md](README.md)
3. Look at the [tests/](tests/) for code examples
4. Open an issue on GitHub if you need specific help

## What's Next

After migrating, you can:
- Use the new CLI for much easier puzzle generation
- Import the library in your own Python projects
- Contribute new features using the organized structure
- Run tests to ensure everything works correctly