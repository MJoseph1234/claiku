"""sylable counter
given a string, returns the number of sylables in the string
"""

__author__ = "Michael Joseph"
__copyright__ = "Copyright 2022, Michael Joseph"
__credits__ = ["Michael Joseph"]
__date__ = "2022-10-21"
__maintainer__ = "Michael Joseph"
__status__ = "Development"
__version__ = "0.1"

def main():
    x = input("Enter a string: ")
    print(count_syllables(x))

class SyllableCounterBase():
    def __init__(self):
        pass

    def get_count(word):
        raise NotImplementedError

class NaiveSyllableCounter(SyllableCounterBase):
    def __init__(self):
        super().__init__()

    def get_count(word):
        if not word or word == '':
            return(0)
        count = 0

        vowels = 'aeiouy'
        if word[0] in vowels:
            count += 1
        for index in range(1, len(word)):
            if word[index] in vowels and word[index - 1] not in vowels:
                count += 1
        if word.endswith('e'):
            count -= 1
        if word.endswith('le') and len(word) > 2 and word[-3] not in vowels:
            count += 1
        if count == 0:
            count += 1
        return(count)

def count_syllables(string, model = NaiveSyllableCounter):
    string = string.lower().strip().split(' ')
    count = 0
    for word in string:
        count += model.get_count(word)
    return(count)

if __name__ in '__main__':
    main()