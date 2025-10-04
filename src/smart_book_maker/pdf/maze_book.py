"""
Maze Book PDF Generator

This module provides functionality to create professional PDF books
containing Maze puzzles with proper formatting and organization.
"""

import os
from typing import List, Dict, Any
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from PIL import Image
import uuid


class MazeBookPDF:
    """A class for creating professional Maze puzzle books in PDF format."""
    
    def __init__(self, output_filename: str = "Complete_Maze_Puzzle_Book.pdf"):
        """
        Initialize the Maze book PDF generator.
        
        Args:
            output_filename: Name of the output PDF file
        """
        self.output_filename = output_filename
        self.page_width, self.page_height = 8.5 * inch, 11 * inch
        self.bleed = 0.125 * inch
        self.content_width = self.page_width - 2 * self.bleed
        self.content_height = self.page_height - 2 * self.bleed
        self.page_count = 1
        
    def get_difficulty_info(self) -> List[Dict[str, Any]]:
        """
        Get information about difficulty levels.
        
        Returns:
            List of dictionaries containing difficulty information
        """
        return [
            {"name": "Very Easy", "range": "1-25", "start": 1, "end": 25, "size": "5x5"},
            {"name": "Easy", "range": "26-55", "start": 26, "end": 55, "size": "12x12"},
            {"name": "Medium", "range": "56-90", "start": 56, "end": 90, "size": "20x20"},
            {"name": "Hard", "range": "91-125", "start": 91, "end": 125, "size": "35x35"},
            {"name": "Very Hard", "range": "126-160", "start": 126, "end": 160, "size": "50x50"}
        ]
    
    def add_image(self, c: canvas.Canvas, img_path: str, x: float, y: float, 
                  w: float, h: float) -> None:
        """
        Add an image to the PDF canvas.
        
        Args:
            c: ReportLab canvas object
            img_path: Path to the image file
            x, y: Position coordinates
            w, h: Width and height dimensions
        """
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
    
    def add_page_number(self, c: canvas.Canvas, page_num: int) -> None:
        """
        Add page number at the bottom of the page.
        
        Args:
            c: ReportLab canvas object
            page_num: Page number to display
        """
        c.setFont('Helvetica', 10)
        c.drawCentredString(self.page_width / 2, 0.5 * inch, str(page_num))
    
    def create_title_page(self, c: canvas.Canvas) -> None:
        """Create the title page of the book."""
        c.setFont('Helvetica-Bold', 28)
        c.drawCentredString(self.page_width / 2, self.page_height / 2 + 80, 
                           'Maze Adventures:')
        c.setFont('Helvetica-Bold', 22)
        c.drawCentredString(self.page_width / 2, self.page_height / 2 + 40, 
                           'Navigate Your Way Through Mind-Bending Challenges')
        c.setFont('Helvetica', 18)
        c.drawCentredString(self.page_width / 2, self.page_height / 2, 
                           'From Simple Paths to Complex Labyrinths')
        c.setFont('Helvetica', 16)
        c.drawCentredString(self.page_width / 2, self.page_height / 2 - 40, 
                           'By Smart Book Maker')
        
        # Footer
        c.setFont('Helvetica', 10)
        footer = ('Copyright © 2025 Smart Book Maker Contributors\\n'
                 'All rights reserved. No part of this book may be reproduced without permission.\\n\\n'
                 'Published by Smart Book Maker\\n'
                 'Open Source Project on GitHub')
        footer_offset = 0.25 * inch
        for i, line in enumerate(footer.split('\\n')):
            c.drawCentredString(self.page_width / 2, 0.7 * inch + footer_offset - i * 12, line)
        
        c.showPage()
        self.page_count += 1
    
    def create_table_of_contents(self, c: canvas.Canvas) -> None:
        """Create the table of contents page."""
        c.setFont('Helvetica-Bold', 24)
        c.drawCentredString(self.page_width / 2, self.page_height - 1.5 * inch, 
                           'Table of Contents')
        
        difficulty_info = self.get_difficulty_info()
        
        # Calculate page numbers for each section
        current_page = 4  # After title, TOC, and how-to-play pages
        toc_entries = []
        
        for diff in difficulty_info:
            puzzle_count = diff['end'] - diff['start'] + 1
            section_start = current_page
            toc_entries.append({
                'name': diff['name'],
                'range': diff['range'],
                'size': diff['size'],
                'page': section_start
            })
            current_page += 1 + puzzle_count  # +1 for divider page
        
        # Draw TOC entries
        c.setFont('Helvetica', 14)
        start_y = self.page_height - 2.5 * inch
        
        # Instructions entry
        c.drawString(self.bleed + 0.5 * inch, start_y, 'How to Navigate Mazes')
        c.drawString(self.page_width - self.bleed - 1 * inch, start_y, '3')
        start_y -= 0.3 * inch
        
        c.drawString(self.bleed + 0.5 * inch, start_y, '')
        start_y -= 0.3 * inch
        
        c.setFont('Helvetica-Bold', 16)
        c.drawString(self.bleed + 0.5 * inch, start_y, 'Mazes by Difficulty:')
        start_y -= 0.4 * inch
        
        c.setFont('Helvetica', 14)
        for entry in toc_entries:
            c.drawString(self.bleed + 0.8 * inch, start_y, 
                        f"{entry['name']} ({entry['size']}) - Mazes {entry['range']}")
            c.drawString(self.page_width - self.bleed - 1 * inch, start_y, 
                        str(entry['page']))
            start_y -= 0.3 * inch
        
        self.add_page_number(c, self.page_count)
        c.showPage()
        self.page_count += 1
    
    def create_instructions_page(self, c: canvas.Canvas) -> None:
        """Create the how-to-navigate instructions page."""
        c.setFont('Helvetica-Bold', 22)
        c.drawCentredString(self.page_width / 2, self.page_height - 1.5 * inch, 
                           'How to Navigate Mazes')
        
        c.setFont('Helvetica', 14)
        instructions = [
            'The goal is to find a path from the start (S) to the end (E) of each maze.',
            '',
            'Rules:',
            '• Black areas are walls - you cannot pass through them',
            '• White areas are paths - you can move through these',
            '• Start at the entrance marked with a blue arrow (S)',
            '• Find your way to the exit marked with a red flag (E)',
            '• You can move up, down, left, or right (no diagonal movement)',
            '',
            'Difficulty Levels:',
            '• Very Easy (5x5): Small mazes perfect for beginners',
            '• Easy (12x12): Slightly larger with more path options',
            '• Medium (20x20): Moderate complexity requiring strategy',
            '• Hard (35x35): Complex mazes with many dead ends',
            '• Very Hard (50x50): Massive labyrinths for experts',
            '',
            'Tips:',
            '• Start by looking for the general direction toward the exit',
            '• Use a pencil to trace possible paths',
            '• If you hit a dead end, backtrack and try a different route',
            '• Look ahead to avoid getting trapped in long dead-end paths',
            '• Take breaks if you get frustrated - fresh eyes often help!',
            '',
            'Good luck and happy maze solving!'
        ]
        
        start_y = self.page_height - 2 * inch
        for i, line in enumerate(instructions):
            if line.startswith('•'):
                c.drawString(self.bleed + 0.5 * inch, start_y - i * 18, line)
            else:
                c.drawCentredString(self.page_width / 2, start_y - i * 18, line)
        
        self.add_page_number(c, self.page_count)
        c.showPage()
        self.page_count += 1
    
    def create_puzzle_pages(self, c: canvas.Canvas, maze_dir: str = "output/mazes_png") -> None:
        """
        Create pages for all mazes organized by difficulty.
        
        Args:
            c: ReportLab canvas object
            maze_dir: Directory containing maze images
        """
        if not os.path.exists(maze_dir):
            print(f"Error: {maze_dir} directory not found. Please generate mazes first.")
            return
        
        difficulty_info = self.get_difficulty_info()
        
        for diff in difficulty_info:
            # Add difficulty divider page
            c.setFont('Helvetica-Bold', 32)
            c.drawCentredString(self.page_width / 2, self.page_height / 2 + 40, 
                               diff['name'])
            c.setFont('Helvetica-Bold', 20)
            c.drawCentredString(self.page_width / 2, self.page_height / 2, 
                               f"Mazes {diff['range']} ({diff['size']})")
            c.setFont('Helvetica', 16)
            puzzle_count = diff['end'] - diff['start'] + 1
            c.drawCentredString(self.page_width / 2, self.page_height / 2 - 40, 
                               f"{puzzle_count} Mazes")
            
            self.add_page_number(c, self.page_count)
            c.showPage()
            self.page_count += 1
            
            # Add mazes for this difficulty
            for maze_num in range(diff['start'], diff['end'] + 1):
                # Determine maze size based on difficulty
                if maze_num <= 25:
                    size = "5x5"
                elif maze_num <= 55:
                    size = "12x12"
                elif maze_num <= 90:
                    size = "20x20"
                elif maze_num <= 125:
                    size = "35x35"
                else:
                    size = "50x50"
                
                maze_file = f'maze_{maze_num:03d}_{size}.png'
                maze_path = os.path.join(maze_dir, maze_file)
                
                if os.path.exists(maze_path):
                    # Title
                    c.setFont('Helvetica-Bold', 18)
                    title_y = self.page_height - 0.8 * inch
                    c.drawCentredString(self.page_width / 2, title_y, f'Maze {maze_num}')
                    
                    # Maze image - centered on page
                    img_size = 6.5 * inch  # Slightly larger for mazes
                    img_x = (self.page_width - img_size) / 2
                    img_y = (self.page_height - img_size) / 2 - 0.2 * inch
                    
                    self.add_image(c, maze_path, img_x, img_y, img_size, img_size)
                    
                    self.add_page_number(c, self.page_count)
                    c.showPage()
                    self.page_count += 1
                    print(f'Added maze {maze_num} to PDF')
                else:
                    print(f'Warning: Maze file not found: {maze_path}')
    
    def create_closing_page(self, c: canvas.Canvas) -> None:
        """Create the closing thank you page."""
        c.setFont('Helvetica-Bold', 20)
        c.drawCentredString(self.page_width / 2, self.page_height - 2 * inch, 
                           'Congratulations, Navigator!')
        
        c.setFont('Helvetica', 12)
        closing_messages = [
            '',
            'You have successfully navigated through all these challenging mazes!',
            'We hope you enjoyed the twists, turns, and puzzle-solving adventure.',
            '',
            'If you enjoyed these mazes, please consider giving us a star on GitHub —',
            'it really helps support this open source project!',
            '',
            'Share your maze-solving achievements with the community!',
            'Visit us at github.com/TheUnknown550/Smart-Book-Maker',
            '',
            'Keep exploring new paths and happy puzzle solving!',
            '',
            '— The Smart Book Maker Contributors'
        ]
        
        start_y = self.page_height - 3 * inch
        for i, line in enumerate(closing_messages):
            if line == '— The Smart Book Maker Contributors':
                c.setFont('Helvetica', 11)
            c.drawCentredString(self.page_width / 2, start_y - i * 20, line)
        
        # Add decorative border
        border_margin = 1 * inch
        c.setStrokeGray(0.7)
        c.setLineWidth(2)
        c.rect(border_margin, border_margin,
               self.page_width - 2 * border_margin, self.page_height - 2 * border_margin)
        
        self.add_page_number(c, self.page_count)
        c.showPage()
        self.page_count += 1
    
    def create_book(self, maze_dir: str = "output/mazes_png") -> None:
        """
        Create the complete Maze puzzle book PDF.
        
        Args:
            maze_dir: Directory containing maze images
        """
        c = canvas.Canvas(self.output_filename, pagesize=(self.page_width, self.page_height))
        
        # Create all sections
        self.create_title_page(c)
        self.create_table_of_contents(c)
        self.create_instructions_page(c)
        self.create_puzzle_pages(c, maze_dir)
        self.create_closing_page(c)
        
        c.save()
        print(f'Complete Maze Puzzle Book PDF created successfully with {self.page_count} pages!')
        print(f'Saved as: {self.output_filename}')