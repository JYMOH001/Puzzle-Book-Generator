# Comprehensive Sudoku Puzzle Book PDF Generator
# Requirements: pip install reportlab pillow
import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from PIL import Image

def add_image(c, img_path, x, y, w, h):
    import uuid
    if not os.path.exists(img_path):
        print(f"Warning: Image not found: {img_path}")
        return
    img = Image.open(img_path)
    img = img.convert('RGB')
    img = img.resize((int(w), int(h)), Image.LANCZOS)
    temp_path = f'temp_img_{uuid.uuid4().hex}.jpg'
    img.save(temp_path)
    img.close()
    c.drawImage(temp_path, x, y, width=w, height=h)
    os.remove(temp_path)

def get_difficulty_info():
    """Return difficulty level information"""
    return [
        {"name": "Very Easy", "range": "1-40", "start": 1, "end": 40},
        {"name": "Easy", "range": "41-80", "start": 41, "end": 80},
        {"name": "Medium", "range": "81-120", "start": 81, "end": 120},
        {"name": "Hard", "range": "121-160", "start": 121, "end": 160},
        {"name": "Expert", "range": "161-200", "start": 161, "end": 200}
    ]

def add_page_number(c, page_num, page_width, page_height):
    """Add page number at the bottom of the page"""
    c.setFont('Helvetica', 10)
    c.drawCentredString(page_width/2, 0.5*inch, str(page_num))

def main():
    # Book size: 8.5 x 11 inches
    page_width, page_height = 8.5 * inch, 11 * inch
    bleed = 0.125 * inch
    content_width = page_width - 2 * bleed
    content_height = page_height - 2 * bleed
    c = canvas.Canvas('Complete_Sudoku_Puzzle_Book.pdf', pagesize=(page_width, page_height))
    
    page_count = 1
    
    # 1. Title page
    c.setFont('Helvetica-Bold', 28)
    c.drawCentredString(page_width/2, page_height/2 + 80, 'Sudoku Journey:')
    c.setFont('Helvetica-Bold', 22)
    c.drawCentredString(page_width/2, page_height/2 + 40, 'Brain-Busting Challenges to Sharpen Your Logic')
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
    page_count += 1

    # 2. Table of Contents
    c.setFont('Helvetica-Bold', 24)
    c.drawCentredString(page_width/2, page_height - 1.5*inch, 'Table of Contents')
    
    difficulty_info = get_difficulty_info()
    
    # Calculate page numbers for each section
    current_page = 4  # After title, TOC, and how-to-play pages
    toc_entries = []
    
    for diff in difficulty_info:
        puzzle_count = diff['end'] - diff['start'] + 1
        section_start = current_page  # Point to the divider page itself
        toc_entries.append({
            'name': diff['name'],
            'range': diff['range'],
            'page': section_start
        })
        current_page += 1 + puzzle_count  # +1 for divider page
    
    # Solutions section starts after all puzzles
    solutions_start = current_page  # Point to the solutions divider page
    toc_entries.append({
        'name': 'Solutions',
        'range': 'All Levels',
        'page': solutions_start
    })
    
    # Draw TOC entries
    c.setFont('Helvetica', 14)
    start_y = page_height - 2.5*inch
    
    # Instructions entry
    c.drawString(bleed + 0.5*inch, start_y, 'How to Play Sudoku')
    c.drawString(page_width - bleed - 1*inch, start_y, '3')
    start_y -= 0.3*inch
    
    c.drawString(bleed + 0.5*inch, start_y, '')
    start_y -= 0.3*inch
    
    c.setFont('Helvetica-Bold', 16)
    c.drawString(bleed + 0.5*inch, start_y, 'Puzzles by Difficulty:')
    start_y -= 0.4*inch
    
    c.setFont('Helvetica', 14)
    for entry in toc_entries:
        if entry['name'] == 'Solutions':
            start_y -= 0.2*inch
            c.setFont('Helvetica-Bold', 16)
            c.drawString(bleed + 0.5*inch, start_y, f"{entry['name']} ({entry['range']})")
            c.drawString(page_width - bleed - 1*inch, start_y, str(entry['page']))
        else:
            c.drawString(bleed + 0.8*inch, start_y, f"{entry['name']} - Puzzles {entry['range']}")
            c.drawString(page_width - bleed - 1*inch, start_y, str(entry['page']))
        start_y -= 0.3*inch
    
    add_page_number(c, page_count, page_width, page_height)
    c.showPage()
    page_count += 1

    # 3. How to play page
    c.setFont('Helvetica-Bold', 22)
    c.drawCentredString(page_width/2, page_height - 1.5*inch, 'How to Play Sudoku')
    
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
        '• Very Easy (Puzzles 1-40): Great for beginners',
        '• Easy (Puzzles 41-80): Build your confidence',
        '• Medium (Puzzles 81-120): Test your skills',
        '• Hard (Puzzles 121-160): Challenge yourself',
        '• Expert (Puzzles 161-200): Master level puzzles',
        '',
        'Tips:',
        '• Start with rows, columns, or boxes with the most given numbers',
        '• Look for numbers that can only go in one place',
        '• Use pencil marks to track possibilities',
        '• Check the solutions section at the back if you get stuck',
        '',
        'Good luck and have fun solving!'
    ]
    
    start_y = page_height - 2*inch
    for i, line in enumerate(instructions):
        if line.startswith('•'):
            c.drawString(bleed + 0.5*inch, start_y - i*18, line)
        else:
            c.drawCentredString(page_width/2, start_y - i*18, line)
    
    add_page_number(c, page_count, page_width, page_height)
    c.showPage()
    page_count += 1

    # 4. Puzzle pages with difficulty dividers
    puzzle_dir = 'puzzles'
    
    if not os.path.exists(puzzle_dir):
        print(f"Error: {puzzle_dir} directory not found. Please run sudoku_generate.py first.")
        return
    
    for diff in difficulty_info:
        # Add difficulty divider page
        c.setFont('Helvetica-Bold', 32)
        c.drawCentredString(page_width/2, page_height/2 + 40, diff['name'])
        c.setFont('Helvetica-Bold', 20)
        c.drawCentredString(page_width/2, page_height/2, f"Puzzles {diff['range']}")
        c.setFont('Helvetica', 16)
        puzzle_count = diff['end'] - diff['start'] + 1
        c.drawCentredString(page_width/2, page_height/2 - 40, f"{puzzle_count} Puzzles")
        
        add_page_number(c, page_count, page_width, page_height)
        c.showPage()
        page_count += 1
        
        # Add puzzles for this difficulty
        for puzzle_num in range(diff['start'], diff['end'] + 1):
            diff_name_file = diff['name'].replace(" ", "_").lower()
            puzzle_file = f'puzzle_{puzzle_num:03d}_{diff_name_file}.png'
            puzzle_path = os.path.join(puzzle_dir, puzzle_file)
            
            if os.path.exists(puzzle_path):
                # Title
                c.setFont('Helvetica-Bold', 18)
                title_y = page_height - 0.8*inch
                c.drawCentredString(page_width/2, title_y, f'Puzzle {puzzle_num}')
                
                # Puzzle image - centered on page
                img_size = 6 * inch  # Square image
                img_x = (page_width - img_size) / 2
                img_y = (page_height - img_size) / 2 - 0.2*inch
                
                add_image(c, puzzle_path, img_x, img_y, img_size, img_size)
                
                add_page_number(c, page_count, page_width, page_height)
                c.showPage()
                page_count += 1
                print(f'Added puzzle {puzzle_num} to PDF')
            else:
                print(f'Warning: Puzzle file not found: {puzzle_path}')

    # 5. Solutions section divider
    c.setFont('Helvetica-Bold', 32)
    c.drawCentredString(page_width/2, page_height/2 + 40, 'Solutions')
    c.setFont('Helvetica', 18)
    c.drawCentredString(page_width/2, page_height/2, 'All Puzzle Solutions')
    c.setFont('Helvetica', 14)
    c.drawCentredString(page_width/2, page_height/2 - 40, 'Organized by Puzzle Number')
    
    add_page_number(c, page_count, page_width, page_height)
    c.showPage()
    page_count += 1

    # 6. Solutions pages
    solution_dir = 'solutions'
    
    if not os.path.exists(solution_dir):
        print(f"Error: {solution_dir} directory not found. Please run sudoku_generate.py first.")
        c.save()
        return
    
    for diff in difficulty_info:
        for puzzle_num in range(diff['start'], diff['end'] + 1):
            diff_name_file = diff['name'].replace(" ", "_").lower()
            solution_file = f'solution_{puzzle_num:03d}_{diff_name_file}.png'
            solution_path = os.path.join(solution_dir, solution_file)
            
            if os.path.exists(solution_path):
                # Title
                c.setFont('Helvetica-Bold', 18)
                title_y = page_height - 0.8*inch
                c.drawCentredString(page_width/2, title_y, f'Solution {puzzle_num}')
                
                # Solution image - centered on page
                img_size = 6 * inch  # Square image
                img_x = (page_width - img_size) / 2
                img_y = (page_height - img_size) / 2 - 0.2*inch
                
                add_image(c, solution_path, img_x, img_y, img_size, img_size)
                
                add_page_number(c, page_count, page_width, page_height)
                c.showPage()
                page_count += 1
                print(f'Added solution {puzzle_num} to PDF')
            else:
                print(f'Warning: Solution file not found: {solution_path}')

    # 7. Add closing page with thank you message
    c.setFont('Helvetica-Bold', 20)
    c.drawCentredString(page_width/2, page_height - 2*inch, 'Thank You for Solving!')
    
    c.setFont('Helvetica', 12)
    closing_messages = [
        '',
        'Congratulations on completing these Sudoku puzzles!',
        'We hope you enjoyed the mental challenge and had fun along the way.',
        '',
        'If you enjoyed these puzzles, please consider leaving a review —',
        'it really helps support our small creative shop!',
        '',
        'Tag us on social media when you\'re solving these puzzles!',
        '@mcxstudios24 — we\'d love to see your progress and celebrate',
        'your puzzle-solving achievements with you.',
        '',
        'Keep challenging your mind and happy puzzling!',
        '',
        '— The MCXStudios24 Team'
    ]
    
    start_y = page_height - 3*inch
    for i, line in enumerate(closing_messages):
        if line == '— The MCXStudios24 Team':
            c.setFont('Helvetica', 11)  # Use regular Helvetica instead of italic
        c.drawCentredString(page_width/2, start_y - i*20, line)
    
    # Add decorative border
    border_margin = 1*inch
    c.setStrokeGray(0.7)  # Light gray
    c.setLineWidth(2)
    c.rect(border_margin, border_margin, 
           page_width - 2*border_margin, page_height - 2*border_margin)
    
    add_page_number(c, page_count, page_width, page_height)
    c.showPage()
    page_count += 1
    
    c.save()
    print(f'Complete Sudoku Puzzle Book PDF created successfully with {page_count} pages!')

if __name__ == '__main__':
    main()
