# turn downloaded articles into data
# erin baggott
# november 9, 2016
# overwriting CDI notre voie to fratmat. backed up notre voie as Out/coteDivoireNotreVoieEnglish10.csv

import os, re, string, nltk, csv, codecs
snow = nltk.stem.SnowballStemmer('french')
dir = '/Users/erinbaggott/Dropbox/Autocratic Press Paper/Data/NewspapersScraped/CotedIvoireFratMat/'
writepath = '/Users/erinbaggott/Dropbox/Autocratic Press Paper/Data/*CLEAN limited dic/'

country = 'coteDivoire'
language = 'French'

#############
# load docs #
#############

docs = []
for file in os.listdir(dir):
    if 'DS' not in file:
        print file
        f = open(dir+file,'r').read()
        filedocs = f.split('\r\n\r\n____________________________________________________________\r\n\r\n')
        docs.extend(filedocs)
        

########################
# eliminate duplicates #
########################

keys = []
dupcount = 0
for article in docs:
    if article in keys:
        print 'duplicate '+str(dupcount) + ': ' + article[0:50] # commented out because slows down
        dupcount +=1
    else:
        keys.append(article)

dupcount # 301

docs = keys
    
docs = [doc for doc in docs if doc != '' and doc != '\xef\xbb\xbf']

####################
# check clean file #
####################


# strip string punctuation, tags, numbers, chinese punctuation
def strip_punctuation(s):
    return re.sub("([%s]+)" % string.punctuation, " ", s)

def strip_tags(s):
    return re.sub(r"<([^>]+)>", "", s)

def strip_numeric(s):
    return re.sub(r"[0-9]+", "", s)


date_list = []
clean = []


for article in docs:
    #article = nltk.clean_html(article)
    article = article.replace('\xc2\xa0','')
    article = article.replace(' &amp','')
    article = re.sub(r'\(\d{1,2}%\)','',article)
    article = article.lower()
    article = article.replace('f\xc3\xa9vrier','fevrier')
    article = article.replace('ao\xc3\xbbt', 'aout')
    article = article.replace('d\xc3\xa9cembre','decembre')
    article = article.replace('december','decembre')
    # date
    date = re.findall(r'\d{1,2} \w{3,9} \d{4}',article)[0]
    months = ['janvier','fevrier','mars','avril','mai','juin','juillet','aout','septembre','octobre','novembre','decembre']
    year = date.split(' ')[2]
    month = date.split(' ')[1]
    monthdic = {'Janvier':1, 'Fevrier':2, 'Mars':3, 'Avril':4, 'Mai':5, 'Juin':6, 'Juillet':7, 'Aout':8, 'Septembre':9, 'Octobre':10, 'Novembre':11, 'Decembre':12}
    month = str(monthdic[month.title()])
    # add resulting date after if fork  
    if len(month)==1:
        month = '0'+month
    day = date.split(' ')[0]
    if len(day)==1:
        day = '0'+day      
    date = year+'-'+month+'-'+day
    date_list.append(date)           
    # strip punctuation, numbers
    article = strip_punctuation(article)
    article = strip_tags(article)
    article = strip_numeric(article)
    # stem
    words = article.split()
    stemmed = [snow.stem(codecs.decode(word,'utf-8')) for word in words]
    stemmed = ' '.join([word for word in stemmed])
    clean.append(stemmed)

os.system('say "for loop complete"')      

#########################
# extract semantic data #
#########################

# load my dictionaries

dicfile = '/Users/erinbaggott/Dropbox/Autocratic Press Paper/Data/Dictionaries/MASTER/'+country+'.csv'

with open(dicfile,'rb') as f:
    reader = csv.reader(f, delimiter="\t")
    next(reader,None)
    groups, subgroups, tokens = zip(*reader)
    
dicfile2 = '/Users/erinbaggott/Dropbox/Autocratic Press Paper/Data/Dictionaries/MASTER/general'+language+'Short.csv'

with open(dicfile2,'rb') as f:
    reader = csv.reader(f, delimiter="\t")
    next(reader,None)
    groups2, subgroups2, tokens2 = zip(*reader)
    
alltokens = tokens+tokens2

exectokens = []
for i, token in enumerate(tokens):
    if subgroups[i] == "executive" or subgroups[i] == "partyExec":
        exectokens.append(tokens[i])

for i, token in enumerate(tokens2):
    if subgroups2[i] == "executive":
        exectokens.append(tokens2[i])

exectokens2 = []
for token in exectokens:
    token = token.lower()
    token = strip_punctuation(token)
    token = snow.stem(codecs.decode(token,'utf-8'))
    token = token.replace(' ','_')
    if len(token) <= 3:
        token= ' '+token+' '
    exectokens2.append(token)

###############
# stem tokens #
###############

# alltokens is what you find in clean, so need to clean it up
# process, underline, stem and add space before and after for short tokens

alltokens1 = []
for token in alltokens:
    token = token.lower()
    token = strip_punctuation(token)
    token = snow.stem(codecs.decode(token,'utf-8'))
    if len(token) <= 3:
        token= ' '+token+' '
    alltokens1.append(token)
    token

# alltokens2 adds underlines

alltokens2 = []
for token in alltokens:
    token = token.lower()
    token = strip_punctuation(token)
    token = snow.stem(codecs.decode(token,'utf-8'))
    token = token.replace(' ','_')
    if len(token) <= 3:
        token= ' '+token+' '
    alltokens2.append(token)
    token
    
tokdic = dict(zip(alltokens1,alltokens2))


tokenized = []

for article in clean:
    for i, entry in enumerate(tokdic):
        #print entry # these are without spaces
        if entry in article:
            article = article.replace(tokdic.keys()[i],tokdic.values()[i]) # replace entry w/ underlined entry so you can find it when you turn string into list below
    tokenized.append(article)
    #g.write(codecs.encode(article,'utf-8')+'\n\n')
    

# create date column

from datetime import date, datetime, timedelta

def perdelta(start, end, delta):
    curr = start
    while curr < end:
        yield curr
        curr += delta
    
df = [str(day) for day in perdelta(date(2013, 1, 1), date(2016, 1, 1), timedelta(days=1))] # cote di'ivoire specifically

# load semantic dictionaries
path = '/Users/erinbaggott/Dropbox/Autocratic Press Paper/Data/Dictionaries/MASTER/'
negativ = frozenset(open(path+'NegativFrench.txt','r').read().lower().split('\n'))
positiv = frozenset(open(path+'PositivFrench.txt','r').read().lower().split('\n'))

# stem the dictionaries

negativ = [snow.stem(codecs.decode(w,'utf-8')) for w in negativ]
positiv = [snow.stem(codecs.decode(w,'utf-8')) for w in positiv]

# drop problematic words created by stemming, and words that are more common during elections
# these words work for french. bad neg and bad pos are not necessary.
politicalWords = ['capital','prime','ministre','polite'] # ,'candidate','race','run',
politicalWords = [snow.stem(w) for w in politicalWords]

#badNegWords = ['home','common','depend']
#negativ = [w for w in negativ if w not in badNegWords]

#badPosWords = ['econom','author']
#positiv = [w for w in positiv if w not in badPosWords]

badWords = list(set(positiv).intersection(negativ))

negativ = [w for w in negativ if w not in (politicalWords+badWords)]
positiv = [w for w in positiv if w not in (politicalWords+badWords)]


# reduce lists to unique words
positiv = list(set(positiv))
negativ = list(set(negativ))


# define count function by total word hits, not unique set hits
def cnt(doc, set):
    count = 0
    for word in doc:
        if word in set:
                count += 1
    return count

# articles, articles which reference

ars = []
awms = []
for date in df:
    print date
    a = 0
    awm = 0
    for i, doc in enumerate(date_list):
        if date == date_list[i]:
            a += 1
            # this is the number of articles published by the newspaper on df[date]
            if any(token in tokenized[i] for token in exectokens2):
                awm += 1
    ars.append(a)
    awms.append(awm)

# write to CSV instead of saving in memory

termPosNames = [term+'Pos' for term in alltokens2]
termNegNames = [term+'Neg' for term in alltokens2]

with open(writepath+country+language+str(n)+'.csv','wb') as f:
    file_writer = csv.writer(f)
    header = ['date','a','awm'] + alltokens2 + termPosNames + termNegNames
    header = [codecs.encode(item,'utf-8') for item in header]
    file_writer.writerow(header)
    for m,date in enumerate(df):  # whole set of dates
        print date
        hitrow = []
        posrow = []
        negrow = []
        for term in alltokens2:
            termHits = 0
            posHits = 0
            negHits = 0
            for i, doc in enumerate(tokenized):
                if date == date_list[i]:  # comparing to the name related dates
                    #doc = doc.decode('utf-8')
                    #term = term.encode('utf-8')
                    termHits += doc.count(term)
                    x = doc.split()
                    for position, item in enumerate(x):
                        if term == item:
                            concordance = x[position-n:position+n+1]
                            mystring = ' '.join([item for item in concordance])
                            mystring = mystring.replace(term,'') # cut term
                            posHits += cnt(mystring.split(),positiv)
                            negHits += cnt(mystring.split(),negativ)
            hitrow.append(termHits)
            posrow.append(posHits)
            negrow.append(negHits)
        row = [date]+[ars[m]]+[awms[m]]+hitrow+posrow+negrow
        # na handler
        if ars[m] == 0: # if there are no articles that day, then it is not possible to count terms.
        #if sum(hitrow) == 0: 
            print 'no hits on ',date
            #print 'hitrow: ',hitrow
            #print 'posrow: ',posrow
            #print 'negrow: ',negrow
            #row = [date]+['NA']*(len(header)-1)
            row = [date]+[ars[m]] + ['NA']*(len(header)-2)
        file_writer.writerow(row)
    os.system('say "final for loop complete"')      

