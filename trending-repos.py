import requests
import bs4
import webbrowser
import os
import sys
if not os.path.isfile('repos.list'):
    f = open('repos.list', 'w+')
    f.close()
with open('repos.list', 'r+') as repos_list:
    repos = repos_list.read().splitlines()
    sys.stdout = open(os.devnull, 'w')
    html = requests.get('https://github.com/trending')
    html.raise_for_status()
    soup = bs4.BeautifulSoup(html.text, 'lxml')
    elements = soup.select('.repo-list > li > div > h3 > a')[:6]
    rel_urls = [el.attrs['href'] for el in elements]
    urls = [rel_url for rel_url in rel_urls if rel_url not in repos]
    for url in urls:
        webbrowser.open('https://github.com' + url)
        repos_list.write(url + '\n')
