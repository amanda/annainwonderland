import argparse
import nltk
from nltk import pos_tag, ne_chunk, word_tokenize
from nltk.tokenize import SpaceTokenizer
from collections import Counter

def people_extractor(text):
	'''returns a list of people in a text,
	people are determined by nltk's named entity
	chunk (ne_chunk) function'''
	tags = pos_tag(word_tokenize(text))
	chunked = ne_chunk(tags) #Tree
	people = [' '.join(map(lambda x: x[0], entity.leaves())) for entity in chunked 
					if isinstance(entity, nltk.tree.Tree) and entity.label() == 'PERSON']
	return people

def list_frequent(people_list):
	'''reorders list by most frequent entries'''
	people_count = Counter(people_list)
	sorted_count = sorted(people_count.keys(), key=people_count.get, reverse=True)
	return sorted_count

def make_cast(roles, players):
	'''maps people from one list to another
	keys are roles (to be replaced), values are players'''
	zipped = zip(roles, players) #list of tuples
	cast = dict(zipped)
	return cast

def file_tokens(text_file):
	'''for getting tokens from a text file
	using nltk's SpaceTokenizer'''
	with open(text_file, 'r') as f:
		tokenizer = SpaceTokenizer()
		return tokenizer.tokenize(f.read())

def insert_people(cast_dict, dest_tokens):
	'''cast dict keys are roles, value is who plays that role.
	dest_tokens must have names of roles/keys.'''
	replaced = [cast_dict.get(x, x) for x in dest_tokens]
	return replaced

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('people', type=file, help='text file to get names from')
	parser.add_argument('plot', type=file, help='text to put names in')
	args = parser.parse_args()
	people_text = ' '.join((args.people).readlines()).decode('utf-8')
	plot_text = ' '.join((args.plot).readlines()).decode('utf-8')
	people_list = people_extractor(people_text)
	plot_list = people_extractor(plot_text)
	most_people = list_frequent(people_list)
	most_plot = list_frequent(plot_list)
	cast = make_cast(most_plot, most_people)
	tokenizer = SpaceTokenizer()
	swapped = insert_people(cast, tokenizer.tokenize(plot_text))
	print ' '.join(swapped)
