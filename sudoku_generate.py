import random
import os
import copy
from PIL import Image, ImageDraw, ImageFont

class SudokuGenerator:
    def __init__(self):
        self.grid = [[0 for _ in range(9)] for _ in range(9)]
        
    def is_valid(self, grid, row, col, num):
        """Check if placing num at (row, col) is valid"""
        # Check row
        for x in range(9):
            if grid[row][x] == num:
                return False
        
        # Check column
        for x in range(9):
            if grid[x][col] == num:
                return False
        
        # Check 3x3 box
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(3):
            for j in range(3):
                if grid[i + start_row][j + start_col] == num:
                    return False
        
        return True
    
    def solve_sudoku(self, grid):
        """Solve sudoku using backtracking"""
        for i in range(9):
            for j in range(9):
                if grid[i][j] == 0:
                    numbers = list(range(1, 10))
                    random.shuffle(numbers)
                    for num in numbers:
                        if self.is_valid(grid, i, j, num):
                            grid[i][j] = num
                            if self.solve_sudoku(grid):
                                return True
                            grid[i][j] = 0
                    return False
        return True
    
    def generate_complete_grid(self):
        """Generate a complete valid Sudoku grid"""
        self.grid = [[0 for _ in range(9)] for _ in range(9)]
        self.solve_sudoku(self.grid)
        return copy.deepcopy(self.grid)
    
    def remove_numbers(self, grid, difficulty):
        """Remove numbers based on difficulty level"""
        # Difficulty levels with number of clues to keep:
        # Very Easy: 45-50 clues (remove 31-36 numbers)
        # Easy: 40-45 clues (remove 36-41 numbers)
        # Medium: 32-40 clues (remove 41-49 numbers)
        # Hard: 28-32 clues (remove 49-53 numbers)
        # Expert: 22-28 clues (remove 53-59 numbers)
        
        if difficulty <= 25:  # Very Easy
            remove_count = random.randint(31, 36)
        elif difficulty <= 55:  # Easy
            remove_count = random.randint(36, 41)
        elif difficulty <= 90:  # Medium
            remove_count = random.randint(41, 49)
        elif difficulty <= 125:  # Hard
            remove_count = random.randint(49, 53)
        else:  # Expert
            remove_count = random.randint(53, 59)
        
        puzzle = copy.deepcopy(grid)
        positions = [(i, j) for i in range(9) for j in range(9)]
        random.shuffle(positions)
        
        # Remove numbers randomly (simplified approach for performance)
        for i in range(remove_count):
            if i < len(positions):
                row, col = positions[i]
                puzzle[row][col] = 0
        
        return puzzle

def save_sudoku_txt(puzzle, solution, filename):
    """Save sudoku puzzle and solution to text file"""
    with open(filename, 'w') as f:
        f.write("PUZZLE:\n")
        for row in puzzle:
            f.write(' '.join('.' if x == 0 else str(x) for x in row) + '\n')
        f.write("\nSOLUTION:\n")
        for row in solution:
            f.write(' '.join(str(x) for x in row) + '\n')

def save_sudoku_puzzle_image(puzzle, filename, cell_size=60):
    """Save sudoku puzzle as a single image without labels"""
    margin = 20
    grid_size = 9 * cell_size
    total_width = grid_size + 2 * margin
    total_height = grid_size + 2 * margin
    
    # Create image
    img = Image.new('RGB', (total_width, total_height), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    
    try:
        # Try to use a TrueType font
        bold_font = ImageFont.truetype("arialbd.ttf", cell_size // 2)
    except:
        # Fallback to default font
        bold_font = ImageFont.load_default()
    
    # Draw grid lines
    for i in range(10):
        line_width = 3 if i % 3 == 0 else 1
        # Vertical lines
        x = margin + i * cell_size
        draw.line([(x, margin), (x, margin + grid_size)], 
                 fill=(0, 0, 0), width=line_width)
        # Horizontal lines
        y = margin + i * cell_size
        draw.line([(margin, y), (margin + grid_size, y)], 
                 fill=(0, 0, 0), width=line_width)
    
    # Fill numbers
    for i in range(9):
        for j in range(9):
            if puzzle[i][j] != 0:
                x = margin + j * cell_size + cell_size // 2
                y = margin + i * cell_size + cell_size // 2
                
                # Center the text
                text = str(puzzle[i][j])
                bbox = draw.textbbox((0, 0), text, font=bold_font)
                text_width = bbox[2] - bbox[0]
                text_height = bbox[3] - bbox[1]
                
                draw.text((x - text_width // 2, y - text_height // 2), 
                         text, fill=(0, 0, 0), font=bold_font)
    
    img.save(filename)

def save_sudoku_solution_image(solution, puzzle, filename, cell_size=60):
    """Save sudoku solution as a single image with given numbers in black and solved numbers in blue"""
    margin = 20
    grid_size = 9 * cell_size
    total_width = grid_size + 2 * margin
    total_height = grid_size + 2 * margin
    
    # Create image
    img = Image.new('RGB', (total_width, total_height), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    
    try:
        # Try to use a TrueType font
        font = ImageFont.truetype("arial.ttf", cell_size // 2)
        bold_font = ImageFont.truetype("arialbd.ttf", cell_size // 2)
    except:
        # Fallback to default font
        font = ImageFont.load_default()
        bold_font = font
    
    # Draw grid lines
    for i in range(10):
        line_width = 3 if i % 3 == 0 else 1
        # Vertical lines
        x = margin + i * cell_size
        draw.line([(x, margin), (x, margin + grid_size)], 
                 fill=(0, 0, 0), width=line_width)
        # Horizontal lines
        y = margin + i * cell_size
        draw.line([(margin, y), (margin + grid_size, y)], 
                 fill=(0, 0, 0), width=line_width)
    
    # Fill numbers with different colors based on whether they were given or solved
    for i in range(9):
        for j in range(9):
            if solution[i][j] != 0:
                x = margin + j * cell_size + cell_size // 2
                y = margin + i * cell_size + cell_size // 2
                
                # Determine color based on whether this was a given clue or solved number
                if puzzle[i][j] != 0:
                    # This was a given clue - use black and bold font
                    color = (0, 0, 0)
                    current_font = bold_font
                else:
                    # This was solved by the player - use blue and regular font
                    color = (0, 0, 255)
                    current_font = font
                
                # Center the text
                text = str(solution[i][j])
                bbox = draw.textbbox((0, 0), text, font=current_font)
                text_width = bbox[2] - bbox[0]
                text_height = bbox[3] - bbox[1]
                
                draw.text((x - text_width // 2, y - text_height // 2), 
                         text, fill=color, font=current_font)
    
    img.save(filename)

def difficulty_name(level):
    """Get difficulty name based on level"""
    if level <= 40:
        return "Very Easy"
    elif level <= 80:
        return "Easy"
    elif level <= 120:
        return "Medium"
    elif level <= 160:
        return "Hard"
    else:
        return "Expert"

def main():
    # Create directories
    os.makedirs('sudokus', exist_ok=True)
    os.makedirs('puzzles', exist_ok=True)
    os.makedirs('solutions', exist_ok=True)
    
    generator = SudokuGenerator()

    for i in range(1, 201):
        print(f'Generating Sudoku {i}/200...')
        
        # Generate complete solution
        solution = generator.generate_complete_grid()
        
        # Create puzzle by removing numbers
        puzzle = generator.remove_numbers(solution, i)
        
        # Get difficulty name
        diff_name = difficulty_name(i)
        
        # Save files
        txt_filename = f'sudokus/sudoku_{i:03d}_{diff_name.replace(" ", "_").lower()}.txt'
        puzzle_png_filename = f'puzzles/puzzle_{i:03d}_{diff_name.replace(" ", "_").lower()}.png'
        solution_png_filename = f'solutions/solution_{i:03d}_{diff_name.replace(" ", "_").lower()}.png'
        
        save_sudoku_txt(puzzle, solution, txt_filename)
        save_sudoku_puzzle_image(puzzle, puzzle_png_filename)
        save_sudoku_solution_image(solution, puzzle, solution_png_filename)
        
        print(f'Generated {txt_filename}, {puzzle_png_filename}, and {solution_png_filename} (Difficulty: {diff_name})')

if __name__ == '__main__':
    main()
