'''
This script opens top 6 today's trending github repos in your browser.
Repos are selected based on https://github.com/trending.
'''
import requests
import bs4
import webbrowser
import os
import sys

devnull = os.open(os.devnull, os.O_WRONLY)
os.dup2(devnull, 1)

repos_file = os.path.dirname(os.path.realpath(__file__)) + '/repos.list'
if not os.path.isfile(repos_file):
    f = open(repos_file, 'w+')
    f.close()
with open(repos_file, 'r+') as repos_list:
    repos = repos_list.read().splitlines()
    sys.stdout = open(os.devnull, 'w')
    html = requests.get('https://github.com/trending')
    html.raise_for_status()
    soup = bs4.BeautifulSoup(html.text, 'lxml')
    elements = soup.select('.repo-list > li > div > h3 > a')[:6]
    rel_urls = [el.attrs['href'] for el in elements]
    urls = [rel_url for rel_url in rel_urls if rel_url not in repos]
    for url in urls:
        webbrowser.get().open('https://github.com' + url)
        repos_list.write(url + '\n')
