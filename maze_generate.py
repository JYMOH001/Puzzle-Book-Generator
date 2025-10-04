
import random
import os
from PIL import Image, ImageDraw

def generate_maze(width, height):
	# Iterative backtracking maze generation (no recursion)
	maze = [['#'] * (2 * width + 1) for _ in range(2 * height + 1)]
	stack = [(0, 0)]
	maze[1][1] = ' '
	visited = set()
	visited.add((0, 0))
	while stack:
		x, y = stack[-1]
		dirs = [(0,1),(1,0),(0,-1),(-1,0)]
		random.shuffle(dirs)
		found = False
		for dx, dy in dirs:
			nx, ny = x + dx, y + dy
			if 0 <= nx < width and 0 <= ny < height and (nx, ny) not in visited:
				maze[y*2+1+dy][x*2+1+dx] = ' '
				maze[ny*2+1][nx*2+1] = ' '
				stack.append((nx, ny))
				visited.add((nx, ny))
				found = True
				break
		if not found:
			stack.pop()
	# Entrance and exit
	maze[1][0] = 'S'
	maze[2*height-1][2*width] = 'E'
	return maze

def save_maze(maze, filename):
	with open(filename, 'w') as f:
		for row in maze:
			f.write(''.join(row) + '\n')

def save_maze_image(maze, filename, cell_size=20, wall_color=(0,0,0), path_color=(255,255,255), start_color=(0,255,0), end_color=(255,0,0)):
	height = len(maze)
	width = len(maze[0])
	img = Image.new('RGB', (width*cell_size, height*cell_size), path_color)
	draw = ImageDraw.Draw(img)
	for y, row in enumerate(maze):
		for x, cell in enumerate(row):
			color = path_color
			if cell == '#':
				color = wall_color
			draw.rectangle([
				x*cell_size, y*cell_size,
				(x+1)*cell_size-1, (y+1)*cell_size-1
			], fill=color)
	# Draw start arrow (right-pointing triangle)
	for y, row in enumerate(maze):
		for x, cell in enumerate(row):
			if cell == 'S':
				cx = x*cell_size + cell_size//2
				cy = y*cell_size + cell_size//2
				size = cell_size//2
				arrow = [
					(cx-size//2, cy-size//2),
					(cx-size//2, cy+size//2),
					(cx+size//2, cy)
				]
				draw.polygon(arrow, fill=(0,128,255))
			elif cell == 'E':
				# Draw a flag for the end
				cx = x*cell_size + cell_size//2
				cy = y*cell_size + cell_size//2
				flag_height = cell_size//2
				flag_width = cell_size//3
				# Flag pole
				draw.line([
					(cx, cy-flag_height//2),
					(cx, cy+flag_height//2)
				], fill=(255,0,0), width=2)
				# Flag triangle
				flag = [
					(cx, cy-flag_height//2),
					(cx+flag_width, cy-flag_height//2+flag_width//2),
					(cx, cy-flag_height//2+flag_width)
				]
				draw.polygon(flag, fill=(255,0,0))
	img.save(filename)

def difficulty_params(level):
	# Map level 1-100 to width/height, with much larger mazes for hard/very hard
	if level <= 25:
		return 5, 5  # very easy
	elif level <= 55:
		return 12, 12  # easy
	elif level <= 90:
		return 20, 20  # medium
	elif level <= 125:
		return 35, 35  # hard
	else:
		return 50, 50  # very hard

def main():
	os.makedirs('mazes', exist_ok=True)
	os.makedirs('mazes_png', exist_ok=True)
	for i in range(1, 161):
		width, height = difficulty_params(i)
		maze = generate_maze(width, height)
		txt_filename = f'mazes/maze_{i:03d}_{width}x{height}.txt'
		png_filename = f'mazes_png/maze_{i:03d}_{width}x{height}.png'
		# Set cell_size based on difficulty
		if width <= 5:
			cell_size = 32
		elif width <= 12:
			cell_size = 24
		elif width <= 20:
			cell_size = 16
		elif width <= 35:
			cell_size = 10
		else:
			cell_size = 7
		save_maze(maze, txt_filename)
		save_maze_image(maze, png_filename, cell_size=cell_size)
		print(f'Generated {txt_filename} and {png_filename} (cell_size={cell_size})')

if __name__ == '__main__':
	main()