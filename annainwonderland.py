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
	#tokenizer = SpaceTokenizer()
	#tags = pos_tag(tokenizer.tokenize(text))
	tags = pos_tag(word_tokenize(text))
	chunked = ne_chunk(tags) #Tree
	people = [' '.join(map(lambda x: x[0], entity.leaves())) for entity in chunked 
					if isinstance(entity, nltk.tree.Tree) and entity.label() == 'PERSON']
	return people

def list_frequent(people_list):
	'''reorders list by most frequent values'''
	people_count = dict(Counter(people_list))
	sorted_count = sorted(people_count.items(), key=operator.itemgetter(1))[::-1]
	sorted_people = [name for name, value in sorted_count]
	#sorted_people.reverse() ...is one better?
	return sorted_people

def equalize_list_length(first_list, second_list):
	if len(first_list) >= len(second_list):
		length = len(first_list)
		longer = first_lists
		shorter = second_list
	else:
		length = len(second_list)
		longer = second_list
		shorter = first_list
	diff = len(longer) - len(shorter)
	for i in range(diff):
		shorter.append(shorter[i]) #check again
	return length #for reference? 

def make_cast(first_list, second_list):
	length = equalize_list_length(first_list, second_list) #so below works...
	cast = {first_list[i]: second_list[i] for i in range(length - 1)}
	return cast

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('people', type=file, help='text file to get names from')
	parser.add_argument('plot', type=file, help='text to put names in')
	args = parser.parse_args()
	with args.people as f:
		people_text = ' '.join(f.readlines()).decode('utf-8')
		people_list = people_extractor(text)
	with args.plot as f:
		plot_text = ' '.join(f.readlines()).decode('utf-8')
		plot_list = people_extractor(plot_text)

	most_people = list_frequent(people_list) #list
	most_plot = list_frequent(plot_list) #list
	equalize_list_length(most_people, most_plot)
	cast = make_cast(most_people, most_plot)
