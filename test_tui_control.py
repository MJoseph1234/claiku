"""tui control tests"""

import tui_control
import time

class TestCursor(tui_control.Cursor):
	def pr(self, inp):
		super().pr(inp)
		time.sleep(0.25)

def test_cursor_controls():
	c = TestCursor(0, 0)
	c.pr(b'\x1b[2J')

	c.pr('hello world')

	c.x = 10
	c.y = 5
	c.pr('this should print at (10, 5)')

	c.x = 20
	c.y = 10
	print(f'({c.x}, {c.y})')

	c.x = 1
	c.y = 13
	c.font_color = 'blue'
	c.background_color = 'red'
	c.font_style = 'underline'
	c.pr('blue font on a red background, underlined')

	c.x = 1
	c.y = 14
	c.font_color = None
	c.pr('plain font on a red background, underlined')

	c.x = 1
	c.y = 15
	c.background_color = None
	c.font_style = None
	c.pr('back to normal font')

	c.x = 1
	c.y = 16
	for color in ['black', 'red', 'green', 'yellow', 'blue', 'magenta'
			,'cyan', 'white']:
		c.font_color = color
		c.pr(f'{c.font_color} ')
	c.font_color = None

	c.x = 1
	c.y = 17
	for color in ['black', 'red', 'green', 'yellow', 'blue', 'magenta'
			,'cyan', 'white']:
		c.background_color = color
		c.pr(f'{c.background_color} ')
	c.background_color = None

	c.x = 1
	c.y = 18
	for style in ['bold', 'underline', 'invert', 'italic']:
		c.font_style = style
		c.pr(f'{c.font_style} ')
		c.font_style = None

	c.xy = (60, 3)
	c.pr(b'\xe2\x94\x8c')
	c.x, c.y = 65, 3
	c.pr(b'\xe2\x94\x90')
	c.x, c.y = 65, 8
	c.pr(b'\xe2\x94\x98')
	c.x, c.y = 60, 8
	c.pr(b'\xe2\x94\x94')
	c.move_up(4)
	c.move_left(1)
	c.pr(b'\xe2\x94\x82')
	c.move_down(1)
	c.move_left(1)
	c.pr(b'\xe2\x94\x82')
	c.move_down(1)
	c.move_left(1)
	c.pr(b'\xe2\x94\x82')
	c.xy = (1, 19)



if __name__ == '__main__':

	test_cursor_controls()