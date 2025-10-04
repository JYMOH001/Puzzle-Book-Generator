"""
Example: Generate Maze Puzzles and Create a Book

This example demonstrates how to use the Smart Book Maker library
to generate Maze puzzles and create a professional PDF book.
"""

from smart_book_maker.generators.maze import MazeGenerator
from smart_book_maker.pdf.maze_book import MazeBookPDF
from smart_book_maker.utils.file_management import ensure_output_directories, get_maze_filenames


def main():
    """Generate Maze puzzles and create a book."""
    
    # Configuration
    num_puzzles = 160
    output_dir = "output"
    
    print(f"Generating {num_puzzles} Maze puzzles...")
    
    # Ensure output directories exist
    ensure_output_directories(output_dir)
    
    # Create generator
    generator = MazeGenerator()
    
    # Generate puzzles
    for i in range(1, num_puzzles + 1):
        print(f'Generating Maze {i}/{num_puzzles}...')
        
        # Generate maze
        maze, width, height, cell_size = generator.generate_puzzle(i)
        
        # Get filenames
        filenames = get_maze_filenames(i, width, height, output_dir)
        
        # Save files
        generator.save_maze_text(maze, filenames["text"])
        generator.save_maze_image(maze, filenames["image"], cell_size)
        
        print(f'Generated maze {i} ({width}x{height}, cell_size={cell_size})')
    
    print(f"Successfully generated {num_puzzles} Maze puzzles!")
    
    # Create PDF book
    print("Creating PDF book...")
    book = MazeBookPDF(f"{output_dir}/books/Complete_Maze_Puzzle_Book.pdf")
    book.create_book(f"{output_dir}/mazes_png")
    
    print("Complete! Check the output directory for your maze book.")


if __name__ == "__main__":
    main()