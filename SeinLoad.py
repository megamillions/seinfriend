#! python3
# SeinLoad.py - Download all Seinfeld scripts as HTML files.

from urllib.request import urlopen
import bs4, os, requests

# Get the episode URL from the show page.
def DownloadEpisodeScripts():

	# Site that hosts all the scripts.
	show_url = "http://www.imsdb.com/TV/Seinfeld.html"

	# Episode suffix URL that will join to episode URL later.
	episode_suffix_url = "/TV Transcripts/Seinfeld"

	res = requests.get(show_url)
	res.raise_for_status()

	# Turn script HTML into a string.
	show_soup = bs4.BeautifulSoup(res.text, features='html.parser')

	# Find all links to episode pages from show page.
	for link in show_soup.select('a[href]'):

		l = link.get('href')

		if l.startswith(episode_suffix_url):
			
			WriteEpisodeScript(l)

# Downloads the episode script as an HTML file.
def WriteEpisodeScript(episode_link):

	episode_url = "http://www.imsdb.com" + episode_link
	
	# Script suffix URL that will join to script URL later.
	script_suffix_url = "/transcripts"
	
	res = requests.get(episode_url)
	res.raise_for_status()
	
	episode_soup = bs4.BeautifulSoup(res.text, features='html.parser')
	
	for link in episode_soup.select('p[align="center"] > a[href]'):
	
		l = link.get('href')
		
		if l.startswith(script_suffix_url):
					
			path = os.getcwd() + '\\Episode scripts\\'

			if not os.path.exists(path):
				os.mkdir(path)

			full_path = os.path.join(path, l[13:])

			page_content = urlopen("http://www.imsdb.com" + l).read()

			print("Downloading... " + full_path)

			# Write page content to new file.
			with open(full_path, "wb") as p:
				p.write(page_content)

# Download all episode scripts from the above show URL.
DownloadEpisodeScripts()