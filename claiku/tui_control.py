"""TUI controls for Haiku Writer
"""

import sys
import os
import termios
import tty


class Cursor():
	"""
	class representing the terminal cursor with methods to get the cursor
	position, move the cursor around the terminal, or change the printed 
	font color/style/background
	"""
	def __init__(self, x = None, y = None):
		self._x = x
		self._y = y
		self._rel_x = 0
		self._rel_y = 0
		self._font_color = None
		self._background_color = None
		self._font_style = None

	@staticmethod
	def _pr(inp):
		if isinstance(inp, str):
			inp = bytes(inp, 'utf-8')
		os.write(1, inp)

	def pr(self, inp):
		self._pr(inp)
		if self._x is not None:
			self._x += len(inp)

	@property
	def x(self):
		return(self._x)

	@property
	def y(self):
		return(self._y)

	@x.setter
	def x(self, position):
		try:
			int(position)
		except ValueError:
			print('x setter called with a non-int')
			raise ValueError
		else:
			self._pr('\x1b[{:d};{:d}H'.format(self._y, position))
			self._x = int(position)

	@y.setter
	def y(self, position):
		try:
			int(position)
		except ValueError:
			print('y setter called with a non-int')
			raise ValueError
		else:
			self._pr('\x1b[{:d};{:d}H'.format(position, self._x))
			self._y = int(position)

	@property
	def xy(self):
		return(self._x, self._y)

	@xy.setter
	def xy(self, point):
		"""sets both x and y position at once. Slightly faster than
		setting x and then y individually since it only requires
		one print statement"""
		x_pos, y_pos = point[0], point[1]
		try:
			int(x_pos)
			int(y_pos)
		except ValueError:
			print('xy setter called with a non-int')
			raise ValueError
		else:
			self._pr(f'\x1b[{y_pos};{x_pos}H')
			self._x = x_pos 
			self._y = y_pos

	@property
	def font_color(self):
		return self._font_color

	@property
	def background_color(self):
		return self._background_color

	@property
	def font_style(self):
		return self._font_style

	@font_color.setter
	def font_color(self, color):
		if color is None or color.lower() in {'off', 'none'}:
			self._pr('\x1b[0m')
			self._font_color = None
			if self._background_color is not None:
				self.background_color = self._background_color
			if self._font_style is not None:
				self.font_style = self._font_style
			return
		
		colors = {
			'black': '30',
			'red': '31',
			'green': '32',
			'yellow': '33',
			'blue': '34',
			'magenta': '35',
			'cyan': '36',
			'white': '37',
		}
		self._pr('\x1b[{}m'.format(colors[color]))
		self._font_color = color
	
	
	@background_color.setter
	def background_color(self, color):
		if color is None or color.lower() in {'off', 'none'}:
			self._pr('\x1b[0m')
			self._background_color = None
			if self._font_color is not None:
				self.font_color = self._font_color
			if self._font_style is not None:
				self.font_style = self._font_style
			return
		
		colors = {
			'black': '40',
			'red': '41',
			'green': '42',
			'yellow': '43',
			'blue': '44',
			'magenta': '45',
			'cyan': '46',
			'white': '47',
		}
		self._pr('\x1b[{}m'.format(colors[color]))
		self._background_color = color

	@font_style.setter
	def font_style(self, style):
		#TODO font styles stack (you can have bold and underlined)
		#figure out hot to handle this (reset each time? allow stacking?)
		if style is None or style.lower() in {'off', 'none'}:
			self._pr('\x1b[0m')
			self._font_style = None
			if self._font_color is not None:
				self._font_color = self._font_color
			if self._background_color is not None:
				self.background_color = self._background_color
			return
		
		styles = {
			'bold': '1',
			'underline': '4',
			'invert': '7',
			'italic': '3'
		}
		self._pr('\x1b[{}m'.format(styles[style]))
		self._font_style = style

	def move_up(self, spaces):
		self._pr(f'\x1b[{spaces}A')
		if self.y is not None:
			self._y = self._y - spaces

	def move_down(self, spaces):
		self._pr(f'\x1b[{spaces}B')
		if self.y is not None:
			self._y = self._y + spaces

	def move_right(self, spaces):
		self._pr(f'\x1b[{spaces}C')
		if self.x is not None:
			self._x = self._x + spaces

	def move_left(self, spaces):
		self._pr(f'\x1b[{spaces}D')
		if self.x is not None:
			self._x = self._x - spaces

class InputContext():
	def __enter__(self):
		self.old = termios.tcgetattr(sys.stdin.fileno())
		tty.setraw(sys.stdin)

	def __exit__(self, exc_type, exc_val, traceback):
		termios.tcsetattr(sys.stdin.fileno(), termios.TCSADRAIN, self.old)

class Prompt():
	def __init__(self, cursor = None):
		self.inp = ''
		self.index = 0
		self.c = cursor

	def get_inp(self, pre_loop = None, loop_start = None):
		c = self.c
		index = 0
		y_index = 0
		inp = ['', '', '']
		if pre_loop is not None:
			pre_loop(c)
		with InputContext() as raw_in:
			while True:

				if loop_start is not None:
					loop_start(c, y_index, index, inp)

				char = ord(sys.stdin.read(1))
				
				if char == 3: #CTRL-C
					return(None)
				
				elif 32 <= char <= 126: #all printable characters
					inp[y_index] = inp[y_index][:index] + chr(char) + inp[y_index][index + 1:]
					c.x -= max(0, index)
					c.pr(inp[y_index])
					index += 1
					c.x += index - len(inp[y_index])

				elif char in {10, 13}: #enter or eol
					c.y += 1
					if y_index == 2:
						return(inp)
					y_index += 1
					c.x, index = 1, 0
				
				elif char == 127: #backspace
					if index > 0:
						inp[y_index] = inp[y_index][:index - 1] + inp[y_index][index:]
						c.x -= max(0, index)
						c.pr(inp[y_index] + ' ') #extra space clears right-most character
						index -= 1
						c.x += index - (len(inp[y_index]) + 1)
						
				
				elif char == 27: #arrow keys
					next1, next2 = ord(sys.stdin.read(1)), ord(sys.stdin.read(1))
					if next1 == 91:
						if next2 == 68: #left
							if index > 0:
								c.x -= 1
							index = max(0, index - 1)
						elif next2 == 67: #right
							if index < len(inp[y_index]):
								c.x += 1
							index = min(len(inp[y_index]), index + 1)
						elif next2 == 65: #up
							if y_index > 0:
								c.y -= 1
								y_index -= 1
								c.x = min(index + 1, len(inp[y_index]) + 1)
								index = min(index, len(inp[y_index]))
						elif next2 == 66: #down
							c.y += 1
							if y_index == 2:
								return(inp)
							y_index += 1
							c.x = min(index + 1, len(inp[y_index]) + 1)
							index = min(index, len(inp[y_index]))
		return(inp)
