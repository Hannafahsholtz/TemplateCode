# scrape CDI fratmat
# november 4, 2016
# need to scrape each section in fratmat, because there isn't one central archive. ugh.
# only scraping from 2015 back (ie ignoring 2016), because there aren't 2016 elections and b/c the rest of our dataset.

import urllib, urllib2, re, os, time, codecs
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from selenium.webdriver.common.action_chains import ActionChains
from numpy import random


writepath = '/Users/erinbaggott/Dropbox/Autocratic Press Paper/Data/NewspapersScraped/CotedIvoireFratMat/'
writefile = 'coteDivoirePoliticsRaw.txt'
driver = webdriver.Firefox()
driver.implicitly_wait(30)


f = open(writepath+writefile,'a')

# politics section
section = 'http://www.fratmat.info/politique?start=' 
resultPages = list(range(400,1620,10))
resultPages = list(range(650,1620,10))
resultPages = list(range(1240,1620,10))
for page in resultPages:
    print 'On page ',str(page),' of ',str(resultPages[len(resultPages)-1])
    url = section+str(page)
    driver.get(url)
    time.sleep(random.uniform(5,10))
    divs = driver.find_elements_by_class_name('catItemHeader')
    links = []
    for div in divs:
        link = div.find_element_by_tag_name('a').get_attribute('href')
        links.append(link)
    print 'len(links) = ',str(len(links))
    for link in links:
        driver.get(link)
        time.sleep(random.uniform(1,2))
        source = driver.page_source
        if "La page que vous recherchez n'existe pas ou une erreur" in source: # 404
            os.system('say "404 error"')
            time.sleep(10)
            driver.refresh()
            time.sleep(10)
        if "La page que vous recherchez n'existe pas ou une erreur" in source: # 404 again
            os.system('say "404 error again, ignoring this article"')
            print '404 error, continue'
            continue
        if 'COMPONENT_NOT_LOADING' in source: # scraping too hard
            os.system('say "bandwidth overload, slowing down now"')
            time.sleep(60)
        title = driver.find_element_by_class_name('itemTitle').text
        date = driver.find_element_by_class_name('itemDateCreated').text
        lede = driver.find_element_by_class_name('itemIntroText').text
        content = driver.find_element_by_class_name('itemFullText').text
        out = codecs.encode(date,'utf-8-sig')+'\n\n'+codecs.encode(title,'utf-8-sig')+'\n\n'+codecs.encode(lede,'utf-8-sig')+'\n\n'+codecs.encode(content,'utf-8-sig')+'\r\n\r\n____________________________________________________________\r\n\r\n'
        f.write(out)

f.close()