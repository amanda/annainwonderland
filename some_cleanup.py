import re

HS_PATH = '/Users/amp/Dropbox/amanda/projects/python/nanogenmo/annainwonderland/hs_pride_swapped_clean.txt'

def cleanup_punc(text):
	new = re.sub(r'\s+([,.;!])', r'\1', text)
	return new

def split_lines(tokens):
	for i in range(len(tokens)):
		if i % 10 == 0:
			tokens.insert(i, "\n")
	return tokens

if __name__ == '__main__':
	with open(HS_PATH) as f:
		cleanup_punc(f.read())
		split_lines(f.read())
