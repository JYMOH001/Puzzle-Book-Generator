def add_page_number(c, page_num, page_width, page_height):
    c.setFont('Helvetica', 10)
    c.drawCentredString(page_width/2, 0.5*inch, str(page_num))
# Maze Puzzle Book PDF Generator
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
    c = canvas.Canvas('Maze_Puzzle_Book_cover.pdf', pagesize=(page_width, page_height))

    # 0. Cover page (no page number)
    cover_path = os.path.join('cover', 'cover.jpeg')
    if os.path.exists(cover_path):
        add_image(c, cover_path, 0, 0, page_width, page_height)
        c.showPage()

    # 1. Title page
    c.setFont('Helvetica-Bold', 28)
    c.drawCentredString(page_width/2, page_height/2 + 40, 'The Great Maze Journey:')
    c.setFont('Helvetica-Bold', 22)
    c.drawCentredString(page_width/2, page_height/2, '150+ Puzzles to Sharpen Your Brain')
    c.setFont('Helvetica', 18)
    c.drawCentredString(page_width/2, page_height/2 - 40, 'By MCXStudios24')
    # Footer
    c.setFont('Helvetica', 10)
    footer = 'Copyright © 2025 MCXStudios24\nAll rights reserved. No part of this book may be reproduced without permission.\n\nPublished by MCXStudios24\nPrinted in the United States by Amazon KDP'
    footer_offset = 0.25 * inch
    for i, line in enumerate(footer.split('\n')):
        c.drawCentredString(page_width/2, 0.7*inch + footer_offset - i*12, line)
    c.showPage()


    # 2. Table of Contents page
    c.setFont('Helvetica-Bold', 24)
    c.drawCentredString(page_width/2, page_height - 1.5*inch, 'Table of Contents')

    # Difficulty info for TOC and dividers
    difficulty_info = [
        {'name': 'Very Easy', 'start': 1, 'end': 25, 'range': '1-26'},
        {'name': 'Easy', 'start': 26, 'end': 55, 'range': '27-56'},
        {'name': 'Medium', 'start': 56, 'end': 90, 'range': '57-90'},
        {'name': 'Hard', 'start': 91, 'end': 125, 'range': '91-125'},
        {'name': 'Very Hard', 'start': 126, 'end': 160, 'range': '126-160'},
    ]
    puzzles_per_page = 2
    current_page = 4  # 1: Title, 2: TOC, 3: How-to-Play, 4: first divider
    toc_entries = []
    for diff in difficulty_info:
        puzzle_count = diff['end'] - diff['start'] + 1
        pages_for_puzzles = (puzzle_count + puzzles_per_page - 1) // puzzles_per_page
        section_start = current_page
        toc_entries.append({
            'name': diff['name'],
            'range': diff['range'],
            'page': section_start
        })
        current_page += 1 + pages_for_puzzles  # +1 for divider page
    # Thank you page
    toc_entries.append({
        'name': 'Thank You',
        'range': '',
        'page': current_page
    })

    c.setFont('Helvetica', 14)
    start_y = page_height - 2.5*inch
    c.drawString(bleed + 0.5*inch, start_y, 'How to Play')
    c.drawString(page_width - bleed - 1*inch, start_y, '3')
    start_y -= 0.3*inch
    c.drawString(bleed + 0.5*inch, start_y, '')
    start_y -= 0.3*inch
    c.setFont('Helvetica-Bold', 16)
    c.drawString(bleed + 0.5*inch, start_y, 'Puzzles by Difficulty:')
    start_y -= 0.4*inch
    c.setFont('Helvetica', 14)
    for entry in toc_entries:
        c.drawString(bleed + 0.8*inch, start_y, f"{entry['name']} {('- Puzzles ' + entry['range']) if entry['range'] else ''}")
        c.drawString(page_width - bleed - 1*inch, start_y, str(entry['page']))
        start_y -= 0.3*inch
    add_page_number(c, 2, page_width, page_height)
    c.showPage()

    # 3. How to play page
    c.setFont('Helvetica-Bold', 22)
    c.drawCentredString(page_width/2, page_height - 2*inch, 'How to Play')
    c.setFont('Helvetica', 16)
    lines = [
        'Welcome to your maze adventure!',
        '- Follow the blue arrows and reach the flags to complete each maze!',
        '- Mazes get harder as you go along.',
        '',
        'Good luck and have fun!'
    ]
    for i, line in enumerate(lines):
        c.drawCentredString(page_width/2, page_height - 2.5*inch - i*24, line)
    add_page_number(c, 3, page_width, page_height)
    c.showPage()

    # 3. Maze pages (2 per page, each with level label and maze centered in its half)
    maze_dir = 'mazes_png'
    maze_files = sorted([f for f in os.listdir(maze_dir) if f.endswith('.png')])
    maze_per_page = 2
    label_height = 0.4 * inch
    block_height = content_height / maze_per_page
    maze_img_height = (block_height - label_height - 0.55*inch) * 0.9  # make puzzles smaller
    maze_img_width = content_width * 0.78  # make puzzles smaller
    block_shift_up = 0.15 * inch  # move all blocks up by 0.15 inch
    # Insert divider pages and maze pages by difficulty
    maze_idx = 0
    level = 1
    page_count = 4
    for diff in difficulty_info:
        # Divider page for this difficulty
        c.setFont('Helvetica-Bold', 32)
        c.drawCentredString(page_width/2, page_height/2, f"{diff['name']}   Puzzles {diff['range']}")
        add_page_number(c, page_count, page_width, page_height)
        c.showPage()
        page_count += 1
        # Maze pages for this difficulty
        num_puzzles = diff['end'] - diff['start'] + 1
        for i in range(0, num_puzzles, maze_per_page):
            for j in range(maze_per_page):
                idx = maze_idx + j
                if idx >= maze_idx + num_puzzles or idx >= len(maze_files):
                    break
                maze_file = maze_files[idx]
                # Calculate the vertical center of this block, then shift up
                block_top = page_height - bleed - j * block_height
                block_center = block_top - block_height / 2 + block_shift_up
                # Place label a bit above the center of the block, but push it down by 0.25 inch
                y_label = block_center + maze_img_height / 2 + label_height / 2 - 0.25 * inch
                c.setFont('Helvetica-Bold', 16)
                c.drawCentredString(page_width/2, y_label, f'Level {level}')
                # Maze image below the label, centered in the block
                img_x = (page_width - maze_img_width) / 2
                img_y = y_label - label_height / 2 - maze_img_height
                add_image(c, os.path.join(maze_dir, maze_file), img_x, img_y, maze_img_width, maze_img_height)
                level += 1
            add_page_number(c, page_count, page_width, page_height)
            c.showPage()
            page_count += 1
        maze_idx += num_puzzles
    
    # 4. Add closing page with thank you message
    c.setFont('Helvetica-Bold', 20)
    c.drawCentredString(page_width/2, page_height - 2*inch, 'Thank You for Solving!')
    c.setFont('Helvetica', 12)
    closing_messages = [
        '',
        'Congratulations on completing these maze puzzles!',
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
            c.setFont('Helvetica', 11)
        c.drawCentredString(page_width/2, start_y - i*20, line)
    border_margin = 1*inch
    c.setStrokeGray(0.7)
    c.setLineWidth(2)
    c.rect(border_margin, border_margin, page_width - 2*border_margin, page_height - 2*border_margin)
    add_page_number(c, page_count, page_width, page_height)
    c.showPage()
    page_count += 1
    # 5. Add one empty page at the end (no page number)
    c.showPage()
    c.save()

if __name__ == '__main__':
    main()
