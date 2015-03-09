__author__ = 'Ramki Subramanian'

li = []
di = {}


url = ['http://www.crummy.com/software/BeautifulSoup/bs4/doc/', 'http://www.imdb.com/title/tt0583452/?ref_=tt_eps_rhs_1']
title = "same"
for i,u in enumerate(url):
    print i, u
    di['url'] = u
    di['title'] = title
    di['id'] = i
    li.append(di.copy()) #
    print "dict :" ,di
    print "list", li
    print "li[", i,"]:::" ,li[i]
    print "li[0]", li[0], type(li[0])


str =  '''16.6. multiprocessing ',uOOenuoonu0094 Process-
based v,uOOenu008tmu009cthreadingxuooenuoogoxu009d interface'''

print str.decode('utf-8')






