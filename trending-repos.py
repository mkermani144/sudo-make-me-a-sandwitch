'''
This script opens top today's trending github repos in your browser
if you have not previously visited them.
Repos are selected based on https://github.com/trending.
'''
import requests
import bs4
import webbrowser
import os
from optparse import OptionParser

parser = OptionParser('usage: trending-repos [options]')
parser.add_option(
    '-n', '--number-of-repos',
    dest='num_of_repos',
    default='6',
    type='int',
    help='set number of trending repos to be opened in the browser')
parser.add_option(
    '-f', '--force',
    action='store_true',
    dest='is_forced',
    help='open all of trending repos, including previously-visited ones.'
)

options, args = parser.parse_args()
num_of_repos = options.num_of_repos
is_forced = options.is_forced
if num_of_repos > 25:
    parser.error('There are only 25 trending repos available')


repos_file = os.path.dirname(os.path.realpath(__file__)) + '/repos.list'
if not os.path.isfile(repos_file):
    f = open(repos_file, 'w+')
    f.close()
with open(repos_file, 'r+') as repos_list:
    repos = repos_list.read().splitlines()
    html = requests.get('https://github.com/trending')
    html.raise_for_status()
    soup = bs4.BeautifulSoup(html.text, 'lxml')
    elements = soup.select('.repo-list > li > div > h3 > a')[:num_of_repos]
    rel_urls = [el.attrs['href'] for el in elements]
    urls = [rel_url for rel_url in rel_urls if rel_url not in repos]
    print('New repos:', len(urls))
    print('Previously visited repos:', num_of_repos - len(urls))
    if is_forced:
        urls = rel_urls
    def_stdout = os.dup(1)
    devnull = os.open(os.devnull, os.O_WRONLY)
    os.dup2(devnull, 1)
    for url in urls:
        webbrowser.open('https://github.com' + url)
        repos_list.write(url + '\n')
    os.dup2(def_stdout, 1)
