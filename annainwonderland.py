# from textblob import TextBlob
import argparse
import nltk
from nltk import pos_tag, ne_chunk
from nltk.tokenize import SpaceTokenizer
from collections import Counter

#maybe use textblob...?
# def get_characters(text):
# 	blob = TextBlob(text)
# 	noun_phrases = blob.noun_phrases #WordList
# 	return noun_phrases

def people_extractor(text):
	'''returns a list of people in a text,
	people are determined by nltk's named entity
	chunk (ne_chunk) function'''
	tokenizer = SpaceTokenizer()
	tags = pos_tag(tokenizer.tokenize(text))
	chunked = ne_chunk(tags) #Tree
	people = [' '.join(map(lambda x: x[0], entity.leaves())) for entity in chunked 
					if isinstance(entity, nltk.tree.Tree) and entity.label() == 'PERSON']
	return people

def find_frequent(people_list):
	people_freq = Counter(people_list)
	return people_freq

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('input', type = file, help = 'text file to get names from')
	args = parser.parse_args()
	with args.input as f:
		text = ' '.join(f.readlines()).decode('utf-8')
		print people_extractor(text)


#people = []
	# for chunk in chunked:
	# 	if isinstance(chunk, nltk.tree.Tree):
	# 		if chunk.label() == 'PERSON':
	# 			people.append(chunk.leaves())
	# chunked_sents = ne_chunk_sents(tagged_sents) #generator, could be useful?
