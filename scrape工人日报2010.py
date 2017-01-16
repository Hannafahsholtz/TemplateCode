# china protest paper# dec 27, 2016# this file scrapes the gongren ribao.# elfstrom protest data covers 2004-2012.# CLB protest data covers 2011-present.# 工人日报 starts at 2009-01-01################### load libraries ###################import math                                                 # this lets you do mathfrom __future__ import division                             # this lets you divide numbers and get floating resultsimport re                                                   # this lets you make string replacements: 'hi there'.replace(' there') --> 'hi'import os                                                   # this lets you set system directoriesimport time                                                 # this lets you slow down your scraper so you don't crash the website =/import codecs                                               # symbols are annoying. this lets you replace them.import random                                               # this lets you draw random numbers.import datetime                                             # this lets you create a list of datesfrom datetime import timedelta                              # samefrom selenium import webdriver                              # the rest of these let you create your scraperfrom selenium.webdriver.common.keys import Keys from selenium.webdriver.common.by import Byfrom selenium.webdriver.support.ui import Selectfrom selenium.webdriver.support.ui import WebDriverWaitwritedir = '/Users/erinbaggott/Dropbox/China Protest Paper/Data/'newspaper = '工人日报'myyear = '2010'driver = webdriver.Firefox()driver.implicitly_wait(60)# initialize filef = open(writedir+newspaper+'raw'+myyear+'.txt','a')# set the dates you want to scrapeenddate = myyear+'1231'startdate = myyear+'0101'startdate = myyear+'0215' # 2010.02.14 missingstartdate = myyear+'0220' # 2010.02.16-19 missingstartdate = myyear+'1008' # 2010.10.03-07 missing * start here!startdate = myyear+'1029' # 2010.10.28 missingdate = datetime.datetime.strptime(startdate, "%Y%m%d")while date <= datetime.datetime.strptime(enddate, "%Y%m%d"):    try:        # format date        strdate = str(date).split(' ')[0].replace('-','')        print strdate        year = str(date.year)        month = str(date.month)        if len(month) == 1:            month = '0'+month        day = str(date.day)        if len(day) == 1:            day = '0'+day            url = 'http://media.workercn.cn/sites/media/grrb/'+year+'_'+month+'/'+day+'/GR0100.htm'        driver.get(url)        time.sleep(random.uniform(5,10))        # count result pages        resultPages = [str(i) for i in driver.find_element_by_id('page_content').text.split(' ')]        print 'resultpages:', resultPages        # get article pages        alllinks = []        for page in resultPages:            #print page            url = 'http://media.workercn.cn/sites/media/grrb/'+year+'_'+month+'/'+day+'/GR'+page+'00.htm'            driver.get(url)            time.sleep(random.uniform(1,3))            mylinks = driver.find_elements_by_xpath("//*[contains(@id, 'GR')]")            for link in mylinks:                #print codecs.encode(link.text,'utf-8')                #print link.get_attribute('href')                alllinks.append(link.get_attribute('href'))        for link in alllinks:            driver.get(link)            time.sleep(random.uniform(1,3))            # scrape articles            source = driver.page_source            if 'An error occurred.' in source or 'The connection has timed out' in source:                    print 'slowdown error'                    time.sleep(random.uniform(300,600))                    driver.refresh()                    time.sleep(random.uniform(60,120))                    source = driver.page_source            title = source.split('<h1>')[1].split('</h1>')[0]            tagline = driver.find_element_by_class_name('lai').text            body = driver.find_element_by_class_name('c_c').text            # save articles            f.write(codecs.encode(tagline+'\n\n'+title+'\n\n'+body+'\n\n******************\n\n','utf-8'))            # for fun            thispage = link.split('GR')[1].split('.htm')[0]            print 'just saved:',thispage, codecs.encode(title,'utf-8').strip('\n')        # progress one date        date += timedelta(days=1)     except:        os.system('say "there has been an error"')        break   f.close()    