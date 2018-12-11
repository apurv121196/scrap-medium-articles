from urllib.request import Request, urlopen
# import os
from bs4 import BeautifulSoup
# print(os.listdir())
import sys
query = str(sys.argv[1])
print('Query:    ', query)
header = {'User-Agent':'Mozilla/5.0'}
req = Request("https://medium.com/search?q={0}".format(query), headers = header)
res = BeautifulSoup(urlopen(req).read(), 'html.parser')

links= [i.a['href'] for i in res.findAll('div', {'class': 'postArticle-content'})]

for i in links:
	print(i)

soups = [BeautifulSoup(urlopen(Request(i, headers = header)).read(), 'html.parser') for i in links]

texts = {links[indx]:' '.join([j.text for j in i.find_all('p')]) for indx, i in enumerate(soups)}

print(texts)

f = open(query + '.txt', 'w')
f.write(' '.join(['{}: {}'.format(i, texts[i]) for  i in texts.keys()]))
f.close()