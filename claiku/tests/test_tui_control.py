"""tui control tests"""

import tui_control
import time
import unittest
from io import StringIO

class MockCursor(tui_control.Cursor):
    def __init__(self):
        super().__init__()
        self.output_buffer = ''

	def _pr(text):
		self.output_buffer += str(text)



class MockPrompt(tui_control.Prompt):
	def __init__(self):
		super().__init__()
		self.input_buffer = ''

	def _rd(self, inp):
		return(ord(self.inp.read(1)))
"""

Basically, we'll test the cursor by telling it to do a bunch of
movements using the standard cursor class methods. 

Our mock cursor is writing those movements to a buffer instead of 
standard output so we'll read the output buffer it created to make 
sure it's what we expect

Then we'll test the Prompt by giving it a stream of fake user input 
(the mocked prompt takes an input string instead of reading from stdin) 
and we'll read the cursor's output buffer again to make sure it's what 
we expect. we can also read the prompt's return value to make sure it's
as expected

TODO: some way to mock our InputContext class
TODO: provide some way to take a whole string, then chunk it out
#and pass it to _rd so _rd takes one byte at a time and does the thing
so like i pass it a string, including a bunch of arrow keys, enters
backspaces and all that and it sorts it out and returns the final string

I think StringIO is the right way to do this, where in the test case
we'd set inp = StringIO('this is the string') and read it off one at a time

"""

class TestCursorMovement(unittest.TestCase):
	def setUp(self):
		self.c = MockCursor()

class TestPrompt(unittest.TestCase):
	def setUp(self):
		self.p = MockPrompt()
		self.p.c = MockCursor()

	def test_ctrlc(self):
		cases = [('\x03', '', None),
				 ('abc\x03', 'abc', None)
				]

		for i in range(len(cases)):
			with self.subTest(i = i):
				self.p.inp = cases[i][0]
				rslt = self.p.run()
				self.assertEqual(self.p.c.output_buffer, cases[i][1])
				self.assertEqual(rslt, cases[i][2])





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
