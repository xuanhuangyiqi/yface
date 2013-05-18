#-*- coding: UTF-8 -*-
import urllib2
import urllib
import os
import sys
import bs4
import re

def crawler(url):
    try:
        html = urllib2.urlopen('http://'+url).read()
        #if len(html) == 0:
    except Exception:
        print "can't download the url %s" % url
    if html!='':
        #html = html.decode(chardet.detect(html)['encoding'])
        html = html.decode("UTF-8")
        return html

def parser(html):
    soup = bs4.BeautifulSoup(html)
    ol = soup.find(start='0')
    if not ol:
        return None
    abr_attr_class = ['sm-abs', 'abstr', 'snip']
    result = []
    #print ol.findAll('li',recursive=False,limit=3)
    
    for li in ol.findAll('li',recursive=False,limit=3):
        #print li
        li_a_all = li.findAll('a', attrs={'class':True})
        li_a = None
        for i in li_a_all:
            if "yschttl" in i['class']:
                li_a = i
                break
        url = li_a['href']
        title = li_a.text
        li_div_all = li.findAll('div', attrs={'class':True})
        li_div = None
        for i in li_div_all:
            #print i['class']
            if i['class'][0] in abr_attr_class:
                li_div = i
                break
        abstract = li_div.text
        #print abstract
        dic = {'url':url,'title':title,'abstract':abstract}
        result.append(dic)
        
    return result

'''
    input: the name of people 
    output: top 3 results from yahoo search engine or None
'''
def query(q):
    q = q.replace('_',' ') #replace '_' with ' ' 
    q = re.sub('\d',' ',q) #replace all numbers
    print q
    url = 'news.search.yahoo.com/search?p='+urllib.quote(q)+'&'+'provider=4551793'
    return parser(crawler(url))
    
#print query('obama_barack')
    
