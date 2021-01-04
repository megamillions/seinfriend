# To crawl through the script of each episode of Seinfeld,
# and pull each line of dialogue and store by character.
# See: SeinScrape.py

# Return each new line and post to Twitter every 6 hours or so.

import numpy as np
import os
import re

characters = ['Bania', 'Elaine', 'Estelle', 'Frank', 'George', 'Helen',
	'Jack', 'Jackie', 'Jerry', 'Kramer', 'Mickey', 'Morty',
	'Mr. Lippman', 'Newman', 'Peterman', 'Pitt', 'Puddy', 'Steinbrenner',
	'Sue Ellen', 'Susan', 'Uncle Leo', 'Wilhelm']

sentence_length = 30

def read_file(character):

	dialogue_directory = '\\Dialogue\\'

	character_file = open(os.path.join(os.getcwd() + dialogue_directory + character + '.txt'))
	return character_file.read()

# Preprocess data for each character.
def build_transition_matrix(corpus):

	corpus = re.split(' |\n', corpus)
	transitions = {}
	
	for k in range(0, len(corpus)):
		word = corpus[k]
		
		# Deal with the last word.
		if k != len(corpus) - 1:
			next_word = corpus[k + 1]
			
		# Loop back to the beginning.
		else:
			next_word = corpus[0]
			
		if word not in transitions:
			transitions[word] = []
			
		transitions[word].append(next_word)
		
	return transitions

# Feed each character's lines to Markov bot to generate new lines.
def sample_sentence(corpus, sentence_length, burn_in = 1000):

	corpus = corpus
	sentence = []
	
	transitions = build_transition_matrix(corpus)
	
	# Sample sentence after running through chain 1,000 times to near stationary distribution.
	current_word = np.random.choice(re.split(' |\n', corpus), size=1)[0]
	
	# Sample from the lists with an equal chance of entry.
	for k in range(0, burn_in + sentence_length):
	
		# Choose word with correct probability distribution in transition matrix.
		current_word = np.random.choice(transitions[current_word], size=1)[0]
		
		if k >= burn_in:
			sentence.append(current_word)
			
	return ' '.join(sentence)

# Produces a cleaned line of dialogue.
def clean_line(character, sentence_length):

	character_lines = read_file(character)

	# Special instances.
	if character == 'Peterman' or character == 'Pitt' or character == 'Steinbrenner':
		character = 'Mr. ' + character
	
	to_clean = sample_sentence(character_lines, sentence_length)

	to_clean = re.split('\. ', to_clean)

    # Begins line with at the start of first sentence.
	if not to_clean[0][0].isupper():
		to_clean.pop(0)

	# Ends line at any sign of punctuation.
	if to_clean[-1][-1] not in ['\.', '\!', '\?']:
		to_clean.pop(-1)

	return character.upper() + ': ' + ". ".join(to_clean) + '.'

# Counts the number of lines a character speaks.
def count_lines(character):

	character_lines = read_file(character)
	count = 1
	
	for c in character_lines:
		if c == '\n':
			count += 1
			
	return count

# Weighs the character dialogue by number of lines each has.
def generate_line():

	# Stores cumulative lines spoken.
	spoken_lines = {}
	gross_count = 0

	# Builds spoken line dictionary.
	for n in range(0, len(characters)):

		gross_count += count_lines(characters[n])
		spoken_lines[characters[n]] = gross_count

	# Draw a line at random.
	draw = np.random.randint(gross_count)

	# Assign the drawn pick to a character and return line.
	for k, v in spoken_lines.items():
		if draw < v:
			return clean_line(k, sentence_length)

print(generate_line())