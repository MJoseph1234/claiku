"""Command line interface haiku assistant
"""

__author__ = "Michael Joseph"
__copyright__ = "Copyright 2022, Michael Joseph"
__credits__ = ["Michael Joseph"]
__date__ = "2022-10-21"
__maintainer__ = "Michael Joseph"
__status__ = "Development"
__version__ = "0.1"

import argparse

import tui_control
from os import environ
from syllable_counter import count_syllables

def main():

	args = get_cli_args()

	if args.version:
		print(f'Claiku {__version__}')
		return

	sd = SyllableDisplay()
	if args.no_color or 'NO_COLOR' in environ:
		sd.color_good = None
		sd.color_bad = None
	if args.short:
		sd.syllable_pattern = [3, 5, 3]

	c = tui_control.Cursor()
	c.pr(b'\x1b[2J')
	c.xy = (1, 1)
	c.pr('Enter your haiku below')
	c.xy = (1, c.y + 1)
	p = tui_control.Prompt(c)
	haiku = p.run(sd.initialize_display, sd.update_display)

	if haiku is None or haiku == ['', '', '']:
		c.xy = (1, 2)
		return

	if args.quiet is False:
		print_centered_haiku(c, haiku)
		c.xy = (1, c.y + 1)
		c.pr('Beautiful!\n')
	else:
		c.pr('\n')

	save(args.output, haiku)

def get_cli_args():
	parser = argparse.ArgumentParser(description = 'a cli haiku assistant')
	parser.add_argument('-s', '--short', action = 'store_true',
		help = 'use a short-form 3-5-3 syllable pattern')
	parser.add_argument('--no-color', action = 'store_true',
		help = 'disable color output')
	parser.add_argument('-o', '--output', default = 'haikus.txt',
		help = 'file path and name to save completed haikus')
	parser.add_argument('-q', '--quiet', action = 'store_true',
		help = 'skip pretty printing your pretty haiku at the end')
	parser.add_argument('-v', '--version', action = 'store_true',
		help = 'display version information and quit')

	return(parser.parse_args())

class SyllableDisplay():
	def __init__(self, color_good = 'green', color_bad = 'red', 
				 syllable_pattern = [5, 7, 5], width = 80):
		self.color_good = color_good
		self.color_bad = color_bad
		self.syllable_pattern = syllable_pattern
		self.width = width
		self.prev_count = [0, 0, 0]

	def initialize_display(self, cursor):
		xy = cursor.xy
		for line in range(3):
			cursor.x = 50
			cursor.font_color = self.color_bad
			cursor.pr(f'0 syllables')
			cursor.y += 1
		cursor.font_color = None
		cursor.xy = xy

	def update_display(self, cursor, y_index, index, inp):
		count = count_syllables(inp[y_index])
		if count == self.prev_count[y_index]:
			return
		self.prev_count[y_index] = count
		
		xy = cursor.xy
		cursor.x = 50
		if count == self.syllable_pattern[y_index]:
			cursor.font_color = self.color_good
		else:
			cursor.font_color = self.color_bad

		cursor.pr(f'{count} syllable{"s" if count != 1 else " "}')
		cursor.font_color = None
		cursor.xy = xy

def print_centered_haiku(c, haiku, width = 80):
	c.xy = (1, 1)
	c._pr(b'\x1b[0K')
	for line in haiku:
		c.xy = (1, c.y + 1)
		c._pr(b'\x1b[0K')
		print_centered_line(c, width, line)

def print_centered_line(c, width, line):
	start = (width - len(line)) / 2
	c.x = int(start)
	c.pr(line)

def save(filepath, haiku):
	with open(filepath, 'a') as file:
		file.write('\n\n')
		file.write('\n'.join(haiku))

if __name__ == '__main__':
	main()

"""
options/configuration/cli flags
3-5-3 vs 5-7-5
file path for save to file
save to file with date/timestamp
"""