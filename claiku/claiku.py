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
from syllable_counter import count_syllables

def main():

	args = get_cli_args()

	if args.version:
		print(f'Claiku {__version__}')
		return

	display_options = {}
	if args.no_color:
		display_options = {'color_good': None, 'color_bad': None}
	elif args.short:
		display_options = {'one': 3, 'two': 5, 'three': 3}
	update_disp = make_display_updater(**display_options)
	init_disp = make_display_initializer(**display_options)

	c = tui_control.Cursor()
	c.pr(b'\x1b[2J')
	c.xy = (1, 1)
	c.pr('Enter your haiku below')
	c.xy = (1, c.y + 1)
	p = tui_control.Prompt(c)
	haiku = p.get_inp(init_disp, update_disp)

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

def make_display_initializer(color_bad = 'red', **kwargs):
	def initialize_display(c):
		xy = c.xy
		for line in range(3):
			c.x = 50
			c.font_color = color_bad
			c.pr(f'0 syllables')
			c.y += 1
		c.font_color = None
		c.xy = xy
	return(initialize_display)

def make_display_updater(one = 5, two = 7, three = 5, color_good = 'green', color_bad = 'red'):
	def update_display(c, y_index, index, inp):
		xy = c.xy
		c.x = 50
		count = count_syllables(inp[y_index])
		if count == [one, two, three][y_index]:
			c.font_color = color_good
		else:
			c.font_color = color_bad
		c.pr(f'{count} syllables')
		c.font_color = None
		c.xy = xy
	
	return update_display

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