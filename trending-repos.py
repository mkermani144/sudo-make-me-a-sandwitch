import requests
import bs4
import webbrowser
import os
import sys
sys.stdout = open(os.devnull, 'w')
print(sys.stdout)
html = requests.get('https://github.com/trending')
html.raise_for_status()
soup = bs4.BeautifulSoup(html.text)
rel_urls = soup.select('.repo-list > li > div > h3 > a')[:6]
urls = ['https://github.com' + rel_url.attrs['href'] for rel_url in rel_urls]
for url in urls:
    webbrowser.open(url)
