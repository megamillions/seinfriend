# To crawl through the script of each episode of Seinfeld,
# and pull each line of dialogue and store by character.
# See: SeinScrape.py


# Return each new line and post to Twitter every 6 hours or so.


import numpy as np
import os
import re

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

characters = ['Bania', 'Elaine', 'Estelle', 'Frank', 'George', 'Helen',
	'Jack', 'Jackie', 'Jerry', 'Kramer', 'Mickey', 'Morty',
	'Mr. Lippman', 'Newman', 'Peterman', 'Pitt', 'Puddy', 'Steinbrenner',
	'Sue Ellen', 'Susan', 'Uncle Leo', 'Wilhelm']

sentence_length = 20

def get_line(character, sentence_length):

	dialogue_directory = '\\Dialogue\\'

	character_file = open(os.path.join(os.getcwd() + dialogue_directory + character + '.txt'))
	character_lines = character_file.read()
	
	# Special instances.
	if character == 'Peterman' or character == 'Pitt' or character == 'Steinbrenner':
		character = 'Mr. ' + character
	
	return character.upper() + ': ' + sample_sentence(character_lines, sentence_length)

for n in range(0, len(characters)):
	print(get_line(characters[n], sentence_length))
