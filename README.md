clhaiku
a CLI haiku tool

at the core:
enter a line of text, return the number of syllables in the text

as a more fun cli program:
allows you to edit three lines at once
counts sylables in each line to confirm count

stretch goals:
modifiable haiku rules (i.e. 7-9-7 instead of 5-7-5)
control the sylable counting model (nltk vs good-ish but imperfect rules and checks)
simple, non-color mode


a new year arrives					5
cold winds from hot air blowing		7
where are we going					5


parts we'll need
1. a sylable counter (string of text goes in, sylable count comes out)
2. TUI interface allowing you to edit three lines of text at once


syllable counting algorithm ideas and prior work:
https://www.syllablecount.com/syllable/rules/
https://stackoverflow.com/questions/46759492/syllable-count-in-python
https://eayd.in/?p=232
https://pypi.org/project/syllables/

cli haiku program
https://www.npmjs.com/package/haiku-cli

# Claiku
A CLI Haiku assistant

Claiku helps you write haikus by counting and showing the number of syllables in each line of your poem.

[Picture or gif of claiku in action]

