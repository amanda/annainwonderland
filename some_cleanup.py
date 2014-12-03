import re

def cleanup_punc(text):
	new = re.sub(r'\s+([,.;])', r'\1', text)
	return new

