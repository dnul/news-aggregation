__author__ = 'dnul'


import feedparser
import requests
import re
from bs4 import BeautifulSoup



rss_uri = ['http://contenidos.lanacion.com.ar/herramientas/rss-origen=2']

feed = feedparser.parse(rss_uri[0])

def parse_double_utf8(txt):
    def parse(m):
        try:
            return m.group(0).encode('latin1').decode('utf8')
        except UnicodeDecodeError:
            return m.group(0)
    return re.sub(u'[\xc2-\xf4][\x80-\xbf]+', parse, txt)

print(feed)
for entry in feed.entries:
    content = []
    print(entry['link'])
    print(entry['title'])
    file = open('noticias/'+entry['title']+'.txt','w')
    r = requests.get(entry['link'])
    html_content = r.text
    # Convert the html content into a beautiful soup object
    soup = BeautifulSoup(html_content)
    cuerpo =soup.find_all('section',attrs={'id':'cuerpo'})
    if cuerpo:
        paragraphs = cuerpo[0].find_all('p')
        for p in paragraphs:
            content.append(parse_double_utf8(p.getText()))
    file.write(''.join(content))
    file.flush()







