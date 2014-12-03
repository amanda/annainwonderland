'''put your friends in classic works of literature.
warning: this will take a really long time for books 
in its current state! but it "works" (poorly).
todo: fix output punct and newlines...'''
import argparse
import nltk
from nltk import pos_tag, ne_chunk, word_tokenize
from collections import Counter
import os.path
import os

def people_extractor(tokens, pos_tags):
	'''returns a list of people in a text,
	people are determined by nltk's named entity
	chunk (ne_chunk) function'''
	chunked = ne_chunk(pos_tags) #Tree
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
	zipped = zip(roles, players)
	cast = dict(zipped)
	return cast

def insert_people(cast_dict, dest_tokens): #dest_tokens must match ne_chunk
	'''cast dict keys are roles, value is who plays that role.
	dest_tokens must have names of roles/keys.'''
	replaced = [cast_dict.get(x, x) for x in dest_tokens]
	return replaced

def tokenize_chunks(chunked):
	treewords = []
	for chunk in chunked:
		if isinstance(chunk, nltk.tree.Tree):
			treewords.append(' '.join([x[0] for x in chunk.leaves()]))
		else:
			treewords.append(chunk[0])
	return treewords #maintains people entities as tokens

def get_cast_from_user():
	'''for easy user input'''
	players = raw_input('enter the names of people you would like to insert into the text, separated by commas: ')
	return [x.strip() for x in players.split(',')]

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('plot', type=file, help='text to put names in')
	parser.add_argument('-l', '--list', type=file, nargs='?', help='optional input list')
	args = parser.parse_args()
	plot_text = args.plot.read()
	if not args.list:
		people_list = get_cast_from_user()
	else:
		people_list = args.list.read().split(',') #hacky for list of hacker schoolers
	tokens = word_tokenize(plot_text)
	tags = pos_tag(tokens)
	plot_list = people_extractor(tokens, tags)
	most_people = list_frequent(people_list)
	most_plot = list_frequent(plot_list)
	cast = make_cast(most_plot, most_people)
	print cast
	try:
		swapped = insert_people(cast, tokenize_chunks(ne_chunk(tags)))
	except UnicodeEncodeError:
		print "working on it!"
	print ' '.join(swapped)
	output_file = '{0}_swapped.txt'.format(args.plot.name[:-4])
	with open(output_file, 'w') as f: #careful, will overwrite
		f.write(' '.join(swapped))

