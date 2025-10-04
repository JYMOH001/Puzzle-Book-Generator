# Sudoku Puzzle Book PDF Generator
# Requirements: pip install reportlab pillow
import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from PIL import Image

def add_image(c, img_path, x, y, w, h):
    import uuid
    img = Image.open(img_path)
    img = img.convert('RGB')
    img = img.resize((int(w), int(h)), Image.LANCZOS)
    temp_path = f'temp_img_{uuid.uuid4().hex}.jpg'
    img.save(temp_path)
    img.close()
    c.drawImage(temp_path, x, y, width=w, height=h)
    os.remove(temp_path)

def main():
    # Book size: 8.5 x 11 inches trim, with bleed (8.625 x 11.25 inches)
    page_width, page_height = 8.5 * inch, 11 * inch
    bleed = 0.125 * inch
    content_width = page_width - 2 * bleed
    content_height = page_height - 2 * bleed
    c = canvas.Canvas('Sudoku_Puzzle_Book.pdf', pagesize=(page_width, page_height))

    # 1. Title page
    c.setFont('Helvetica-Bold', 28)
    c.drawCentredString(page_width/2, page_height/2 + 80, 'Brain Sudoku Challenge:')
    c.setFont('Helvetica-Bold', 22)
    c.drawCentredString(page_width/2, page_height/2 + 40, '160 Puzzles to Master Logic & Focus')
    c.setFont('Helvetica', 18)
    c.drawCentredString(page_width/2, page_height/2, 'From Very Easy to Expert Level')
    c.setFont('Helvetica', 16)
    c.drawCentredString(page_width/2, page_height/2 - 40, 'By MCXStudios24')
    
    # Footer
    c.setFont('Helvetica', 10)
    footer = 'Copyright © 2025 MCXStudios24\nAll rights reserved. No part of this book may be reproduced without permission.\n\nPublished by MCXStudios24\nPrinted in the United States by Amazon KDP'
    footer_offset = 0.25 * inch
    for i, line in enumerate(footer.split('\n')):
        c.drawCentredString(page_width/2, 0.7*inch + footer_offset - i*12, line)
    c.showPage()

    # 2. How to play page
    c.setFont('Helvetica-Bold', 22)
    c.drawCentredString(page_width/2, page_height - 2*inch, 'How to Play Sudoku')
    
    c.setFont('Helvetica', 14)
    instructions = [
        'The goal is to fill the 9×9 grid with digits 1-9, following these rules:',
        '',
        '• Each row must contain all digits from 1 to 9 (no repeats)',
        '• Each column must contain all digits from 1 to 9 (no repeats)', 
        '• Each 3×3 box must contain all digits from 1 to 9 (no repeats)',
        '',
        'Some numbers are already given as clues to get you started.',
        '',
        'Difficulty Levels:',
        '• Very Easy (Levels 1-25): Great for beginners',
        '• Easy (Levels 26-55): Build your confidence', 
        '• Medium (Levels 56-90): Test your skills',
        '• Hard (Levels 91-125): Challenge yourself',
        '• Expert (Levels 126-160): Master level puzzles',
        '',
        'Tips:',
        '• Start with rows, columns, or boxes with the most given numbers',
        '• Look for numbers that can only go in one place',
        '• Use pencil marks to track possibilities',
        '',
        'Good luck and have fun solving!'
    ]
    
    start_y = page_height - 2.5*inch
    for i, line in enumerate(instructions):
        if line.startswith('•'):
            c.drawString(bleed + 0.3*inch, start_y - i*18, line)
        else:
            c.drawCentredString(page_width/2, start_y - i*18, line)
    c.showPage()

    # 3. Sudoku puzzle pages (1 per page for better visibility)
    sudoku_dir = 'sudokus_png'
    sudoku_files = sorted([f for f in os.listdir(sudoku_dir) if f.endswith('.png')])
    
    for i, sudoku_file in enumerate(sudoku_files):
        level = i + 1
        
        # Extract difficulty from filename
        if 'very_easy' in sudoku_file:
            difficulty = 'Very Easy'
        elif 'easy' in sudoku_file:
            difficulty = 'Easy'
        elif 'medium' in sudoku_file:
            difficulty = 'Medium'
        elif 'hard' in sudoku_file:
            difficulty = 'Hard'
        elif 'expert' in sudoku_file:
            difficulty = 'Expert'
        else:
            difficulty = 'Unknown'
        
        # Title
        c.setFont('Helvetica-Bold', 20)
        title_y = page_height - 0.7*inch
        c.drawCentredString(page_width/2, title_y, f'Puzzle {level} - {difficulty}')
        
        # Sudoku image - centered on page
        img_width = 7.5 * inch  # Large enough to be clearly readable
        img_height = 4 * inch   # Maintain aspect ratio from our image
        img_x = (page_width - img_width) / 2
        img_y = (page_height - img_height) / 2 - 0.2*inch  # Slightly below center
        
        add_image(c, os.path.join(sudoku_dir, sudoku_file), img_x, img_y, img_width, img_height)
        
        # Page number at bottom
        c.setFont('Helvetica', 10)
        c.drawCentredString(page_width/2, 0.5*inch, f'Page {level + 2}')
        
        c.showPage()
        print(f'Added puzzle {level} to PDF')

    # 4. Add one empty page at the end
    c.showPage()
    c.save()
    print('Sudoku Puzzle Book PDF created successfully!')

if __name__ == '__main__':
    main()
