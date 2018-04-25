from bs4 import BeautifulSoup
import requests
import os
import pandas as pd
import itertools
import urllib

urls = open('train_urls.txt').readlines()

soup = BeautifulSoup()

try:
    from google.appengine.api import urlfetch
except ImportError:
    urlfetch = None


def wget(url):
    if urlfetch:
        return urlfetch.fetch(url).content
    else:
        req = urllib.request.Request(url)
        req.add_header("User-Agent", "Mozilla/5.0 (Compatible)")
        return urllib.request.urlopen(req).read()

def wikisnip(url):
    html = wget(url)
    soup = BeautifulSoup(html)

    div = soup.find('div', {'id': 'bodyContent'})

    snip = BeautifulSoup('')

    for node in div.childGenerator():
        if (isinstance(node, str) or
            node.name.lower() in ["table", "script"] or
            node.get('id') in ["siteSub", "contentSub", "jump-to-nav"] or
            node.get('class') in ['dablink', 'toclimit-2']):
            continue

        snip.append(node)

    for a in snip.findAll('a'):
        if a.get('href'):
            a['href'] = urllib.parse.urljoin(url, a['href'])

    return snip

url_df = pd.DataFrame(columns=['DOCNUM', 'URL'])
doc_nums = []
used_urls = []
for i in range(len(urls)):
    url = urls[i]
    try:
        ws = wikisnip(url)
        filepath = 'wiki_data/{0}.txt'.format(str(i), url)
        print(filepath)
        with open(filepath, 'wb') as f:
            f.write(ws.text.encode('utf8'))
            f.close()
            
        doc_nums.append(i)
        used_urls.append(url)
    except:
        pass
    
url_df['DOCNUM'] = doc_nums
url_df['URL'] = used_urls
url_df.to_csv('url_docnums.csv', index=False)