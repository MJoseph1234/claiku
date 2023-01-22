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

class DictionarySyllableCounter(SyllableCounterBase):
	def __init__(self):
		super().__init__()

	def get_count(word):
		file_name = 'data.csv'
		with open(file_name, newline = '') as file:
			reader = csv.reader(file)
			for row in reader:
				if row[0] == word:
					return(int(row[1]))

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

class SyllableRule():
	def __init__(self):
		return

	def evaluate(self, word):
		pass

class VowelCount(SyllableRule):
	def evaluate(self, word):
		vowels = 'aeiouy'
		count = 0
		for idx in range(len(word)):
			if word[idx] in vowels:
				if idx < len(word) and word[idx + 1] not in vowels:
					count += 1
		return(count)

class SilentSuffixE(SyllableRule):
	def evaluate(self, word):
		if word.endswith('e'):
			return(-1)
		return(0)

class DoubleConsonantE(SyllableRule):
	"""word ends with 'le' and has some consonant before the 'l'
	like able, acceptable, accountable
	fails for words like aisle

	"""
	def evaluate(self, word):
		vowels = 'aeiouy'
		if word.endswith('le') and len(word) > 2 and word[-3] not in vowels:
			return(1)
		return(0)

class VariableRuleCounter(SyllableCounterBase):
	def get_count(word, rule_list):
		if not word or word == '':
			return(0)
		count = 0

		for rule in rule_list:
			count += rule.evaluate(word)

		return(count)

test_naive_method()
