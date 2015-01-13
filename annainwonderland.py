#!/bin/env python

import argparse, os, os.path, pickle, codecs, nltk, re
from nltk import pos_tag, ne_chunk, word_tokenize
from collections import Counter

def people_extractor(pos_tags):
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
	cast = dict(zip(roles, players))
	return cast

def get_cast_from_user():
	'''for easy user input'''
	players = raw_input('enter the names of people you would like to insert into the text, separated by commas: ')
	return [x.strip() for x in players.split(',')]

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('plot', help='text to put names in')
	parser.add_argument('-l', '--list', type=file, nargs='?', help='optional input list')
	args = parser.parse_args()
	if not args.list:
		people_list = get_cast_from_user()
	else:
		people_list = args.list.read().split(',') #hacky for list of hacker schoolers
	
	print 'inserting your characters...'

	with open(args.plot) as f:
		tags = pos_tag(word_tokenize(f.read()))
	plot_list = people_extractor(tags)
	print 'plot list: {}'.format(plot_list)
	most_people = list_frequent(people_list)
	most_plot = list_frequent(plot_list)
	cast = make_cast(most_plot, most_people)
	print 'cast: {}'.format(cast)

	def repl(match):
		return cast[match.group(0)]

	p = re.compile('|'.join(re.escape(x) for x in cast))
	
	filename, ext = os.path.splitext(args.plot)
	swapped_file = filename + '-swapped' + ext
	
	with codecs.open(args.plot, 'r', encoding='utf-8') as infile:
		with codecs.open(swapped_file, 'w') as outfile:
			for line in infile:
				outfile.write(p.sub(repl, line))
	print 'done'
