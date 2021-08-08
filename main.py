import argparse

from filter_cellphone import fetchCellPhone
from fetchChromeHistory import fetchChromeHistory
import numpy as np
import pandas as pd 
from output import output 

from fetchArxiv import ArxivFetcher

def getTitles(filename):
    return np.genfromtxt(filename, dtype=str, delimiter=',')

def parse_arguments():
    parser = argparse.ArgumentParser(description='Arxiv Librarian', prog='')

    parser.add_argument('-v','--version',  action="version", help='Show version',version='Version is 1.0')
    parser.add_argument('-u', '--update', nargs='?', const='chrome', default=None, help='Update the list from either chrome history (-u chrome) or file (-u path/to/file)')
    parser.add_argument('-o', '--output', nargs='?', const='output.html', default=None, help='Output in HTML format')
    args = parser.parse_args()

    if args.update:
        if args.update == 'arxiv':
            try:
                old_arxiv = pd.read_csv('arxiv_list', dtype=str, delimiter=',',index_col=0)
            except OSError:
                old_arxiv = None 

            new_arxivs = ArxivFetcher(input('Please input your field:')).update_last_week()
            if old_arxiv is None: 
                new_arxivs.to_csv('arxiv_list', )
            else: 
                pd.merge(old_arxiv, new_arxivs, 'outer').to_csv('arxiv_list')
              
        else:
            try:
                old_data = np.genfromtxt('data', dtype=str, delimiter=',')
            except OSError:
                old_data = None 
            
            if args.update == 'chrome':
                new_titles = fetchChromeHistory()
            elif args.update == 'phone':
                new_titles = fetchCellPhone()
            else:
                try:
                    new_titles = getTitles(args.update)
                except OSError:
                    raise Exception('File %s not found.' % args.update)
            if old_data is None: 
                np.savetxt('data', new_titles, '%s', ',')
            else: 
                np.savetxt('data', sorted(list(set(old_data,).union(new_titles))), '%s', ',')
                
    if args.output: 
        output(args.output)


parse_arguments()
