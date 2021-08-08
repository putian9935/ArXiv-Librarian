import requests 
from bs4 import BeautifulSoup as bs 

import pandas as pd 

class ArxivFetcher:
    supported_fields = {'quant-ph', 'physics.optics'}
    def __init__(self, field) -> None: 
        if field not in ArxivFetcher.supported_fields:
            raise Exception('Unsupported field!')
        self.field = field 
        pass

    def update_last_week(self):
        soup = bs(requests.get('https://arxiv.org/list/%s/pastweek?show=2000'%self.field).content, 'html.parser')
        cur_date = soup.find('h3')
        article_entry = soup.find('dl')

        articles = []
        while cur_date:
            date = cur_date.string
            for dt, dd in zip(article_entry.find_all('dt'), article_entry.find_all('dd')):
                articles.append(Article(dt, dd, date))
            cur_date = cur_date.find_next_sibling('h3')
            article_entry = article_entry.find_next_sibling('dl')
        
        return pd.DataFrame(((_.id, _.date, _.title, _.authors, self.field) for _ in articles), columns=['Id', 'Date', 'Title', 'Authors', 'Field'])







class Article:
    def __init__(self, dt, dd, date=None) -> None:
        self.id = dt.find('span', {'class':'list-identifier'}).contents[0].string.strip('arXiv:')
        self.title = list(dd.find('div', {'class':'list-title mathjax'}).descendants)[-1].strip()
        self.authors = ', '.join(list(author.descendants)[-1].strip() for author in dd.find('div', {'class':'list-authors'}).find_all('a'))
        self.date = date 
        # print(self.id, self.title, self.authors)

if __name__ == '__main__':
    ArxivFetcher('quant-ph').update_last_week()

