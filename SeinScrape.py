#! python3
# SeinScrape.py - Save all dialogue spoke by each character in Seinfeld as TXT files.

import bs4, os, re, requests

# Run through each episode script before searching by character.
def ScrapeEpisodeScripts():

	characters = [
		"JERRY",
		"GEORGE",
		"ELAINE",
		"KRAMER",
		"MORTY",
		"HELEN",
		"FRANK",
		"ESTELLE",
		"NEWMAN",
		"UNCLE LEO",
		"SUSAN",
		"MR. LIPPMAN",
		"STEINBRENNER",
		"WILHELM",
		"PETERMAN",
		"PUDDY",
		"SUE ELLEN",
		"PITT",
		"MICKEY",
		"BANIA",
		"JACK",
		"JACKIE"
		]

	episode_path = os.getcwd() + '\\Episode scripts\\'

	assert os.path.exists(episode_path), 'Episode path is not defined.'

	# Read the contents of the episode path.
	for filename in os.listdir(episode_path):

		file_path = os.path.join(episode_path, filename)

		# Scan each episode by character.
		for character in characters:
			WriteCharacterLines(character, file_path)

# Appends character lines from episode to respective txt file.
def WriteCharacterLines(character, file_path):

	dialogue_path = os.path.join(os.getcwd() + '\\Dialogue')

	# If destination director does not exist, create it.
	if not os.path.exists(dialogue_path):
		os.mkdir(dialogue_path)

	# Get path of character file and open file.
	character_path = os.path.join(dialogue_path, character + '.txt')
	character_file = open(character_path, 'a+')

	# Any excessive spacing.
	excessSpaceRegex = re.compile(r'\s+')

	# Any text within parentheses.
	parenTextRegex = re.compile(r'\([^()]*\)')

	lines = ''

	soup = bs4.BeautifulSoup(open(file_path), features='html.parser')

	# Looks at each line by character.
	for c in soup.find_all('b', text=re.compile("\s+" + character + "\s+")):

		# Tidy string and remove text between parentheses.
		try:

			# Eliminate any text within parentheses.
			new_line = parenTextRegex.sub('', c.next_sibling.strip())

			# Replace any excess space with a single space.
			new_line = excessSpaceRegex.sub(' ', c.next_sibling.strip())

			# Check for any parentheses edge cases.
			if '(' in new_line:
				new_line = new_line.split('(')[0]
			elif ')' in new_line:
				new_line = new_line.split(')')[2]

			# Check that line is not empty or null.
			if not new_line:
				break
			else:
				lines += new_line + '\n'

		# Bit actors are not credited in the script.
		except:
			break

	print("Adding to " + character_path + " FROM..." + file_path)

	# Write line to file, then close file.
	character_file.write(lines)
	character_file.close()
	
# Search episode scripts and store dialogue by character.
ScrapeEpisodeScripts()