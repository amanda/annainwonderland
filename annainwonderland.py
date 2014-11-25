import argparse
import nltk
from nltk import pos_tag, ne_chunk, word_tokenize
from nltk.tokenize import SpaceTokenizer
from collections import Counter
import operator

def people_extractor(text):
	'''returns a list of people in a text,
	people are determined by nltk's named entity
	chunk (ne_chunk) function'''
	tokenizer = SpaceTokenizer()
	tags = pos_tag(tokenizer.tokenize(text))
	#tags = pos_tag(word_tokenize(text))
	chunked = ne_chunk(tags) #Tree
	people = [' '.join(map(lambda x: x[0], entity.leaves())) for entity in chunked 
					if isinstance(entity, nltk.tree.Tree) and entity.label() == 'PERSON']
	return people

def list_frequent(people_list):
	'''reorders list by most frequent values'''
	people_count = dict(Counter(people_list))
	sorted_count = sorted(people_count.items(), key=operator.itemgetter(1))[::-1]
	sorted_people = [name for name, value in sorted_count]
	return sorted_people

def equalize_list_length(first_list, second_list):
	'''makes the longer of two lists the length of the shorter,
	used to make a cast list'''
	if len(first_list) >= len(second_list):
		length = len(second_list)
		longer = first_list
		shorter = second_list
	else:
		length = len(first_list)
		longer = second_list
		shorter = first_list
	diff = len(longer) - len(shorter)
	for i in range(diff):
		longer.pop(-i)
	return length #for reference

def make_cast(players, roles):
	'''maps people from one list to another
	keys are roles (to be replaced), values are players'''
	length = equalize_list_length(players, roles)
	cast = {players[i]: roles[i] for i in range(length)}
	return cast

def file_tokens(text_file):
	'''for getting tokens from a text file'''
	with open(text_file, 'r') as f:
		tokenizer = SpaceTokenizer()
		return tokenizer.tokenize(f.read())
		# tokens = word_tokenize(f.read())
		return tokens

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
	people_list = people_extractor(people_text)
	plot_text = ' '.join((args.plot).readlines()).decode('utf-8')
	plot_list = people_extractor(plot_text)
	most_people = list_frequent(people_list)
	most_plot = list_frequent(plot_list)
	equalize_list_length(most_people, most_plot)
	cast = make_cast(most_plot, most_people)
	tokenizer = SpaceTokenizer()
	swapped_list = insert_people(cast, tokenizer.tokenize(plot_text))
	print ' '.join(swapped_list)
