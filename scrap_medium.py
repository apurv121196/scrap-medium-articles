from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import sys
import os
import itertools
import pickle

query = str(sys.argv[1])
print('Query:    ', query)
try:
	os.mkdir(f'./{query}')
except FileExistsError:
	pass
header = {'User-Agent':'Mozilla/5.0'}
url = "https://medium.com/search"


'''
https://medium.com/search/posts?q=ethereum&count=10&ignore=79956138bea3&ignore=22d1df506369&ignore=9e5dc29e33ce&ignore=dcab52905bba&ignore=8fcd5f8abcdf&ignore=88718e08124f&ignore=46dd486ceecf&ignore=9401b7188841&ignore=2b650b5f4f62
'''

def generate_query(ids):
	return url + "/posts?q={0}&count=10&ignore=".format(query) + '&ignore='.join(list(itertools.chain.from_iterable(ids)))

path = f'./{query}/'
id_collection = []
link_collection = []
texts_collection = {}
fw = open(path + f'links-{query}.txt', 'w')
fids = open(path + f'ids-{query}', 'wb')
ftxts = open(path + f'texts-{query}', 'wb')
def get_data(url, req_ids=False):
	print(generate_query(id_collection) if req_ids else url + "?q={0}".format(query))
	req = None
	while req is None:
		try:
			req = Request(generate_query(id_collection) if req_ids else url + "?q={0}".format(query), headers = header)
		except:
			print('=======================CONNECTION ERROR 1==============================')
			fw.write('\n'.join(list(itertools.chain.from_iterable(link_collection))))
			pickle.dump('\n'.join(list(itertools.chain.from_iterable(id_collection))), fids)
			pass
	res = BeautifulSoup(urlopen(req).read(), 'html.parser')

	links = [i.a['href'] for i in res.findAll('div', {'class': 'postArticle-content'})]
		
	ids = [i.a['data-post-id'] for i in res.findAll('div', {'class': 'postArticle-content'})]
	
	if len(links) == 0:
		print('=======================NO ARTICLE LEFT==============================')
		fw.write('\n'.join(list(itertools.chain.from_iterable(link_collection))))
		pickle.dump('\n'.join(list(itertools.chain.from_iterable(id_collection))), fids)
		return

	link_collection.append(links)
	id_collection.append(ids)
	print('TOTAL LINKS: ' + str(len(links)))
	# for i in links:
		# print(i)
	soups = None
	while soups is None:
		try:
			soups = [BeautifulSoup(urlopen(Request(i, headers = header)).read(), 'html.parser') for i in links]
		except:
			print('=======================CONNECTION ERROR 2==============================')
			fw.write('\n'.join(list(itertools.chain.from_iterable(link_collection))))
			pickle.dump('\n'.join(list(itertools.chain.from_iterable(id_collection))), fids)
			pass
	
	texts = {links[indx]:' '.join([j.text for j in i.find_all('p')]) for indx, i in enumerate(soups)}
	texts_collection[generate_query(id_collection) if req_ids else url + "?q={0}".format(query)] = texts
	pickle.dump(texts_collection, ftxts)
	print(texts_collection.keys())
	# f = open(query + '.txt', 'w')
	# f.write(' '.join(['{}: {}'.format(i, texts[i]) for  i in texts.keys()]))
	# f.close()
	# fw.close()
	# fids.close()
	return get_data(url, True)
	# return ids

get_data(url)
fw.close()
fids.close()
ftxts.close()
# for i in id_collection:
# 	print(i)