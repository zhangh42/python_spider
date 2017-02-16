import requests
from bs4 import BeautifulSoup
import urllib.parse
from functools import partial
import time

# 根目录
ROOT_PATH = 'http://www.liaoxuefeng.com/wiki/0014316089557264a6b348958f449949df42a6d3a2e542c000'
# 将相对路径与根路径合并为绝对路径s
urljoin = partial(urllib.parse.urljoin, ROOT_PATH)


class MDGenetor:
    '''markdown生成器S'''

    def __init__(self):
        # 以行为单位存取
        self.content = []

    def add_title(self, title, level=1):
        '''添加标题'''
        prefix = ''
        for i in range(level):
            prefix += '#'
        self.content.append(prefix + title + prefix)

    def add_text(self, text):
        '''添加正文'''
        self.content.append(text)

    @property
    def text(self):
        '''获取markdown文本内容'''
        return '\n'.join(self.content)

    def __str__(self):
        return '\n'.join(self.content)


def get_titles_url():
    '''获取所有目录的url'''
    relative_urls = []
    # 获取目录路径
    titles_request = requests.get(ROOT_PATH)
    soup = BeautifulSoup(titles_request.text)
    titles_tag = soup.find_all('ul', class_='uk-nav uk-nav-side')[1]
    for title_tag in titles_tag.find_all('li'):
        relative_urls.append(title_tag.a['href'])
    return list(map(urljoin, relative_urls))


absolute_urls = get_titles_url()
mdGenetor = MDGenetor()


def catch(url):
    '''抓取内容'''
    r = requests.get(url)
    soup = BeautifulSoup(r.text)
    title = soup.find('h4').string
    _text = soup.find('div', class_='x-wiki-content')
    raw_text = str(_text)
    text = _text.get_text()
    if title == 'Python教程':
        mdGenetor.add_title(title)
    else:
        mdGenetor.add_title(title, 2)
    mdGenetor.add_text(text)


for url in absolute_urls:
    print(url)
    catch(url)
    time.sleep(0.2)


with open('file\\python教程_廖雪峰版本.md', 'w') as file:
    file.write(mdGenetor.text)
