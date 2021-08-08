import bs4
import matplotlib
from numpy.lib.financial import ipmt 

import pandas as pd 

from datetime import datetime, date
from bs4 import BeautifulSoup as bs

import numpy as np 

def get_read_list():
    try: 
        return set(np.genfromtxt('data', dtype=str, delimiter=','))
    except OSError:
        print('Read data not generated. Run "py main.py -u chrome" first. ')
        exit()

def output(filename):
    try:
        arxiv = pd.read_csv('arxiv_list', dtype=str, delimiter=',',index_col=0)
    except FileNotFoundError: 
        print('File arxiv_list cannot be found. Run "py main.py -u arxiv" first. ')
        exit()
        



    read_list = get_read_list()
    f = open(filename, 'w', encoding='utf-8')
    f.write(r'<html> <head> </head> <body>')
    for article_date in pd.unique(arxiv.loc[:,'Date']):
        dd = datetime.strptime(article_date, r'%a, %d %b %Y').date()
        now = date.today()
        
        if (now-dd).days > 7:
            break
        
        soup = bs(arxiv[arxiv.Date==article_date].drop(['Date','Field', 'Authors'],axis=1).to_html(index=False), 'html.parser').table
        soup['style'] = "margin-top:10px"
        soup.tr['style']="text-align: center; margin: 1cm top"
        
        article = soup.tbody.tr 

        read_plot = r'<div style="width: 100%; margin: 50px bottom;">'
        read_cnt = 0
        while article:
            if str(article.td.string) in read_list:
                article['style'] = 'background:lightgreen;'
                read_plot += r'<div style="width:15px;height:100px; background: lightgreen; float:left;"></div>'
                read_cnt += 1
            else:
                article['style'] = 'background:lightpink'
                read_plot += r'<div style="width:15px;height:100px; background: lightpink; float:left;"></div>'

            article_id = str(article.td.string)
            link = bs((r'<a href="https://arxiv.org/abs/%s/" target="_blank">%s</a>'%(article_id, article_id)), 'html.parser')
            article.td.clear()
            article.td.insert(1,link)

            article = article.find_next_sibling('tr')

        read_plot += '</div><br style="clear:both" />'
        
        f.write('<h3>%s, %d articles in total, %d read</h3>'%(article_date, len(arxiv[arxiv.Date==article_date]), read_cnt))
        f.write(read_plot)
        f.write(str(soup))
        
    f.write('</body></html>')


        