"""
Example: Generate Sudoku Puzzles and Create a Book

This example demonstrates how to use the Smart Book Maker library
to generate Sudoku puzzles and create a professional PDF book.
"""

from smart_book_maker.generators.sudoku import SudokuGenerator
from smart_book_maker.pdf.sudoku_book import SudokuBookPDF
from smart_book_maker.utils.file_management import ensure_output_directories, get_sudoku_filenames


def main():
    """Generate Sudoku puzzles and create a book."""
    
    # Configuration
    num_puzzles = 160
    output_dir = "output"
    
    print(f"Generating {num_puzzles} Sudoku puzzles...")
    
    # Ensure output directories exist
    ensure_output_directories(output_dir)
    
    # Create generator
    generator = SudokuGenerator()
    
    # Generate puzzles
    for i in range(1, num_puzzles + 1):
        print(f'Generating Sudoku {i}/{num_puzzles}...')
        
        # Generate puzzle and solution
        puzzle, solution = generator.generate_puzzle(i)
        
        # Get difficulty name
        difficulty_name = generator.get_difficulty_name(i)
        
        # Get filenames
        filenames = get_sudoku_filenames(i, difficulty_name, output_dir)
        
        # Save files
        generator.save_puzzle_text(puzzle, solution, filenames["text"])
        generator.save_puzzle_image(puzzle, filenames["puzzle"])
        generator.save_solution_image(solution, puzzle, filenames["solution"])
        
        print(f'Generated puzzle {i} (Difficulty: {difficulty_name})')
    
    print(f"Successfully generated {num_puzzles} Sudoku puzzles!")
    
    # Create PDF book
    print("Creating PDF book...")
    book = SudokuBookPDF(f"{output_dir}/books/Complete_Sudoku_Puzzle_Book.pdf")
    book.create_book(f"{output_dir}/puzzles", f"{output_dir}/solutions")
    
    print("Complete! Check the output directory for your puzzle book.")


if __name__ == "__main__":
    main()