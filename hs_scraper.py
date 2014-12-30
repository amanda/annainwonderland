import re

HS_HTML = "/Users/amp/Dropbox/amanda/projects/python/nanogenmo/annainwonderland/hackerschoolers.html"

def get_hackerschoolers_from(html):
	with open(html) as f:
		content = f.read()
	return re.findall("'name'><a.*>.*</a>", content)

def cleanup(hs_list):
	names = []
	for i in hs_list:
		names.append(re.search("\">(.*)<", i).group(1))
	return names

messy = get_hackerschoolers_from(HS_HTML)
hackerschoolers = cleanup(messy)

if __name__ == '__main__':
	print hackerschoolers
	