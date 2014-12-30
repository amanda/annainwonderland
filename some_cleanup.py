import re
from nltk import word_tokenize

HS_PATH = '/Users/amp/Dropbox/amanda/projects/python/nanogenmo/annainwonderland/hs_pride_swapped.txt'

def cleanup_punc(text):
	new = re.sub(r'\s+([,.;!])', r'\1', text)
	no_ticks = re.sub(r'\s+([`])', r'\1', text)
	return no_ticks

def split_lines(tokens):
	for i in range(len(tokens)):
		if i % 10 == 0:
			tokens.insert(i, "\n")
	return ' '.join(tokens)

with open(HS_PATH, 'r') as f:
	messy = f.read()

if __name__ == '__main__':
	cleaner = cleanup_punc(messy)
	splitty = split_lines(word_tokenize(messy))
	with open('hs_pride_swapped_clean.txt', 'w') as f:
		f.write(splitty)
