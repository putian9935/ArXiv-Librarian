import re 

def fetchCellPhone():
    ret = []
    with open('test.txt', 'r', encoding='utf-8') as f: 
        for ln in f.readlines():
            if re.match(r'[0-9]+\.[0-9]+\.pdf', ln):
                ret.append(ln[:-5])
    return ret
