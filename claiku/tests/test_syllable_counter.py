"""test syllable counter methods"""

import csv
import syllable_counter

def load_dict():
	"""
	Loads reference data to dictionary.
	:return: dictionary of the syllable reference data
	"""
	file_name = "data.csv"
	words = {}

	with open(file_path, newline="") as file:
		reader = csv.reader(file)
		for row in reader:
			words[row[0]] = int(row[1])
	return words

def test_naive_method():
	"""
	Loads reference data to dictionary.
	:return: dictionary of the syllable reference data
	"""
	file_name = "data.csv"
	with open(file_name, newline="") as file:
		reader = csv.reader(file)
		total = 0
		correct = 0
		missed = {}
		for row in reader:
			total += 1
			count = syllable_counter.count_syllables(row[0])
			if count == int(row[1]):
				correct += 1
			else:
				missed[row[0]] = (count, row[1])
	print(f'{correct} out of {total} (%{correct/total * 100:.1f})')

	for key, val in missed.items():
		print(f'{key:<25}expected: {val[1]:<3}got: {val[0]}')

test_naive_method()
