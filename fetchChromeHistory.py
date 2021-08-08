import sqlite3 
import os, os.path
import re 

def fetchChromeHistory():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, "History")

    # copy history from Chrome directory to here
    os.system(r"powershell cp 'C:\Users\%s\AppData\Local\Google\Chrome\User Data\Default\History' %s"%(input(r'Input user name (enter "Administrator" if the path to Chrome installation starts with "C:\Users\Administrator\..."):'+'\n'),db_path))

    ret = []
    with sqlite3.connect(db_path)  as con:

        for row in con.execute(r"select url from urls where url like '%arxiv.org%pdf';"):
            ret.append(re.search(r'([^\/]+)\.pdf', row[0]).group(1))

    con.close()
    os.remove(db_path)

    return ret 