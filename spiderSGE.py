# -*- coding: utf-8 -*-
"""
Created on Mon Jun 20 15:07:05 2016

@author: Lufan CHEN
         Tong LI
"""

import time
start = time.time()
start2 = time.clock()

import urllib.request
from bs4 import BeautifulSoup
import pandas as pd
import re
import pickle

def saveFile(content,save_path):    
    f_obj = open(save_path, 'wb+')
    pickle.dump(content, f_obj)
    f_obj.close()
    
def searchLinks(soup):
    # Get the url of the next page
    nextPage = soup.find_all("a",text="下一页")[0].attrs['href']
    nextPage = "http://www.sge.com.cn/xqzx/mrxq/" + nextPage
    # Get the url of all load-links on the current page
    loadlist = soup.find_all("a",{"class":"load_list"})
    thisPageLinks = []    
    for loadlink in loadlist:
        thisPageLinks.append("http://www.sge.com.cn" + loadlink.attrs['href'])
    return nextPage, thisPageLinks
    
def getData(soup):
    # 13 columns in every table
    C0,C1,C2,C3,C4,C5,C6,C7,C8,C9,C10,C11,C12 = [],[],[],[],[],[],[],[],[],[],[],[],[]
    # tr is row,td is column/cell
    for row in soup.find_all("tr"):
        cells = row.find_all("td")
        C0.append(cells[0].get_text())
        C1.append(cells[1].get_text())
        C2.append(cells[2].get_text())
        C3.append(cells[3].get_text())
        C4.append(cells[4].get_text())
        C5.append(cells[5].get_text())
        C6.append(cells[6].get_text())
        C7.append(cells[7].get_text())
        C8.append(cells[8].get_text())
        C9.append(cells[9].get_text())
        C10.append(cells[10].get_text())
        C11.append(cells[11].get_text())
        C12.append(cells[12].get_text())
        data = {C1[0]:C1[1:],C2[0]:C2[1:],C3[0]:C3[1:],C4[0]:C4[1:],C5[0]:C5[1:],
                C6[0]:C6[1:],C7[0]:C7[1:],C8[0]:C8[1:],C9[0]:C9[1:],C10[0]:C10[1:],
                C11[0]:C11[1:],C12[0]:C12[1:]}
        df = pd.DataFrame(data,index=C0[1:]) # contract name as index
    day = soup.h5.get_text()
    date = re.findall(r'(\d*[0-9]+)\d*',day)
    return df,date

# Main
url_start = "http://www.sge.com.cn/xqzx/mrxq/"
dataDict = {}
for i in range(20): # number of pages to browse
    homePage = urllib.request.urlopen(url_start)
    homeSoup = BeautifulSoup(homePage, "lxml")
    nextPage, thisPageLinks = searchLinks(homeSoup)
    
    for url in thisPageLinks:
        page = urllib.request.urlopen(url)
        soup = BeautifulSoup(page, "lxml")
        df, date = getData(soup)
        
        date = "-".join(date)
        #df.to_excel('save.xlsx', date)
        newdict = {date:df}
        dataDict.update(newdict)
        
    url_start = nextPage

saveFile(dataDict,save_path='save.txt')

end = time.time()
end2 = time.clock()
print('total time=',end-start,'s\n')
print('Processing time=',end2-start2,'s\n')